# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import nearest_points
import random

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitizenAdvocate:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Persona templates
        self.persona_templates = {
            'child': {
                'name': 'Child',
                'age_range': '5-12',
                'mobility_type': 'pedestrian',
                'speed': 1.0,  # m/s
                'max_distance': 400,  # meters
                'priorities': ['safety', 'play', 'education'],
                'barriers': ['unsafe_crossings', 'no_sidewalks', 'high_traffic', 'poor_lighting'],
                'needs': ['playgrounds', 'schools', 'safe_routes', 'crossing_guards']
            },
            'senior': {
                'name': 'Senior',
                'age_range': '65+',
                'mobility_type': 'pedestrian',
                'speed': 0.8,  # m/s
                'max_distance': 300,  # meters
                'priorities': ['safety', 'comfort', 'accessibility'],
                'barriers': ['steep_slopes', 'poor_surfaces', 'no_benches', 'long_distances'],
                'needs': ['benches', 'smooth_surfaces', 'shade', 'rest_areas']
            },
            'low_income': {
                'name': 'Low-Income Resident',
                'age_range': '18-65',
                'mobility_type': 'transit',
                'speed': 1.2,  # m/s
                'max_distance': 800,  # meters
                'priorities': ['affordability', 'accessibility', 'time_efficiency'],
                'barriers': ['high_fares', 'poor_frequency', 'long_walks', 'unsafe_areas'],
                'needs': ['affordable_transit', 'frequent_service', 'safe_routes', 'amenities']
            },
            'assistive_mobility': {
                'name': 'Assistive Mobility User',
                'age_range': 'all',
                'mobility_type': 'wheelchair',
                'speed': 0.6,  # m/s
                'max_distance': 500,  # meters
                'priorities': ['accessibility', 'safety', 'independence'],
                'barriers': ['curbs', 'narrow_paths', 'poor_surfaces', 'no_ramps'],
                'needs': ['ramps', 'wide_paths', 'smooth_surfaces', 'accessible_amenities']
            },
            'cyclist': {
                'name': 'Cyclist',
                'age_range': '12-65',
                'mobility_type': 'bicycle',
                'speed': 4.0,  # m/s
                'max_distance': 5000,  # meters
                'priorities': ['safety', 'efficiency', 'connectivity'],
                'barriers': ['no_bike_lanes', 'high_traffic', 'poor_surfaces', 'theft_risk'],
                'needs': ['bike_lanes', 'secure_parking', 'good_surfaces', 'bike_amenities']
            }
        }

        # Journey types
        self.journey_types = {
            'home_to_work': {
                'name': 'Home to Work',
                'frequency': 'daily',
                'time_constraint': 'peak_hours',
                'priority': 'efficiency'
            },
            'home_to_school': {
                'name': 'Home to School',
                'frequency': 'daily',
                'time_constraint': 'school_hours',
                'priority': 'safety'
            },
            'home_to_shop': {
                'name': 'Home to Shopping',
                'frequency': 'weekly',
                'time_constraint': 'flexible',
                'priority': 'convenience'
            },
            'home_to_healthcare': {
                'name': 'Home to Healthcare',
                'frequency': 'monthly',
                'time_constraint': 'appointment',
                'priority': 'accessibility'
            },
            'home_to_recreation': {
                'name': 'Home to Recreation',
                'frequency': 'weekly',
                'time_constraint': 'leisure',
                'priority': 'enjoyment'
            }
        }

    def generate_personas(self, scenario_id: str, persona_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate personas for a scenario"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Use all persona types if none specified
            if not persona_types:
                persona_types = list(self.persona_templates.keys())

            personas = {}
            for persona_type in persona_types:
                if persona_type in self.persona_templates:
                    persona = self._create_persona(scenario_data, persona_type)
                    personas[persona_type] = persona

            # Store personas
            self._store_personas(scenario_id, personas)

            return {
                'success': True,
                'message': f'Generated {len(personas)} personas',
                'data': personas
            }

        except Exception as e:
            logger.error(f"Error generating personas: {str(e)}")
            return {'success': False, 'error': str(e)}

    def analyze_journeys(self, scenario_id: str, persona_type: str, journey_type: str) -> Dict[str, Any]:
        """Analyze journey paths for a specific persona and journey type"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Get persona
            personas = self._get_personas(scenario_id)
            if persona_type not in personas:
                return {'success': False, 'error': f'Persona {persona_type} not found'}

            persona = personas[persona_type]
            
            # Analyze journey
            journey_analysis = self._analyze_journey_path(scenario_data, persona, journey_type)
            
            # Store journey analysis
            self._store_journey_analysis(scenario_id, persona_type, journey_type, journey_analysis)

            return {
                'success': True,
                'message': f'Analyzed {journey_type} journey for {persona_type}',
                'data': journey_analysis
            }

        except Exception as e:
            logger.error(f"Error analyzing journey: {str(e)}")
            return {'success': False, 'error': str(e)}

    def detect_barriers(self, scenario_id: str, persona_type: str) -> Dict[str, Any]:
        """Detect barriers for a specific persona"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Get persona
            personas = self._get_personas(scenario_id)
            if persona_type not in personas:
                return {'success': False, 'error': f'Persona {persona_type} not found'}

            persona = personas[persona_type]
            
            # Detect barriers
            barriers = self._detect_persona_barriers(scenario_data, persona)
            
            # Store barrier analysis
            self._store_barrier_analysis(scenario_id, persona_type, barriers)

            return {
                'success': True,
                'message': f'Detected barriers for {persona_type}',
                'data': barriers
            }

        except Exception as e:
            logger.error(f"Error detecting barriers: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _get_scenario_data(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get scenario data for persona analysis"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get scenario with parcels and links
            query = """
            SELECT s.*, 
                   COUNT(p.id) as parcel_count,
                   SUM(ST_Area(p.geometry)) as total_area
            FROM scenarios s
            LEFT JOIN parcels p ON s.id = p.scenario_id AND p.status = 'active'
            WHERE s.id = %s
            GROUP BY s.id
            """
            cursor.execute(query, (scenario_id,))
            scenario = cursor.fetchone()
            
            if not scenario:
                return None

            # Get parcels with properties
            query = """
            SELECT id, ST_AsGeoJSON(geometry) as geometry, properties
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            parcels = cursor.fetchall()

            # Get links with properties
            query = """
            SELECT id, ST_AsGeoJSON(geometry) as geometry, properties, link_class
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            links = cursor.fetchall()

            return {
                'scenario': scenario,
                'parcels': parcels,
                'links': links
            }
            
        finally:
            cursor.close()
            conn.close()

    def _create_persona(self, scenario_data: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Create a specific persona for the scenario"""
        template = self.persona_templates[persona_type]
        
        # Generate persona details
        persona = {
            'type': persona_type,
            'name': template['name'],
            'age_range': template['age_range'],
            'mobility_type': template['mobility_type'],
            'speed': template['speed'],
            'max_distance': template['max_distance'],
            'priorities': template['priorities'],
            'barriers': template['barriers'],
            'needs': template['needs'],
            'home_location': self._generate_home_location(scenario_data),
            'destinations': self._generate_destinations(scenario_data, persona_type),
            'preferences': self._generate_preferences(persona_type)
        }
        
        return persona

    def _generate_home_location(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a home location for the persona"""
        parcels = scenario_data['parcels']
        
        # Find residential parcels
        residential_parcels = [
            p for p in parcels 
            if p['properties'].get('useMix', {}).get('residential', 0) > 0.5
        ]
        
        if not residential_parcels:
            # Use any parcel if no residential found
            residential_parcels = parcels
        
        # Select random residential parcel
        home_parcel = random.choice(residential_parcels)
        
        # Generate point within parcel
        geometry = json.loads(home_parcel['geometry'])
        if geometry['type'] == 'Polygon':
            polygon = Polygon(geometry['coordinates'][0])
            point = polygon.representative_point()
        else:
            # Use centroid if not polygon
            point = polygon.centroid
        
        return {
            'parcel_id': home_parcel['id'],
            'coordinates': [point.x, point.y],
            'properties': home_parcel['properties']
        }

    def _generate_destinations(self, scenario_data: Dict[str, Any], persona_type: str) -> Dict[str, Any]:
        """Generate destinations for the persona"""
        parcels = scenario_data['parcels']
        destinations = {}
        
        # Define destination types by persona
        destination_types = {
            'child': ['school', 'playground', 'library'],
            'senior': ['healthcare', 'community_center', 'park'],
            'low_income': ['transit_station', 'grocery', 'employment'],
            'assistive_mobility': ['healthcare', 'community_center', 'accessible_amenity'],
            'cyclist': ['employment', 'transit_station', 'recreation']
        }
        
        persona_destinations = destination_types.get(persona_type, ['employment', 'shopping', 'recreation'])
        
        for dest_type in persona_destinations:
            # Find parcels that could serve as this destination
            suitable_parcels = self._find_suitable_destinations(parcels, dest_type)
            
            if suitable_parcels:
                dest_parcel = random.choice(suitable_parcels)
                geometry = json.loads(dest_parcel['geometry'])
                
                if geometry['type'] == 'Polygon':
                    polygon = Polygon(geometry['coordinates'][0])
                    point = polygon.representative_point()
                else:
                    point = polygon.centroid
                
                destinations[dest_type] = {
                    'parcel_id': dest_parcel['id'],
                    'coordinates': [point.x, point.y],
                    'properties': dest_parcel['properties'],
                    'type': dest_type
                }
        
        return destinations

    def _find_suitable_destinations(self, parcels: List[Dict[str, Any]], dest_type: str) -> List[Dict[str, Any]]:
        """Find parcels suitable for a specific destination type"""
        suitable_parcels = []
        
        for parcel in parcels:
            properties = parcel['properties']
            use_mix = properties.get('useMix', {})
            
            # Simple logic to match destination types to use mixes
            if dest_type == 'school' and use_mix.get('institutional', 0) > 0.3:
                suitable_parcels.append(parcel)
            elif dest_type == 'playground' and properties.get('greenSpacePercent', 0) > 0.5:
                suitable_parcels.append(parcel)
            elif dest_type == 'healthcare' and use_mix.get('institutional', 0) > 0.3:
                suitable_parcels.append(parcel)
            elif dest_type == 'employment' and use_mix.get('commercial', 0) > 0.3:
                suitable_parcels.append(parcel)
            elif dest_type == 'shopping' and use_mix.get('commercial', 0) > 0.3:
                suitable_parcels.append(parcel)
            elif dest_type == 'recreation' and properties.get('greenSpacePercent', 0) > 0.3:
                suitable_parcels.append(parcel)
            elif dest_type == 'transit_station':
                # Assume transit stations are near major roads
                suitable_parcels.append(parcel)
            else:
                # Default: any parcel
                suitable_parcels.append(parcel)
        
        return suitable_parcels

    def _generate_preferences(self, persona_type: str) -> Dict[str, Any]:
        """Generate preferences for the persona"""
        preferences = {
            'route_preference': 'shortest',  # or 'safest', 'most_accessible'
            'time_preference': 'flexible',   # or 'peak_hours', 'off_peak'
            'weather_sensitivity': 'medium', # or 'high', 'low'
            'crowd_tolerance': 'medium',     # or 'high', 'low'
            'cost_sensitivity': 'high'       # or 'medium', 'low'
        }
        
        # Adjust preferences based on persona type
        if persona_type == 'child':
            preferences.update({
                'route_preference': 'safest',
                'weather_sensitivity': 'high',
                'crowd_tolerance': 'low'
            })
        elif persona_type == 'senior':
            preferences.update({
                'route_preference': 'most_accessible',
                'weather_sensitivity': 'high',
                'crowd_tolerance': 'medium'
            })
        elif persona_type == 'low_income':
            preferences.update({
                'route_preference': 'shortest',
                'cost_sensitivity': 'high',
                'time_preference': 'peak_hours'
            })
        elif persona_type == 'assistive_mobility':
            preferences.update({
                'route_preference': 'most_accessible',
                'weather_sensitivity': 'high',
                'crowd_tolerance': 'low'
            })
        elif persona_type == 'cyclist':
            preferences.update({
                'route_preference': 'safest',
                'weather_sensitivity': 'medium',
                'crowd_tolerance': 'high'
            })
        
        return preferences

    def _analyze_journey_path(self, scenario_data: Dict[str, Any], persona: Dict[str, Any], journey_type: str) -> Dict[str, Any]:
        """Analyze a specific journey path"""
        home = persona['home_location']
        destinations = persona['destinations']
        
        # Find destination for this journey type
        destination = None
        if journey_type == 'home_to_work':
            destination = destinations.get('employment')
        elif journey_type == 'home_to_school':
            destination = destinations.get('school')
        elif journey_type == 'home_to_shop':
            destination = destinations.get('shopping')
        elif journey_type == 'home_to_healthcare':
            destination = destinations.get('healthcare')
        elif journey_type == 'home_to_recreation':
            destination = destinations.get('recreation')
        
        if not destination:
            return {'error': f'No destination found for journey type: {journey_type}'}
        
        # Calculate route
        route = self._calculate_route(scenario_data, home, destination, persona)
        
        # Analyze route quality
        route_quality = self._analyze_route_quality(scenario_data, route, persona)
        
        # Calculate journey metrics
        journey_metrics = self._calculate_journey_metrics(route, persona)
        
        return {
            'journey_type': journey_type,
            'origin': home,
            'destination': destination,
            'route': route,
            'route_quality': route_quality,
            'metrics': journey_metrics
        }

    def _calculate_route(self, scenario_data: Dict[str, Any], origin: Dict[str, Any], destination: Dict[str, Any], persona: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate route between origin and destination"""
        # Simplified route calculation
        origin_point = Point(origin['coordinates'])
        dest_point = Point(destination['coordinates'])
        
        # Calculate direct distance
        direct_distance = origin_point.distance(dest_point)
        
        # Simple route with some deviation
        route_factor = 1.2  # Route is 20% longer than direct distance
        route_distance = direct_distance * route_factor
        
        # Calculate travel time
        travel_time = route_distance / persona['speed']
        
        # Generate route points (simplified)
        route_points = self._generate_route_points(origin_point, dest_point, route_factor)
        
        return {
            'distance': route_distance,
            'travel_time': travel_time,
            'route_factor': route_factor,
            'points': route_points,
            'direct_distance': direct_distance
        }

    def _generate_route_points(self, origin: Point, destination: Point, route_factor: float) -> List[List[float]]:
        """Generate route points between origin and destination"""
        # Simplified route generation with some deviation
        points = []
        
        # Add origin
        points.append([origin.x, origin.y])
        
        # Generate intermediate points
        num_points = 5
        for i in range(1, num_points):
            t = i / num_points
            
            # Linear interpolation with some random deviation
            x = origin.x + (destination.x - origin.x) * t
            y = origin.y + (destination.y - origin.y) * t
            
            # Add some random deviation
            deviation = 0.001  # Small deviation
            x += random.uniform(-deviation, deviation)
            y += random.uniform(-deviation, deviation)
            
            points.append([x, y])
        
        # Add destination
        points.append([destination.x, destination.y])
        
        return points

    def _analyze_route_quality(self, scenario_data: Dict[str, Any], route: Dict[str, Any], persona: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality of a route for a specific persona"""
        links = scenario_data['links']
        
        # Analyze route segments
        route_quality = {
            'safety_score': 0.7,  # Placeholder
            'accessibility_score': 0.8,  # Placeholder
            'comfort_score': 0.6,  # Placeholder
            'efficiency_score': 0.9,  # Placeholder
            'overall_score': 0.75,  # Placeholder
            'barriers': [],
            'amenities': []
        }
        
        # Check for barriers along route
        barriers = self._check_route_barriers(route, links, persona)
        route_quality['barriers'] = barriers
        
        # Check for amenities along route
        amenities = self._check_route_amenities(route, scenario_data, persona)
        route_quality['amenities'] = amenities
        
        # Adjust scores based on barriers and amenities
        route_quality = self._adjust_route_scores(route_quality, barriers, amenities, persona)
        
        return route_quality

    def _check_route_barriers(self, route: Dict[str, Any], links: List[Dict[str, Any]], persona: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for barriers along the route"""
        barriers = []
        
        # Check for common barriers based on persona type
        persona_type = persona['type']
        
        if persona_type in ['child', 'senior', 'assistive_mobility']:
            # Check for unsafe crossings
            barriers.append({
                'type': 'unsafe_crossing',
                'severity': 'high',
                'description': 'Major intersection without pedestrian signals',
                'location': route['points'][2]  # Simplified location
            })
        
        if persona_type == 'assistive_mobility':
            # Check for accessibility barriers
            barriers.append({
                'type': 'no_ramp',
                'severity': 'high',
                'description': 'Curb without ramp access',
                'location': route['points'][1]  # Simplified location
            })
        
        if persona_type == 'cyclist':
            # Check for cycling barriers
            barriers.append({
                'type': 'no_bike_lane',
                'severity': 'medium',
                'description': 'Street without dedicated bike lane',
                'location': route['points'][3]  # Simplified location
            })
        
        return barriers

    def _check_route_amenities(self, route: Dict[str, Any], scenario_data: Dict[str, Any], persona: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for amenities along the route"""
        amenities = []
        
        # Check for benches, shade, etc.
        amenities.append({
            'type': 'bench',
            'description': 'Rest area with seating',
            'location': route['points'][2],  # Simplified location
            'usefulness': 'high'
        })
        
        amenities.append({
            'type': 'shade',
            'description': 'Tree canopy providing shade',
            'location': route['points'][1],  # Simplified location
            'usefulness': 'medium'
        })
        
        return amenities

    def _adjust_route_scores(self, route_quality: Dict[str, Any], barriers: List[Dict[str, Any]], amenities: List[Dict[str, Any]], persona: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust route quality scores based on barriers and amenities"""
        # Adjust safety score based on barriers
        safety_penalty = len([b for b in barriers if b['severity'] == 'high']) * 0.1
        route_quality['safety_score'] = max(0, route_quality['safety_score'] - safety_penalty)
        
        # Adjust accessibility score
        accessibility_penalty = len([b for b in barriers if b['type'] in ['no_ramp', 'narrow_path']]) * 0.15
        route_quality['accessibility_score'] = max(0, route_quality['accessibility_score'] - accessibility_penalty)
        
        # Adjust comfort score based on amenities
        comfort_boost = len([a for a in amenities if a['usefulness'] == 'high']) * 0.05
        route_quality['comfort_score'] = min(1.0, route_quality['comfort_score'] + comfort_boost)
        
        # Recalculate overall score
        route_quality['overall_score'] = (
            route_quality['safety_score'] * 0.3 +
            route_quality['accessibility_score'] * 0.3 +
            route_quality['comfort_score'] * 0.2 +
            route_quality['efficiency_score'] * 0.2
        )
        
        return route_quality

    def _calculate_journey_metrics(self, route: Dict[str, Any], persona: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate journey metrics"""
        return {
            'distance_meters': route['distance'],
            'travel_time_minutes': route['travel_time'] / 60,
            'speed_mps': persona['speed'],
            'feasibility': route['distance'] <= persona['max_distance'],
            'energy_expenditure': route['distance'] * 0.1,  # Simplified calculation
            'carbon_footprint': route['distance'] * 0.0001  # Simplified calculation
        }

    def _detect_persona_barriers(self, scenario_data: Dict[str, Any], persona: Dict[str, Any]) -> Dict[str, Any]:
        """Detect barriers for a specific persona"""
        barriers = {
            'physical_barriers': [],
            'accessibility_barriers': [],
            'safety_barriers': [],
            'comfort_barriers': [],
            'mitigation_suggestions': []
        }
        
        persona_type = persona['type']
        links = scenario_data['links']
        
        # Detect barriers based on persona type
        if persona_type in ['child', 'senior', 'assistive_mobility']:
            # Check for pedestrian barriers
            barriers['safety_barriers'].append({
                'type': 'unsafe_crossing',
                'count': len([l for l in links if l['link_class'] in ['arterial', 'collector']]),
                'description': 'Major roads without pedestrian signals',
                'impact': 'high'
            })
        
        if persona_type == 'assistive_mobility':
            barriers['accessibility_barriers'].append({
                'type': 'no_ramps',
                'count': len(links),  # Simplified
                'description': 'Curb cuts missing at intersections',
                'impact': 'high'
            })
        
        if persona_type == 'cyclist':
            barriers['safety_barriers'].append({
                'type': 'no_bike_lanes',
                'count': len([l for l in links if l['link_class'] in ['arterial', 'collector']]),
                'description': 'Major roads without bike lanes',
                'impact': 'medium'
            })
        
        # Generate mitigation suggestions
        barriers['mitigation_suggestions'] = self._generate_mitigation_suggestions(barriers, persona_type)
        
        return barriers

    def _generate_mitigation_suggestions(self, barriers: Dict[str, Any], persona_type: str) -> List[Dict[str, Any]]:
        """Generate mitigation suggestions for detected barriers"""
        suggestions = []
        
        for barrier_type, barrier_list in barriers.items():
            if barrier_type == 'mitigation_suggestions':
                continue
                
            for barrier in barrier_list:
                if barrier['type'] == 'unsafe_crossing':
                    suggestions.append({
                        'barrier_type': barrier['type'],
                        'suggestion': 'Install pedestrian signals and crosswalks',
                        'priority': 'high',
                        'cost_estimate': 'medium',
                        'implementation_time': '3-6 months'
                    })
                
                elif barrier['type'] == 'no_ramps':
                    suggestions.append({
                        'barrier_type': barrier['type'],
                        'suggestion': 'Add curb cuts and ramps at all intersections',
                        'priority': 'high',
                        'cost_estimate': 'low',
                        'implementation_time': '1-3 months'
                    })
                
                elif barrier['type'] == 'no_bike_lanes':
                    suggestions.append({
                        'barrier_type': barrier['type'],
                        'suggestion': 'Install dedicated bike lanes on major roads',
                        'priority': 'medium',
                        'cost_estimate': 'medium',
                        'implementation_time': '6-12 months'
                    })
        
        return suggestions

    def _store_personas(self, scenario_id: str, personas: Dict[str, Any]):
        """Store personas in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with personas data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{personas}',
                %s::jsonb
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            cursor.execute(query, (json.dumps(personas), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def _get_personas(self, scenario_id: str) -> Dict[str, Any]:
        """Get personas from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT kpis->'personas' as personas
            FROM scenarios
            WHERE id = %s
            """
            cursor.execute(query, (scenario_id,))
            result = cursor.fetchone()
            
            if result and result['personas']:
                return result['personas']
            else:
                return {}
                
        finally:
            cursor.close()
            conn.close()

    def _store_journey_analysis(self, scenario_id: str, persona_type: str, journey_type: str, analysis: Dict[str, Any]):
        """Store journey analysis in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with journey analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{journey_analysis}',
                jsonb_set(
                    COALESCE(kpis->'journey_analysis', '{}'::jsonb),
                    %s,
                    %s::jsonb
                )
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            key = f'{{{persona_type}_{journey_type}}}'
            cursor.execute(query, (key, json.dumps(analysis), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def _store_barrier_analysis(self, scenario_id: str, persona_type: str, barriers: Dict[str, Any]):
        """Store barrier analysis in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with barrier analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{barrier_analysis}',
                jsonb_set(
                    COALESCE(kpis->'barrier_analysis', '{}'::jsonb),
                    %s,
                    %s::jsonb
                )
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            key = f'{{{persona_type}}}'
            cursor.execute(query, (key, json.dumps(barriers), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
