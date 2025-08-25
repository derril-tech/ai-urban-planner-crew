# Created automatically by Cursor AI (2025-01-27)
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import networkx as nx
from shapely.geometry import Point, LineString
import numpy as np
from scipy.spatial.distance import cdist

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MobilityModel:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Default mobility parameters
        self.defaults = {
            # Trip generation
            'daily_trips_per_person': 3.5,  # Average daily trips per person
            'work_trip_ratio': 0.25,  # 25% of trips are work-related
            'shopping_trip_ratio': 0.30,  # 30% are shopping/errands
            'recreation_trip_ratio': 0.25,  # 25% are recreation
            'other_trip_ratio': 0.20,  # 20% are other purposes
            
            # Mode choice parameters
            'walk_threshold': 800,  # meters - people will walk for trips under 800m
            'bike_threshold': 3000,  # meters - people will bike for trips under 3km
            'transit_threshold': 8000,  # meters - transit competitive up to 8km
            
            # Speed assumptions (m/s)
            'walk_speed': 1.3,  # 1.3 m/s (4.7 km/h)
            'bike_speed': 4.2,  # 4.2 m/s (15 km/h)
            'transit_speed': 8.3,  # 8.3 m/s (30 km/h)
            'car_speed': 11.1,  # 11.1 m/s (40 km/h)
            
            # Mode choice elasticities
            'parking_cost_elasticity': -0.3,  # Higher parking costs reduce car use
            'bike_infrastructure_elasticity': 0.4,  # Better bike infra increases bike use
            'transit_frequency_elasticity': 0.5,  # More frequent transit increases use
            'walkability_elasticity': 0.6,  # Better walkability increases walking
            
            # Level of Service thresholds
            'los_walk_excellent': 0.8,  # 80%+ of population within 400m of amenities
            'los_walk_good': 0.6,  # 60%+ of population within 400m of amenities
            'los_walk_fair': 0.4,  # 40%+ of population within 400m of amenities
            'los_walk_poor': 0.2,  # 20%+ of population within 400m of amenities
            
            # 15-minute city parameters
            'fifteen_minute_walk_distance': 1200,  # meters (15 min * 1.3 m/s)
            'fifteen_minute_bike_distance': 5000,  # meters (15 min * 5.6 m/s)
            'fifteen_minute_transit_distance': 8000,  # meters (15 min * 8.9 m/s)
        }

    def analyze_mobility(self, scenario_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze mobility patterns and accessibility for a scenario"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'Scenario not found'}

            # Get network data
            network_data = self._get_network_data(scenario_id)
            if not network_data:
                return {'success': False, 'error': 'No network data found'}

            # Get parcels and amenities
            parcels = self._get_parcels(scenario_id)
            amenities = self._get_amenities(scenario_id)

            # Update defaults with provided parameters
            if params:
                self.defaults.update(params)

            # Calculate trip generation
            trip_generation = self._calculate_trip_generation(scenario_data, parcels)
            
            # Calculate mode choice
            mode_choice = self._calculate_mode_choice(scenario_data, network_data, parcels, amenities)
            
            # Calculate VMT
            vmt_analysis = self._calculate_vmt(trip_generation, mode_choice, network_data)
            
            # Calculate 15-minute access
            fifteen_minute_access = self._calculate_fifteen_minute_access(parcels, amenities, network_data)
            
            # Calculate walk/bike LOS
            walk_bike_los = self._calculate_walk_bike_los(parcels, amenities, network_data)
            
            # Calculate accessibility metrics
            accessibility_metrics = self._calculate_accessibility_metrics(parcels, amenities, network_data)

            # Store results
            self._store_mobility_analysis(scenario_id, {
                'trip_generation': trip_generation,
                'mode_choice': mode_choice,
                'vmt_analysis': vmt_analysis,
                'fifteen_minute_access': fifteen_minute_access,
                'walk_bike_los': walk_bike_los,
                'accessibility_metrics': accessibility_metrics
            })

            return {
                'success': True,
                'message': f'Analyzed mobility for scenario with {len(parcels)} parcels',
                'data': {
                    'trip_generation': trip_generation,
                    'mode_choice': mode_choice,
                    'vmt_analysis': vmt_analysis,
                    'fifteen_minute_access': fifteen_minute_access,
                    'walk_bike_los': walk_bike_los,
                    'accessibility_metrics': accessibility_metrics
                }
            }

        except Exception as e:
            logger.error(f"Error analyzing mobility: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_scenario_data(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get scenario data including population and land use"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, name, properties, kpis
            FROM scenarios
            WHERE id = %s
            """
            cursor.execute(query, (scenario_id,))
            result = cursor.fetchone()
            return result
            
        finally:
            cursor.close()
            conn.close()

    def _get_network_data(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get network links and their properties"""
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
        """Get parcels with capacity and land use data"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_AsText(ST_Centroid(geometry)) as centroid_wkt, 
                   ST_Area(geometry) as area, properties, capacity
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _get_amenities(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get amenities and their locations"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_AsText(ST_Centroid(geometry)) as centroid_wkt, 
                   amenity_type, properties
            FROM amenities
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _calculate_trip_generation(self, scenario_data: Dict[str, Any], parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate daily trip generation by purpose"""
        total_population = 0
        total_jobs = 0
        
        # Sum population and jobs from parcels
        for parcel in parcels:
            capacity = parcel.get('capacity', {})
            total_population += capacity.get('population', 0)
            total_jobs += capacity.get('jobs', 0)

        # Calculate trips by purpose
        work_trips = total_population * self.defaults['daily_trips_per_person'] * self.defaults['work_trip_ratio']
        shopping_trips = total_population * self.defaults['daily_trips_per_person'] * self.defaults['shopping_trip_ratio']
        recreation_trips = total_population * self.defaults['daily_trips_per_person'] * self.defaults['recreation_trip_ratio']
        other_trips = total_population * self.defaults['daily_trips_per_person'] * self.defaults['other_trip_ratio']
        
        total_trips = work_trips + shopping_trips + recreation_trips + other_trips

        return {
            'total_population': total_population,
            'total_jobs': total_jobs,
            'total_daily_trips': total_trips,
            'trips_by_purpose': {
                'work': work_trips,
                'shopping': shopping_trips,
                'recreation': recreation_trips,
                'other': other_trips
            },
            'trips_per_person': self.defaults['daily_trips_per_person']
        }

    def _calculate_mode_choice(self, scenario_data: Dict[str, Any], network_data: List[Dict[str, Any]], 
                              parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate mode choice based on network characteristics and policies"""
        
        # Analyze network characteristics
        bike_lanes_km = 0
        transit_stops = 0
        parking_spaces = 0
        
        for link in network_data:
            properties = link.get('properties', {})
            link_class = link.get('link_class', 'local')
            
            # Count bike infrastructure
            if properties.get('bike_lanes', 0) > 0:
                bike_lanes_km += properties.get('length', 0) / 1000  # Convert to km
                
            # Count transit stops (simplified - would need actual stop data)
            if link_class in ['arterial', 'collector']:
                transit_stops += 1
                
            # Estimate parking (simplified)
            if link_class == 'local':
                parking_spaces += properties.get('length', 0) * 0.1  # Rough estimate

        # Calculate mode choice factors
        walk_factor = self._calculate_walk_factor(parcels, amenities)
        bike_factor = self._calculate_bike_factor(bike_lanes_km, len(network_data))
        transit_factor = self._calculate_transit_factor(transit_stops, len(parcels))
        car_factor = self._calculate_car_factor(parking_spaces, total_population)

        # Normalize factors to sum to 1
        total_factor = walk_factor + bike_factor + transit_factor + car_factor
        
        mode_share = {
            'walk': walk_factor / total_factor if total_factor > 0 else 0.25,
            'bike': bike_factor / total_factor if total_factor > 0 else 0.05,
            'transit': transit_factor / total_factor if total_factor > 0 else 0.15,
            'car': car_factor / total_factor if total_factor > 0 else 0.55
        }

        return {
            'mode_share': mode_share,
            'network_characteristics': {
                'bike_lanes_km': bike_lanes_km,
                'transit_stops': transit_stops,
                'parking_spaces': parking_spaces
            },
            'mode_factors': {
                'walk_factor': walk_factor,
                'bike_factor': bike_factor,
                'transit_factor': transit_factor,
                'car_factor': car_factor
            }
        }

    def _calculate_walk_factor(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]]) -> float:
        """Calculate walking attractiveness factor"""
        if not parcels or not amenities:
            return 0.1
            
        # Calculate average distance to amenities
        total_distance = 0
        count = 0
        
        for parcel in parcels:
            parcel_centroid = Point.from_wkt(parcel['centroid_wkt'])
            min_distance = float('inf')
            
            for amenity in amenities:
                amenity_centroid = Point.from_wkt(amenity['centroid_wkt'])
                distance = parcel_centroid.distance(amenity_centroid)
                min_distance = min(min_distance, distance)
            
            if min_distance < float('inf'):
                total_distance += min_distance
                count += 1
        
        avg_distance = total_distance / count if count > 0 else 1000
        
        # Convert to walk factor (closer = higher factor)
        walk_factor = max(0.1, 1.0 - (avg_distance / 1000))  # Normalize to 0-1
        return walk_factor * self.defaults['walkability_elasticity']

    def _calculate_bike_factor(self, bike_lanes_km: float, total_network_length: int) -> float:
        """Calculate biking attractiveness factor"""
        bike_coverage = bike_lanes_km / (total_network_length / 1000) if total_network_length > 0 else 0
        bike_factor = bike_coverage * self.defaults['bike_infrastructure_elasticity']
        return max(0.05, bike_factor)  # Minimum 5% bike mode share

    def _calculate_transit_factor(self, transit_stops: int, total_parcels: int) -> float:
        """Calculate transit attractiveness factor"""
        stop_density = transit_stops / total_parcels if total_parcels > 0 else 0
        transit_factor = stop_density * self.defaults['transit_frequency_elasticity']
        return max(0.05, transit_factor)  # Minimum 5% transit mode share

    def _calculate_car_factor(self, parking_spaces: float, total_population: int) -> float:
        """Calculate car attractiveness factor"""
        parking_ratio = parking_spaces / total_population if total_population > 0 else 0
        car_factor = 1.0 - (parking_ratio * self.defaults['parking_cost_elasticity'])
        return max(0.2, car_factor)  # Minimum 20% car mode share

    def _calculate_vmt(self, trip_generation: Dict[str, Any], mode_choice: Dict[str, Any], 
                      network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Vehicle Miles Traveled"""
        
        total_trips = trip_generation['total_daily_trips']
        car_share = mode_choice['mode_share']['car']
        
        # Estimate average trip length based on network characteristics
        total_network_length = sum(link.get('properties', {}).get('length', 0) for link in network_data)
        avg_trip_length = total_network_length / len(network_data) if network_data else 1000  # meters
        
        # Calculate VMT
        car_trips = total_trips * car_share
        daily_vmt = car_trips * (avg_trip_length / 1609.34)  # Convert to miles
        annual_vmt = daily_vmt * 365
        
        # Calculate per capita VMT
        total_population = trip_generation['total_population']
        per_capita_vmt = annual_vmt / total_population if total_population > 0 else 0
        
        return {
            'daily_vmt': daily_vmt,
            'annual_vmt': annual_vmt,
            'per_capita_vmt': per_capita_vmt,
            'car_trips_per_day': car_trips,
            'avg_trip_length_miles': avg_trip_length / 1609.34,
            'vmt_reduction_potential': self._calculate_vmt_reduction_potential(mode_choice)
        }

    def _calculate_vmt_reduction_potential(self, mode_choice: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential VMT reduction through mode shift"""
        current_car_share = mode_choice['mode_share']['car']
        
        # Calculate potential mode shifts
        potential_walk_share = min(0.4, current_car_share * 0.3)  # Up to 40% walking
        potential_bike_share = min(0.15, current_car_share * 0.2)  # Up to 15% biking
        potential_transit_share = min(0.25, current_car_share * 0.3)  # Up to 25% transit
        
        potential_car_share = current_car_share - potential_walk_share - potential_bike_share - potential_transit_share
        vmt_reduction = (current_car_share - potential_car_share) / current_car_share if current_car_share > 0 else 0
        
        return {
            'current_car_share': current_car_share,
            'potential_car_share': potential_car_share,
            'vmt_reduction_percent': vmt_reduction * 100,
            'potential_mode_shifts': {
                'walk': potential_walk_share,
                'bike': potential_bike_share,
                'transit': potential_transit_share
            }
        }

    def _calculate_fifteen_minute_access(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]], 
                                        network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate 15-minute access metrics"""
        
        if not parcels or not amenities:
            return {'access_percentages': {}, 'accessibility_score': 0}
        
        # Group amenities by type
        amenity_types = {}
        for amenity in amenities:
            amenity_type = amenity.get('amenity_type', 'other')
            if amenity_type not in amenity_types:
                amenity_types[amenity_type] = []
            amenity_types[amenity_type].append(amenity)
        
        access_percentages = {}
        total_accessibility = 0
        
        for amenity_type, type_amenities in amenity_types.items():
            accessible_population = 0
            total_population = 0
            
            for parcel in parcels:
                parcel_centroid = Point.from_wkt(parcel['centroid_wkt'])
                parcel_population = parcel.get('capacity', {}).get('population', 0)
                total_population += parcel_population
                
                # Check if any amenity of this type is within 15-minute walk
                for amenity in type_amenities:
                    amenity_centroid = Point.from_wkt(amenity['centroid_wkt'])
                    distance = parcel_centroid.distance(amenity_centroid)
                    
                    if distance <= self.defaults['fifteen_minute_walk_distance']:
                        accessible_population += parcel_population
                        break
            
            access_percentage = (accessible_population / total_population * 100) if total_population > 0 else 0
            access_percentages[amenity_type] = access_percentage
            total_accessibility += access_percentage
        
        # Calculate overall accessibility score
        overall_accessibility = total_accessibility / len(amenity_types) if amenity_types else 0
        
        return {
            'access_percentages': access_percentages,
            'accessibility_score': overall_accessibility,
            'fifteen_minute_walk_distance': self.defaults['fifteen_minute_walk_distance'],
            'amenity_types_analyzed': list(amenity_types.keys())
        }

    def _calculate_walk_bike_los(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]], 
                                network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate walk and bike Level of Service"""
        
        if not parcels or not amenities:
            return {'walk_los': 'F', 'bike_los': 'F', 'scores': {}}
        
        # Calculate walk LOS
        walk_score = self._calculate_walk_score(parcels, amenities, network_data)
        walk_los = self._score_to_los(walk_score)
        
        # Calculate bike LOS
        bike_score = self._calculate_bike_score(network_data)
        bike_los = self._score_to_los(bike_score)
        
        return {
            'walk_los': walk_los,
            'bike_los': bike_los,
            'scores': {
                'walk_score': walk_score,
                'bike_score': bike_score
            },
            'factors': {
                'walk_factors': self._get_walk_los_factors(parcels, amenities, network_data),
                'bike_factors': self._get_bike_los_factors(network_data)
            }
        }

    def _calculate_walk_score(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]], 
                             network_data: List[Dict[str, Any]]) -> float:
        """Calculate walkability score (0-100)"""
        if not parcels or not amenities:
            return 0
        
        # Calculate average distance to amenities
        total_distance = 0
        count = 0
        
        for parcel in parcels:
            parcel_centroid = Point.from_wkt(parcel['centroid_wkt'])
            min_distance = float('inf')
            
            for amenity in amenities:
                amenity_centroid = Point.from_wkt(amenity['centroid_wkt'])
                distance = parcel_centroid.distance(amenity_centroid)
                min_distance = min(min_distance, distance)
            
            if min_distance < float('inf'):
                total_distance += min_distance
                count += 1
        
        avg_distance = total_distance / count if count > 0 else 1000
        
        # Convert distance to score (closer = higher score)
        walk_score = max(0, 100 - (avg_distance / 10))  # 100m = 90 points, 1000m = 0 points
        return walk_score

    def _calculate_bike_score(self, network_data: List[Dict[str, Any]]) -> float:
        """Calculate bikeability score (0-100)"""
        if not network_data:
            return 0
        
        bike_lanes_km = 0
        total_network_km = 0
        
        for link in network_data:
            properties = link.get('properties', {})
            link_length_km = properties.get('length', 0) / 1000
            total_network_km += link_length_km
            
            if properties.get('bike_lanes', 0) > 0:
                bike_lanes_km += link_length_km
        
        bike_coverage = bike_lanes_km / total_network_km if total_network_km > 0 else 0
        bike_score = bike_coverage * 100
        return bike_score

    def _score_to_los(self, score: float) -> str:
        """Convert score to Level of Service grade"""
        if score >= 80:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 40:
            return 'C'
        elif score >= 20:
            return 'D'
        else:
            return 'F'

    def _get_walk_los_factors(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]], 
                             network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get factors affecting walk LOS"""
        return {
            'amenity_density': len(amenities) / len(parcels) if parcels else 0,
            'avg_distance_to_amenities': self._calculate_avg_distance_to_amenities(parcels, amenities),
            'sidewalk_coverage': self._estimate_sidewalk_coverage(network_data)
        }

    def _get_bike_los_factors(self, network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get factors affecting bike LOS"""
        bike_lanes_km = 0
        total_network_km = 0
        
        for link in network_data:
            properties = link.get('properties', {})
            link_length_km = properties.get('length', 0) / 1000
            total_network_km += link_length_km
            
            if properties.get('bike_lanes', 0) > 0:
                bike_lanes_km += link_length_km
        
        return {
            'bike_lane_coverage': bike_lanes_km / total_network_km if total_network_km > 0 else 0,
            'bike_lanes_km': bike_lanes_km,
            'total_network_km': total_network_km
        }

    def _calculate_avg_distance_to_amenities(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]]) -> float:
        """Calculate average distance from parcels to nearest amenity"""
        if not parcels or not amenities:
            return 1000
        
        total_distance = 0
        count = 0
        
        for parcel in parcels:
            parcel_centroid = Point.from_wkt(parcel['centroid_wkt'])
            min_distance = float('inf')
            
            for amenity in amenities:
                amenity_centroid = Point.from_wkt(amenity['centroid_wkt'])
                distance = parcel_centroid.distance(amenity_centroid)
                min_distance = min(min_distance, distance)
            
            if min_distance < float('inf'):
                total_distance += min_distance
                count += 1
        
        return total_distance / count if count > 0 else 1000

    def _estimate_sidewalk_coverage(self, network_data: List[Dict[str, Any]]) -> float:
        """Estimate sidewalk coverage (simplified)"""
        if not network_data:
            return 0
        
        sidewalk_length = 0
        total_length = 0
        
        for link in network_data:
            properties = link.get('properties', {})
            link_length = properties.get('length', 0)
            total_length += link_length
            
            # Assume sidewalks on arterials and collectors
            link_class = link.get('link_class', 'local')
            if link_class in ['arterial', 'collector']:
                sidewalk_length += link_length
        
        return sidewalk_length / total_length if total_length > 0 else 0

    def _calculate_accessibility_metrics(self, parcels: List[Dict[str, Any]], amenities: List[Dict[str, Any]], 
                                       network_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive accessibility metrics"""
        
        if not parcels or not amenities:
            return {'metrics': {}, 'summary': {}}
        
        # Calculate various accessibility metrics
        metrics = {
            'avg_distance_to_nearest_amenity': self._calculate_avg_distance_to_amenities(parcels, amenities),
            'amenity_density': len(amenities) / len(parcels) if parcels else 0,
            'network_density': sum(link.get('properties', {}).get('length', 0) for link in network_data) / len(parcels) if parcels else 0,
            'intersection_density': len(network_data) / len(parcels) if parcels else 0
        }
        
        # Calculate accessibility by amenity type
        amenity_accessibility = {}
        for amenity in amenities:
            amenity_type = amenity.get('amenity_type', 'other')
            if amenity_type not in amenity_accessibility:
                amenity_accessibility[amenity_type] = {
                    'count': 0,
                    'avg_distance': 0,
                    'accessible_population': 0
                }
            
            amenity_accessibility[amenity_type]['count'] += 1
            
            # Calculate average distance to this amenity type
            total_distance = 0
            accessible_population = 0
            total_population = 0
            
            for parcel in parcels:
                parcel_centroid = Point.from_wkt(parcel['centroid_wkt'])
                parcel_population = parcel.get('capacity', {}).get('population', 0)
                total_population += parcel_population
                
                amenity_centroid = Point.from_wkt(amenity['centroid_wkt'])
                distance = parcel_centroid.distance(amenity_centroid)
                total_distance += distance
                
                if distance <= self.defaults['fifteen_minute_walk_distance']:
                    accessible_population += parcel_population
            
            amenity_accessibility[amenity_type]['avg_distance'] = total_distance / len(parcels) if parcels else 0
            amenity_accessibility[amenity_type]['accessible_population'] = accessible_population
        
        metrics['amenity_accessibility'] = amenity_accessibility
        
        # Summary statistics
        summary = {
            'total_amenities': len(amenities),
            'total_parcels': len(parcels),
            'avg_amenities_per_parcel': len(amenities) / len(parcels) if parcels else 0,
            'overall_accessibility_score': self._calculate_overall_accessibility_score(metrics)
        }
        
        return {
            'metrics': metrics,
            'summary': summary
        }

    def _calculate_overall_accessibility_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall accessibility score (0-100)"""
        # Weighted combination of various metrics
        distance_score = max(0, 100 - (metrics['avg_distance_to_nearest_amenity'] / 10))
        density_score = min(100, metrics['amenity_density'] * 100)
        network_score = min(100, metrics['network_density'] / 10)
        
        # Weighted average
        overall_score = (distance_score * 0.4 + density_score * 0.4 + network_score * 0.2)
        return max(0, min(100, overall_score))

    def _store_mobility_analysis(self, scenario_id: str, analysis_data: Dict[str, Any]):
        """Store mobility analysis results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with mobility analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{mobility_analysis}',
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

    def get_mobility_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get mobility analysis summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'mobility_analysis' as mobility_analysis
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['mobility_analysis']:
                    return {
                        'success': True,
                        'data': result['mobility_analysis']
                    }
                else:
                    return {'success': False, 'error': 'No mobility analysis data found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting mobility summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
