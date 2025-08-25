# Created automatically by Cursor AI (2025-08-25)
import unittest
import json
from apps.workers.src.sustainability.sustainability_score import SustainabilityScore

class TestSustainabilityScore(unittest.TestCase):
    def setUp(self):
        self.scorer = SustainabilityScore()

    def test_energy_score_calculation(self):
        """Test energy sustainability score calculation"""
        energy_data = {
            'renewable_fraction': 0.8,  # 80% renewable
            'energy_efficiency': 0.85,  # 85% efficiency
            'emissions_reduction': 0.7   # 70% reduction
        }
        
        energy_score = self.scorer._calculate_energy_score(energy_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(energy_score['score'], 0)
        self.assertLessEqual(energy_score['score'], 100)
        self.assertIn('grade', energy_score)

    def test_mobility_score_calculation(self):
        """Test mobility sustainability score calculation"""
        mobility_data = {
            'walkability_score': 85,
            'transit_accessibility': 0.9,
            'bike_infrastructure': 0.8,
            'vmt_reduction': 0.6
        }
        
        mobility_score = self.scorer._calculate_mobility_score(mobility_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(mobility_score['score'], 0)
        self.assertLessEqual(mobility_score['score'], 100)
        self.assertIn('grade', mobility_score)

    def test_land_use_score_calculation(self):
        """Test land use sustainability score calculation"""
        land_use_data = {
            'density': 75,  # units per hectare
            'mixed_use_index': 0.8,
            'green_space_ratio': 0.25,
            'compactness': 0.7
        }
        
        land_use_score = self.scorer._calculate_land_use_score(land_use_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(land_use_score['score'], 0)
        self.assertLessEqual(land_use_score['score'], 100)
        self.assertIn('grade', land_use_score)

    def test_water_score_calculation(self):
        """Test water sustainability score calculation"""
        water_data = {
            'water_efficiency': 0.8,
            'stormwater_management': 0.9,
            'water_reuse': 0.6,
            'water_quality': 0.85
        }
        
        water_score = self.scorer._calculate_water_score(water_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(water_score['score'], 0)
        self.assertLessEqual(water_score['score'], 100)
        self.assertIn('grade', water_score)

    def test_materials_score_calculation(self):
        """Test materials sustainability score calculation"""
        materials_data = {
            'recycled_content': 0.7,
            'local_materials': 0.8,
            'embodied_carbon': 0.6,
            'durability': 0.9
        }
        
        materials_score = self.scorer._calculate_materials_score(materials_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(materials_score['score'], 0)
        self.assertLessEqual(materials_score['score'], 100)
        self.assertIn('grade', materials_score)

    def test_resilience_score_calculation(self):
        """Test resilience sustainability score calculation"""
        resilience_data = {
            'climate_adaptation': 0.8,
            'disaster_preparedness': 0.7,
            'social_cohesion': 0.9,
            'economic_diversity': 0.75
        }
        
        resilience_score = self.scorer._calculate_resilience_score(resilience_data)
        
        # Should return a score between 0 and 100
        self.assertGreaterEqual(resilience_score['score'], 0)
        self.assertLessEqual(resilience_score['score'], 100)
        self.assertIn('grade', resilience_score)

    def test_metric_scoring(self):
        """Test individual metric scoring"""
        # Test high value (should score well)
        high_score = self.scorer._score_metric(0.9, {'excellent': 0.8, 'good': 0.6, 'fair': 0.4})
        self.assertGreater(high_score, 80)
        
        # Test medium value (should score moderately)
        medium_score = self.scorer._score_metric(0.5, {'excellent': 0.8, 'good': 0.6, 'fair': 0.4})
        self.assertGreater(medium_score, 40)
        self.assertLess(medium_score, 80)
        
        # Test low value (should score poorly)
        low_score = self.scorer._score_metric(0.2, {'excellent': 0.8, 'good': 0.6, 'fair': 0.4})
        self.assertLess(low_score, 40)

    def test_reverse_metric_scoring(self):
        """Test reverse metric scoring (lower is better)"""
        # Test low value (should score well for reverse metrics)
        high_score = self.scorer._score_metric(0.2, {'excellent': 0.2, 'good': 0.4, 'fair': 0.6}, reverse=True)
        self.assertGreater(high_score, 80)
        
        # Test high value (should score poorly for reverse metrics)
        low_score = self.scorer._score_metric(0.8, {'excellent': 0.2, 'good': 0.4, 'fair': 0.6}, reverse=True)
        self.assertLess(low_score, 40)

    def test_grade_calculation(self):
        """Test letter grade calculation"""
        # Test A grade
        grade_a = self.scorer._calculate_grade(95)
        self.assertEqual(grade_a, 'A')
        
        # Test B grade
        grade_b = self.scorer._calculate_grade(85)
        self.assertEqual(grade_b, 'B')
        
        # Test C grade
        grade_c = self.scorer._calculate_grade(75)
        self.assertEqual(grade_c, 'C')
        
        # Test D grade
        grade_d = self.scorer._calculate_grade(65)
        self.assertEqual(grade_d, 'D')
        
        # Test F grade
        grade_f = self.scorer._calculate_grade(45)
        self.assertEqual(grade_f, 'F')

    def test_weighted_average_calculation(self):
        """Test weighted average calculation"""
        scores = {
            'energy': {'score': 85, 'weight': 0.25},
            'mobility': {'score': 90, 'weight': 0.20},
            'land_use': {'score': 75, 'weight': 0.20},
            'water': {'score': 80, 'weight': 0.15},
            'materials': {'score': 70, 'weight': 0.10},
            'resilience': {'score': 95, 'weight': 0.10}
        }
        
        weighted_average = self.scorer._calculate_weighted_average(scores)
        
        # Expected: 85*0.25 + 90*0.20 + 75*0.20 + 80*0.15 + 70*0.10 + 95*0.10 = 83.25
        expected_score = 85*0.25 + 90*0.20 + 75*0.20 + 80*0.15 + 70*0.10 + 95*0.10
        self.assertAlmostEqual(weighted_average, expected_score, places=2)

    def test_score_normalization(self):
        """Test score normalization to 0-100 range"""
        # Test normalization of values in different ranges
        raw_scores = [0.5, 0.8, 0.3, 0.9]
        normalized_scores = self.scorer._normalize_scores(raw_scores)
        
        # All normalized scores should be between 0 and 100
        for score in normalized_scores:
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)

    def test_comprehensive_sustainability_score(self):
        """Test comprehensive sustainability score calculation"""
        scenario_data = {
            'energy_metrics': {
                'renewable_fraction': 0.8,
                'energy_efficiency': 0.85,
                'emissions_reduction': 0.7
            },
            'mobility_metrics': {
                'walkability_score': 85,
                'transit_accessibility': 0.9,
                'bike_infrastructure': 0.8,
                'vmt_reduction': 0.6
            },
            'land_use_metrics': {
                'density': 75,
                'mixed_use_index': 0.8,
                'green_space_ratio': 0.25,
                'compactness': 0.7
            },
            'water_metrics': {
                'water_efficiency': 0.8,
                'stormwater_management': 0.9,
                'water_reuse': 0.6,
                'water_quality': 0.85
            },
            'materials_metrics': {
                'recycled_content': 0.7,
                'local_materials': 0.8,
                'embodied_carbon': 0.6,
                'durability': 0.9
            },
            'resilience_metrics': {
                'climate_adaptation': 0.8,
                'disaster_preparedness': 0.7,
                'social_cohesion': 0.9,
                'economic_diversity': 0.75
            }
        }
        
        sustainability_score = self.scorer.calculate_sustainability_score('test_scenario', scenario_data)
        
        # Should return comprehensive score data
        self.assertIn('overall_score', sustainability_score)
        self.assertIn('overall_grade', sustainability_score)
        self.assertIn('category_scores', sustainability_score)
        self.assertIn('weights', sustainability_score)
        
        # Overall score should be between 0 and 100
        self.assertGreaterEqual(sustainability_score['overall_score'], 0)
        self.assertLessEqual(sustainability_score['overall_score'], 100)

    def test_custom_weights(self):
        """Test sustainability score calculation with custom weights"""
        custom_weights = {
            'energy': 0.30,
            'mobility': 0.25,
            'land_use': 0.15,
            'water': 0.15,
            'materials': 0.10,
            'resilience': 0.05
        }
        
        scenario_data = {
            'energy_metrics': {'renewable_fraction': 0.8},
            'mobility_metrics': {'walkability_score': 85},
            'land_use_metrics': {'density': 75},
            'water_metrics': {'water_efficiency': 0.8},
            'materials_metrics': {'recycled_content': 0.7},
            'resilience_metrics': {'climate_adaptation': 0.8}
        }
        
        sustainability_score = self.scorer.calculate_sustainability_score('test_scenario', scenario_data, custom_weights)
        
        # Should use custom weights
        self.assertEqual(sustainability_score['weights'], custom_weights)

    def test_score_validation(self):
        """Test score validation and error handling"""
        # Test with invalid data
        invalid_data = {
            'energy_metrics': {'invalid_metric': 'invalid_value'}
        }
        
        # Should handle invalid data gracefully
        try:
            score = self.scorer.calculate_sustainability_score('test_scenario', invalid_data)
            # Should still return a valid score structure
            self.assertIn('overall_score', score)
        except Exception as e:
            # Should handle errors gracefully
            self.fail(f"Score calculation should handle invalid data gracefully: {e}")

    def test_score_comparison(self):
        """Test sustainability score comparison between scenarios"""
        scenario_a_data = {
            'energy_metrics': {'renewable_fraction': 0.9},
            'mobility_metrics': {'walkability_score': 90}
        }
        
        scenario_b_data = {
            'energy_metrics': {'renewable_fraction': 0.7},
            'mobility_metrics': {'walkability_score': 70}
        }
        
        score_a = self.scorer.calculate_sustainability_score('scenario_a', scenario_a_data)
        score_b = self.scorer.calculate_sustainability_score('scenario_b', scenario_b_data)
        
        # Scenario A should score higher than Scenario B
        self.assertGreater(score_a['overall_score'], score_b['overall_score'])

if __name__ == '__main__':
    unittest.main()
