# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BudgetModel:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Default cost parameters (USD)
        self.cost_library = {
            'infrastructure': {
                'streets': {
                    'arterial': 2500,  # USD per linear meter
                    'collector': 1800,
                    'local': 1200,
                    'pedestrian': 800,
                    'bike_lane': 200,  # USD per linear meter
                    'sidewalk': 150,
                    'transit_lane': 300
                },
                'utilities': {
                    'water_main': 800,  # USD per linear meter
                    'sewer_main': 1000,
                    'storm_drain': 600,
                    'electrical': 400,
                    'telecom': 200,
                    'gas': 300
                },
                'parks': {
                    'neighborhood_park': 150,  # USD per m²
                    'pocket_park': 200,
                    'playground': 300,
                    'bioswale': 100,
                    'tree_planting': 500  # USD per tree
                }
            },
            'buildings': {
                'residential': {
                    'low_rise': 2000,  # USD per m²
                    'mid_rise': 2500,
                    'high_rise': 3500,
                    'affordable': 1800
                },
                'commercial': {
                    'office': 3000,
                    'retail': 2500,
                    'industrial': 1500,
                    'mixed_use': 2800
                },
                'institutional': {
                    'school': 3500,
                    'community_center': 3000,
                    'library': 4000,
                    'healthcare': 4500
                }
            },
            'sustainability': {
                'solar_pv': 2000,  # USD per kW
                'battery_storage': 500,  # USD per kWh
                'green_roof': 300,  # USD per m²
                'rainwater_harvesting': 100,  # USD per m³
                'ev_charging': 5000,  # USD per station
                'bike_infrastructure': 200  # USD per bike space
            },
            'soft_costs': {
                'design': 0.08,  # 8% of construction cost
                'permits': 0.02,  # 2% of construction cost
                'legal': 0.01,  # 1% of construction cost
                'insurance': 0.015,  # 1.5% of construction cost
                'contingency': 0.10  # 10% of construction cost
            }
        }

    def calculate_budget(self, scenario_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate comprehensive budget for a scenario"""
        try:
            # Get scenario data
            parcels = self._get_parcels(scenario_id)
            links = self._get_links(scenario_id)
            
            if not parcels:
                return {'success': False, 'error': 'No parcels found for scenario'}

            # Update cost library with provided parameters
            if params:
                self._update_cost_library(params)

            # Calculate infrastructure costs
            infrastructure_costs = self._calculate_infrastructure_costs(links)
            
            # Calculate building costs
            building_costs = self._calculate_building_costs(parcels)
            
            # Calculate sustainability costs
            sustainability_costs = self._calculate_sustainability_costs(parcels)
            
            # Calculate soft costs
            soft_costs = self._calculate_soft_costs(infrastructure_costs, building_costs, sustainability_costs)
            
            # Calculate total budget
            total_budget = self._calculate_total_budget(infrastructure_costs, building_costs, sustainability_costs, soft_costs)
            
            # Calculate per-unit and per-area costs
            unit_metrics = self._calculate_unit_metrics(total_budget, parcels)

            # Store results
            self._store_budget_analysis(scenario_id, {
                'infrastructure': infrastructure_costs,
                'buildings': building_costs,
                'sustainability': sustainability_costs,
                'soft_costs': soft_costs,
                'total': total_budget,
                'unit_metrics': unit_metrics
            })

            return {
                'success': True,
                'message': f'Calculated budget for {len(parcels)} parcels',
                'data': {
                    'infrastructure': infrastructure_costs,
                    'buildings': building_costs,
                    'sustainability': sustainability_costs,
                    'soft_costs': soft_costs,
                    'total': total_budget,
                    'unit_metrics': unit_metrics
                }
            }

        except Exception as e:
            logger.error(f"Error calculating budget: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_parcels(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get parcels with capacity data from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_Area(geometry) as area, properties, capacity
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _get_links(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get network links from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_Length(geometry) as length, properties, link_class
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _update_cost_library(self, params: Dict[str, Any]):
        """Update cost library with provided parameters"""
        for category, values in params.items():
            if category in self.cost_library:
                if isinstance(values, dict):
                    self.cost_library[category].update(values)
                else:
                    self.cost_library[category] = values

    def _calculate_infrastructure_costs(self, links: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate infrastructure costs"""
        street_costs = {}
        utility_costs = {}
        total_street_cost = 0
        total_utility_cost = 0
        
        for link in links:
            properties = link['properties']
            length = link['length']
            link_class = link['link_class']
            
            # Street costs
            if link_class in self.cost_library['infrastructure']['streets']:
                street_cost = length * self.cost_library['infrastructure']['streets'][link_class]
                street_costs[link_class] = street_costs.get(link_class, 0) + street_cost
                total_street_cost += street_cost
            
            # Utility costs (simplified - assume all streets have utilities)
            utility_cost_per_meter = sum(self.cost_library['infrastructure']['utilities'].values())
            utility_cost = length * utility_cost_per_meter
            total_utility_cost += utility_cost
        
        # Park costs (simplified - assume 10% of total area for parks)
        total_area = sum(link['length'] * 20 for link in links)  # Assume 20m average street width
        park_area = total_area * 0.1
        park_cost = park_area * self.cost_library['infrastructure']['parks']['neighborhood_park']
        
        return {
            'streets': street_costs,
            'utilities': {'total': total_utility_cost},
            'parks': {'total': park_cost},
            'total': total_street_cost + total_utility_cost + park_cost
        }

    def _calculate_building_costs(self, parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate building costs by use type"""
        building_costs = {}
        total_cost = 0
        
        for parcel in parcels:
            properties = parcel['properties']
            capacity = parcel.get('capacity', {})
            
            use_mix = properties.get('useMix', {'residential': 1.0})
            floor_area = capacity.get('floor_area', 0)
            height = properties.get('height', 15)
            
            # Determine building type based on height
            if height <= 12:  # 3-4 stories
                building_type = 'low_rise'
            elif height <= 30:  # 5-10 stories
                building_type = 'mid_rise'
            else:
                building_type = 'high_rise'
            
            # Calculate costs by use type
            for use_type, mix_ratio in use_mix.items():
                use_floor_area = floor_area * mix_ratio
                
                if use_type == 'residential':
                    # Check if affordable housing
                    inclusionary = properties.get('inclusionary', 0)
                    if inclusionary > 0:
                        affordable_area = use_floor_area * (inclusionary / 100)
                        market_area = use_floor_area - affordable_area
                        
                        affordable_cost = affordable_area * self.cost_library['buildings']['residential']['affordable']
                        market_cost = market_area * self.cost_library['buildings']['residential'][building_type]
                        use_cost = affordable_cost + market_cost
                    else:
                        use_cost = use_floor_area * self.cost_library['buildings']['residential'][building_type]
                else:
                    # Commercial/industrial/institutional
                    if use_type in self.cost_library['buildings']:
                        use_cost = use_floor_area * self.cost_library['buildings'][use_type].get('office', 3000)
                    else:
                        use_cost = use_floor_area * 2500  # Default commercial cost
                
                building_costs[use_type] = building_costs.get(use_type, 0) + use_cost
                total_cost += use_cost
        
        building_costs['total'] = total_cost
        return building_costs

    def _calculate_sustainability_costs(self, parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate sustainability feature costs"""
        sustainability_costs = {}
        total_cost = 0
        
        for parcel in parcels:
            properties = parcel['properties']
            capacity = parcel.get('capacity', {})
            
            # Solar PV costs (from energy analysis)
            if 'solar_potential' in capacity:
                solar_kw = capacity['solar_potential'].get('system_size_kw', 0)
                solar_cost = solar_kw * self.cost_library['sustainability']['solar_pv']
                sustainability_costs['solar_pv'] = sustainability_costs.get('solar_pv', 0) + solar_cost
                total_cost += solar_cost
            
            # Green roof costs
            roof_area = capacity.get('floor_area', 0) / max(properties.get('floors', 1), 1)
            green_roof_coverage = properties.get('greenRoofPercent', 0) / 100
            green_roof_cost = roof_area * green_roof_coverage * self.cost_library['sustainability']['green_roof']
            sustainability_costs['green_roof'] = sustainability_costs.get('green_roof', 0) + green_roof_cost
            total_cost += green_roof_cost
            
            # EV charging costs
            parking_spaces = capacity.get('parking_spaces', 0)
            ev_charging_ratio = 0.1  # Assume 10% of parking spaces have EV charging
            ev_charging_cost = parking_spaces * ev_charging_ratio * self.cost_library['sustainability']['ev_charging']
            sustainability_costs['ev_charging'] = sustainability_costs.get('ev_charging', 0) + ev_charging_cost
            total_cost += ev_charging_cost
        
        sustainability_costs['total'] = total_cost
        return sustainability_costs

    def _calculate_soft_costs(self, infrastructure_costs: Dict[str, Any], building_costs: Dict[str, Any], sustainability_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate soft costs"""
        construction_cost = infrastructure_costs['total'] + building_costs['total'] + sustainability_costs['total']
        
        soft_costs = {}
        total_soft_cost = 0
        
        for cost_type, percentage in self.cost_library['soft_costs'].items():
            cost = construction_cost * percentage
            soft_costs[cost_type] = cost
            total_soft_cost += cost
        
        soft_costs['total'] = total_soft_cost
        return soft_costs

    def _calculate_total_budget(self, infrastructure_costs: Dict[str, Any], building_costs: Dict[str, Any], sustainability_costs: Dict[str, Any], soft_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total budget"""
        construction_cost = infrastructure_costs['total'] + building_costs['total'] + sustainability_costs['total']
        total_cost = construction_cost + soft_costs['total']
        
        return {
            'construction': construction_cost,
            'soft_costs': soft_costs['total'],
            'total': total_cost,
            'breakdown': {
                'infrastructure': infrastructure_costs['total'],
                'buildings': building_costs['total'],
                'sustainability': sustainability_costs['total']
            }
        }

    def _calculate_unit_metrics(self, total_budget: Dict[str, Any], parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate per-unit and per-area metrics"""
        total_units = sum(p.get('capacity', {}).get('units', 0) for p in parcels)
        total_area = sum(p['area'] for p in parcels)
        total_floor_area = sum(p.get('capacity', {}).get('floor_area', 0) for p in parcels)
        
        return {
            'cost_per_unit': total_budget['total'] / total_units if total_units > 0 else 0,
            'cost_per_sqm': total_budget['total'] / total_area if total_area > 0 else 0,
            'cost_per_floor_sqm': total_budget['total'] / total_floor_area if total_floor_area > 0 else 0,
            'total_units': total_units,
            'total_area': total_area,
            'total_floor_area': total_floor_area
        }

    def _store_budget_analysis(self, scenario_id: str, analysis_data: Dict[str, Any]):
        """Store budget analysis results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with budget analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{budget_analysis}',
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

    def get_budget_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get budget analysis summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'budget_analysis' as budget_analysis
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['budget_analysis']:
                    return {
                        'success': True,
                        'data': result['budget_analysis']
                    }
                else:
                    return {'success': False, 'error': 'No budget analysis data found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting budget summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
