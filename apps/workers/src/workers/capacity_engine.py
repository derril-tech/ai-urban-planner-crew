# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CapacityEngine:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Default assumptions
        self.defaults = {
            'avg_unit_floor_area': 85,  # m² per unit
            'efficiency': 0.85,  # 85% efficiency (corridors, etc.)
            'occupancy': 2.5,  # persons per unit
            'job_density': {
                'residential': 0,
                'commercial': 50,  # jobs per 1000m²
                'industrial': 25,
                'institutional': 15,
                'mixed_use': 30
            },
            'floor_height': 3.5,  # meters
            'parking_spaces_per_unit': 1.5
        }

    def calculate_capacity(self, scenario_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate capacity for all parcels in a scenario"""
        try:
            # Get parcels for scenario
            parcels = self._get_parcels(scenario_id)
            if not parcels:
                return {'success': False, 'error': 'No parcels found for scenario'}

            # Update defaults with provided parameters
            if params:
                self.defaults.update(params)

            # Calculate capacity for each parcel
            results = []
            total_units = 0
            total_population = 0
            total_jobs = 0
            total_floor_area = 0

            for parcel in parcels:
                capacity = self._calculate_parcel_capacity(parcel)
                results.append(capacity)
                
                total_units += capacity['units']
                total_population += capacity['population']
                total_jobs += capacity['jobs']
                total_floor_area += capacity['floor_area']

            # Store results in database
            self._store_capacity_results(scenario_id, results)

            return {
                'success': True,
                'message': f'Calculated capacity for {len(parcels)} parcels',
                'data': {
                    'parcels_count': len(parcels),
                    'total_units': total_units,
                    'total_population': total_population,
                    'total_jobs': total_jobs,
                    'total_floor_area': total_floor_area,
                    'parcels': results
                }
            }

        except Exception as e:
            logger.error(f"Error calculating capacity: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_parcels(self, scenario_id: str) -> List[Dict[str, Any]]:
        """Get parcels from database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT id, ST_Area(geometry) as area, properties
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()

    def _calculate_parcel_capacity(self, parcel: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate capacity for a single parcel"""
        area = parcel['area']  # m²
        properties = parcel['properties']
        
        # Extract zoning properties
        use_mix = properties.get('useMix', {'residential': 1.0})
        far = properties.get('far', 2.0)
        height = properties.get('height', 15)
        lot_coverage = properties.get('lotCoverage', 0.6)
        
        # Calculate floor area
        floor_area = area * far * lot_coverage
        
        # Calculate units by use type
        units_by_use = {}
        total_units = 0
        
        for use_type, mix_ratio in use_mix.items():
            if use_type == 'residential':
                use_floor_area = floor_area * mix_ratio
                units = int(use_floor_area / self.defaults['avg_unit_floor_area'] * self.defaults['efficiency'])
                units_by_use[use_type] = units
                total_units += units
        
        # Calculate population
        population = total_units * self.defaults['occupancy']
        
        # Calculate jobs by use type
        jobs_by_use = {}
        total_jobs = 0
        
        for use_type, mix_ratio in use_mix.items():
            if use_type != 'residential':
                use_floor_area = floor_area * mix_ratio
                job_density = self.defaults['job_density'].get(use_type, 0)
                jobs = int(use_floor_area / 1000 * job_density)  # jobs per 1000m²
                jobs_by_use[use_type] = jobs
                total_jobs += jobs
        
        # Calculate parking spaces
        parking_spaces = total_units * self.defaults['parking_spaces_per_unit']
        
        # Calculate building height and floors
        floors = int(height / self.defaults['floor_height'])
        
        return {
            'parcel_id': parcel['id'],
            'area': area,
            'floor_area': floor_area,
            'units': total_units,
            'units_by_use': units_by_use,
            'population': population,
            'jobs': total_jobs,
            'jobs_by_use': jobs_by_use,
            'parking_spaces': parking_spaces,
            'floors': floors,
            'far': far,
            'height': height,
            'lot_coverage': lot_coverage
        }

    def _store_capacity_results(self, scenario_id: str, results: List[Dict[str, Any]]):
        """Store capacity results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update parcels with capacity data
            for result in results:
                capacity_data = {
                    'units': result['units'],
                    'population': result['population'],
                    'jobs': result['jobs'],
                    'floor_area': result['floor_area'],
                    'parking_spaces': result['parking_spaces'],
                    'units_by_use': result['units_by_use'],
                    'jobs_by_use': result['jobs_by_use']
                }
                
                query = """
                UPDATE parcels 
                SET capacity = %s, updated_at = NOW()
                WHERE id = %s
                """
                cursor.execute(query, (json.dumps(capacity_data), result['parcel_id']))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def validate_zoning(self, scenario_id: str) -> Dict[str, Any]:
        """Validate zoning compliance and constraints"""
        try:
            parcels = self._get_parcels(scenario_id)
            
            validation_results = {
                'valid': True,
                'issues': [],
                'warnings': [],
                'parcels_checked': len(parcels)
            }
            
            for parcel in parcels:
                properties = parcel['properties']
                area = parcel['area']
                
                # Check use mix sums to 100%
                use_mix = properties.get('useMix', {})
                total_mix = sum(use_mix.values())
                if abs(total_mix - 1.0) > 0.01:
                    validation_results['issues'].append({
                        'parcel_id': parcel['id'],
                        'type': 'use_mix_sum',
                        'message': f'Use mix does not sum to 100% (sum: {total_mix:.2f})'
                    })
                    validation_results['valid'] = False
                
                # Check FAR constraints
                far = properties.get('far', 0)
                if far > 10:  # Arbitrary max FAR
                    validation_results['warnings'].append({
                        'parcel_id': parcel['id'],
                        'type': 'high_far',
                        'message': f'FAR of {far} seems very high'
                    })
                
                # Check setbacks feasibility
                setbacks = properties.get('setbacks', {})
                lot_coverage = properties.get('lotCoverage', 0.6)
                
                # Simple setback validation
                if lot_coverage > 0.9:
                    validation_results['warnings'].append({
                        'parcel_id': parcel['id'],
                        'type': 'high_coverage',
                        'message': f'Lot coverage of {lot_coverage:.1%} may not leave room for setbacks'
                    })
                
                # Check area constraints
                if area < 100:  # 100m² minimum
                    validation_results['issues'].append({
                        'parcel_id': parcel['id'],
                        'type': 'small_area',
                        'message': f'Parcel area of {area:.1f}m² is very small'
                    })
                    validation_results['valid'] = False
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating zoning: {str(e)}")
            return {
                'valid': False,
                'error': str(e)
            }

    def get_capacity_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get capacity summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                # Get capacity data from parcels
                query = """
                SELECT capacity, properties
                FROM parcels
                WHERE scenario_id = %s AND status = 'active' AND capacity IS NOT NULL
                """
                cursor.execute(query, (scenario_id,))
                parcels = cursor.fetchall()
                
                if not parcels:
                    return {'success': False, 'error': 'No capacity data found'}
                
                # Aggregate totals
                totals = {
                    'total_units': 0,
                    'total_population': 0,
                    'total_jobs': 0,
                    'total_floor_area': 0,
                    'total_parking_spaces': 0,
                    'units_by_use': {},
                    'jobs_by_use': {}
                }
                
                for parcel in parcels:
                    capacity = parcel['capacity']
                    totals['total_units'] += capacity.get('units', 0)
                    totals['total_population'] += capacity.get('population', 0)
                    totals['total_jobs'] += capacity.get('jobs', 0)
                    totals['total_floor_area'] += capacity.get('floor_area', 0)
                    totals['total_parking_spaces'] += capacity.get('parking_spaces', 0)
                    
                    # Aggregate by use type
                    for use_type, units in capacity.get('units_by_use', {}).items():
                        totals['units_by_use'][use_type] = totals['units_by_use'].get(use_type, 0) + units
                    
                    for use_type, jobs in capacity.get('jobs_by_use', {}).items():
                        totals['jobs_by_use'][use_type] = totals['jobs_by_use'].get(use_type, 0) + jobs
                
                return {
                    'success': True,
                    'data': totals
                }
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting capacity summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
