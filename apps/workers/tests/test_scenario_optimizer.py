# Created automatically by Cursor AI (2025-01-27)
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimizer.scenario_optimizer import ScenarioOptimizer

class TestScenarioOptimizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = ScenarioOptimizer()
        
        # Mock scenario data
        self.mock_scenario_data = {
            'scenario': {
                'id': 'test-scenario-1',
                'name': 'Test Scenario',
                'total_area': 100000,  # 10 hectares
                'avg_far': 2.0,
                'avg_height': 15,
                'avg_lot_coverage': 0.5,
                'kpis': {}
            },
            'parcels': [
                {
                    'properties': {
                        'far': 2.0,
                        'height': 15,
                        'lot_coverage': 0.5,
                        'parking_ratio': 1.0,
                        'green_space_ratio': 0.15,
                        'inclusionary': 10
                    },
                    'capacity': {
                        'units': 50,
                        'population': 125,
                        'jobs': 40,
                        'floor_area': 50000
                    },
                    'area': 25000
                },
                {
                    'properties': {
                        'far': 3.0,
                        'height': 20,
                        'lot_coverage': 0.6,
                        'parking_ratio': 1.2,
                        'green_space_ratio': 0.1,
                        'inclusionary': 15
                    },
                    'capacity': {
                        'units': 75,
                        'population': 188,
                        'jobs': 60,
                        'floor_area': 75000
                    },
                    'area': 25000
                }
            ],
            'links': [
                {
                    'properties': {
                        'length': 200,
                        'lanes': 2,
                        'speedLimit': 30
                    },
                    'link_class': 'arterial'
                },
                {
                    'properties': {
                        'length': 150,
                        'lanes': 1,
                        'speedLimit': 20
                    },
                    'link_class': 'collector'
                },
                {
                    'properties': {
                        'length': 100,
                        'lanes': 1,
                        'speedLimit': 15
                    },
                    'link_class': 'local'
                }
            ],
            'kpis': {
                'sustainability_score': 75,
                'budget': 50000000,
                'units': 125
            }
        }

    @patch('optimizer.scenario_optimizer.psycopg2.connect')
    def test_optimize_scenario_success(self, mock_connect):
        """Test successful scenario optimization"""
        # Mock database connections
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock scenario data query
        mock_cursor.fetchone.return_value = self.mock_scenario_data['scenario']
        mock_cursor.fetchall.side_effect = [
            self.mock_scenario_data['parcels'],  # parcels data
            self.mock_scenario_data['links']  # links data
        ]
        
        result = self.optimizer.optimize_scenario('test-scenario-1')
        
        self.assertTrue(result['success'])
        self.assertIn('pareto_solutions', result['data'])
        self.assertIn('trade_offs', result['data'])
        self.assertIn('tornado_chart', result['data'])
        self.assertIn('baseline', result['data'])
        self.assertIn('optimization_params', result['data'])

    @patch('optimizer.scenario_optimizer.psycopg2.connect')
    def test_optimize_scenario_no_data(self, mock_connect):
        """Test optimization with no scenario data"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # No scenario found
        
        result = self.optimizer.optimize_scenario('non-existent-scenario')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'No scenario data found')

    def test_generate_pareto_solutions(self):
        """Test Pareto solution generation"""
        pareto_solutions = self.optimizer._generate_pareto_solutions(self.mock_scenario_data)
        
        self.assertIsInstance(pareto_solutions, list)
        self.assertGreater(len(pareto_solutions), 0)
        
        # Check that each solution has required fields
        for solution in pareto_solutions:
            self.assertIn('sustainability_score', solution)
            self.assertIn('cost_efficiency', solution)
            self.assertIn('density', solution)
            self.assertIn('accessibility', solution)
            self.assertIn('total_score', solution)
            self.assertIn('budget', solution)
            self.assertIn('units', solution)
            self.assertIn('area', solution)
            self.assertIn('name', solution)
            self.assertIn('parameters', solution)

    def test_evaluate_solution(self):
        """Test solution evaluation"""
        solution = self.optimizer._evaluate_solution(
            self.mock_scenario_data,
            self.mock_scenario_data
        )
        
        self.assertIn('sustainability_score', solution)
        self.assertIn('cost_efficiency', solution)
        self.assertIn('density', solution)
        self.assertIn('accessibility', solution)
        self.assertIn('total_score', solution)
        self.assertIn('budget', solution)
        self.assertIn('units', solution)
        self.assertIn('area', solution)
        
        # Check that scores are within valid ranges
        self.assertGreaterEqual(solution['sustainability_score'], 0)
        self.assertLessEqual(solution['sustainability_score'], 100)
        self.assertGreaterEqual(solution['cost_efficiency'], 0)
        self.assertLessEqual(solution['cost_efficiency'], 100)
        self.assertGreaterEqual(solution['density'], 0)
        self.assertLessEqual(solution['density'], 100)
        self.assertGreaterEqual(solution['accessibility'], 0)
        self.assertLessEqual(solution['accessibility'], 100)

    def test_extract_baseline_parameters(self):
        """Test baseline parameter extraction"""
        params = self.optimizer._extract_baseline_parameters(self.mock_scenario_data)
        
        self.assertIn('far', params)
        self.assertIn('height', params)
        self.assertIn('lot_coverage', params)
        self.assertIn('parking_ratio', params)
        self.assertIn('green_space_ratio', params)
        self.assertIn('mixed_use_ratio', params)
        self.assertIn('solar_coverage', params)
        self.assertIn('bike_infrastructure', params)
        self.assertIn('transit_priority', params)
        self.assertIn('inclusionary_housing', params)
        
        # Check that parameters are within expected ranges
        self.assertGreaterEqual(params['far'], 0)
        self.assertGreaterEqual(params['height'], 0)
        self.assertGreaterEqual(params['lot_coverage'], 0)
        self.assertLessEqual(params['lot_coverage'], 1)

    def test_apply_parameters_to_scenario(self):
        """Test parameter application to scenario"""
        test_params = {
            'far': 3.0,
            'height': 25,
            'lot_coverage': 0.7,
            'parking_ratio': 1.5,
            'inclusionary_housing': 0.2
        }
        
        modified_scenario = self.optimizer._apply_parameters_to_scenario(
            self.mock_scenario_data,
            test_params
        )
        
        # Check that parameters were applied to parcels
        for parcel in modified_scenario['parcels']:
            properties = parcel['properties']
            self.assertEqual(properties['far'], 3.0)
            self.assertEqual(properties['height'], 25)
            self.assertEqual(properties['lot_coverage'], 0.7)
            self.assertEqual(properties['parking_ratio'], 1.5)
            self.assertEqual(properties['inclusionary'], 20)  # 0.2 * 100

    def test_recalculate_capacity(self):
        """Test capacity recalculation"""
        parcel = {
            'properties': {'far': 2.0},
            'area': 10000
        }
        
        params = {
            'far': 3.0,
            'parking_ratio': 1.2
        }
        
        capacity = self.optimizer._recalculate_capacity(parcel, params)
        
        self.assertIn('units', capacity)
        self.assertIn('population', capacity)
        self.assertIn('jobs', capacity)
        self.assertIn('floor_area', capacity)
        self.assertIn('parking_spaces', capacity)
        
        # Check calculations
        expected_floor_area = 10000 * 3.0
        self.assertEqual(capacity['floor_area'], expected_floor_area)
        self.assertGreater(capacity['units'], 0)
        self.assertGreater(capacity['population'], 0)

    def test_calculate_sustainability_score(self):
        """Test sustainability score calculation"""
        score = self.optimizer._calculate_sustainability_score(self.mock_scenario_data)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIsInstance(score, float)

    def test_calculate_cost_efficiency(self):
        """Test cost efficiency calculation"""
        efficiency = self.optimizer._calculate_cost_efficiency(self.mock_scenario_data)
        
        self.assertGreaterEqual(efficiency, 0)
        self.assertLessEqual(efficiency, 100)
        self.assertIsInstance(efficiency, float)

    def test_calculate_density(self):
        """Test density calculation"""
        density = self.optimizer._calculate_density(self.mock_scenario_data)
        
        self.assertGreaterEqual(density, 0)
        self.assertLessEqual(density, 100)
        self.assertIsInstance(density, float)

    def test_calculate_accessibility(self):
        """Test accessibility calculation"""
        accessibility = self.optimizer._calculate_accessibility(self.mock_scenario_data)
        
        self.assertGreaterEqual(accessibility, 0)
        self.assertLessEqual(accessibility, 100)
        self.assertIsInstance(accessibility, float)

    def test_calculate_budget(self):
        """Test budget calculation"""
        budget = self.optimizer._calculate_budget(self.mock_scenario_data)
        
        self.assertGreaterEqual(budget, 0)
        self.assertIsInstance(budget, float)

    def test_calculate_units(self):
        """Test units calculation"""
        units = self.optimizer._calculate_units(self.mock_scenario_data)
        
        self.assertGreaterEqual(units, 0)
        self.assertIsInstance(units, int)

    def test_calculate_area(self):
        """Test area calculation"""
        area = self.optimizer._calculate_area(self.mock_scenario_data)
        
        self.assertGreaterEqual(area, 0)
        self.assertIsInstance(area, float)

    def test_filter_pareto_optimal(self):
        """Test Pareto optimal filtering"""
        solutions = [
            {
                'sustainability_score': 80,
                'cost_efficiency': 70,
                'density': 60,
                'accessibility': 50
            },
            {
                'sustainability_score': 90,
                'cost_efficiency': 80,
                'density': 70,
                'accessibility': 60
            },
            {
                'sustainability_score': 70,
                'cost_efficiency': 60,
                'density': 50,
                'accessibility': 40
            }
        ]
        
        pareto_solutions = self.optimizer._filter_pareto_optimal(solutions)
        
        self.assertIsInstance(pareto_solutions, list)
        self.assertLessEqual(len(pareto_solutions), len(solutions))

    def test_calculate_trade_offs(self):
        """Test trade-off calculation"""
        pareto_solutions = [
            {
                'sustainability_score': 80,
                'cost_efficiency': 70,
                'density': 60,
                'accessibility': 50
            },
            {
                'sustainability_score': 90,
                'cost_efficiency': 80,
                'density': 70,
                'accessibility': 60
            }
        ]
        
        trade_offs = self.optimizer._calculate_trade_offs(pareto_solutions)
        
        self.assertIn('correlations', trade_offs)
        self.assertIn('trade_off_ratios', trade_offs)
        self.assertIn('solution_count', trade_offs)
        self.assertEqual(trade_offs['solution_count'], 2)

    def test_generate_tornado_chart(self):
        """Test tornado chart generation"""
        tornado_data = self.optimizer._generate_tornado_chart(self.mock_scenario_data)
        
        self.assertIn('parameters', tornado_data)
        self.assertIn('baseline_score', tornado_data)
        self.assertIsInstance(tornado_data['parameters'], dict)
        self.assertIsInstance(tornado_data['baseline_score'], float)

    def test_update_optimization_params(self):
        """Test optimization parameter updates"""
        original_ranges = self.optimizer.parameter_ranges.copy()
        original_objectives = self.optimizer.objectives.copy()
        original_constraints = self.optimizer.constraints.copy()
        
        new_params = {
            'parameter_ranges': {
                'far': {'min': 1.0, 'max': 10.0, 'default': 5.0}
            },
            'objectives': {
                'sustainability_score': {'weight': 0.5, 'direction': 'maximize'}
            },
            'constraints': {
                'min_units': 200
            }
        }
        
        self.optimizer._update_optimization_params(new_params)
        
        # Check that parameters were updated
        self.assertEqual(self.optimizer.parameter_ranges['far']['min'], 1.0)
        self.assertEqual(self.optimizer.objectives['sustainability_score']['weight'], 0.5)
        self.assertEqual(self.optimizer.constraints['min_units'], 200)

    @patch('optimizer.scenario_optimizer.psycopg2.connect')
    def test_get_optimization_summary(self, mock_connect):
        """Test getting optimization summary"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock existing optimization data
        mock_optimization_data = {
            'pareto_solutions': [{'name': 'Solution 1'}],
            'trade_offs': {'correlations': {}},
            'tornado_chart': {'parameters': {}}
        }
        
        mock_cursor.fetchone.return_value = {
            'optimization_results': mock_optimization_data
        }
        
        result = self.optimizer.get_optimization_summary('test-scenario-1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data'], mock_optimization_data)

    @patch('optimizer.scenario_optimizer.psycopg2.connect')
    def test_get_optimization_summary_no_data(self, mock_connect):
        """Test getting optimization summary when no data exists"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'optimization_results': None}
        
        result = self.optimizer.get_optimization_summary('test-scenario-1')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'No optimization results found')

    def test_parameter_ranges_validation(self):
        """Test that parameter ranges are valid"""
        for param, range_info in self.optimizer.parameter_ranges.items():
            self.assertIn('min', range_info)
            self.assertIn('max', range_info)
            self.assertIn('default', range_info)
            self.assertLess(range_info['min'], range_info['max'])
            self.assertGreaterEqual(range_info['default'], range_info['min'])
            self.assertLessEqual(range_info['default'], range_info['max'])

    def test_objectives_validation(self):
        """Test that objectives are valid"""
        total_weight = sum(obj['weight'] for obj in self.optimizer.objectives.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
        
        for obj_name, obj_info in self.optimizer.objectives.items():
            self.assertIn('weight', obj_info)
            self.assertIn('direction', obj_info)
            self.assertGreater(obj_info['weight'], 0)
            self.assertLessEqual(obj_info['weight'], 1)
            self.assertIn(obj_info['direction'], ['maximize', 'minimize'])

if __name__ == '__main__':
    unittest.main()
