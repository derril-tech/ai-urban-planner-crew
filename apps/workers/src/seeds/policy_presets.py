# Created automatically by Cursor AI (2025-08-25)

import json
from typing import Dict, Any, List
from datetime import datetime

class PolicyPresets:
    def __init__(self):
        self.policy_categories = {
            'zoning': self._create_zoning_policies(),
            'sustainability': self._create_sustainability_policies(),
            'transportation': self._create_transportation_policies(),
            'housing': self._create_housing_policies(),
            'economic_development': self._create_economic_development_policies(),
            'environmental': self._create_environmental_policies(),
            'social_equity': self._create_social_equity_policies(),
            'infrastructure': self._create_infrastructure_policies()
        }
        
        self.policy_templates = self._create_policy_templates()
        self.compliance_checkers = self._create_compliance_checkers()

    def get_policy_category(self, category: str) -> Dict[str, Any]:
        """Get all policies in a category"""
        return self.policy_categories.get(category, {})

    def get_all_policies(self) -> Dict[str, Any]:
        """Get all policy categories"""
        return self.policy_categories

    def get_policy_by_id(self, policy_id: str) -> Dict[str, Any]:
        """Get a specific policy by ID"""
        for category in self.policy_categories.values():
            if policy_id in category:
                return category[policy_id]
        return {}

    def search_policies(self, query: str) -> List[Dict[str, Any]]:
        """Search policies by name or description"""
        results = []
        query_lower = query.lower()
        
        for category in self.policy_categories.values():
            for policy_id, policy in category.items():
                if (query_lower in policy['name'].lower() or 
                    query_lower in policy['description'].lower() or
                    query_lower in policy['type'].lower()):
                    results.append(policy)
        
        return results

    def get_policies_by_region(self, region_type: str) -> List[Dict[str, Any]]:
        """Get policies by region type (urban, suburban, rural, etc.)"""
        results = []
        
        for category in self.policy_categories.values():
            for policy_id, policy in category.items():
                if region_type.lower() in policy.get('applicable_regions', []):
                    results.append(policy)
        
        return results

    def check_compliance(self, scenario_data: Dict[str, Any], policy_id: str) -> Dict[str, Any]:
        """Check compliance with a specific policy"""
        policy = self.get_policy_by_id(policy_id)
        if not policy:
            return {'compliant': False, 'errors': ['Policy not found']}
        
        checker = self.compliance_checkers.get(policy_id)
        if checker:
            return checker(scenario_data, policy)
        
        return {'compliant': True, 'message': 'No compliance checker available'}

    def generate_policy_report(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive policy compliance report"""
        report = {
            'summary': {
                'total_policies': 0,
                'compliant_policies': 0,
                'non_compliant_policies': 0,
                'compliance_rate': 0.0
            },
            'details': [],
            'recommendations': []
        }
        
        total_policies = 0
        compliant_policies = 0
        
        for category_name, category_policies in self.policy_categories.items():
            for policy_id, policy in category_policies.items():
                total_policies += 1
                compliance_result = self.check_compliance(scenario_data, policy_id)
                
                detail = {
                    'policy_id': policy_id,
                    'policy_name': policy['name'],
                    'category': category_name,
                    'compliant': compliance_result.get('compliant', False),
                    'details': compliance_result.get('details', {}),
                    'errors': compliance_result.get('errors', []),
                    'recommendations': compliance_result.get('recommendations', [])
                }
                
                report['details'].append(detail)
                
                if detail['compliant']:
                    compliant_policies += 1
                else:
                    report['recommendations'].extend(detail['recommendations'])
        
        report['summary']['total_policies'] = total_policies
        report['summary']['compliant_policies'] = compliant_policies
        report['summary']['non_compliant_policies'] = total_policies - compliant_policies
        report['summary']['compliance_rate'] = (compliant_policies / total_policies * 100) if total_policies > 0 else 0
        
        return report

    def _create_zoning_policies(self) -> Dict[str, Any]:
        return {
            'mixed_use_development': {
                'id': 'mixed_use_development',
                'name': 'Mixed-Use Development',
                'type': 'zoning',
                'description': 'Encourage mixed-use development combining residential, commercial, and institutional uses',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'minimum_density': 50,  # units per hectare
                    'maximum_far': 3.0,
                    'ground_floor_commercial': 0.3,  # 30% of ground floor
                    'residential_units_required': 0.5,  # 50% of total floor area
                    'parking_maximum': 1.0,  # spaces per unit
                    'setback_minimum': 3,  # meters
                    'height_maximum': 45  # meters
                },
                'incentives': ['density_bonus', 'parking_reduction', 'fee_waivers'],
                'sustainability_requirements': ['green_building_standards', 'transit_access', 'walkability']
            },
            'transit_oriented_development': {
                'id': 'transit_oriented_development',
                'name': 'Transit-Oriented Development',
                'type': 'zoning',
                'description': 'High-density development within walking distance of transit stations',
                'applicable_regions': ['urban'],
                'requirements': {
                    'minimum_density': 100,  # units per hectare
                    'maximum_far': 5.0,
                    'transit_distance': 400,  # meters from transit
                    'parking_maximum': 0.5,  # spaces per unit
                    'setback_minimum': 2,  # meters
                    'height_maximum': 60  # meters
                },
                'incentives': ['density_bonus', 'parking_reduction', 'fee_waivers', 'fast_track_permitting'],
                'sustainability_requirements': ['green_building_standards', 'transit_access', 'walkability', 'bike_infrastructure']
            },
            'residential_density': {
                'id': 'residential_density',
                'name': 'Residential Density Standards',
                'type': 'zoning',
                'description': 'Minimum and maximum residential density requirements by zone',
                'applicable_regions': ['urban', 'suburban', 'rural'],
                'requirements': {
                    'urban_core': {'min_density': 80, 'max_density': 200},  # units per hectare
                    'urban_general': {'min_density': 40, 'max_density': 120},
                    'suburban': {'min_density': 20, 'max_density': 60},
                    'rural': {'min_density': 5, 'max_density': 20}
                },
                'incentives': ['density_bonus', 'fee_waivers'],
                'sustainability_requirements': ['green_building_standards', 'infrastructure_efficiency']
            },
            'commercial_zoning': {
                'id': 'commercial_zoning',
                'name': 'Commercial Zoning Standards',
                'type': 'zoning',
                'description': 'Commercial development standards and requirements',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'minimum_lot_size': 500,  # square meters
                    'maximum_far': 2.5,
                    'parking_ratio': 3.0,  # spaces per 100 sqm
                    'setback_minimum': 5,  # meters
                    'height_maximum': 30,  # meters
                    'loading_requirements': True
                },
                'incentives': ['green_building_bonus', 'transit_access_bonus'],
                'sustainability_requirements': ['green_building_standards', 'energy_efficiency', 'waste_management']
            }
        }

    def _create_sustainability_policies(self) -> Dict[str, Any]:
        return {
            'green_building_standards': {
                'id': 'green_building_standards',
                'name': 'Green Building Standards',
                'type': 'sustainability',
                'description': 'Mandatory green building certification and energy efficiency standards',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'energy_efficiency': 'ASHRAE_90.1_2019',
                    'water_efficiency': 'EPA_WaterSense',
                    'materials': 'LEED_Materials_Selection',
                    'indoor_air_quality': 'ASHRAE_62.1',
                    'site_sustainability': 'LEED_Site_Selection',
                    'certification_required': 'LEED_Silver'
                },
                'incentives': ['fee_waivers', 'density_bonus', 'fast_track_permitting'],
                'sustainability_requirements': ['renewable_energy', 'water_conservation', 'sustainable_materials']
            },
            'renewable_energy_requirements': {
                'id': 'renewable_energy_requirements',
                'name': 'Renewable Energy Requirements',
                'type': 'sustainability',
                'description': 'Minimum renewable energy generation requirements for new development',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'solar_pv_requirement': 0.15,  # 15% of building energy
                    'roof_solar_requirement': 0.3,  # 30% of roof area
                    'energy_storage': 0.1,  # 10% of peak demand
                    'electric_vehicle_charging': 0.2,  # 20% of parking spaces
                    'net_zero_ready': True
                },
                'incentives': ['solar_rebates', 'energy_storage_rebates', 'ev_charging_rebates'],
                'sustainability_requirements': ['renewable_energy', 'energy_efficiency', 'carbon_reduction']
            },
            'water_conservation': {
                'id': 'water_conservation',
                'name': 'Water Conservation Standards',
                'type': 'sustainability',
                'description': 'Water efficiency and conservation requirements',
                'applicable_regions': ['urban', 'suburban', 'rural'],
                'requirements': {
                    'indoor_water_efficiency': 0.3,  # 30% reduction from baseline
                    'outdoor_water_efficiency': 0.5,  # 50% reduction from baseline
                    'rainwater_harvesting': True,
                    'graywater_reuse': True,
                    'drought_resistant_landscaping': 0.8  # 80% of landscape
                },
                'incentives': ['water_efficiency_rebates', 'landscaping_rebates'],
                'sustainability_requirements': ['water_conservation', 'drought_resistance', 'sustainable_landscaping']
            },
            'waste_reduction': {
                'id': 'waste_reduction',
                'name': 'Waste Reduction and Recycling',
                'type': 'sustainability',
                'description': 'Construction and operational waste reduction requirements',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'construction_waste_recycling': 0.75,  # 75% diversion
                    'operational_waste_recycling': 0.6,  # 60% diversion
                    'composting_requirements': True,
                    'single_use_plastic_reduction': 0.8,  # 80% reduction
                    'circular_economy_principles': True
                },
                'incentives': ['waste_reduction_rebates', 'composting_rebates'],
                'sustainability_requirements': ['waste_reduction', 'recycling', 'circular_economy']
            }
        }

    def _create_transportation_policies(self) -> Dict[str, Any]:
        return {
            'complete_streets': {
                'id': 'complete_streets',
                'name': 'Complete Streets',
                'type': 'transportation',
                'description': 'Streets designed for all users including pedestrians, cyclists, and transit',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'pedestrian_facilities': True,
                    'bicycle_facilities': True,
                    'transit_facilities': True,
                    'accessible_design': True,
                    'traffic_calming': True,
                    'street_trees': True
                },
                'incentives': ['transportation_grants', 'infrastructure_funding'],
                'sustainability_requirements': ['active_transportation', 'transit_access', 'green_infrastructure']
            },
            'parking_maximums': {
                'id': 'parking_maximums',
                'name': 'Parking Maximums',
                'type': 'transportation',
                'description': 'Maximum parking requirements to encourage alternative transportation',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'residential_parking_maximum': 1.0,  # spaces per unit
                    'commercial_parking_maximum': 2.0,  # spaces per 100 sqm
                    'shared_parking_encouraged': True,
                    'bike_parking_required': 0.1,  # spaces per unit
                    'ev_charging_required': 0.2  # 20% of spaces
                },
                'incentives': ['parking_reduction_bonus', 'transit_access_bonus'],
                'sustainability_requirements': ['reduced_car_dependency', 'active_transportation', 'ev_infrastructure']
            },
            'transit_access': {
                'id': 'transit_access',
                'name': 'Transit Access Requirements',
                'type': 'transportation',
                'description': 'Requirements for transit access and connectivity',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'transit_stop_distance': 400,  # meters
                    'transit_frequency': 15,  # minutes
                    'transit_amenities': True,
                    'pedestrian_connectivity': True,
                    'bike_connectivity': True
                },
                'incentives': ['transit_access_bonus', 'density_bonus'],
                'sustainability_requirements': ['transit_access', 'active_transportation', 'reduced_vmt']
            },
            'bike_infrastructure': {
                'id': 'bike_infrastructure',
                'name': 'Bicycle Infrastructure Requirements',
                'type': 'transportation',
                'description': 'Comprehensive bicycle infrastructure and connectivity requirements',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'bike_lane_coverage': 0.8,  # 80% of streets
                    'bike_parking_ratio': 0.1,  # spaces per unit
                    'bike_share_stations': 0.05,  # stations per hectare
                    'bike_connectivity': True,
                    'bike_safety_features': True
                },
                'incentives': ['bike_infrastructure_grants', 'active_transportation_bonus'],
                'sustainability_requirements': ['active_transportation', 'reduced_car_dependency', 'health_benefits']
            }
        }

    def _create_housing_policies(self) -> Dict[str, Any]:
        return {
            'inclusionary_housing': {
                'id': 'inclusionary_housing',
                'name': 'Inclusionary Housing',
                'type': 'housing',
                'description': 'Requirements for affordable housing in new developments',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'affordable_units_required': 0.15,  # 15% of units
                    'affordability_levels': ['60%_ami', '80%_ami', '120%_ami'],
                    'affordability_duration': 30,  # years
                    'unit_size_mix': True,
                    'accessibility_requirements': True
                },
                'incentives': ['density_bonus', 'fee_waivers', 'fast_track_permitting'],
                'sustainability_requirements': ['affordable_housing', 'social_equity', 'community_diversity']
            },
            'housing_diversity': {
                'id': 'housing_diversity',
                'name': 'Housing Diversity Requirements',
                'type': 'housing',
                'description': 'Requirements for diverse housing types and sizes',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'unit_size_mix': {
                        'studio': 0.1,  # 10% of units
                        'one_bedroom': 0.25,  # 25% of units
                        'two_bedroom': 0.4,  # 40% of units
                        'three_bedroom': 0.2,  # 20% of units
                        'four_plus_bedroom': 0.05  # 5% of units
                    },
                    'housing_types': ['apartments', 'townhouses', 'single_family'],
                    'family_housing_priority': True
                },
                'incentives': ['diversity_bonus', 'family_housing_bonus'],
                'sustainability_requirements': ['housing_diversity', 'family_friendly_design', 'community_stability']
            },
            'universal_design': {
                'id': 'universal_design',
                'name': 'Universal Design Requirements',
                'type': 'housing',
                'description': 'Accessibility and universal design requirements for all housing',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'accessible_units_required': 0.1,  # 10% of units
                    'visitability_standards': True,
                    'aging_in_place_features': True,
                    'mobility_accessibility': True,
                    'sensory_accessibility': True
                },
                'incentives': ['accessibility_bonus', 'aging_in_place_bonus'],
                'sustainability_requirements': ['accessibility', 'inclusive_design', 'lifelong_housing']
            }
        }

    def _create_economic_development_policies(self) -> Dict[str, Any]:
        return {
            'local_business_support': {
                'id': 'local_business_support',
                'name': 'Local Business Support',
                'type': 'economic_development',
                'description': 'Policies to support local business development and retention',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'ground_floor_commercial': 0.3,  # 30% of ground floor
                    'local_business_preference': True,
                    'small_business_support': True,
                    'entrepreneurial_space': 0.1,  # 10% of commercial space
                    'business_incubation': True
                },
                'incentives': ['local_business_grants', 'rent_subsidies', 'technical_assistance'],
                'sustainability_requirements': ['local_economy', 'job_creation', 'economic_diversity']
            },
            'job_access': {
                'id': 'job_access',
                'name': 'Job Access and Workforce Development',
                'type': 'economic_development',
                'description': 'Policies to ensure job access and workforce development opportunities',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'job_training_facilities': True,
                    'workforce_development_programs': True,
                    'local_hiring_preferences': True,
                    'apprenticeship_programs': True,
                    'career_pathways': True
                },
                'incentives': ['workforce_development_grants', 'job_training_subsidies'],
                'sustainability_requirements': ['economic_opportunity', 'workforce_development', 'social_mobility']
            }
        }

    def _create_environmental_policies(self) -> Dict[str, Any]:
        return {
            'green_infrastructure': {
                'id': 'green_infrastructure',
                'name': 'Green Infrastructure Requirements',
                'type': 'environmental',
                'description': 'Requirements for green infrastructure and stormwater management',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'stormwater_management': 'green_infrastructure',
                    'tree_canopy_coverage': 0.3,  # 30% coverage
                    'green_roof_requirements': 0.2,  # 20% of roof area
                    'permeable_surfaces': 0.4,  # 40% of site
                    'biodiversity_enhancement': True
                },
                'incentives': ['green_infrastructure_grants', 'stormwater_fee_reduction'],
                'sustainability_requirements': ['stormwater_management', 'biodiversity', 'urban_forestry']
            },
            'climate_resilience': {
                'id': 'climate_resilience',
                'name': 'Climate Resilience Standards',
                'type': 'environmental',
                'description': 'Climate adaptation and resilience requirements',
                'applicable_regions': ['urban', 'suburban', 'rural'],
                'requirements': {
                    'flood_resistance': True,
                    'heat_island_reduction': True,
                    'drought_resistance': True,
                    'extreme_weather_preparation': True,
                    'climate_risk_assessment': True
                },
                'incentives': ['resilience_grants', 'insurance_reductions'],
                'sustainability_requirements': ['climate_adaptation', 'resilience', 'risk_reduction']
            }
        }

    def _create_social_equity_policies(self) -> Dict[str, Any]:
        return {
            'community_engagement': {
                'id': 'community_engagement',
                'name': 'Community Engagement Requirements',
                'type': 'social_equity',
                'description': 'Requirements for meaningful community engagement in development',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'public_meetings_required': 3,
                    'stakeholder_consultation': True,
                    'transparency_requirements': True,
                    'community_benefits_agreement': True,
                    'local_preference_programs': True
                },
                'incentives': ['community_engagement_grants', 'partnership_opportunities'],
                'sustainability_requirements': ['community_voice', 'social_equity', 'transparency']
            },
            'cultural_preservation': {
                'id': 'cultural_preservation',
                'name': 'Cultural Preservation and Heritage',
                'type': 'social_equity',
                'description': 'Policies to preserve cultural heritage and community character',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'historic_preservation': True,
                    'cultural_facilities': True,
                    'community_gathering_spaces': True,
                    'local_arts_support': True,
                    'heritage_interpretation': True
                },
                'incentives': ['cultural_preservation_grants', 'heritage_tax_credits'],
                'sustainability_requirements': ['cultural_heritage', 'community_identity', 'social_cohesion']
            }
        }

    def _create_infrastructure_policies(self) -> Dict[str, Any]:
        return {
            'smart_infrastructure': {
                'id': 'smart_infrastructure',
                'name': 'Smart Infrastructure Requirements',
                'type': 'infrastructure',
                'description': 'Smart city infrastructure and technology requirements',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'smart_lighting': True,
                    'traffic_management': True,
                    'environmental_monitoring': True,
                    'digital_connectivity': True,
                    'data_collection': True
                },
                'incentives': ['smart_city_grants', 'technology_partnerships'],
                'sustainability_requirements': ['energy_efficiency', 'data_driven_planning', 'technology_integration']
            },
            'utility_efficiency': {
                'id': 'utility_efficiency',
                'name': 'Utility Efficiency Standards',
                'type': 'infrastructure',
                'description': 'Energy and water utility efficiency requirements',
                'applicable_regions': ['urban', 'suburban'],
                'requirements': {
                    'energy_efficiency': 'ASHRAE_90.1_2019',
                    'water_efficiency': 'EPA_WaterSense',
                    'waste_management': 'Zero_Waste_Goals',
                    'renewable_energy_integration': True,
                    'microgrid_capability': True
                },
                'incentives': ['utility_efficiency_grants', 'renewable_energy_rebates'],
                'sustainability_requirements': ['energy_efficiency', 'water_conservation', 'waste_reduction']
            }
        }

    def _create_policy_templates(self) -> Dict[str, str]:
        return {
            'zoning_ordinance': """ZONING ORDINANCE SECTION {section_number}
            
            {policy_name}
            
            Purpose: {description}
            
            Applicability: This section applies to {applicable_regions} development.
            
            Requirements:
            {requirements_list}
            
            Incentives: {incentives_list}
            
            Compliance: {compliance_requirements}
            
            Enforcement: {enforcement_mechanisms}""",
            
            'sustainability_standard': """SUSTAINABILITY STANDARD {standard_number}
            
            {policy_name}
            
            Objective: {description}
            
            Scope: This standard applies to {applicable_regions} projects.
            
            Performance Requirements:
            {requirements_list}
            
            Compliance Pathways:
            {compliance_pathways}
            
            Verification: {verification_methods}
            
            Reporting: {reporting_requirements}""",
            
            'development_guideline': """DEVELOPMENT GUIDELINE {guideline_number}
            
            {policy_name}
            
            Intent: {description}
            
            Application: These guidelines apply to {applicable_regions} development.
            
            Design Principles:
            {design_principles}
            
            Implementation Strategies:
            {implementation_strategies}
            
            Best Practices:
            {best_practices}
            
            Resources: {additional_resources}"""
        }

    def _create_compliance_checkers(self) -> Dict[str, callable]:
        return {
            'mixed_use_development': self._check_mixed_use_compliance,
            'transit_oriented_development': self._check_tod_compliance,
            'green_building_standards': self._check_green_building_compliance,
            'inclusionary_housing': self._check_inclusionary_housing_compliance,
            'complete_streets': self._check_complete_streets_compliance
        }

    def _check_mixed_use_compliance(self, scenario_data: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with mixed-use development policy"""
        requirements = policy['requirements']
        errors = []
        recommendations = []
        
        # Check density requirements
        if scenario_data.get('density', 0) < requirements['minimum_density']:
            errors.append(f"Density {scenario_data.get('density', 0)} units/ha below minimum {requirements['minimum_density']} units/ha")
            recommendations.append("Increase residential density or reduce lot sizes")
        
        # Check FAR requirements
        if scenario_data.get('far', 0) > requirements['maximum_far']:
            errors.append(f"FAR {scenario_data.get('far', 0)} exceeds maximum {requirements['maximum_far']}")
            recommendations.append("Reduce building height or increase lot size")
        
        # Check ground floor commercial
        ground_floor_commercial = scenario_data.get('ground_floor_commercial_ratio', 0)
        if ground_floor_commercial < requirements['ground_floor_commercial']:
            errors.append(f"Ground floor commercial {ground_floor_commercial} below required {requirements['ground_floor_commercial']}")
            recommendations.append("Increase ground floor commercial space")
        
        return {
            'compliant': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations,
            'details': {
                'density_check': scenario_data.get('density', 0) >= requirements['minimum_density'],
                'far_check': scenario_data.get('far', 0) <= requirements['maximum_far'],
                'commercial_check': ground_floor_commercial >= requirements['ground_floor_commercial']
            }
        }

    def _check_tod_compliance(self, scenario_data: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with transit-oriented development policy"""
        requirements = policy['requirements']
        errors = []
        recommendations = []
        
        # Check transit distance
        transit_distance = scenario_data.get('transit_distance', float('inf'))
        if transit_distance > requirements['transit_distance']:
            errors.append(f"Transit distance {transit_distance}m exceeds maximum {requirements['transit_distance']}m")
            recommendations.append("Relocate development closer to transit or improve transit access")
        
        # Check density requirements
        if scenario_data.get('density', 0) < requirements['minimum_density']:
            errors.append(f"Density {scenario_data.get('density', 0)} units/ha below minimum {requirements['minimum_density']} units/ha")
            recommendations.append("Increase residential density")
        
        return {
            'compliant': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations,
            'details': {
                'transit_distance_check': transit_distance <= requirements['transit_distance'],
                'density_check': scenario_data.get('density', 0) >= requirements['minimum_density']
            }
        }

    def _check_green_building_compliance(self, scenario_data: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with green building standards"""
        requirements = policy['requirements']
        errors = []
        recommendations = []
        
        # Check energy efficiency
        energy_efficiency = scenario_data.get('energy_efficiency_standard', '')
        if energy_efficiency != requirements['energy_efficiency']:
            errors.append(f"Energy efficiency standard {energy_efficiency} does not meet required {requirements['energy_efficiency']}")
            recommendations.append("Upgrade to required energy efficiency standard")
        
        # Check certification
        certification = scenario_data.get('green_certification', '')
        if not certification or 'LEED' not in certification:
            errors.append("LEED certification required but not specified")
            recommendations.append("Pursue LEED Silver or higher certification")
        
        return {
            'compliant': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations,
            'details': {
                'energy_efficiency_check': energy_efficiency == requirements['energy_efficiency'],
                'certification_check': 'LEED' in certification
            }
        }

    def _check_inclusionary_housing_compliance(self, scenario_data: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with inclusionary housing policy"""
        requirements = policy['requirements']
        errors = []
        recommendations = []
        
        # Check affordable units
        affordable_units = scenario_data.get('affordable_units_ratio', 0)
        if affordable_units < requirements['affordable_units_required']:
            errors.append(f"Affordable units {affordable_units} below required {requirements['affordable_units_required']}")
            recommendations.append("Increase affordable housing units")
        
        return {
            'compliant': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations,
            'details': {
                'affordable_units_check': affordable_units >= requirements['affordable_units_required']
            }
        }

    def _check_complete_streets_compliance(self, scenario_data: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with complete streets policy"""
        requirements = policy['requirements']
        errors = []
        recommendations = []
        
        # Check pedestrian facilities
        if not scenario_data.get('pedestrian_facilities', False):
            errors.append("Pedestrian facilities required but not provided")
            recommendations.append("Add sidewalks and pedestrian crossings")
        
        # Check bicycle facilities
        if not scenario_data.get('bicycle_facilities', False):
            errors.append("Bicycle facilities required but not provided")
            recommendations.append("Add bike lanes or shared paths")
        
        return {
            'compliant': len(errors) == 0,
            'errors': errors,
            'recommendations': recommendations,
            'details': {
                'pedestrian_facilities_check': scenario_data.get('pedestrian_facilities', False),
                'bicycle_facilities_check': scenario_data.get('bicycle_facilities', False)
            }
        }

    def export_policy_data(self, format: str = 'json') -> str:
        """Export policy data in specified format"""
        if format == 'json':
            return json.dumps(self.policy_categories, indent=2)
        elif format == 'csv':
            # Convert to CSV format
            csv_data = []
            for category, policies in self.policy_categories.items():
                for policy_id, policy in policies.items():
                    csv_data.append({
                        'category': category,
                        'id': policy_id,
                        'name': policy['name'],
                        'type': policy['type'],
                        'description': policy['description'],
                        'applicable_regions': ','.join(policy['applicable_regions'])
                    })
            return json.dumps(csv_data, indent=2)  # Simplified CSV-like structure
        else:
            return json.dumps(self.policy_categories, indent=2)
