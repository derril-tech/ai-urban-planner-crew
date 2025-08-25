# Created automatically by Cursor AI (2025-08-25)
import unittest
import json
import numpy as np
from apps.workers.src.energy.energy_model import EnergyModel

class TestEnergyModel(unittest.TestCase):
    def setUp(self):
        self.model = EnergyModel()

    def test_solar_irradiance_calculation(self):
        """Test solar irradiance calculation based on location and time"""
        latitude = 40.7128  # New York City
        longitude = -74.0060
        date = '2024-06-21'  # Summer solstice
        
        irradiance = self.model.calculate_solar_irradiance(latitude, longitude, date)
        
        # Should be positive and reasonable for summer
        self.assertGreater(irradiance, 0)
        self.assertLess(irradiance, 1000)  # W/m²

    def test_pv_panel_efficiency_calculation(self):
        """Test PV panel efficiency calculation"""
        panel_type = 'monocrystalline'
        temperature = 25  # Celsius
        irradiance = 800  # W/m²
        
        efficiency = self.model.calculate_pv_efficiency(panel_type, temperature, irradiance)
        
        # Efficiency should be between 15-25%
        self.assertGreater(efficiency, 0.15)
        self.assertLess(efficiency, 0.25)

    def test_pv_system_yield_calculation(self):
        """Test PV system yield calculation"""
        panel_area = 100  # 100 sq meters
        panel_efficiency = 0.20  # 20%
        irradiance = 800  # W/m²
        system_losses = 0.15  # 15% losses
        
        daily_yield = self.model.calculate_daily_pv_yield(panel_area, panel_efficiency, irradiance, system_losses)
        
        # Expected yield = 100 * 0.20 * 800 * (1-0.15) * 24 / 1000 = 326.4 kWh
        expected_yield = panel_area * panel_efficiency * irradiance * (1 - system_losses) * 24 / 1000
        
        self.assertAlmostEqual(daily_yield, expected_yield, places=1)

    def test_annual_energy_yield(self):
        """Test annual energy yield calculation"""
        daily_yield = 30  # kWh per day
        location = 'New York'
        
        annual_yield = self.model.calculate_annual_yield(daily_yield, location)
        
        # Should be reasonable annual yield
        self.assertGreater(annual_yield, daily_yield * 300)  # At least 300 days
        self.assertLess(annual_yield, daily_yield * 400)     # Less than 400 days

    def test_energy_demand_calculation(self):
        """Test energy demand calculation for different building types"""
        residential_units = 50
        commercial_area = 2000  # sq meters
        institutional_area = 1000  # sq meters
        
        demand = self.model.calculate_energy_demand(residential_units, commercial_area, institutional_area)
        
        # Should have positive values for all building types
        self.assertGreater(demand['residential'], 0)
        self.assertGreater(demand['commercial'], 0)
        self.assertGreater(demand['institutional'], 0)
        self.assertGreater(demand['total'], 0)

    def test_battery_storage_sizing(self):
        """Test battery storage sizing calculation"""
        daily_energy_demand = 1000  # kWh
        autonomy_days = 2  # 2 days of autonomy
        depth_of_discharge = 0.8  # 80% DoD
        
        battery_capacity = self.model.calculate_battery_capacity(daily_energy_demand, autonomy_days, depth_of_discharge)
        
        # Expected capacity = 1000 * 2 / 0.8 = 2500 kWh
        expected_capacity = daily_energy_demand * autonomy_days / depth_of_discharge
        
        self.assertAlmostEqual(battery_capacity, expected_capacity, places=1)

    def test_emissions_calculation(self):
        """Test emissions calculation"""
        grid_energy = 5000  # kWh from grid
        renewable_energy = 2000  # kWh from renewables
        grid_emission_factor = 0.5  # kg CO2/kWh
        
        emissions = self.model.calculate_emissions(grid_energy, renewable_energy, grid_emission_factor)
        
        # Grid emissions = 5000 * 0.5 = 2500 kg CO2
        expected_grid_emissions = grid_energy * grid_emission_factor
        
        # Renewable emissions = 0 (assumed)
        expected_renewable_emissions = 0
        
        self.assertEqual(emissions['grid_emissions'], expected_grid_emissions)
        self.assertEqual(emissions['renewable_emissions'], expected_renewable_emissions)
        self.assertEqual(emissions['total_emissions'], expected_grid_emissions + expected_renewable_emissions)

    def test_energy_cost_calculation(self):
        """Test energy cost calculation"""
        grid_energy = 3000  # kWh
        renewable_energy = 1000  # kWh
        grid_rate = 0.12  # $0.12/kWh
        renewable_rate = 0.08  # $0.08/kWh
        
        cost = self.model.calculate_energy_cost(grid_energy, renewable_energy, grid_rate, renewable_rate)
        
        expected_grid_cost = grid_energy * grid_rate
        expected_renewable_cost = renewable_energy * renewable_rate
        expected_total_cost = expected_grid_cost + expected_renewable_cost
        
        self.assertEqual(cost['grid_cost'], expected_grid_cost)
        self.assertEqual(cost['renewable_cost'], expected_renewable_cost)
        self.assertEqual(cost['total_cost'], expected_total_cost)

    def test_roof_pv_potential(self):
        """Test roof PV potential calculation"""
        roof_area = 500  # sq meters
        roof_orientation = 180  # degrees (south-facing)
        roof_tilt = 30  # degrees
        shading_factor = 0.9  # 90% of roof available
        
        potential = self.model.calculate_roof_pv_potential(roof_area, roof_orientation, roof_tilt, shading_factor)
        
        # Should be positive and reasonable
        self.assertGreater(potential['available_area'], 0)
        self.assertLess(potential['available_area'], roof_area)
        self.assertGreater(potential['max_capacity'], 0)

    def test_ground_mounted_pv_potential(self):
        """Test ground-mounted PV potential calculation"""
        available_area = 1000  # sq meters
        panel_spacing = 0.3  # 30% spacing between panels
        tracking_system = False  # Fixed tilt
        
        potential = self.model.calculate_ground_pv_potential(available_area, panel_spacing, tracking_system)
        
        # Available area should be reduced by spacing
        expected_available = available_area * (1 - panel_spacing)
        self.assertAlmostEqual(potential['available_area'], expected_available, places=1)

    def test_energy_storage_optimization(self):
        """Test energy storage optimization"""
        daily_demand = 800  # kWh
        daily_generation = 600  # kWh
        storage_capacity = 200  # kWh
        
        optimization = self.model.optimize_energy_storage(daily_demand, daily_generation, storage_capacity)
        
        # Should provide optimization results
        self.assertIn('grid_import', optimization)
        self.assertIn('grid_export', optimization)
        self.assertIn('storage_utilization', optimization)

    def test_energy_system_economics(self):
        """Test energy system economics calculation"""
        pv_capacity = 100  # kW
        battery_capacity = 200  # kWh
        pv_cost_per_kw = 1500  # $/kW
        battery_cost_per_kwh = 300  # $/kWh
        
        economics = self.model.calculate_energy_economics(pv_capacity, battery_capacity, pv_cost_per_kw, battery_cost_per_kwh)
        
        expected_pv_cost = pv_capacity * pv_cost_per_kw
        expected_battery_cost = battery_capacity * battery_cost_per_kwh
        expected_total_cost = expected_pv_cost + expected_battery_cost
        
        self.assertEqual(economics['pv_cost'], expected_pv_cost)
        self.assertEqual(economics['battery_cost'], expected_battery_cost)
        self.assertEqual(economics['total_cost'], expected_total_cost)

    def test_energy_performance_metrics(self):
        """Test energy performance metrics calculation"""
        annual_generation = 50000  # kWh
        annual_demand = 60000  # kWh
        renewable_fraction = annual_generation / annual_demand
        
        metrics = self.model.calculate_performance_metrics(annual_generation, annual_demand)
        
        self.assertEqual(metrics['renewable_fraction'], renewable_fraction)
        self.assertEqual(metrics['grid_dependency'], 1 - renewable_fraction)

    def test_parcel_energy_analysis(self):
        """Test complete parcel energy analysis"""
        parcel_data = {
            'area': 10000,  # 10,000 sq meters
            'roof_area': 2000,  # 2,000 sq meters
            'residential_units': 30,
            'commercial_area': 1500,
            'institutional_area': 500
        }
        
        analysis = self.model.analyze_parcel_energy(parcel_data)
        
        # Should return comprehensive analysis
        self.assertIn('demand', analysis)
        self.assertIn('pv_potential', analysis)
        self.assertIn('storage_requirements', analysis)
        self.assertIn('emissions', analysis)
        self.assertIn('economics', analysis)

if __name__ == '__main__':
    unittest.main()
