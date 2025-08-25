# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import networkx as nx
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
import numpy as np

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkAnalyzer:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

    def analyze_network(self, scenario_id: str) -> Dict[str, Any]:
        """Analyze street network and calculate block statistics"""
        try:
            # Get network data
            links = self._get_links(scenario_id)
            parcels = self._get_parcels(scenario_id)
            
            if not links:
                return {'success': False, 'error': 'No network links found'}

            # Build network graph
            graph = self._build_network_graph(links)
            
            # Calculate network metrics
            network_metrics = self._calculate_network_metrics(graph, links)
            
            # Calculate block statistics
            block_stats = self._calculate_block_statistics(parcels, links)
            
            # Calculate intersection density
            intersection_density = self._calculate_intersection_density(links)
            
            # Store results
            self._store_network_analysis(scenario_id, {
                'network_metrics': network_metrics,
                'block_stats': block_stats,
                'intersection_density': intersection_density
            })

            return {
                'success': True,
                'message': f'Analyzed network with {len(links)} links',
                'data': {
                    'network_metrics': network_metrics,
                    'block_stats': block_stats,
                    'intersection_density': intersection_density
                }
            }

        except Exception as e:
            logger.error(f"Error analyzing network: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_links(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get network links from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_AsText(geometry) as geom_wkt, properties, link_class
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _get_parcels(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get parcels from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_AsText(geometry) as geom_wkt, ST_Area(geometry) as area
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _build_network_graph(self, links: List[Dict[str, Any]]) -> nx.Graph:
        """Build NetworkX graph from links"""
        graph = nx.Graph()
        
        for link in links:
            line = LineString.from_wkt(link['geom_wkt'])
            properties = link['properties']
            
            # Get start and end points
            start_point = Point(line.coords[0])
            end_point = Point(line.coords[-1])
            
            # Add nodes
            start_node = (start_point.x, start_point.y)
            end_node = (end_point.x, end_point.y)
            
            graph.add_node(start_node)
            graph.add_node(end_node)
            
            # Add edge with properties
            graph.add_edge(
                start_node, 
                end_node,
                length=properties.get('length', line.length),
                link_class=link['link_class'],
                lanes=properties.get('lanes', 1),
                speed_limit=properties.get('speedLimit', 30)
            )
        
        return graph

    def _calculate_network_metrics(self, graph: nx.Graph, links: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate network-level metrics"""
        if len(graph.nodes) == 0:
            return {}
        
        # Basic metrics
        total_length = sum(link['properties'].get('length', 0) for link in links)
        avg_link_length = total_length / len(links) if links else 0
        
        # Connectivity metrics
        node_count = len(graph.nodes)
        edge_count = len(graph.edges)
        connectivity_ratio = edge_count / node_count if node_count > 0 else 0
        
        # Network density
        network_density = nx.density(graph)
        
        # Average degree
        avg_degree = sum(dict(graph.degree()).values()) / node_count if node_count > 0 else 0
        
        # Centrality measures
        try:
            betweenness_centrality = nx.betweenness_centrality(graph)
            avg_betweenness = sum(betweenness_centrality.values()) / len(betweenness_centrality) if betweenness_centrality else 0
        except:
            avg_betweenness = 0
        
        # Link class distribution
        link_class_dist = {}
        for link in links:
            link_class = link['link_class']
            link_class_dist[link_class] = link_class_dist.get(link_class, 0) + 1
        
        return {
            'total_length': total_length,
            'avg_link_length': avg_link_length,
            'node_count': node_count,
            'edge_count': edge_count,
            'connectivity_ratio': connectivity_ratio,
            'network_density': network_density,
            'avg_degree': avg_degree,
            'avg_betweenness_centrality': avg_betweenness,
            'link_class_distribution': link_class_dist
        }

    def _calculate_block_statistics(self, parcels: List[Dict[str, Any]], links: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate block-level statistics"""
        if not parcels:
            return {}
        
        # Calculate block areas
        areas = [parcel['area'] for parcel in parcels]
        
        # Calculate block perimeters (approximate using parcel boundaries)
        perimeters = []
        for parcel in parcels:
            try:
                geom = parcel['geom_wkt']
                # This is a simplified perimeter calculation
                # In a real implementation, you'd calculate actual block perimeters
                perimeter = np.sqrt(parcel['area']) * 4  # Approximate
                perimeters.append(perimeter)
            except:
                perimeters.append(0)
        
        # Calculate block sizes
        block_sizes = []
        for area in areas:
            if area < 1000:  # < 1000 m²
                block_sizes.append('small')
            elif area < 10000:  # 1000-10000 m²
                block_sizes.append('medium')
            else:  # > 10000 m²
                block_sizes.append('large')
        
        # Calculate statistics
        stats = {
            'total_blocks': len(parcels),
            'avg_block_area': np.mean(areas) if areas else 0,
            'median_block_area': np.median(areas) if areas else 0,
            'min_block_area': np.min(areas) if areas else 0,
            'max_block_area': np.max(areas) if areas else 0,
            'avg_block_perimeter': np.mean(perimeters) if perimeters else 0,
            'block_size_distribution': {
                'small': block_sizes.count('small'),
                'medium': block_sizes.count('medium'),
                'large': block_sizes.count('large')
            }
        }
        
        return stats

    def _calculate_intersection_density(self, links: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate intersection density metrics"""
        if not links:
            return {}
        
        # Extract intersection points
        intersection_points = []
        for link in links:
            line = LineString.from_wkt(link['geom_wkt'])
            start_point = Point(line.coords[0])
            end_point = Point(line.coords[-1])
            intersection_points.extend([start_point, end_point])
        
        # Count unique intersections (within tolerance)
        tolerance = 10  # meters
        unique_intersections = []
        
        for point in intersection_points:
            is_unique = True
            for existing in unique_intersections:
                if point.distance(existing) < tolerance:
                    is_unique = False
                    break
            if is_unique:
                unique_intersections.append(point)
        
        # Calculate total network length
        total_length = sum(link['properties'].get('length', 0) for link in links)
        
        # Calculate intersection density
        intersection_density = len(unique_intersections) / (total_length / 1000) if total_length > 0 else 0  # intersections per km
        
        return {
            'intersection_count': len(unique_intersections),
            'total_network_length': total_length,
            'intersection_density': intersection_density,  # intersections per km
            'avg_distance_between_intersections': total_length / len(unique_intersections) if unique_intersections else 0
        }

    def _store_network_analysis(self, scenario_id: str, analysis_data: Dict[str, Any]):
        """Store network analysis results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with network analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{network_analysis}',
                %s::jsonb
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            cursor.execute(query, (json.dumps(analysis_data), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_network_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get network analysis summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'network_analysis' as network_analysis
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['network_analysis']:
                    return {
                        'success': True,
                        'data': result['network_analysis']
                    }
                else:
                    return {'success': False, 'error': 'No network analysis data found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting network summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
