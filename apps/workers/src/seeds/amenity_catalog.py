# Created automatically by Cursor AI (2025-08-25)

import json
from typing import Dict, Any, List
from datetime import datetime

class AmenityCatalog:
    def __init__(self):
        self.amenities = {
            'essential_services': self._create_essential_services(),
            'education': self._create_education_amenities(),
            'healthcare': self._create_healthcare_amenities(),
            'recreation': self._create_recreation_amenities(),
            'commercial': self._create_commercial_amenities(),
            'cultural': self._create_cultural_amenities(),
            'transportation': self._create_transportation_amenities(),
            'social_services': self._create_social_service_amenities(),
            'utilities': self._create_utility_amenities(),
            'safety': self._create_safety_amenities()
        }
        
        self.amenity_categories = self._create_amenity_categories()
        self.planning_standards = self._create_planning_standards()

    def get_amenity_category(self, category: str) -> Dict[str, Any]:
        """Get all amenities in a category"""
        return self.amenities.get(category, {})

    def get_all_amenities(self) -> Dict[str, Any]:
        """Get all amenity categories"""
        return self.amenities

    def get_amenity_by_id(self, amenity_id: str) -> Dict[str, Any]:
        """Get a specific amenity by ID"""
        for category in self.amenities.values():
            if amenity_id in category:
                return category[amenity_id]
        return {}

    def search_amenities(self, query: str) -> List[Dict[str, Any]]:
        """Search amenities by name or description"""
        results = []
        query_lower = query.lower()
        
        for category in self.amenities.values():
            for amenity_id, amenity in category.items():
                if (query_lower in amenity['name'].lower() or 
                    query_lower in amenity['description'].lower() or
                    query_lower in amenity['type'].lower()):
                    results.append(amenity)
        
        return results

    def get_amenities_by_use_type(self, use_type: str) -> List[Dict[str, Any]]:
        """Get amenities by use type (residential, commercial, mixed, etc.)"""
        results = []
        
        for category in self.amenities.values():
            for amenity_id, amenity in category.items():
                if use_type.lower() in amenity['use_type'].lower():
                    results.append(amenity)
        
        return results

    def get_amenities_by_size(self, min_size: float = 0, max_size: float = float('inf')) -> List[Dict[str, Any]]:
        """Get amenities by size range (in square meters)"""
        results = []
        
        for category in self.amenities.values():
            for amenity_id, amenity in category.items():
                size = amenity.get('typical_size', 0)
                if min_size <= size <= max_size:
                    results.append(amenity)
        
        return results

    def get_planning_standards(self, amenity_type: str = None) -> Dict[str, Any]:
        """Get planning standards for amenities"""
        if amenity_type:
            return self.planning_standards.get(amenity_type, {})
        return self.planning_standards

    def calculate_amenity_coverage(self, population: int, amenity_type: str) -> Dict[str, Any]:
        """Calculate amenity coverage for a given population"""
        standard = self.planning_standards.get(amenity_type, {})
        if not standard:
            return {}
        
        required_units = standard.get('units_per_capita', 0) * population
        service_radius = standard.get('service_radius_meters', 0)
        
        return {
            'amenity_type': amenity_type,
            'population': population,
            'required_units': required_units,
            'service_radius_meters': service_radius,
            'coverage_area_sqm': 3.14159 * (service_radius ** 2) if service_radius > 0 else 0,
            'planning_standard': standard
        }

    def _create_essential_services(self) -> Dict[str, Any]:
        return {
            'grocery_store': {
                'id': 'grocery_store',
                'name': 'Grocery Store',
                'type': 'retail',
                'use_type': 'commercial',
                'description': 'Full-service grocery store with fresh produce, dairy, and household items',
                'typical_size': 2000,
                'service_radius': 800,
                'hours': '7:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'parking_minimums', 'loading_dock'],
                'sustainability_features': ['energy_efficient_lighting', 'waste_recycling', 'local_produce']
            },
            'pharmacy': {
                'id': 'pharmacy',
                'name': 'Pharmacy',
                'type': 'healthcare',
                'use_type': 'commercial',
                'description': 'Pharmacy with prescription services and basic health supplies',
                'typical_size': 300,
                'service_radius': 1000,
                'hours': '8:00-21:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'healthcare_licensing'],
                'sustainability_features': ['energy_efficient_lighting', 'waste_management']
            },
            'bank_atm': {
                'id': 'bank_atm',
                'name': 'Bank/ATM',
                'type': 'financial',
                'use_type': 'commercial',
                'description': 'Bank branch or ATM for financial services',
                'typical_size': 150,
                'service_radius': 1200,
                'hours': '9:00-17:00 (24h ATM)',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'security_standards'],
                'sustainability_features': ['energy_efficient_lighting', 'digital_services']
            },
            'post_office': {
                'id': 'post_office',
                'name': 'Post Office',
                'type': 'government',
                'use_type': 'institutional',
                'description': 'Postal services and mail handling',
                'typical_size': 400,
                'service_radius': 1500,
                'hours': '8:00-18:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['government_facility', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'recycling_programs']
            },
            'laundromat': {
                'id': 'laundromat',
                'name': 'Laundromat',
                'type': 'service',
                'use_type': 'commercial',
                'description': 'Self-service laundry facilities',
                'typical_size': 200,
                'service_radius': 600,
                'hours': '6:00-23:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'utility_connections'],
                'sustainability_features': ['energy_efficient_machines', 'water_conservation']
            }
        }

    def _create_education_amenities(self) -> Dict[str, Any]:
        return {
            'elementary_school': {
                'id': 'elementary_school',
                'name': 'Elementary School',
                'type': 'education',
                'use_type': 'institutional',
                'description': 'Public elementary school (K-5)',
                'typical_size': 8000,
                'service_radius': 800,
                'hours': '8:00-15:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['school_zoning', 'playground', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_building', 'green_playground', 'solar_panels']
            },
            'middle_school': {
                'id': 'middle_school',
                'name': 'Middle School',
                'type': 'education',
                'use_type': 'institutional',
                'description': 'Public middle school (6-8)',
                'typical_size': 12000,
                'service_radius': 1200,
                'hours': '8:00-15:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['school_zoning', 'sports_facilities', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_building', 'sports_fields', 'solar_panels']
            },
            'high_school': {
                'id': 'high_school',
                'name': 'High School',
                'type': 'education',
                'use_type': 'institutional',
                'description': 'Public high school (9-12)',
                'typical_size': 20000,
                'service_radius': 2000,
                'hours': '8:00-15:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['school_zoning', 'sports_complex', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_building', 'sports_complex', 'solar_panels']
            },
            'library': {
                'id': 'library',
                'name': 'Public Library',
                'type': 'education',
                'use_type': 'institutional',
                'description': 'Public library with books, computers, and community space',
                'typical_size': 1500,
                'service_radius': 1500,
                'hours': '9:00-21:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'quiet_zones'],
                'sustainability_features': ['energy_efficient_lighting', 'digital_resources', 'green_building']
            },
            'daycare': {
                'id': 'daycare',
                'name': 'Daycare Center',
                'type': 'education',
                'use_type': 'commercial',
                'description': 'Childcare facility for young children',
                'typical_size': 500,
                'service_radius': 500,
                'hours': '7:00-18:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'playground', 'safety_standards'],
                'sustainability_features': ['energy_efficient_building', 'green_playground', 'healthy_materials']
            }
        }

    def _create_healthcare_amenities(self) -> Dict[str, Any]:
        return {
            'medical_clinic': {
                'id': 'medical_clinic',
                'name': 'Medical Clinic',
                'type': 'healthcare',
                'use_type': 'commercial',
                'description': 'Primary care medical clinic',
                'typical_size': 800,
                'service_radius': 1500,
                'hours': '8:00-18:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'healthcare_licensing', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'medical_waste_management', 'green_building']
            },
            'dental_office': {
                'id': 'dental_office',
                'name': 'Dental Office',
                'type': 'healthcare',
                'use_type': 'commercial',
                'description': 'Dental care and oral health services',
                'typical_size': 400,
                'service_radius': 2000,
                'hours': '8:00-17:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'healthcare_licensing', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'dental_waste_management']
            },
            'urgent_care': {
                'id': 'urgent_care',
                'name': 'Urgent Care',
                'type': 'healthcare',
                'use_type': 'commercial',
                'description': 'Urgent care facility for non-emergency medical needs',
                'typical_size': 1000,
                'service_radius': 3000,
                'hours': '8:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'healthcare_licensing', 'emergency_access'],
                'sustainability_features': ['energy_efficient_lighting', 'medical_waste_management', 'green_building']
            },
            'mental_health_clinic': {
                'id': 'mental_health_clinic',
                'name': 'Mental Health Clinic',
                'type': 'healthcare',
                'use_type': 'commercial',
                'description': 'Mental health and counseling services',
                'typical_size': 600,
                'service_radius': 2500,
                'hours': '9:00-17:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'healthcare_licensing', 'privacy_standards'],
                'sustainability_features': ['energy_efficient_lighting', 'quiet_environment', 'green_building']
            }
        }

    def _create_recreation_amenities(self) -> Dict[str, Any]:
        return {
            'park': {
                'id': 'park',
                'name': 'Public Park',
                'type': 'recreation',
                'use_type': 'public',
                'description': 'Public green space with walking paths and seating',
                'typical_size': 5000,
                'service_radius': 800,
                'hours': '6:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['park_zoning', 'landscaping', 'lighting'],
                'sustainability_features': ['native_plants', 'water_conservation', 'solar_lighting']
            },
            'playground': {
                'id': 'playground',
                'name': 'Playground',
                'type': 'recreation',
                'use_type': 'public',
                'description': 'Children\'s playground with equipment',
                'typical_size': 1000,
                'service_radius': 400,
                'hours': '6:00-22:00',
                'accessibility': 'inclusive_design',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['park_zoning', 'safety_surfacing', 'fencing'],
                'sustainability_features': ['inclusive_equipment', 'safety_surfacing', 'shade_trees']
            },
            'community_center': {
                'id': 'community_center',
                'name': 'Community Center',
                'type': 'recreation',
                'use_type': 'institutional',
                'description': 'Multi-purpose community facility',
                'typical_size': 2000,
                'service_radius': 1500,
                'hours': '8:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'parking_minimums', 'multi_purpose_rooms'],
                'sustainability_features': ['energy_efficient_building', 'multi_purpose_design', 'green_building']
            },
            'sports_field': {
                'id': 'sports_field',
                'name': 'Sports Field',
                'type': 'recreation',
                'use_type': 'public',
                'description': 'Athletic field for soccer, baseball, etc.',
                'typical_size': 8000,
                'service_radius': 2000,
                'hours': '6:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['park_zoning', 'field_maintenance', 'parking_minimums'],
                'sustainability_features': ['drought_resistant_grass', 'water_efficient_irrigation', 'solar_lighting']
            },
            'swimming_pool': {
                'id': 'swimming_pool',
                'name': 'Swimming Pool',
                'type': 'recreation',
                'use_type': 'public',
                'description': 'Public swimming pool and aquatic center',
                'typical_size': 3000,
                'service_radius': 3000,
                'hours': '6:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['recreation_zoning', 'pool_safety', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_heating', 'water_conservation', 'solar_heating']
            }
        }

    def _create_commercial_amenities(self) -> Dict[str, Any]:
        return {
            'restaurant': {
                'id': 'restaurant',
                'name': 'Restaurant',
                'type': 'food_service',
                'use_type': 'commercial',
                'description': 'Full-service restaurant',
                'typical_size': 400,
                'service_radius': 1000,
                'hours': '11:00-23:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'kitchen_ventilation', 'restroom_requirements'],
                'sustainability_features': ['energy_efficient_kitchen', 'waste_composting', 'local_ingredients']
            },
            'coffee_shop': {
                'id': 'coffee_shop',
                'name': 'Coffee Shop',
                'type': 'food_service',
                'use_type': 'commercial',
                'description': 'Coffee shop and cafe',
                'typical_size': 200,
                'service_radius': 500,
                'hours': '6:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'kitchen_ventilation'],
                'sustainability_features': ['energy_efficient_equipment', 'fair_trade_coffee', 'waste_recycling']
            },
            'retail_store': {
                'id': 'retail_store',
                'name': 'Retail Store',
                'type': 'retail',
                'use_type': 'commercial',
                'description': 'General retail store',
                'typical_size': 800,
                'service_radius': 800,
                'hours': '9:00-21:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'display_windows', 'loading_area'],
                'sustainability_features': ['energy_efficient_lighting', 'sustainable_products', 'waste_recycling']
            },
            'convenience_store': {
                'id': 'convenience_store',
                'name': 'Convenience Store',
                'type': 'retail',
                'use_type': 'commercial',
                'description': 'Small convenience store',
                'typical_size': 150,
                'service_radius': 400,
                'hours': '6:00-24:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'security_lighting'],
                'sustainability_features': ['energy_efficient_lighting', 'local_products', 'waste_recycling']
            }
        }

    def _create_cultural_amenities(self) -> Dict[str, Any]:
        return {
            'museum': {
                'id': 'museum',
                'name': 'Museum',
                'type': 'cultural',
                'use_type': 'institutional',
                'description': 'Cultural museum and exhibition space',
                'typical_size': 5000,
                'service_radius': 5000,
                'hours': '10:00-18:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['cultural_zoning', 'exhibition_space', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'climate_control', 'green_building']
            },
            'theater': {
                'id': 'theater',
                'name': 'Theater',
                'type': 'cultural',
                'use_type': 'commercial',
                'description': 'Performance theater and entertainment venue',
                'typical_size': 3000,
                'service_radius': 3000,
                'hours': '19:00-23:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['entertainment_zoning', 'performance_space', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'acoustic_design', 'green_building']
            },
            'art_gallery': {
                'id': 'art_gallery',
                'name': 'Art Gallery',
                'type': 'cultural',
                'use_type': 'commercial',
                'description': 'Art gallery and exhibition space',
                'typical_size': 800,
                'service_radius': 2000,
                'hours': '10:00-18:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['commercial_zoning', 'exhibition_space', 'climate_control'],
                'sustainability_features': ['energy_efficient_lighting', 'climate_control', 'local_artists']
            }
        }

    def _create_transportation_amenities(self) -> Dict[str, Any]:
        return {
            'bus_stop': {
                'id': 'bus_stop',
                'name': 'Bus Stop',
                'type': 'transit',
                'use_type': 'public',
                'description': 'Public bus stop with shelter',
                'typical_size': 20,
                'service_radius': 400,
                'hours': '24/7',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['transit_zoning', 'shelter', 'lighting'],
                'sustainability_features': ['solar_lighting', 'rainwater_collection', 'green_shelter']
            },
            'train_station': {
                'id': 'train_station',
                'name': 'Train Station',
                'type': 'transit',
                'use_type': 'public',
                'description': 'Rail transit station',
                'typical_size': 2000,
                'service_radius': 800,
                'hours': '5:00-24:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['transit_zoning', 'platform_access', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_lighting', 'solar_panels', 'green_building']
            },
            'bike_share': {
                'id': 'bike_share',
                'name': 'Bike Share Station',
                'type': 'transit',
                'use_type': 'public',
                'description': 'Bicycle sharing station',
                'typical_size': 50,
                'service_radius': 300,
                'hours': '24/7',
                'accessibility': 'universal_design',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['transit_zoning', 'bike_lanes', 'shelter'],
                'sustainability_features': ['solar_powered', 'zero_emissions', 'active_transportation']
            },
            'parking_garage': {
                'id': 'parking_garage',
                'name': 'Parking Garage',
                'type': 'transit',
                'use_type': 'public',
                'description': 'Multi-level parking facility',
                'typical_size': 5000,
                'service_radius': 800,
                'hours': '24/7',
                'accessibility': 'wheelchair_accessible',
                'parking_required': False,
                'transit_access': True,
                'planning_requirements': ['parking_zoning', 'access_ramps', 'lighting'],
                'sustainability_features': ['energy_efficient_lighting', 'ev_charging', 'solar_panels']
            }
        }

    def _create_social_service_amenities(self) -> Dict[str, Any]:
        return {
            'senior_center': {
                'id': 'senior_center',
                'name': 'Senior Center',
                'type': 'social_service',
                'use_type': 'institutional',
                'description': 'Community center for senior citizens',
                'typical_size': 1500,
                'service_radius': 2000,
                'hours': '8:00-17:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'activity_rooms', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_building', 'accessible_design', 'green_building']
            },
            'youth_center': {
                'id': 'youth_center',
                'name': 'Youth Center',
                'type': 'social_service',
                'use_type': 'institutional',
                'description': 'Community center for youth activities',
                'typical_size': 1200,
                'service_radius': 1500,
                'hours': '14:00-22:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'activity_rooms', 'supervision'],
                'sustainability_features': ['energy_efficient_building', 'sports_facilities', 'green_building']
            },
            'food_bank': {
                'id': 'food_bank',
                'name': 'Food Bank',
                'type': 'social_service',
                'use_type': 'institutional',
                'description': 'Food assistance and distribution center',
                'typical_size': 1000,
                'service_radius': 3000,
                'hours': '9:00-17:00',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'storage_facilities', 'distribution_area'],
                'sustainability_features': ['food_waste_reduction', 'energy_efficient_cooling', 'local_partnerships']
            }
        }

    def _create_utility_amenities(self) -> Dict[str, Any]:
        return {
            'water_treatment': {
                'id': 'water_treatment',
                'name': 'Water Treatment Plant',
                'type': 'utility',
                'use_type': 'industrial',
                'description': 'Water treatment and distribution facility',
                'typical_size': 50000,
                'service_radius': 10000,
                'hours': '24/7',
                'accessibility': 'limited_access',
                'parking_required': True,
                'transit_access': False,
                'planning_requirements': ['industrial_zoning', 'environmental_compliance', 'security'],
                'sustainability_features': ['water_conservation', 'energy_efficiency', 'renewable_energy']
            },
            'wastewater_treatment': {
                'id': 'wastewater_treatment',
                'name': 'Wastewater Treatment Plant',
                'type': 'utility',
                'use_type': 'industrial',
                'description': 'Sewage treatment and disposal facility',
                'typical_size': 80000,
                'service_radius': 15000,
                'hours': '24/7',
                'accessibility': 'limited_access',
                'parking_required': True,
                'transit_access': False,
                'planning_requirements': ['industrial_zoning', 'environmental_compliance', 'odor_control'],
                'sustainability_features': ['biogas_generation', 'water_recycling', 'energy_efficiency']
            },
            'electrical_substation': {
                'id': 'electrical_substation',
                'name': 'Electrical Substation',
                'type': 'utility',
                'use_type': 'industrial',
                'description': 'Electrical power distribution substation',
                'typical_size': 2000,
                'service_radius': 5000,
                'hours': '24/7',
                'accessibility': 'limited_access',
                'parking_required': False,
                'transit_access': False,
                'planning_requirements': ['utility_zoning', 'safety_standards', 'security'],
                'sustainability_features': ['smart_grid', 'energy_efficiency', 'renewable_integration']
            }
        }

    def _create_safety_amenities(self) -> Dict[str, Any]:
        return {
            'police_station': {
                'id': 'police_station',
                'name': 'Police Station',
                'type': 'safety',
                'use_type': 'institutional',
                'description': 'Local police station and public safety facility',
                'typical_size': 3000,
                'service_radius': 5000,
                'hours': '24/7',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'emergency_access', 'parking_minimums'],
                'sustainability_features': ['energy_efficient_building', 'emergency_power', 'green_building']
            },
            'fire_station': {
                'id': 'fire_station',
                'name': 'Fire Station',
                'type': 'safety',
                'use_type': 'institutional',
                'description': 'Fire station and emergency response facility',
                'typical_size': 2500,
                'service_radius': 3000,
                'hours': '24/7',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'emergency_access', 'vehicle_bays'],
                'sustainability_features': ['energy_efficient_building', 'emergency_power', 'green_building']
            },
            'emergency_shelter': {
                'id': 'emergency_shelter',
                'name': 'Emergency Shelter',
                'type': 'safety',
                'use_type': 'institutional',
                'description': 'Emergency shelter for disasters and crises',
                'typical_size': 2000,
                'service_radius': 5000,
                'hours': '24/7',
                'accessibility': 'wheelchair_accessible',
                'parking_required': True,
                'transit_access': True,
                'planning_requirements': ['institutional_zoning', 'emergency_access', 'shelter_space'],
                'sustainability_features': ['emergency_power', 'water_storage', 'sustainable_materials']
            }
        }

    def _create_amenity_categories(self) -> Dict[str, Any]:
        return {
            'essential_services': {
                'name': 'Essential Services',
                'description': 'Basic services needed for daily life',
                'color': '#4CAF50',
                'icon': 'shopping-cart'
            },
            'education': {
                'name': 'Education',
                'description': 'Educational facilities and learning spaces',
                'color': '#2196F3',
                'icon': 'graduation-cap'
            },
            'healthcare': {
                'name': 'Healthcare',
                'description': 'Medical and health-related facilities',
                'color': '#F44336',
                'icon': 'heart-pulse'
            },
            'recreation': {
                'name': 'Recreation',
                'description': 'Parks, sports, and recreational facilities',
                'color': '#8BC34A',
                'icon': 'tree-pine'
            },
            'commercial': {
                'name': 'Commercial',
                'description': 'Retail, dining, and commercial services',
                'color': '#FF9800',
                'icon': 'store'
            },
            'cultural': {
                'name': 'Cultural',
                'description': 'Arts, culture, and entertainment venues',
                'color': '#9C27B0',
                'icon': 'palette'
            },
            'transportation': {
                'name': 'Transportation',
                'description': 'Transit facilities and transportation infrastructure',
                'color': '#607D8B',
                'icon': 'bus'
            },
            'social_services': {
                'name': 'Social Services',
                'description': 'Community support and social service facilities',
                'color': '#795548',
                'icon': 'users'
            },
            'utilities': {
                'name': 'Utilities',
                'description': 'Infrastructure and utility facilities',
                'color': '#00BCD4',
                'icon': 'zap'
            },
            'safety': {
                'name': 'Safety',
                'description': 'Public safety and emergency facilities',
                'color': '#E91E63',
                'icon': 'shield'
            }
        }

    def _create_planning_standards(self) -> Dict[str, Any]:
        return {
            'grocery_store': {
                'units_per_capita': 0.0001,
                'service_radius_meters': 800,
                'parking_spaces_per_sqm': 0.1,
                'minimum_lot_size': 2000,
                'setback_requirements': 10,
                'height_restrictions': 15
            },
            'elementary_school': {
                'units_per_capita': 0.00005,
                'service_radius_meters': 800,
                'parking_spaces_per_sqm': 0.05,
                'minimum_lot_size': 8000,
                'setback_requirements': 20,
                'height_restrictions': 12
            },
            'park': {
                'units_per_capita': 0.0002,
                'service_radius_meters': 800,
                'parking_spaces_per_sqm': 0.02,
                'minimum_lot_size': 5000,
                'setback_requirements': 5,
                'height_restrictions': 0
            },
            'medical_clinic': {
                'units_per_capita': 0.00002,
                'service_radius_meters': 1500,
                'parking_spaces_per_sqm': 0.15,
                'minimum_lot_size': 800,
                'setback_requirements': 15,
                'height_restrictions': 20
            },
            'community_center': {
                'units_per_capita': 0.00003,
                'service_radius_meters': 1500,
                'parking_spaces_per_sqm': 0.08,
                'minimum_lot_size': 2000,
                'setback_requirements': 15,
                'height_restrictions': 15
            }
        }

    def export_amenity_data(self, format: str = 'json') -> str:
        """Export amenity data in specified format"""
        if format == 'json':
            return json.dumps(self.amenities, indent=2)
        elif format == 'csv':
            # Convert to CSV format
            csv_data = []
            for category, amenities in self.amenities.items():
                for amenity_id, amenity in amenities.items():
                    csv_data.append({
                        'category': category,
                        'id': amenity_id,
                        'name': amenity['name'],
                        'type': amenity['type'],
                        'use_type': amenity['use_type'],
                        'description': amenity['description'],
                        'typical_size': amenity['typical_size'],
                        'service_radius': amenity['service_radius'],
                        'hours': amenity['hours'],
                        'accessibility': amenity['accessibility'],
                        'parking_required': amenity['parking_required'],
                        'transit_access': amenity['transit_access']
                    })
            return json.dumps(csv_data, indent=2)  # Simplified CSV-like structure
        else:
            return json.dumps(self.amenities, indent=2)
