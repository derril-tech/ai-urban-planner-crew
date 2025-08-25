# Created automatically by Cursor AI (2025-08-25)
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import unary_union, split
from shapely.affinity import scale
import numpy as np
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParcelizerWorker:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

    def parcelize_site(self, scenario_id: str, parcelization_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate parcels from site boundary"""
        try:
            # Get site boundary
            site_boundary = self._get_site_boundary(scenario_id)
            if not site_boundary:
                return {'success': False, 'error': 'No site boundary found'}

            # Get existing roads/links
            existing_roads = self._get_existing_roads(scenario_id)

            # Generate parcels
            parcels = self._generate_parcels(site_boundary, existing_roads, parcelization_params)

            # Store parcels in database
            result = self._store_parcels(parcels, scenario_id)

            return {
                'success': True,
                'message': f'Generated {len(parcels)} parcels',
                'data': result
            }

        except Exception as e:
            logger.error(f"Error parcelizing site: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_site_boundary(self, scenario_id: str) -> Optional[Polygon]:
        """Get site boundary from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT ST_AsText(geometry) as geom_wkt
            FROM site_boundaries
            WHERE scenario_id = %s AND status = 'active'
            LIMIT 1
            """
            cursor.execute(query, (scenario_id,))
            result = cursor.fetchone()
            
            if result:
                return Polygon.from_wkt(result[0])
            return None
            
        finally:
            cursor.close()
            conn.close()

    def _get_existing_roads(self, scenario_id: str) -> List[LineString]:
        """Get existing roads from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT ST_AsText(geometry) as geom_wkt
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            results = cursor.fetchall()
            
            roads = []
            for result in results:
                roads.append(LineString.from_wkt(result[0]))
            
            return roads
            
        finally:
            cursor.close()
            conn.close()

    def _generate_parcels(self, site_boundary: Polygon, existing_roads: List[LineString], 
                         params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate parcels using different strategies"""
        strategy = params.get('strategy', 'grid')
        
        if strategy == 'grid':
            return self._generate_grid_parcels(site_boundary, existing_roads, params)
        elif strategy == 'irregular':
            return self._generate_irregular_parcels(site_boundary, existing_roads, params)
        else:
            raise ValueError(f"Unknown parcelization strategy: {strategy}")

    def _generate_grid_parcels(self, site_boundary: Polygon, existing_roads: List[LineString],
                              params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate regular grid parcels"""
        target_area = params.get('target_area', 1000)  # m²
        min_width = params.get('min_width', 20)  # m
        max_width = params.get('max_width', 50)  # m
        
        # Calculate grid dimensions
        parcel_width = np.sqrt(target_area)
        parcel_width = max(min_width, min(max_width, parcel_width))
        parcel_height = target_area / parcel_width
        
        # Create grid
        bounds = site_boundary.bounds
        x_min, y_min, x_max, y_max = bounds
        
        parcels = []
        x = x_min
        while x < x_max:
            y = y_min
            while y < y_max:
                # Create parcel polygon
                parcel_poly = Polygon([
                    (x, y),
                    (x + parcel_width, y),
                    (x + parcel_width, y + parcel_height),
                    (x, y + parcel_height),
                    (x, y)
                ])
                
                # Check if parcel intersects with site boundary
                if parcel_poly.intersects(site_boundary):
                    intersection = parcel_poly.intersection(site_boundary)
                    
                    # Only keep parcels with sufficient area
                    if intersection.area > target_area * 0.5:
                        parcels.append({
                            'geometry': intersection,
                            'properties': self._generate_parcel_properties(intersection, params)
                        })
                
                y += parcel_height
            x += parcel_width
        
        return parcels

    def _generate_irregular_parcels(self, site_boundary: Polygon, existing_roads: List[LineString],
                                   params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate irregular parcels based on road network"""
        target_area = params.get('target_area', 1000)  # m²
        min_area = target_area * 0.5
        max_area = target_area * 2.0
        
        # Use existing roads to split the site
        if existing_roads:
            parcels = self._split_by_roads(site_boundary, existing_roads, target_area)
        else:
            # Generate simple irregular parcels
            parcels = self._generate_simple_irregular(site_boundary, target_area)
        
        # Filter by area constraints
        filtered_parcels = []
        for parcel in parcels:
            if min_area <= parcel['geometry'].area <= max_area:
                parcel['properties'] = self._generate_parcel_properties(parcel['geometry'], params)
                filtered_parcels.append(parcel)
        
        return filtered_parcels

    def _split_by_roads(self, site_boundary: Polygon, roads: List[LineString], 
                       target_area: float) -> List[Dict[str, Any]]:
        """Split site by existing road network"""
        # Union all roads
        road_network = unary_union(roads)
        
        # Buffer roads to create right-of-way
        road_buffer = road_network.buffer(10)  # 10m buffer
        
        # Split site by road buffer
        split_polygons = site_boundary.difference(road_buffer)
        
        parcels = []
        if split_polygons.geom_type == 'Polygon':
            parcels.append({'geometry': split_polygons})
        elif split_polygons.geom_type == 'MultiPolygon':
            for poly in split_polygons.geoms:
                parcels.append({'geometry': poly})
        
        return parcels

    def _generate_simple_irregular(self, site_boundary: Polygon, target_area: float) -> List[Dict[str, Any]]:
        """Generate simple irregular parcels by recursive subdivision"""
        parcels = []
        
        def subdivide(polygon: Polygon, depth: int = 0):
            if depth > 3 or polygon.area < target_area * 0.5:
                parcels.append({'geometry': polygon})
                return
            
            # Split polygon along its longest axis
            bounds = polygon.bounds
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            
            if width > height:
                # Split vertically
                mid_x = (bounds[0] + bounds[2]) / 2
                split_line = LineString([(mid_x, bounds[1]), (mid_x, bounds[3])])
            else:
                # Split horizontally
                mid_y = (bounds[1] + bounds[3]) / 2
                split_line = LineString([(bounds[0], mid_y), (bounds[2], mid_y)])
            
            # Split polygon
            try:
                parts = split(polygon, split_line)
                for part in parts:
                    if part.area > target_area * 0.3:
                        subdivide(part, depth + 1)
                    else:
                        parcels.append({'geometry': part})
            except:
                # If split fails, keep the original polygon
                parcels.append({'geometry': polygon})
        
        subdivide(site_boundary)
        return parcels

    def _generate_parcel_properties(self, geometry: Polygon, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate default properties for a parcel"""
        area = geometry.area
        
        # Calculate basic properties
        properties = {
            'useMix': {
                'residential': 0.7,
                'commercial': 0.2,
                'institutional': 0.1
            },
            'far': params.get('default_far', 2.0),
            'height': params.get('default_height', 15),
            'setbacks': {
                'front': 3,
                'side': 1.5,
                'rear': 3
            },
            'inclusionary': params.get('inclusionary_percent', 15),
            'phase': 1,
            'lotCoverage': 0.6,
            'groundFloorActivation': True,
            'parkingRatio': params.get('parking_ratio', 1.5),
            'density': area / 10000  # units per hectare
        }
        
        return properties

    def _store_parcels(self, parcels: List[Dict[str, Any]], scenario_id: str) -> Dict[str, Any]:
        """Store parcels in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Clear existing parcels for this scenario
            cursor.execute("DELETE FROM parcels WHERE scenario_id = %s", (scenario_id,))
            
            # Insert new parcels
            for parcel in parcels:
                geom_wkt = parcel['geometry'].wkt
                properties = json.dumps(parcel['properties'])
                
                query = """
                INSERT INTO parcels (scenario_id, geometry, properties, created_at, updated_at)
                VALUES (%s, ST_GeomFromText(%s, 4326), %s, NOW(), NOW())
                """
                cursor.execute(query, (scenario_id, geom_wkt, properties))
            
            conn.commit()
            
            return {
                'parcels_count': len(parcels),
                'scenario_id': scenario_id
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
