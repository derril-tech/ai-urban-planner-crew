# Created automatically by Cursor AI (2025-08-25)
import unittest
import json
from apps.workers.src.capacity.capacity_engine import CapacityEngine

class TestCapacityMath(unittest.TestCase):
    def setUp(self):
        self.engine = CapacityEngine()

    def test_basic_capacity_calculation(self):
        """Test basic capacity calculation for a single parcel"""
        parcel_data = {
            'area': 10000,  # 10,000 sq meters
            'far': 2.0,     # Floor Area Ratio
            'height': 30,   # 30 meters
            'useMix': {
                'residential': 0.7,
                'commercial': 0.2,
                'institutional': 0.1
            },
            'avg_unit_size': 80,  # 80 sq meters per unit
            'avg_office_size': 150,  # 150 sq meters per job
            'avg_institutional_size': 200  # 200 sq meters per job
        }
        
        capacity = self.engine.calculate_parcel_capacity(parcel_data)
        
        # Total floor area = 10,000 * 2.0 = 20,000 sq meters
        expected_floor_area = 20000
        
        # Residential units = 20,000 * 0.7 / 80 = 175 units
        expected_residential_units = int(expected_floor_area * 0.7 / 80)
        
        # Commercial jobs = 20,000 * 0.2 / 150 = 26 jobs
        expected_commercial_jobs = int(expected_floor_area * 0.2 / 150)
        
        # Institutional jobs = 20,000 * 0.1 / 200 = 10 jobs
        expected_institutional_jobs = int(expected_floor_area * 0.1 / 200)
        
        self.assertEqual(capacity['total_floor_area'], expected_floor_area)
        self.assertEqual(capacity['residential_units'], expected_residential_units)
        self.assertEqual(capacity['commercial_jobs'], expected_commercial_jobs)
        self.assertEqual(capacity['institutional_jobs'], expected_institutional_jobs)

    def test_population_calculation(self):
        """Test population calculation based on units"""
        units = 100
        avg_household_size = 2.5
        
        population = self.engine.calculate_population(units, avg_household_size)
        expected_population = units * avg_household_size
        
        self.assertEqual(population, expected_population)

    def test_jobs_calculation(self):
        """Test jobs calculation based on commercial and institutional space"""
        commercial_area = 5000  # 5,000 sq meters
        institutional_area = 2000  # 2,000 sq meters
        avg_office_size = 150
        avg_institutional_size = 200
        
        jobs = self.engine.calculate_jobs(commercial_area, institutional_area, 
                                        avg_office_size, avg_institutional_size)
        
        expected_commercial_jobs = int(commercial_area / avg_office_size)
        expected_institutional_jobs = int(institutional_area / avg_institutional_size)
        
        self.assertEqual(jobs['commercial'], expected_commercial_jobs)
        self.assertEqual(jobs['institutional'], expected_institutional_jobs)
        self.assertEqual(jobs['total'], expected_commercial_jobs + expected_institutional_jobs)

    def test_use_mix_validation(self):
        """Test that use mix percentages sum to 100%"""
        valid_mix = {
            'residential': 0.6,
            'commercial': 0.3,
            'institutional': 0.1
        }
        
        invalid_mix = {
            'residential': 0.6,
            'commercial': 0.3,
            'institutional': 0.2  # Sum = 1.1 (110%)
        }
        
        self.assertTrue(self.engine.validate_use_mix(valid_mix))
        self.assertFalse(self.engine.validate_use_mix(invalid_mix))

    def test_far_validation(self):
        """Test FAR validation within reasonable bounds"""
        valid_far = 2.5
        invalid_far_high = 15.0
        invalid_far_low = -0.5
        
        self.assertTrue(self.engine.validate_far(valid_far))
        self.assertFalse(self.engine.validate_far(invalid_far_high))
        self.assertFalse(self.engine.validate_far(invalid_far_low))

    def test_height_validation(self):
        """Test building height validation"""
        valid_height = 45  # 45 meters
        invalid_height_high = 500  # 500 meters (unreasonable)
        invalid_height_low = -10  # Negative height
        
        self.assertTrue(self.engine.validate_height(valid_height))
        self.assertFalse(self.engine.validate_height(invalid_height_high))
        self.assertFalse(self.engine.validate_height(invalid_height_low))

    def test_setback_validation(self):
        """Test setback validation"""
        parcel_width = 50  # 50 meters
        parcel_depth = 30  # 30 meters
        setbacks = {
            'front': 5,
            'rear': 5,
            'side': 3
        }
        
        # Valid setbacks
        self.assertTrue(self.engine.validate_setbacks(parcel_width, parcel_depth, setbacks))
        
        # Invalid setbacks (too large)
        invalid_setbacks = {
            'front': 20,
            'rear': 20,
            'side': 15
        }
        self.assertFalse(self.engine.validate_setbacks(parcel_width, parcel_depth, invalid_setbacks))

    def test_density_calculation(self):
        """Test density calculations"""
        parcel_area = 10000  # 10,000 sq meters
        units = 50
        population = 125
        
        density = self.engine.calculate_density(parcel_area, units, population)
        
        # Units per hectare = 50 / 1 = 50 units/ha
        expected_units_per_ha = units / (parcel_area / 10000)
        
        # Population per hectare = 125 / 1 = 125 people/ha
        expected_pop_per_ha = population / (parcel_area / 10000)
        
        self.assertEqual(density['units_per_hectare'], expected_units_per_ha)
        self.assertEqual(density['population_per_hectare'], expected_pop_per_ha)

    def test_floor_area_ratio_calculation(self):
        """Test FAR calculation"""
        parcel_area = 5000  # 5,000 sq meters
        total_floor_area = 15000  # 15,000 sq meters
        
        far = self.engine.calculate_far(parcel_area, total_floor_area)
        expected_far = total_floor_area / parcel_area
        
        self.assertEqual(far, expected_far)

    def test_coverage_ratio_calculation(self):
        """Test lot coverage calculation"""
        parcel_area = 10000  # 10,000 sq meters
        building_footprint = 4000  # 4,000 sq meters
        
        coverage = self.engine.calculate_coverage_ratio(parcel_area, building_footprint)
        expected_coverage = building_footprint / parcel_area
        
        self.assertEqual(coverage, expected_coverage)

    def test_inclusionary_housing_calculation(self):
        """Test inclusionary housing requirements"""
        total_units = 100
        inclusionary_percentage = 0.15  # 15%
        
        inclusionary_units = self.engine.calculate_inclusionary_units(total_units, inclusionary_percentage)
        expected_units = int(total_units * inclusionary_percentage)
        
        self.assertEqual(inclusionary_units, expected_units)

    def test_parking_requirement_calculation(self):
        """Test parking requirement calculations"""
        residential_units = 50
        commercial_area = 2000  # 2,000 sq meters
        parking_ratios = {
            'residential': 1.5,  # 1.5 spaces per unit
            'commercial': 0.05   # 1 space per 20 sq meters
        }
        
        parking_spaces = self.engine.calculate_parking_requirements(
            residential_units, commercial_area, parking_ratios
        )
        
        expected_residential_spaces = int(residential_units * parking_ratios['residential'])
        expected_commercial_spaces = int(commercial_area * parking_ratios['commercial'])
        
        self.assertEqual(parking_spaces['residential'], expected_residential_spaces)
        self.assertEqual(parking_spaces['commercial'], expected_commercial_spaces)
        self.assertEqual(parking_spaces['total'], expected_residential_spaces + expected_commercial_spaces)

    def test_scenario_capacity_aggregation(self):
        """Test capacity aggregation across multiple parcels"""
        parcels = [
            {
                'id': 'parcel_1',
                'capacity': {
                    'residential_units': 25,
                    'commercial_jobs': 10,
                    'institutional_jobs': 5
                }
            },
            {
                'id': 'parcel_2',
                'capacity': {
                    'residential_units': 30,
                    'commercial_jobs': 15,
                    'institutional_jobs': 8
                }
            }
        ]
        
        total_capacity = self.engine.aggregate_scenario_capacity(parcels)
        
        expected_units = 25 + 30
        expected_commercial_jobs = 10 + 15
        expected_institutional_jobs = 5 + 8
        
        self.assertEqual(total_capacity['total_units'], expected_units)
        self.assertEqual(total_capacity['total_commercial_jobs'], expected_commercial_jobs)
        self.assertEqual(total_capacity['total_institutional_jobs'], expected_institutional_jobs)
        self.assertEqual(total_capacity['total_jobs'], expected_commercial_jobs + expected_institutional_jobs)

if __name__ == '__main__':
    unittest.main()
