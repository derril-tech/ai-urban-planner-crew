# Created automatically by Cursor AI (2025-08-25)
import unittest
import json
from apps.workers.src.budget.budget_model import BudgetModel

class TestBudgetModel(unittest.TestCase):
    def setUp(self):
        self.model = BudgetModel()

    def test_infrastructure_cost_calculation(self):
        """Test infrastructure cost calculation"""
        road_length = 1000  # meters
        road_width = 12  # meters
        utility_length = 800  # meters
        
        infrastructure_cost = self.model.calculate_infrastructure_cost(road_length, road_width, utility_length)
        
        # Should have positive costs for all components
        self.assertGreater(infrastructure_cost['road_cost'], 0)
        self.assertGreater(infrastructure_cost['utility_cost'], 0)
        self.assertGreater(infrastructure_cost['total'], 0)

    def test_building_cost_calculation(self):
        """Test building cost calculation"""
        residential_area = 5000  # sq meters
        commercial_area = 2000  # sq meters
        institutional_area = 1000  # sq meters
        
        building_cost = self.model.calculate_building_cost(residential_area, commercial_area, institutional_area)
        
        # Should have positive costs for all building types
        self.assertGreater(building_cost['residential_cost'], 0)
        self.assertGreater(building_cost['commercial_cost'], 0)
        self.assertGreater(building_cost['institutional_cost'], 0)
        self.assertGreater(building_cost['total'], 0)

    def test_sustainability_cost_calculation(self):
        """Test sustainability feature cost calculation"""
        pv_capacity = 100  # kW
        green_roof_area = 500  # sq meters
        stormwater_area = 200  # sq meters
        
        sustainability_cost = self.model.calculate_sustainability_cost(pv_capacity, green_roof_area, stormwater_area)
        
        # Should have positive costs for all sustainability features
        self.assertGreater(sustainability_cost['pv_cost'], 0)
        self.assertGreater(sustainability_cost['green_roof_cost'], 0)
        self.assertGreater(sustainability_cost['stormwater_cost'], 0)
        self.assertGreater(sustainability_cost['total'], 0)

    def test_soft_cost_calculation(self):
        """Test soft cost calculation"""
        total_construction_cost = 10000000  # $10M
        soft_cost_percentage = 0.15  # 15%
        
        soft_cost = self.model.calculate_soft_costs(total_construction_cost, soft_cost_percentage)
        
        expected_soft_cost = total_construction_cost * soft_cost_percentage
        self.assertEqual(soft_cost, expected_soft_cost)

    def test_total_budget_calculation(self):
        """Test total budget calculation"""
        infrastructure_cost = 2000000  # $2M
        building_cost = 8000000  # $8M
        sustainability_cost = 1500000  # $1.5M
        soft_cost = 1725000  # $1.725M (15% of construction)
        
        total_budget = self.model.calculate_total_budget(infrastructure_cost, building_cost, sustainability_cost, soft_cost)
        
        expected_total = infrastructure_cost + building_cost + sustainability_cost + soft_cost
        self.assertEqual(total_budget, expected_total)

    def test_cost_per_unit_calculation(self):
        """Test cost per unit calculation"""
        total_budget = 10000000  # $10M
        total_units = 100
        
        cost_per_unit = self.model.calculate_cost_per_unit(total_budget, total_units)
        
        expected_cost_per_unit = total_budget / total_units
        self.assertEqual(cost_per_unit, expected_cost_per_unit)

    def test_cost_per_sqm_calculation(self):
        """Test cost per square meter calculation"""
        total_budget = 10000000  # $10M
        total_area = 50000  # 50,000 sq meters
        
        cost_per_sqm = self.model.calculate_cost_per_sqm(total_budget, total_area)
        
        expected_cost_per_sqm = total_budget / total_area
        self.assertEqual(cost_per_sqm, expected_cost_per_sqm)

    def test_construction_vs_soft_cost_ratio(self):
        """Test construction vs soft cost ratio calculation"""
        construction_cost = 8500000  # $8.5M
        soft_cost = 1500000  # $1.5M
        
        ratio = self.model.calculate_construction_soft_ratio(construction_cost, soft_cost)
        
        expected_ratio = construction_cost / soft_cost
        self.assertEqual(ratio, expected_ratio)

    def test_cost_breakdown_percentage(self):
        """Test cost breakdown percentage calculation"""
        infrastructure_cost = 2000000
        building_cost = 6000000
        sustainability_cost = 1500000
        soft_cost = 1425000
        total_budget = infrastructure_cost + building_cost + sustainability_cost + soft_cost
        
        breakdown = self.model.calculate_cost_breakdown_percentages(
            infrastructure_cost, building_cost, sustainability_cost, soft_cost, total_budget
        )
        
        # Percentages should sum to 100%
        total_percentage = (breakdown['infrastructure_percentage'] + 
                          breakdown['building_percentage'] + 
                          breakdown['sustainability_percentage'] + 
                          breakdown['soft_percentage'])
        
        self.assertAlmostEqual(total_percentage, 100.0, places=1)

    def test_affordability_analysis(self):
        """Test affordability analysis"""
        cost_per_unit = 200000  # $200k per unit
        median_income = 60000  # $60k median income
        affordability_ratio = 0.3  # 30% of income for housing
        
        affordability = self.model.analyze_affordability(cost_per_unit, median_income, affordability_ratio)
        
        # Should provide affordability metrics
        self.assertIn('affordable_price', affordability)
        self.assertIn('affordability_gap', affordability)
        self.assertIn('affordability_score', affordability)

    def test_cost_escalation_calculation(self):
        """Test cost escalation calculation"""
        base_cost = 1000000  # $1M base cost
        escalation_rate = 0.03  # 3% annual escalation
        years = 3
        
        escalated_cost = self.model.calculate_cost_escalation(base_cost, escalation_rate, years)
        
        expected_cost = base_cost * (1 + escalation_rate) ** years
        self.assertAlmostEqual(escalated_cost, expected_cost, places=2)

    def test_contingency_calculation(self):
        """Test contingency calculation"""
        base_cost = 10000000  # $10M base cost
        contingency_rate = 0.10  # 10% contingency
        
        contingency = self.model.calculate_contingency(base_cost, contingency_rate)
        
        expected_contingency = base_cost * contingency_rate
        self.assertEqual(contingency, expected_contingency)

    def test_operating_cost_calculation(self):
        """Test operating cost calculation"""
        building_area = 50000  # 50,000 sq meters
        energy_cost_per_sqm = 15  # $15/sq meter/year
        maintenance_cost_per_sqm = 8  # $8/sq meter/year
        management_cost_per_sqm = 5  # $5/sq meter/year
        
        operating_cost = self.model.calculate_operating_cost(
            building_area, energy_cost_per_sqm, maintenance_cost_per_sqm, management_cost_per_sqm
        )
        
        expected_energy_cost = building_area * energy_cost_per_sqm
        expected_maintenance_cost = building_area * maintenance_cost_per_sqm
        expected_management_cost = building_area * management_cost_per_sqm
        expected_total = expected_energy_cost + expected_maintenance_cost + expected_management_cost
        
        self.assertEqual(operating_cost['energy_cost'], expected_energy_cost)
        self.assertEqual(operating_cost['maintenance_cost'], expected_maintenance_cost)
        self.assertEqual(operating_cost['management_cost'], expected_management_cost)
        self.assertEqual(operating_cost['total'], expected_total)

    def test_return_on_investment_calculation(self):
        """Test ROI calculation"""
        total_investment = 10000000  # $10M investment
        annual_revenue = 1200000  # $1.2M annual revenue
        annual_operating_cost = 400000  # $400k annual operating cost
        
        roi = self.model.calculate_roi(total_investment, annual_revenue, annual_operating_cost)
        
        annual_profit = annual_revenue - annual_operating_cost
        expected_roi = (annual_profit / total_investment) * 100
        
        self.assertEqual(roi, expected_roi)

    def test_payback_period_calculation(self):
        """Test payback period calculation"""
        total_investment = 10000000  # $10M investment
        annual_savings = 800000  # $800k annual savings
        
        payback_period = self.model.calculate_payback_period(total_investment, annual_savings)
        
        expected_payback = total_investment / annual_savings
        self.assertEqual(payback_period, expected_payback)

    def test_scenario_budget_comparison(self):
        """Test budget comparison between scenarios"""
        scenario_a = {
            'total_budget': 10000000,
            'cost_per_unit': 200000,
            'cost_per_sqm': 2000
        }
        
        scenario_b = {
            'total_budget': 12000000,
            'cost_per_unit': 240000,
            'cost_per_sqm': 2400
        }
        
        comparison = self.model.compare_scenario_budgets(scenario_a, scenario_b)
        
        # Should provide comparison metrics
        self.assertIn('budget_difference', comparison)
        self.assertIn('cost_per_unit_difference', comparison)
        self.assertIn('cost_per_sqm_difference', comparison)

    def test_budget_sensitivity_analysis(self):
        """Test budget sensitivity analysis"""
        base_budget = 10000000  # $10M base budget
        cost_variables = {
            'material_cost_variance': 0.15,  # ±15%
            'labor_cost_variance': 0.10,     # ±10%
            'overhead_variance': 0.05        # ±5%
        }
        
        sensitivity = self.model.analyze_budget_sensitivity(base_budget, cost_variables)
        
        # Should provide sensitivity ranges
        self.assertIn('min_budget', sensitivity)
        self.assertIn('max_budget', sensitivity)
        self.assertIn('budget_range', sensitivity)

if __name__ == '__main__':
    unittest.main()
