# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np
from scipy.optimize import minimize, differential_evolution
from itertools import combinations
import random

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScenarioOptimizer:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Parameter ranges for optimization
        self.parameter_ranges = {
            'far': {'min': 0.5, 'max': 8.0, 'default': 2.0},
            'height': {'min': 3, 'max': 50, 'default': 15},
            'lot_coverage': {'min': 0.2, 'max': 0.8, 'default': 0.5},
            'parking_ratio': {'min': 0.5, 'max': 2.0, 'default': 1.0},
            'green_space_ratio': {'min': 0.05, 'max': 0.4, 'default': 0.15},
            'mixed_use_ratio': {'min': 0.1, 'max': 0.9, 'default': 0.3},
            'solar_coverage': {'min': 0.1, 'max': 0.8, 'default': 0.3},
            'bike_infrastructure': {'min': 0.1, 'max': 0.9, 'default': 0.3},
            'transit_priority': {'min': 0.0, 'max': 1.0, 'default': 0.5},
            'inclusionary_housing': {'min': 0.0, 'max': 0.3, 'default': 0.1}
        }

        # Optimization objectives and weights
        self.objectives = {
            'sustainability_score': {'weight': 0.4, 'direction': 'maximize'},
            'cost_efficiency': {'weight': 0.3, 'direction': 'maximize'},
            'density': {'weight': 0.2, 'direction': 'maximize'},
            'accessibility': {'weight': 0.1, 'direction': 'maximize'}
        }

        # Constraints
        self.constraints = {
            'min_units': 100,
            'max_budget': 100000000,  # $100M
            'min_sustainability_score': 60,
            'max_height_variance': 0.5,  # 50% variance from baseline
            'min_parking_spaces': 0.8  # 80% of calculated need
        }

    def optimize_scenario(self, scenario_id: str, optimization_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate Pareto optimal solutions for a scenario"""
        try:
            # Get baseline scenario data
            baseline_data = self._get_scenario_data(scenario_id)
            if not baseline_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Update parameters if provided
            if optimization_params:
                self._update_optimization_params(optimization_params)

            # Generate parameter combinations for Pareto analysis
            pareto_solutions = self._generate_pareto_solutions(baseline_data)
            
            # Calculate trade-off analysis
            trade_offs = self._calculate_trade_offs(pareto_solutions)
            
            # Generate tornado chart data
            tornado_data = self._generate_tornado_chart(baseline_data)
            
            # Store optimization results
            results = {
                'pareto_solutions': pareto_solutions,
                'trade_offs': trade_offs,
                'tornado_chart': tornado_data,
                'baseline': baseline_data,
                'optimization_params': {
                    'parameter_ranges': self.parameter_ranges,
                    'objectives': self.objectives,
                    'constraints': self.constraints
                }
            }

            self._store_optimization_results(scenario_id, results)

            return {
                'success': True,
                'message': f'Generated {len(pareto_solutions)} Pareto optimal solutions',
                'data': results
            }

        except Exception as e:
            logger.error(f"Error optimizing scenario: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _get_scenario_data(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get scenario data for optimization"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get scenario with all analysis data
            query = """
            SELECT s.*, 
                   COUNT(p.id) as parcel_count,
                   SUM(ST_Area(p.geometry)) as total_area,
                   AVG(p.properties->>'far')::float as avg_far,
                   AVG(p.properties->>'height')::float as avg_height,
                   AVG(p.properties->>'lot_coverage')::float as avg_lot_coverage
            FROM scenarios s
            LEFT JOIN parcels p ON s.id = p.scenario_id AND p.status = 'active'
            WHERE s.id = %s
            GROUP BY s.id
            """
            cursor.execute(query, (scenario_id,))
            scenario = cursor.fetchone()
            
            if not scenario:
                return None

            # Get parcels with all data
            query = """
            SELECT properties, capacity, utilities
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            parcels = cursor.fetchall()

            # Get links
            query = """
            SELECT properties, link_class
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            links = cursor.fetchall()

            return {
                'scenario': scenario,
                'parcels': parcels,
                'links': links,
                'kpis': scenario.get('kpis', {})
            }
            
        finally:
            cursor.close()
            conn.close()

    def _update_optimization_params(self, params: Dict[str, Any]):
        """Update optimization parameters"""
        if 'parameter_ranges' in params:
            self.parameter_ranges.update(params['parameter_ranges'])
        if 'objectives' in params:
            self.objectives.update(params['objectives'])
        if 'constraints' in params:
            self.constraints.update(params['constraints'])

    def _generate_pareto_solutions(self, baseline_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Pareto optimal solutions using multi-objective optimization"""
        solutions = []
        
        # Generate baseline solution
        baseline_solution = self._evaluate_solution(baseline_data, baseline_data)
        baseline_solution['name'] = 'Baseline'
        baseline_solution['parameters'] = self._extract_baseline_parameters(baseline_data)
        solutions.append(baseline_solution)

        # Generate random parameter combinations
        num_solutions = 20
        for i in range(num_solutions):
            # Generate random parameters within ranges
            params = {}
            for param, range_info in self.parameter_ranges.items():
                params[param] = random.uniform(range_info['min'], range_info['max'])
            
            # Evaluate solution
            solution = self._evaluate_solution(baseline_data, baseline_data, params)
            solution['name'] = f'Solution {i+1}'
            solution['parameters'] = params
            solutions.append(solution)

        # Filter to Pareto optimal solutions
        pareto_solutions = self._filter_pareto_optimal(solutions)
        
        return pareto_solutions

    def _evaluate_solution(self, baseline_data: Dict[str, Any], scenario_data: Dict[str, Any], 
                          parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate a solution and calculate objectives"""
        
        # Use baseline data if no parameters provided
        if not parameters:
            parameters = self._extract_baseline_parameters(baseline_data)

        # Calculate modified scenario based on parameters
        modified_scenario = self._apply_parameters_to_scenario(scenario_data, parameters)
        
        # Calculate objectives
        sustainability_score = self._calculate_sustainability_score(modified_scenario)
        cost_efficiency = self._calculate_cost_efficiency(modified_scenario)
        density = self._calculate_density(modified_scenario)
        accessibility = self._calculate_accessibility(modified_scenario)
        
        # Calculate total score
        total_score = (
            sustainability_score * self.objectives['sustainability_score']['weight'] +
            cost_efficiency * self.objectives['cost_efficiency']['weight'] +
            density * self.objectives['density']['weight'] +
            accessibility * self.objectives['accessibility']['weight']
        )

        return {
            'sustainability_score': sustainability_score,
            'cost_efficiency': cost_efficiency,
            'density': density,
            'accessibility': accessibility,
            'total_score': total_score,
            'budget': self._calculate_budget(modified_scenario),
            'units': self._calculate_units(modified_scenario),
            'area': self._calculate_area(modified_scenario)
        }

    def _extract_baseline_parameters(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract baseline parameters from scenario data"""
        scenario = scenario_data['scenario']
        parcels = scenario_data['parcels']
        
        # Calculate averages from existing data
        avg_far = scenario.get('avg_far', 2.0)
        avg_height = scenario.get('avg_height', 15)
        avg_lot_coverage = scenario.get('avg_lot_coverage', 0.5)
        
        return {
            'far': avg_far,
            'height': avg_height,
            'lot_coverage': avg_lot_coverage,
            'parking_ratio': 1.0,
            'green_space_ratio': 0.15,
            'mixed_use_ratio': 0.3,
            'solar_coverage': 0.3,
            'bike_infrastructure': 0.3,
            'transit_priority': 0.5,
            'inclusionary_housing': 0.1
        }

    def _apply_parameters_to_scenario(self, scenario_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization parameters to scenario data"""
        # Create a copy of scenario data
        modified_scenario = {
            'scenario': scenario_data['scenario'].copy(),
            'parcels': [parcel.copy() for parcel in scenario_data['parcels']],
            'links': scenario_data['links'].copy(),
            'kpis': scenario_data['kpis'].copy()
        }
        
        # Apply parameters to parcels
        for parcel in modified_scenario['parcels']:
            properties = parcel['properties'].copy()
            
            # Update properties based on parameters
            if 'far' in parameters:
                properties['far'] = parameters['far']
            if 'height' in parameters:
                properties['height'] = parameters['height']
            if 'lot_coverage' in parameters:
                properties['lot_coverage'] = parameters['lot_coverage']
            if 'parking_ratio' in parameters:
                properties['parking_ratio'] = parameters['parking_ratio']
            if 'inclusionary_housing' in parameters:
                properties['inclusionary'] = parameters['inclusionary_housing'] * 100
            
            parcel['properties'] = properties
            
            # Recalculate capacity based on new parameters
            parcel['capacity'] = self._recalculate_capacity(parcel, parameters)
        
        return modified_scenario

    def _recalculate_capacity(self, parcel: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Recalculate parcel capacity based on new parameters"""
        properties = parcel['properties']
        area = parcel.get('area', 1000)  # Default area if not available
        
        # Calculate floor area
        far = parameters.get('far', properties.get('far', 2.0))
        floor_area = area * far
        
        # Calculate units (simplified)
        avg_unit_size = 80  # m² per unit
        units = max(1, int(floor_area / avg_unit_size))
        
        # Calculate population
        avg_household_size = 2.5
        population = units * avg_household_size
        
        # Calculate jobs (simplified)
        jobs = units * 0.8  # Assume 0.8 jobs per unit
        
        return {
            'units': units,
            'population': population,
            'jobs': jobs,
            'floor_area': floor_area,
            'parking_spaces': units * parameters.get('parking_ratio', 1.0)
        }

    def _calculate_sustainability_score(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate sustainability score (0-100)"""
        # Simplified calculation - would integrate with actual sustainability score worker
        parcels = scenario_data['parcels']
        
        # Calculate average metrics
        avg_far = np.mean([p['properties'].get('far', 2.0) for p in parcels])
        avg_height = np.mean([p['properties'].get('height', 15) for p in parcels])
        green_space = np.mean([p['properties'].get('green_space_ratio', 0.15) for p in parcels])
        
        # Simple scoring algorithm
        score = 0
        score += min(100, avg_far * 20)  # Higher FAR = better
        score += min(100, avg_height * 2)  # Higher height = better (to a point)
        score += green_space * 200  # More green space = better
        
        return min(100, score / 3)

    def _calculate_cost_efficiency(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate cost efficiency (0-100)"""
        # Simplified calculation
        total_budget = self._calculate_budget(scenario_data)
        total_units = self._calculate_units(scenario_data)
        
        if total_units == 0:
            return 0
        
        cost_per_unit = total_budget / total_units
        
        # Score based on cost per unit (lower is better)
        if cost_per_unit < 200000:  # $200K per unit
            return 100
        elif cost_per_unit < 300000:
            return 80
        elif cost_per_unit < 400000:
            return 60
        elif cost_per_unit < 500000:
            return 40
        else:
            return 20

    def _calculate_density(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate density score (0-100)"""
        total_population = sum(p.get('capacity', {}).get('population', 0) for p in scenario_data['parcels'])
        total_area = scenario_data['scenario'].get('total_area', 100000)  # m²
        
        if total_area == 0:
            return 0
        
        density = total_population / (total_area / 10000)  # people per hectare
        
        # Score based on density
        if density >= 150:
            return 100
        elif density >= 100:
            return 80
        elif density >= 50:
            return 60
        elif density >= 25:
            return 40
        else:
            return 20

    def _calculate_accessibility(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate accessibility score (0-100)"""
        # Simplified calculation based on network data
        links = scenario_data['links']
        
        if not links:
            return 50  # Default score
        
        # Calculate intersection density
        intersection_count = len([l for l in links if l['link_class'] in ['arterial', 'collector']])
        total_length = sum(l['properties'].get('length', 0) for l in links)
        
        if total_length == 0:
            return 50
        
        intersection_density = intersection_count / (total_length / 1000)  # per km
        
        # Score based on intersection density
        if intersection_density >= 8:
            return 100
        elif intersection_density >= 6:
            return 80
        elif intersection_density >= 4:
            return 60
        elif intersection_density >= 2:
            return 40
        else:
            return 20

    def _calculate_budget(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate total budget"""
        # Simplified budget calculation
        total_area = sum(p.get('capacity', {}).get('floor_area', 0) for p in scenario_data['parcels'])
        
        # Assume $3000 per m² construction cost
        construction_cost = total_area * 3000
        
        # Add infrastructure costs (simplified)
        infrastructure_cost = construction_cost * 0.3
        
        # Add soft costs
        soft_costs = (construction_cost + infrastructure_cost) * 0.2
        
        return construction_cost + infrastructure_cost + soft_costs

    def _calculate_units(self, scenario_data: Dict[str, Any]) -> int:
        """Calculate total units"""
        return sum(p.get('capacity', {}).get('units', 0) for p in scenario_data['parcels'])

    def _calculate_area(self, scenario_data: Dict[str, Any]) -> float:
        """Calculate total area"""
        return scenario_data['scenario'].get('total_area', 0)

    def _filter_pareto_optimal(self, solutions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter solutions to Pareto optimal set"""
        pareto_solutions = []
        
        for solution in solutions:
            is_pareto_optimal = True
            
            for other_solution in solutions:
                if solution == other_solution:
                    continue
                
                # Check if other solution dominates this one
                if (other_solution['sustainability_score'] >= solution['sustainability_score'] and
                    other_solution['cost_efficiency'] >= solution['cost_efficiency'] and
                    other_solution['density'] >= solution['density'] and
                    other_solution['accessibility'] >= solution['accessibility'] and
                    (other_solution['sustainability_score'] > solution['sustainability_score'] or
                     other_solution['cost_efficiency'] > solution['cost_efficiency'] or
                     other_solution['density'] > solution['density'] or
                     other_solution['accessibility'] > solution['accessibility'])):
                    is_pareto_optimal = False
                    break
            
            if is_pareto_optimal:
                pareto_solutions.append(solution)
        
        return pareto_solutions

    def _calculate_trade_offs(self, pareto_solutions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trade-offs between objectives"""
        if len(pareto_solutions) < 2:
            return {}
        
        # Calculate correlations between objectives
        objectives = ['sustainability_score', 'cost_efficiency', 'density', 'accessibility']
        correlations = {}
        
        for obj1, obj2 in combinations(objectives, 2):
            values1 = [s[obj1] for s in pareto_solutions]
            values2 = [s[obj2] for s in pareto_solutions]
            correlation = np.corrcoef(values1, values2)[0, 1]
            correlations[f'{obj1}_vs_{obj2}'] = correlation
        
        # Calculate trade-off ratios
        trade_off_ratios = {}
        for obj1, obj2 in combinations(objectives, 2):
            values1 = [s[obj1] for s in pareto_solutions]
            values2 = [s[obj2] for s in pareto_solutions]
            
            # Calculate average trade-off ratio
            ratios = []
            for i in range(len(pareto_solutions)):
                for j in range(i + 1, len(pareto_solutions)):
                    if values2[j] != values2[i]:
                        ratio = (values1[j] - values1[i]) / (values2[j] - values2[i])
                        ratios.append(ratio)
            
            if ratios:
                trade_off_ratios[f'{obj1}_vs_{obj2}'] = np.mean(ratios)
        
        return {
            'correlations': correlations,
            'trade_off_ratios': trade_off_ratios,
            'solution_count': len(pareto_solutions)
        }

    def _generate_tornado_chart(self, baseline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tornado chart data for sensitivity analysis"""
        baseline_solution = self._evaluate_solution(baseline_data, baseline_data)
        tornado_data = {}
        
        for param, range_info in self.parameter_ranges.items():
            # Test high and low values
            high_params = {param: range_info['max']}
            low_params = {param: range_info['min']}
            
            high_solution = self._evaluate_solution(baseline_data, baseline_data, high_params)
            low_solution = self._evaluate_solution(baseline_data, baseline_data, low_params)
            
            # Calculate impact on total score
            high_impact = high_solution['total_score'] - baseline_solution['total_score']
            low_impact = low_solution['total_score'] - baseline_solution['total_score']
            
            tornado_data[param] = {
                'high_impact': high_impact,
                'low_impact': low_impact,
                'max_impact': max(abs(high_impact), abs(low_impact)),
                'direction': 'positive' if high_impact > low_impact else 'negative'
            }
        
        # Sort by impact magnitude
        sorted_params = sorted(tornado_data.items(), 
                             key=lambda x: x[1]['max_impact'], 
                             reverse=True)
        
        return {
            'parameters': dict(sorted_params),
            'baseline_score': baseline_solution['total_score']
        }

    def _store_optimization_results(self, scenario_id: str, results: Dict[str, Any]):
        """Store optimization results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with optimization results
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{optimization_results}',
                %s::jsonb
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            cursor.execute(query, (json.dumps(results), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_optimization_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get optimization results summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'optimization_results' as optimization_results
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['optimization_results']:
                    return {
                        'success': True,
                        'data': result['optimization_results']
                    }
                else:
                    return {'success': False, 'error': 'No optimization results found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting optimization summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
