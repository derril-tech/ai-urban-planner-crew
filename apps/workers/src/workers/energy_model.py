# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnergyModel:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Default energy parameters
        self.defaults = {
            'solar_irradiance': 4.5,  # kWh/m²/day (average US)
            'panel_efficiency': 0.20,  # 20% efficient panels
            'system_losses': 0.14,  # 14% system losses
            'roof_coverage': 0.7,  # 70% of roof area available for panels
            'energy_demand_per_unit': 30,  # kWh/day per residential unit
            'energy_demand_per_sqm': 0.15,  # kWh/day per m² of commercial space
            'battery_efficiency': 0.9,  # 90% round-trip efficiency
            'battery_depth_of_discharge': 0.8,  # 80% DoD
            'grid_emissions': 0.4,  # kg CO2/kWh (US average)
            'solar_emissions': 0.04,  # kg CO2/kWh (manufacturing)
        }

    def analyze_energy(self, scenario_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze energy demand and solar potential for a scenario"""
        try:
            # Get parcels and their properties
            parcels = self._get_parcels(scenario_id)
            if not parcels:
                return {'success': False, 'error': 'No parcels found for scenario'}

            # Update defaults with provided parameters
            if params:
                self.defaults.update(params)

            # Calculate energy demand
            demand_analysis = self._calculate_energy_demand(parcels)
            
            # Calculate solar potential
            solar_analysis = self._calculate_solar_potential(parcels)
            
            # Calculate storage requirements
            storage_analysis = self._calculate_storage_requirements(demand_analysis, solar_analysis)
            
            # Calculate emissions impact
            emissions_analysis = self._calculate_emissions_impact(demand_analysis, solar_analysis)

            # Store results
            self._store_energy_analysis(scenario_id, {
                'demand': demand_analysis,
                'solar': solar_analysis,
                'storage': storage_analysis,
                'emissions': emissions_analysis
            })

            return {
                'success': True,
                'message': f'Analyzed energy for {len(parcels)} parcels',
                'data': {
                    'demand': demand_analysis,
                    'solar': solar_analysis,
                    'storage': storage_analysis,
                    'emissions': emissions_analysis
                }
            }

        except Exception as e:
            logger.error(f"Error analyzing energy: {str(e)}")
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

    def _calculate_energy_demand(self, parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate energy demand by use type"""
        total_demand = 0
        demand_by_use = {}
        
        for parcel in parcels:
            properties = parcel['properties']
            capacity = parcel.get('capacity', {})
            
            # Get use mix and floor area
            use_mix = properties.get('useMix', {'residential': 1.0})
            floor_area = capacity.get('floor_area', 0)
            
            # Calculate demand by use type
            parcel_demand = 0
            for use_type, mix_ratio in use_mix.items():
                if use_type == 'residential':
                    units = capacity.get('units', 0)
                    use_demand = units * self.defaults['energy_demand_per_unit']
                else:
                    # Commercial/industrial/institutional
                    use_floor_area = floor_area * mix_ratio
                    use_demand = use_floor_area * self.defaults['energy_demand_per_sqm']
                
                demand_by_use[use_type] = demand_by_use.get(use_type, 0) + use_demand
                parcel_demand += use_demand
            
            total_demand += parcel_demand
        
        return {
            'total_demand_kwh_day': total_demand,
            'total_demand_kwh_year': total_demand * 365,
            'demand_by_use': demand_by_use,
            'avg_demand_per_unit': total_demand / sum(p.get('capacity', {}).get('units', 0) for p in parcels) if any(p.get('capacity', {}).get('units', 0) for p in parcels) else 0
        }

    def _calculate_solar_potential(self, parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate solar PV potential"""
        total_potential = 0
        total_roof_area = 0
        solar_by_parcel = []
        
        for parcel in parcels:
            properties = parcel['properties']
            capacity = parcel.get('capacity', {})
            
            # Calculate roof area (simplified)
            floor_area = capacity.get('floor_area', 0)
            floors = capacity.get('floors', 1)
            
            # Assume roof area equals ground floor area
            roof_area = floor_area / floors if floors > 0 else 0
            available_roof_area = roof_area * self.defaults['roof_coverage']
            
            # Calculate solar potential
            daily_energy = (
                available_roof_area * 
                self.defaults['solar_irradiance'] * 
                self.defaults['panel_efficiency'] * 
                (1 - self.defaults['system_losses'])
            )
            
            annual_energy = daily_energy * 365
            
            # Calculate system size (kW)
            system_size = (daily_energy / self.defaults['solar_irradiance']) / self.defaults['panel_efficiency']
            
            solar_by_parcel.append({
                'parcel_id': parcel['id'],
                'roof_area': roof_area,
                'available_area': available_roof_area,
                'system_size_kw': system_size,
                'daily_energy_kwh': daily_energy,
                'annual_energy_kwh': annual_energy
            })
            
            total_potential += annual_energy
            total_roof_area += roof_area
        
        return {
            'total_annual_energy_kwh': total_potential,
            'total_roof_area_m2': total_roof_area,
            'total_system_size_kw': total_potential / (365 * self.defaults['solar_irradiance'] * self.defaults['panel_efficiency']),
            'solar_by_parcel': solar_by_parcel,
            'avg_system_size_kw': total_potential / (len(parcels) * 365 * self.defaults['solar_irradiance'] * self.defaults['panel_efficiency']) if parcels else 0
        }

    def _calculate_storage_requirements(self, demand_analysis: Dict[str, Any], solar_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate battery storage requirements"""
        daily_demand = demand_analysis['total_demand_kwh_day']
        daily_solar = solar_analysis['total_annual_energy_kwh'] / 365
        
        # Calculate energy deficit/surplus
        daily_deficit = max(0, daily_demand - daily_solar)
        daily_surplus = max(0, daily_solar - daily_demand)
        
        # Calculate storage requirements
        # Assume we want to store surplus for 1 day of deficit
        storage_capacity_kwh = daily_deficit / self.defaults['battery_depth_of_discharge']
        
        # Calculate battery size (kWh to kW conversion)
        battery_power_kw = storage_capacity_kwh / 4  # Assume 4-hour discharge rate
        
        # Calculate cost estimates (rough)
        solar_cost_per_kw = 2000  # USD per kW
        battery_cost_per_kwh = 500  # USD per kWh
        
        solar_cost = solar_analysis['total_system_size_kw'] * solar_cost_per_kw
        battery_cost = storage_capacity_kwh * battery_cost_per_kwh
        
        return {
            'daily_deficit_kwh': daily_deficit,
            'daily_surplus_kwh': daily_surplus,
            'storage_capacity_kwh': storage_capacity_kwh,
            'battery_power_kw': battery_power_kw,
            'solar_cost_usd': solar_cost,
            'battery_cost_usd': battery_cost,
            'total_cost_usd': solar_cost + battery_cost,
            'energy_self_sufficiency': min(1.0, daily_solar / daily_demand) if daily_demand > 0 else 0
        }

    def _calculate_emissions_impact(self, demand_analysis: Dict[str, Any], solar_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions impact of solar vs grid"""
        annual_demand = demand_analysis['total_demand_kwh_year']
        annual_solar = solar_analysis['total_annual_energy_kwh']
        
        # Grid emissions
        grid_emissions = annual_demand * self.defaults['grid_emissions']
        
        # Solar emissions (manufacturing only)
        solar_emissions = annual_solar * self.defaults['solar_emissions']
        
        # Net emissions reduction
        emissions_reduction = grid_emissions - solar_emissions
        
        # Carbon offset equivalent
        # 1 tree absorbs ~22 kg CO2/year
        trees_equivalent = emissions_reduction / 22
        
        return {
            'grid_emissions_kg_co2_year': grid_emissions,
            'solar_emissions_kg_co2_year': solar_emissions,
            'emissions_reduction_kg_co2_year': emissions_reduction,
            'emissions_reduction_percent': (emissions_reduction / grid_emissions * 100) if grid_emissions > 0 else 0,
            'trees_equivalent': trees_equivalent,
            'carbon_offset_value_usd': emissions_reduction * 0.05  # $0.05 per kg CO2
        }

    def _store_energy_analysis(self, scenario_id: str, analysis_data: Dict[str, Any]):
        """Store energy analysis results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with energy analysis data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{energy_analysis}',
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

    def get_energy_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get energy analysis summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'energy_analysis' as energy_analysis
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['energy_analysis']:
                    return {
                        'success': True,
                        'data': result['energy_analysis']
                    }
                else:
                    return {'success': False, 'error': 'No energy analysis data found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting energy summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
