# Created automatically by Cursor AI (2025-01-27)
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from workers.mobility_model import MobilityModel

class TestMobilityModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.mobility_model = MobilityModel()
        
        # Mock scenario data
        self.mock_scenario_data = {
            'id': 'test-scenario-1',
            'name': 'Test Scenario',
            'properties': {
                'area': 1000000,  # 1 km²
                'population_target': 5000
            },
            'kpis': {}
        }
        
        # Mock parcels data
        self.mock_parcels = [
            {
                'id': 'parcel-1',
                'centroid_wkt': 'POINT(0 0)',
                'area': 10000,
                'properties': {'land_use': 'residential'},
                'capacity': {'population': 100, 'jobs': 0}
            },
            {
                'id': 'parcel-2',
                'centroid_wkt': 'POINT(100 100)',
                'area': 15000,
                'properties': {'land_use': 'commercial'},
                'capacity': {'population': 0, 'jobs': 50}
            }
        ]
        
        # Mock network data
        self.mock_network_data = [
            {
                'id': 'link-1',
                'geom_wkt': 'LINESTRING(0 0, 100 0)',
                'properties': {
                    'length': 100,
                    'bike_lanes': 1,
                    'lanes': 2,
                    'speedLimit': 30
                },
                'link_class': 'arterial'
            },
            {
                'id': 'link-2',
                'geom_wkt': 'LINESTRING(0 0, 0 100)',
                'properties': {
                    'length': 100,
                    'bike_lanes': 0,
                    'lanes': 1,
                    'speedLimit': 20
                },
                'link_class': 'local'
            }
        ]
        
        # Mock amenities data
        self.mock_amenities = [
            {
                'id': 'amenity-1',
                'centroid_wkt': 'POINT(50 50)',
                'amenity_type': 'retail',
                'properties': {'name': 'Shopping Center'}
            },
            {
                'id': 'amenity-2',
                'centroid_wkt': 'POINT(200 200)',
                'amenity_type': 'park',
                'properties': {'name': 'Community Park'}
            }
        ]

    @patch('workers.mobility_model.psycopg2.connect')
    def test_analyze_mobility_success(self, mock_connect):
        """Test successful mobility analysis"""
        # Mock database connections
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock scenario data query
        mock_cursor.fetchone.side_effect = [
            self.mock_scenario_data,  # scenario data
            None  # store results
        ]
        
        # Mock network data query
        mock_cursor.fetchall.side_effect = [
            self.mock_network_data,  # network data
            self.mock_parcels,  # parcels data
            self.mock_amenities  # amenities data
        ]
        
        result = self.mobility_model.analyze_mobility('test-scenario-1')
        
        self.assertTrue(result['success'])
        self.assertIn('trip_generation', result['data'])
        self.assertIn('mode_choice', result['data'])
        self.assertIn('vmt_analysis', result['data'])
        self.assertIn('fifteen_minute_access', result['data'])
        self.assertIn('walk_bike_los', result['data'])
        self.assertIn('accessibility_metrics', result['data'])

    @patch('workers.mobility_model.psycopg2.connect')
    def test_analyze_mobility_no_scenario(self, mock_connect):
        """Test mobility analysis with non-existent scenario"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # No scenario found
        
        result = self.mobility_model.analyze_mobility('non-existent-scenario')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Scenario not found')

    @patch('workers.mobility_model.psycopg2.connect')
    def test_analyze_mobility_no_network(self, mock_connect):
        """Test mobility analysis with no network data"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock scenario data but no network data
        mock_cursor.fetchone.return_value = self.mock_scenario_data
        mock_cursor.fetchall.side_effect = [
            [],  # No network data
            self.mock_parcels,
            self.mock_amenities
        ]
        
        result = self.mobility_model.analyze_mobility('test-scenario-1')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'No network data found')

    def test_calculate_trip_generation(self):
        """Test trip generation calculation"""
        trip_generation = self.mobility_model._calculate_trip_generation(
            self.mock_scenario_data, 
            self.mock_parcels
        )
        
        self.assertEqual(trip_generation['total_population'], 100)
        self.assertEqual(trip_generation['total_jobs'], 50)
        self.assertIn('total_daily_trips', trip_generation)
        self.assertIn('trips_by_purpose', trip_generation)
        
        # Check that trips are calculated correctly
        expected_trips = 100 * self.mobility_model.defaults['daily_trips_per_person']
        self.assertAlmostEqual(trip_generation['total_daily_trips'], expected_trips, places=1)

    def test_calculate_mode_choice(self):
        """Test mode choice calculation"""
        mode_choice = self.mobility_model._calculate_mode_choice(
            self.mock_scenario_data,
            self.mock_network_data,
            self.mock_parcels,
            self.mock_amenities
        )
        
        self.assertIn('mode_share', mode_choice)
        self.assertIn('network_characteristics', mode_choice)
        self.assertIn('mode_factors', mode_choice)
        
        # Check that mode shares sum to approximately 1
        mode_shares = mode_choice['mode_share']
        total_share = sum(mode_shares.values())
        self.assertAlmostEqual(total_share, 1.0, places=2)
        
        # Check that all mode shares are between 0 and 1
        for mode, share in mode_shares.items():
            self.assertGreaterEqual(share, 0)
            self.assertLessEqual(share, 1)

    def test_calculate_vmt(self):
        """Test VMT calculation"""
        trip_generation = self.mobility_model._calculate_trip_generation(
            self.mock_scenario_data, 
            self.mock_parcels
        )
        
        mode_choice = self.mobility_model._calculate_mode_choice(
            self.mock_scenario_data,
            self.mock_network_data,
            self.mock_parcels,
            self.mock_amenities
        )
        
        vmt_analysis = self.mobility_model._calculate_vmt(
            trip_generation,
            mode_choice,
            self.mock_network_data
        )
        
        self.assertIn('daily_vmt', vmt_analysis)
        self.assertIn('annual_vmt', vmt_analysis)
        self.assertIn('per_capita_vmt', vmt_analysis)
        self.assertIn('vmt_reduction_potential', vmt_analysis)
        
        # Check that VMT values are reasonable
        self.assertGreaterEqual(vmt_analysis['daily_vmt'], 0)
        self.assertGreaterEqual(vmt_analysis['annual_vmt'], 0)
        self.assertGreaterEqual(vmt_analysis['per_capita_vmt'], 0)

    def test_calculate_fifteen_minute_access(self):
        """Test 15-minute access calculation"""
        fifteen_minute_access = self.mobility_model._calculate_fifteen_minute_access(
            self.mock_parcels,
            self.mock_amenities,
            self.mock_network_data
        )
        
        self.assertIn('access_percentages', fifteen_minute_access)
        self.assertIn('accessibility_score', fifteen_minute_access)
        self.assertIn('amenity_types_analyzed', fifteen_minute_access)
        
        # Check that accessibility score is between 0 and 100
        self.assertGreaterEqual(fifteen_minute_access['accessibility_score'], 0)
        self.assertLessEqual(fifteen_minute_access['accessibility_score'], 100)

    def test_calculate_walk_bike_los(self):
        """Test walk/bike Level of Service calculation"""
        walk_bike_los = self.mobility_model._calculate_walk_bike_los(
            self.mock_parcels,
            self.mock_amenities,
            self.mock_network_data
        )
        
        self.assertIn('walk_los', walk_bike_los)
        self.assertIn('bike_los', walk_bike_los)
        self.assertIn('scores', walk_bike_los)
        self.assertIn('factors', walk_bike_los)
        
        # Check that LOS grades are valid
        valid_grades = ['A', 'B', 'C', 'D', 'F']
        self.assertIn(walk_bike_los['walk_los'], valid_grades)
        self.assertIn(walk_bike_los['bike_los'], valid_grades)

    def test_score_to_los(self):
        """Test score to Level of Service conversion"""
        # Test various scores
        self.assertEqual(self.mobility_model._score_to_los(90), 'A')
        self.assertEqual(self.mobility_model._score_to_los(70), 'B')
        self.assertEqual(self.mobility_model._score_to_los(50), 'C')
        self.assertEqual(self.mobility_model._score_to_los(30), 'D')
        self.assertEqual(self.mobility_model._score_to_los(10), 'F')

    def test_calculate_walk_factor(self):
        """Test walk factor calculation"""
        walk_factor = self.mobility_model._calculate_walk_factor(
            self.mock_parcels,
            self.mock_amenities
        )
        
        self.assertGreaterEqual(walk_factor, 0)
        self.assertLessEqual(walk_factor, 1)

    def test_calculate_bike_factor(self):
        """Test bike factor calculation"""
        bike_factor = self.mobility_model._calculate_bike_factor(1.0, 2)
        
        self.assertGreaterEqual(bike_factor, 0.05)  # Minimum 5%

    def test_calculate_transit_factor(self):
        """Test transit factor calculation"""
        transit_factor = self.mobility_model._calculate_transit_factor(2, 10)
        
        self.assertGreaterEqual(transit_factor, 0.05)  # Minimum 5%

    def test_calculate_car_factor(self):
        """Test car factor calculation"""
        car_factor = self.mobility_model._calculate_car_factor(100, 100)
        
        self.assertGreaterEqual(car_factor, 0.2)  # Minimum 20%

    def test_empty_data_handling(self):
        """Test handling of empty data"""
        # Test with empty parcels
        trip_generation = self.mobility_model._calculate_trip_generation(
            self.mock_scenario_data, 
            []
        )
        
        self.assertEqual(trip_generation['total_population'], 0)
        self.assertEqual(trip_generation['total_jobs'], 0)
        self.assertEqual(trip_generation['total_daily_trips'], 0)
        
        # Test with empty amenities
        fifteen_minute_access = self.mobility_model._calculate_fifteen_minute_access(
            self.mock_parcels,
            [],
            self.mock_network_data
        )
        
        self.assertEqual(fifteen_minute_access['accessibility_score'], 0)
        self.assertEqual(fifteen_minute_access['access_percentages'], {})

    def test_vmt_reduction_potential(self):
        """Test VMT reduction potential calculation"""
        mode_choice = {
            'mode_share': {
                'walk': 0.1,
                'bike': 0.05,
                'transit': 0.15,
                'car': 0.7
            }
        }
        
        vmt_reduction = self.mobility_model._calculate_vmt_reduction_potential(mode_choice)
        
        self.assertIn('current_car_share', vmt_reduction)
        self.assertIn('potential_car_share', vmt_reduction)
        self.assertIn('vmt_reduction_percent', vmt_reduction)
        self.assertIn('potential_mode_shifts', vmt_reduction)
        
        # Check that potential car share is less than current
        self.assertLessEqual(vmt_reduction['potential_car_share'], vmt_reduction['current_car_share'])

    @patch('workers.mobility_model.psycopg2.connect')
    def test_get_mobility_summary(self, mock_connect):
        """Test getting mobility summary"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock existing mobility analysis data
        mock_analysis_data = {
            'trip_generation': {'total_population': 100},
            'mode_choice': {'mode_share': {'walk': 0.3}},
            'vmt_analysis': {'daily_vmt': 1000}
        }
        
        mock_cursor.fetchone.return_value = {
            'mobility_analysis': mock_analysis_data
        }
        
        result = self.mobility_model.get_mobility_summary('test-scenario-1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data'], mock_analysis_data)

    @patch('workers.mobility_model.psycopg2.connect')
    def test_get_mobility_summary_no_data(self, mock_connect):
        """Test getting mobility summary when no data exists"""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'mobility_analysis': None}
        
        result = self.mobility_model.get_mobility_summary('test-scenario-1')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'No mobility analysis data found')

if __name__ == '__main__':
    unittest.main()
