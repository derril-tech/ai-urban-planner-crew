# Created automatically by Cursor AI (2025-08-25)

import json
from typing import Dict, Any, List
from datetime import datetime

class PersonaNarratives:
    def __init__(self):
        self.personas = {
            'families': self._create_family_personas(),
            'seniors': self._create_senior_personas(),
            'young_professionals': self._create_young_professional_personas(),
            'students': self._create_student_personas(),
            'low_income': self._create_low_income_personas(),
            'disabled': self._create_disabled_personas(),
            'small_business': self._create_small_business_personas()
        }
        
        self.narrative_templates = self._create_narrative_templates()
        self.urban_priorities = self._create_urban_priorities()

    def get_persona_category(self, category: str) -> Dict[str, Any]:
        """Get all personas in a category"""
        return self.personas.get(category, {})

    def get_all_personas(self) -> Dict[str, Any]:
        """Get all persona categories"""
        return self.personas

    def get_persona_by_id(self, persona_id: str) -> Dict[str, Any]:
        """Get a specific persona by ID"""
        for category in self.personas.values():
            if persona_id in category:
                return category[persona_id]
        return {}

    def generate_narrative(self, persona_id: str, scenario_type: str = 'general') -> str:
        """Generate a narrative for a specific persona and scenario"""
        persona = self.get_persona_by_id(persona_id)
        if not persona:
            return ""
        
        template = self.narrative_templates.get(scenario_type, self.narrative_templates['general'])
        
        # Fill template with persona data
        narrative = template.format(
            name=persona['name'],
            age=persona['age'],
            occupation=persona['occupation'],
            household_size=persona['household_size'],
            income_level=persona['income_level'],
            primary_concern=persona['primary_concern'],
            mobility_preference=persona['mobility_preference'],
            housing_preference=persona['housing_preference'],
            community_priority=persona['community_priority']
        )
        
        return narrative

    def get_urban_priorities(self, persona_id: str) -> List[Dict[str, Any]]:
        """Get urban planning priorities for a persona"""
        persona = self.get_persona_by_id(persona_id)
        if not persona:
            return []
        
        priorities = []
        for priority in persona.get('urban_priorities', []):
            priority_data = self.urban_priorities.get(priority, {})
            if priority_data:
                priorities.append(priority_data)
        
        return priorities

    def _create_family_personas(self) -> Dict[str, Any]:
        return {
            'family_young': {
                'id': 'family_young',
                'name': 'Sarah & Mike Chen',
                'age': 32,
                'occupation': 'Software Engineer & Marketing Manager',
                'household_size': 4,
                'income_level': 'middle',
                'primary_concern': 'schools_and_safety',
                'mobility_preference': 'walking_and_transit',
                'housing_preference': 'townhouse_or_duplex',
                'community_priority': 'family_friendly_amenities',
                'urban_priorities': ['safe_streets', 'quality_schools', 'parks_playgrounds', 'transit_access'],
                'story': 'Young family with two kids (ages 4 and 7) looking for a walkable neighborhood with good schools and safe streets for their children to play.',
                'daily_routine': 'Drop kids at school, work from home 3 days/week, weekend family activities',
                'transportation_needs': 'Walking to school, transit to work, occasional car trips',
                'housing_needs': '3-4 bedrooms, outdoor space, near schools and parks'
            },
            'family_established': {
                'id': 'family_established',
                'name': 'Maria & David Rodriguez',
                'age': 45,
                'occupation': 'Teacher & Construction Manager',
                'household_size': 5,
                'income_level': 'middle',
                'primary_concern': 'affordability_and_stability',
                'mobility_preference': 'mixed_transportation',
                'housing_preference': 'single_family_home',
                'community_priority': 'stable_community',
                'urban_priorities': ['affordable_housing', 'job_access', 'community_centers', 'recreation_facilities'],
                'story': 'Established family with three teenagers, concerned about housing costs and providing opportunities for their children.',
                'daily_routine': 'Work commute, after-school activities, weekend sports',
                'transportation_needs': 'Reliable transit, car for family trips, bike lanes for teens',
                'housing_needs': '4+ bedrooms, space for growing family, storage'
            }
        }

    def _create_senior_personas(self) -> Dict[str, Any]:
        return {
            'senior_active': {
                'id': 'senior_active',
                'name': 'Robert Johnson',
                'age': 72,
                'occupation': 'Retired Professor',
                'household_size': 2,
                'income_level': 'upper_middle',
                'primary_concern': 'accessibility_and_community',
                'mobility_preference': 'walking_and_transit',
                'housing_preference': 'accessible_apartment',
                'community_priority': 'social_connections',
                'urban_priorities': ['accessible_design', 'transit_access', 'healthcare_access', 'social_spaces'],
                'story': 'Active senior who wants to stay independent and engaged in the community, concerned about accessibility and social isolation.',
                'daily_routine': 'Morning walks, community activities, library visits, social gatherings',
                'transportation_needs': 'Walking-friendly streets, accessible transit, occasional rideshare',
                'housing_needs': 'Ground floor or elevator, accessible bathroom, low maintenance'
            },
            'senior_fixed_income': {
                'id': 'senior_fixed_income',
                'name': 'Ethel Washington',
                'age': 78,
                'occupation': 'Retired',
                'household_size': 1,
                'income_level': 'low',
                'primary_concern': 'affordability_and_safety',
                'mobility_preference': 'walking_only',
                'housing_preference': 'senior_housing',
                'community_priority': 'safety_and_support',
                'urban_priorities': ['affordable_housing', 'safe_streets', 'healthcare_access', 'social_services'],
                'story': 'Senior on fixed income, concerned about rising housing costs and maintaining independence.',
                'daily_routine': 'Local errands, senior center activities, medical appointments',
                'transportation_needs': 'Walking to essential services, accessible transit for medical trips',
                'housing_needs': 'Small, affordable, accessible, near services'
            }
        }

    def _create_young_professional_personas(self) -> Dict[str, Any]:
        return {
            'young_professional_urban': {
                'id': 'young_professional_urban',
                'name': 'Alex Kim',
                'age': 28,
                'occupation': 'Data Scientist',
                'household_size': 1,
                'income_level': 'upper_middle',
                'primary_concern': 'convenience_and_lifestyle',
                'mobility_preference': 'walking_biking_transit',
                'housing_preference': 'modern_apartment',
                'community_priority': 'urban_amenities',
                'urban_priorities': ['transit_access', 'bike_infrastructure', 'nightlife_entertainment', 'coffee_shops'],
                'story': 'Young professional who values convenience, sustainability, and urban lifestyle. Prefers walking, biking, and transit over driving.',
                'daily_routine': 'Work from home/office, gym, social activities, weekend exploration',
                'transportation_needs': 'Bike lanes, reliable transit, walking-friendly streets',
                'housing_needs': '1-2 bedrooms, modern amenities, near transit and amenities'
            },
            'young_professional_suburban': {
                'id': 'young_professional_suburban',
                'name': 'Jennifer Park',
                'age': 31,
                'occupation': 'Marketing Director',
                'household_size': 2,
                'income_level': 'upper_middle',
                'primary_concern': 'space_and_investment',
                'mobility_preference': 'car_primary',
                'housing_preference': 'townhouse_or_condo',
                'community_priority': 'quiet_residential',
                'urban_priorities': ['parking', 'quiet_streets', 'parks', 'good_schools'],
                'story': 'Young professional planning for family, wants space and investment potential while maintaining some urban convenience.',
                'daily_routine': 'Work commute, evening activities, weekend relaxation',
                'transportation_needs': 'Reliable parking, good road access, occasional transit',
                'housing_needs': '2-3 bedrooms, outdoor space, parking, investment potential'
            }
        }

    def _create_student_personas(self) -> Dict[str, Any]:
        return {
            'student_undergraduate': {
                'id': 'student_undergraduate',
                'name': 'Jordan Smith',
                'age': 20,
                'occupation': 'University Student',
                'household_size': 3,
                'income_level': 'low',
                'primary_concern': 'affordability_and_access',
                'mobility_preference': 'walking_biking_transit',
                'housing_preference': 'shared_housing',
                'community_priority': 'student_amenities',
                'urban_priorities': ['affordable_housing', 'transit_access', 'student_services', '24_hour_amenities'],
                'story': 'Undergraduate student sharing housing with roommates, needs affordable options near campus with good transit access.',
                'daily_routine': 'Classes, study sessions, part-time work, social activities',
                'transportation_needs': 'Walking to campus, transit for errands, bike for local trips',
                'housing_needs': 'Shared housing, near campus, affordable, basic amenities'
            },
            'student_graduate': {
                'id': 'student_graduate',
                'name': 'Priya Patel',
                'age': 25,
                'occupation': 'Graduate Student',
                'household_size': 1,
                'income_level': 'low',
                'primary_concern': 'quiet_study_environment',
                'mobility_preference': 'walking_and_transit',
                'housing_preference': 'studio_apartment',
                'community_priority': 'academic_environment',
                'urban_priorities': ['quiet_neighborhoods', 'library_access', 'transit_access', 'affordable_housing'],
                'story': 'Graduate student who needs quiet environment for research and study, with access to academic resources.',
                'daily_routine': 'Research, classes, library study, occasional social activities',
                'transportation_needs': 'Walking to campus, transit for errands, occasional rideshare',
                'housing_needs': 'Studio or 1-bedroom, quiet location, near campus, affordable'
            }
        }

    def _create_low_income_personas(self) -> Dict[str, Any]:
        return {
            'low_income_worker': {
                'id': 'low_income_worker',
                'name': 'Marcus Thompson',
                'age': 35,
                'occupation': 'Service Worker',
                'household_size': 3,
                'income_level': 'low',
                'primary_concern': 'affordability_and_job_access',
                'mobility_preference': 'transit_primary',
                'housing_preference': 'affordable_apartment',
                'community_priority': 'essential_services',
                'urban_priorities': ['affordable_housing', 'job_access', 'transit_access', 'essential_services'],
                'story': 'Service worker supporting family, needs affordable housing near job opportunities with reliable transit access.',
                'daily_routine': 'Work shifts, family care, essential errands, community activities',
                'transportation_needs': 'Reliable transit to work, walking to local services',
                'housing_needs': '2-3 bedrooms, affordable, near transit and jobs'
            },
            'low_income_single_parent': {
                'id': 'low_income_single_parent',
                'name': 'Tanisha Williams',
                'age': 29,
                'occupation': 'Healthcare Aide',
                'household_size': 2,
                'income_level': 'low',
                'primary_concern': 'childcare_and_safety',
                'mobility_preference': 'transit_and_walking',
                'housing_preference': 'family_housing',
                'community_priority': 'family_support',
                'urban_priorities': ['affordable_housing', 'childcare_access', 'safe_streets', 'family_services'],
                'story': 'Single parent working in healthcare, needs affordable housing with access to childcare and safe environment for child.',
                'daily_routine': 'Work, childcare drop-off/pickup, family time, community activities',
                'transportation_needs': 'Transit to work, walking to childcare and services',
                'housing_needs': '2 bedrooms, affordable, safe neighborhood, near childcare'
            }
        }

    def _create_disabled_personas(self) -> Dict[str, Any]:
        return {
            'disabled_wheelchair': {
                'id': 'disabled_wheelchair',
                'name': 'David Chen',
                'age': 42,
                'occupation': 'IT Consultant',
                'household_size': 2,
                'income_level': 'middle',
                'primary_concern': 'accessibility_and_independence',
                'mobility_preference': 'accessible_transit',
                'housing_preference': 'accessible_apartment',
                'community_priority': 'inclusive_design',
                'urban_priorities': ['accessible_design', 'accessible_transit', 'healthcare_access', 'inclusive_spaces'],
                'story': 'Wheelchair user who values independence and accessibility in all aspects of urban life.',
                'daily_routine': 'Work from home/office, community activities, healthcare appointments',
                'transportation_needs': 'Accessible transit, curb cuts, wide sidewalks',
                'housing_needs': 'Accessible entrance, wide doorways, accessible bathroom, near transit'
            },
            'disabled_vision': {
                'id': 'disabled_vision',
                'name': 'Lisa Rodriguez',
                'age': 38,
                'occupation': 'Social Worker',
                'household_size': 1,
                'income_level': 'middle',
                'primary_concern': 'navigability_and_safety',
                'mobility_preference': 'walking_and_transit',
                'housing_preference': 'accessible_apartment',
                'community_priority': 'sensory_accessibility',
                'urban_priorities': ['accessible_design', 'safe_streets', 'transit_access', 'sensory_cues'],
                'story': 'Person with visual impairment who relies on auditory cues and tactile guidance for navigation.',
                'daily_routine': 'Work, community activities, social services, independent living',
                'transportation_needs': 'Audible signals, tactile guidance, reliable transit',
                'housing_needs': 'Accessible design, near transit, safe walking routes'
            }
        }

    def _create_small_business_personas(self) -> Dict[str, Any]:
        return {
            'small_business_owner': {
                'id': 'small_business_owner',
                'name': 'Carlos Mendez',
                'age': 45,
                'occupation': 'Restaurant Owner',
                'household_size': 4,
                'income_level': 'middle',
                'primary_concern': 'business_success_and_community',
                'mobility_preference': 'mixed_transportation',
                'housing_preference': 'mixed_use_property',
                'community_priority': 'vibrant_commercial_district',
                'urban_priorities': ['commercial_zoning', 'parking_access', 'pedestrian_traffic', 'transit_access'],
                'story': 'Small business owner who wants to create a successful business while contributing to community vibrancy.',
                'daily_routine': 'Business operations, community engagement, family time',
                'transportation_needs': 'Customer parking, delivery access, transit for employees',
                'housing_needs': 'Mixed-use property, commercial space, residential space'
            },
            'artisan_craftsman': {
                'id': 'artisan_craftsman',
                'name': 'Emma Wilson',
                'age': 39,
                'occupation': 'Artisan Craftsman',
                'household_size': 2,
                'income_level': 'middle',
                'primary_concern': 'workspace_and_market_access',
                'mobility_preference': 'walking_and_transit',
                'housing_preference': 'live_work_space',
                'community_priority': 'creative_district',
                'urban_priorities': ['creative_zoning', 'pedestrian_traffic', 'affordable_workspace', 'cultural_amenities'],
                'story': 'Artisan who needs affordable workspace and access to markets while contributing to cultural vibrancy.',
                'daily_routine': 'Creative work, market sales, community events, skill sharing',
                'transportation_needs': 'Walking to markets, transit for supplies, bike for local trips',
                'housing_needs': 'Live-work space, workshop area, affordable, near markets'
            }
        }

    def _create_narrative_templates(self) -> Dict[str, str]:
        return {
            'general': """Meet {name}, a {age}-year-old {occupation} living in a household of {household_size} people. 
            With a {income_level} income level, {name}'s primary concern is {primary_concern}. 
            They prefer {mobility_preference} for getting around and are looking for {housing_preference} housing. 
            Their top community priority is {community_priority}.""",
            
            'development_scenario': """In this development scenario, {name} would be most impacted by changes to {primary_concern}. 
            As someone who relies on {mobility_preference}, they need {community_priority} to be prioritized in the planning process. 
            Their {income_level} income level means {housing_preference} options must be available and affordable.""",
            
            'community_engagement': """{name} represents the voice of {occupation}s in our community. 
            Their story highlights the importance of {primary_concern} and {community_priority} in urban planning. 
            By understanding their needs for {mobility_preference} and {housing_preference}, we can create more inclusive development.""",
            
            'policy_impact': """Policy decisions around {primary_concern} directly affect {name} and similar residents. 
            Their {income_level} income level and need for {housing_preference} housing must be considered in affordability policies. 
            Their preference for {mobility_preference} should inform transportation and accessibility planning."""
        }

    def _create_urban_priorities(self) -> Dict[str, Any]:
        return {
            'safe_streets': {
                'id': 'safe_streets',
                'name': 'Safe Streets',
                'description': 'Traffic calming, pedestrian safety, crime prevention',
                'metrics': ['traffic_speed', 'pedestrian_injuries', 'crime_rate'],
                'planning_implications': ['traffic_calming', 'lighting', 'community_policing']
            },
            'quality_schools': {
                'id': 'quality_schools',
                'name': 'Quality Schools',
                'description': 'Access to good public schools and educational facilities',
                'metrics': ['school_ratings', 'walking_distance', 'class_sizes'],
                'planning_implications': ['school_siting', 'walking_routes', 'community_facilities']
            },
            'parks_playgrounds': {
                'id': 'parks_playgrounds',
                'name': 'Parks & Playgrounds',
                'description': 'Access to green spaces and recreational facilities',
                'metrics': ['park_access', 'playground_quality', 'green_space_per_capita'],
                'planning_implications': ['park_distribution', 'recreation_facilities', 'green_infrastructure']
            },
            'transit_access': {
                'id': 'transit_access',
                'name': 'Transit Access',
                'description': 'Reliable and accessible public transportation',
                'metrics': ['transit_frequency', 'walking_distance', 'accessibility'],
                'planning_implications': ['transit_routes', 'density_around_stops', 'accessibility_design']
            },
            'affordable_housing': {
                'id': 'affordable_housing',
                'name': 'Affordable Housing',
                'description': 'Housing options within reach of different income levels',
                'metrics': ['housing_costs', 'income_housing_ratio', 'availability'],
                'planning_implications': ['inclusionary_zoning', 'density_bonuses', 'subsidized_housing']
            },
            'job_access': {
                'id': 'job_access',
                'name': 'Job Access',
                'description': 'Access to employment opportunities',
                'metrics': ['commute_time', 'job_density', 'employment_rate'],
                'planning_implications': ['mixed_use_development', 'transit_to_jobs', 'economic_development']
            },
            'community_centers': {
                'id': 'community_centers',
                'name': 'Community Centers',
                'description': 'Spaces for community gathering and activities',
                'metrics': ['facility_access', 'programming', 'usage_rates'],
                'planning_implications': ['community_facilities', 'public_spaces', 'programming_support']
            },
            'recreation_facilities': {
                'id': 'recreation_facilities',
                'name': 'Recreation Facilities',
                'description': 'Sports, fitness, and recreational opportunities',
                'metrics': ['facility_access', 'programming', 'affordability'],
                'planning_implications': ['recreation_centers', 'sports_facilities', 'programming_support']
            },
            'accessible_design': {
                'id': 'accessible_design',
                'name': 'Accessible Design',
                'description': 'Universal design for people with disabilities',
                'metrics': ['accessibility_compliance', 'barrier_free_routes', 'inclusive_spaces'],
                'planning_implications': ['universal_design', 'accessibility_standards', 'inclusive_planning']
            },
            'healthcare_access': {
                'id': 'healthcare_access',
                'name': 'Healthcare Access',
                'description': 'Access to medical facilities and services',
                'metrics': ['facility_distance', 'service_availability', 'affordability'],
                'planning_implications': ['healthcare_facilities', 'transit_access', 'service_distribution']
            },
            'social_spaces': {
                'id': 'social_spaces',
                'name': 'Social Spaces',
                'description': 'Places for social interaction and community building',
                'metrics': ['space_availability', 'usage_patterns', 'social_connectivity'],
                'planning_implications': ['public_spaces', 'community_gathering', 'social_infrastructure']
            },
            'social_services': {
                'id': 'social_services',
                'name': 'Social Services',
                'description': 'Access to support services and assistance programs',
                'metrics': ['service_availability', 'accessibility', 'effectiveness'],
                'planning_implications': ['service_centers', 'outreach_programs', 'support_networks']
            },
            'bike_infrastructure': {
                'id': 'bike_infrastructure',
                'name': 'Bike Infrastructure',
                'description': 'Safe and connected bicycle facilities',
                'metrics': ['bike_lane_coverage', 'safety_ratings', 'connectivity'],
                'planning_implications': ['bike_lanes', 'bike_parking', 'bike_networks']
            },
            'nightlife_entertainment': {
                'id': 'nightlife_entertainment',
                'name': 'Nightlife & Entertainment',
                'description': 'Evening entertainment and cultural activities',
                'metrics': ['venue_density', 'variety', 'accessibility'],
                'planning_implications': ['entertainment_districts', 'cultural_facilities', 'nightlife_zoning']
            },
            'coffee_shops': {
                'id': 'coffee_shops',
                'name': 'Coffee Shops & Cafes',
                'description': 'Third places for social interaction and work',
                'metrics': ['cafe_density', 'walking_access', 'affordability'],
                'planning_implications': ['commercial_zoning', 'pedestrian_amenities', 'social_spaces']
            },
            'parking': {
                'id': 'parking',
                'name': 'Parking',
                'description': 'Adequate and accessible parking options',
                'metrics': ['parking_availability', 'cost', 'accessibility'],
                'planning_implications': ['parking_requirements', 'shared_parking', 'parking_management']
            },
            'quiet_streets': {
                'id': 'quiet_streets',
                'name': 'Quiet Streets',
                'description': 'Low-traffic, peaceful residential streets',
                'metrics': ['traffic_volume', 'noise_levels', 'safety'],
                'planning_implications': ['traffic_calming', 'residential_zoning', 'noise_reduction']
            },
            'student_services': {
                'id': 'student_services',
                'name': 'Student Services',
                'description': 'Support services for student population',
                'metrics': ['service_availability', 'accessibility', 'effectiveness'],
                'planning_implications': ['student_centers', 'support_services', 'campus_planning']
            },
            '24_hour_amenities': {
                'id': '24_hour_amenities',
                'name': '24-Hour Amenities',
                'description': 'Round-the-clock services and facilities',
                'metrics': ['availability', 'variety', 'accessibility'],
                'planning_implications': ['24_hour_zoning', 'service_distribution', 'safety_measures']
            },
            'quiet_neighborhoods': {
                'id': 'quiet_neighborhoods',
                'name': 'Quiet Neighborhoods',
                'description': 'Peaceful residential areas for study and rest',
                'metrics': ['noise_levels', 'traffic_volume', 'disturbance_frequency'],
                'planning_implications': ['residential_zoning', 'noise_control', 'traffic_management']
            },
            'library_access': {
                'id': 'library_access',
                'name': 'Library Access',
                'description': 'Access to libraries and educational resources',
                'metrics': ['library_distance', 'hours', 'resources'],
                'planning_implications': ['library_siting', 'educational_facilities', 'resource_access']
            },
            'essential_services': {
                'id': 'essential_services',
                'name': 'Essential Services',
                'description': 'Access to basic services like grocery stores and healthcare',
                'metrics': ['service_distance', 'availability', 'affordability'],
                'planning_implications': ['service_distribution', 'commercial_zoning', 'accessibility']
            },
            'childcare_access': {
                'id': 'childcare_access',
                'name': 'Childcare Access',
                'description': 'Access to quality childcare facilities',
                'metrics': ['facility_distance', 'availability', 'affordability'],
                'planning_implications': ['childcare_facilities', 'family_support', 'workforce_development']
            },
            'family_services': {
                'id': 'family_services',
                'name': 'Family Services',
                'description': 'Support services for families with children',
                'metrics': ['service_availability', 'accessibility', 'effectiveness'],
                'planning_implications': ['family_centers', 'support_programs', 'community_services']
            },
            'inclusive_spaces': {
                'id': 'inclusive_spaces',
                'name': 'Inclusive Spaces',
                'description': 'Spaces designed for people of all abilities',
                'metrics': ['accessibility_compliance', 'inclusive_design', 'usage_by_disabled'],
                'planning_implications': ['universal_design', 'accessibility_standards', 'inclusive_planning']
            },
            'sensory_cues': {
                'id': 'sensory_cues',
                'name': 'Sensory Cues',
                'description': 'Auditory and tactile guidance for navigation',
                'metrics': ['audible_signals', 'tactile_guidance', 'sensory_accessibility'],
                'planning_implications': ['accessible_signals', 'tactile_paving', 'sensory_design']
            },
            'commercial_zoning': {
                'id': 'commercial_zoning',
                'name': 'Commercial Zoning',
                'description': 'Appropriate zoning for business activities',
                'metrics': ['zoning_appropriateness', 'business_success', 'economic_vitality'],
                'planning_implications': ['commercial_districts', 'mixed_use_development', 'economic_development']
            },
            'pedestrian_traffic': {
                'id': 'pedestrian_traffic',
                'name': 'Pedestrian Traffic',
                'description': 'High foot traffic for business success',
                'metrics': ['pedestrian_volume', 'walking_access', 'business_visibility'],
                'planning_implications': ['pedestrian_amenities', 'walking_routes', 'commercial_siting']
            },
            'creative_zoning': {
                'id': 'creative_zoning',
                'name': 'Creative Zoning',
                'description': 'Zoning that supports creative and cultural activities',
                'metrics': ['creative_space_availability', 'cultural_vitality', 'artist_affordability'],
                'planning_implications': ['creative_districts', 'cultural_facilities', 'artist_housing']
            },
            'cultural_amenities': {
                'id': 'cultural_amenities',
                'name': 'Cultural Amenities',
                'description': 'Access to cultural facilities and activities',
                'metrics': ['facility_access', 'programming', 'cultural_vitality'],
                'planning_implications': ['cultural_districts', 'arts_facilities', 'cultural_programming']
            },
            'affordable_workspace': {
                'id': 'affordable_workspace',
                'name': 'Affordable Workspace',
                'description': 'Affordable spaces for creative and small business work',
                'metrics': ['workspace_costs', 'availability', 'accessibility'],
                'planning_implications': ['live_work_spaces', 'creative_incubators', 'affordable_commercial']
            }
        }

    def export_persona_data(self, format: str = 'json') -> str:
        """Export persona data in specified format"""
        if format == 'json':
            return json.dumps(self.personas, indent=2)
        elif format == 'csv':
            # Convert to CSV format
            csv_data = []
            for category, personas in self.personas.items():
                for persona_id, persona in personas.items():
                    csv_data.append({
                        'category': category,
                        'id': persona_id,
                        'name': persona['name'],
                        'age': persona['age'],
                        'occupation': persona['occupation'],
                        'household_size': persona['household_size'],
                        'income_level': persona['income_level'],
                        'primary_concern': persona['primary_concern'],
                        'mobility_preference': persona['mobility_preference'],
                        'housing_preference': persona['housing_preference'],
                        'community_priority': persona['community_priority']
                    })
            return json.dumps(csv_data, indent=2)  # Simplified CSV-like structure
        else:
            return json.dumps(self.personas, indent=2)
