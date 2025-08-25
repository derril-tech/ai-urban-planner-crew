# Created automatically by Cursor AI (2025-08-25)
import json
from typing import Dict, Any, List
from datetime import datetime

class DemoSiteGenerator:
    def __init__(self):
        self.demo_sites = {
            'coastal_flood': self._create_coastal_flood_site(),
            'brownfield_grid': self._create_brownfield_grid_site(),
            'greenfield_edge': self._create_greenfield_edge_site()
        }

    def get_demo_site(self, site_type: str) -> Dict[str, Any]:
        """Get demo site data by type"""
        return self.demo_sites.get(site_type, {})

    def get_all_demo_sites(self) -> Dict[str, Any]:
        """Get all demo sites"""
        return self.demo_sites

    def _create_coastal_flood_site(self) -> Dict[str, Any]:
        """Create coastal flood-adjacent demo site"""
        return {
            'id': 'coastal_flood_demo',
            'name': 'Coastal Resilience District',
            'description': 'A 2.5 km² coastal development site with flood risk management and climate adaptation features',
            'location': {
                'city': 'Miami Beach',
                'state': 'FL',
                'country': 'USA',
                'latitude': 25.7617,
                'longitude': -80.1918
            },
            'site_boundary': {
                'type': 'Polygon',
                'coordinates': [[
                    [-80.195, 25.760], [-80.185, 25.760], [-80.185, 25.770], 
                    [-80.195, 25.770], [-80.195, 25.760]
                ]]
            },
            'area_hectares': 250,
            'existing_conditions': {
                'land_use': 'Mixed urban and vacant',
                'flood_risk': 'High (100-year floodplain)',
                'elevation': '1-3 meters above sea level',
                'existing_buildings': 15,
                'vacant_parcels': 45
            },
            'development_constraints': {
                'flood_elevation': 3.5,  # meters
                'storm_surge_risk': 'High',
                'sea_level_rise': 0.3,  # meters by 2050
                'wetland_protection': True,
                'coastal_setbacks': 50  # meters
            },
            'target_development': {
                'residential_units': 800,
                'commercial_space': 25000,  # sq meters
                'institutional_space': 8000,  # sq meters
                'open_space_ratio': 0.25,
                'flood_resilient_design': True
            },
            'sustainability_features': {
                'elevated_construction': True,
                'stormwater_management': 'Bioswales and retention ponds',
                'renewable_energy': 'Solar PV and wind',
                'green_infrastructure': 'Living shorelines and wetlands',
                'climate_adaptation': 'Resilient building codes'
            },
            'infrastructure_requirements': {
                'elevated_roads': True,
                'stormwater_pumps': True,
                'backup_power': True,
                'flood_barriers': True
            },
            'estimated_costs': {
                'infrastructure': 45000000,  # $45M
                'buildings': 180000000,      # $180M
                'sustainability': 25000000,   # $25M
                'flood_protection': 35000000, # $35M
                'total': 285000000           # $285M
            },
            'timeline': {
                'planning_phase': '12 months',
                'infrastructure_phase': '18 months',
                'construction_phase': '36 months',
                'total_duration': '66 months'
            }
        }

    def _create_brownfield_grid_site(self) -> Dict[str, Any]:
        """Create brownfield grid demo site"""
        return {
            'id': 'brownfield_grid_demo',
            'name': 'Industrial District Redevelopment',
            'description': 'A 1.8 km² former industrial area with existing grid infrastructure and contamination challenges',
            'location': {
                'city': 'Detroit',
                'state': 'MI',
                'country': 'USA',
                'latitude': 42.3314,
                'longitude': -83.0458
            },
            'site_boundary': {
                'type': 'Polygon',
                'coordinates': [[
                    [-83.050, 42.330], [-83.040, 42.330], [-83.040, 42.340], 
                    [-83.050, 42.340], [-83.050, 42.330]
                ]]
            },
            'area_hectares': 180,
            'existing_conditions': {
                'land_use': 'Former industrial',
                'contamination': 'Medium (petroleum, heavy metals)',
                'existing_buildings': 25,
                'vacant_parcels': 60,
                'grid_infrastructure': 'Existing but deteriorated'
            },
            'development_constraints': {
                'soil_remediation': True,
                'building_demolition': True,
                'infrastructure_upgrade': True,
                'historic_preservation': 3,  # buildings to preserve
                'contamination_cleanup': 'Required'
            },
            'target_development': {
                'residential_units': 600,
                'commercial_space': 30000,  # sq meters
                'light_industrial': 15000,  # sq meters
                'mixed_use_ratio': 0.7,
                'adaptive_reuse': True
            },
            'sustainability_features': {
                'brownfield_remediation': True,
                'adaptive_reuse': 'Historic building preservation',
                'renewable_energy': 'Solar PV and geothermal',
                'stormwater_management': 'Green infrastructure',
                'transit_oriented': True
            },
            'infrastructure_requirements': {
                'soil_remediation': True,
                'utility_upgrades': True,
                'transit_connection': True,
                'pedestrian_network': True
            },
            'estimated_costs': {
                'remediation': 20000000,     # $20M
                'infrastructure': 30000000,   # $30M
                'buildings': 150000000,      # $150M
                'sustainability': 20000000,   # $20M
                'total': 220000000           # $220M
            },
            'timeline': {
                'remediation_phase': '18 months',
                'infrastructure_phase': '12 months',
                'construction_phase': '30 months',
                'total_duration': '60 months'
            }
        }

    def _create_greenfield_edge_site(self) -> Dict[str, Any]:
        """Create greenfield edge demo site"""
        return {
            'id': 'greenfield_edge_demo',
            'name': 'Suburban Expansion District',
            'description': 'A 3.2 km² greenfield site for suburban expansion with natural features and agricultural land',
            'location': {
                'city': 'Austin',
                'state': 'TX',
                'country': 'USA',
                'latitude': 30.2672,
                'longitude': -97.7431
            },
            'site_boundary': {
                'type': 'Polygon',
                'coordinates': [[
                    [-97.750, 30.265], [-97.735, 30.265], [-97.735, 30.280], 
                    [-97.750, 30.280], [-97.750, 30.265]
                ]]
            },
            'area_hectares': 320,
            'existing_conditions': {
                'land_use': 'Agricultural and natural',
                'vegetation': 'Mixed grassland and woodland',
                'water_features': 'Seasonal creeks',
                'existing_buildings': 5,
                'agricultural_land': 200  # hectares
            },
            'development_constraints': {
                'environmental_protection': True,
                'habitat_preservation': True,
                'water_quality': 'Protected watershed',
                'agricultural_land_loss': 'Minimize impact',
                'natural_features': 'Preserve existing'
            },
            'target_development': {
                'residential_units': 1200,
                'commercial_space': 40000,  # sq meters
                'institutional_space': 12000,  # sq meters
                'open_space_ratio': 0.35,
                'agricultural_preservation': 50  # hectares
            },
            'sustainability_features': {
                'low_impact_development': True,
                'habitat_corridors': True,
                'agricultural_integration': True,
                'renewable_energy': 'Solar and wind',
                'water_conservation': 'Rainwater harvesting'
            },
            'infrastructure_requirements': {
                'new_roads': True,
                'utility_extension': True,
                'water_systems': True,
                'wastewater_treatment': True
            },
            'estimated_costs': {
                'land_acquisition': 80000000,  # $80M
                'infrastructure': 40000000,    # $40M
                'buildings': 240000000,       # $240M
                'sustainability': 30000000,    # $30M
                'total': 390000000            # $390M
            },
            'timeline': {
                'land_acquisition': '6 months',
                'infrastructure_phase': '24 months',
                'construction_phase': '42 months',
                'total_duration': '72 months'
            }
        }

    def generate_parcel_data(self, site_type: str) -> List[Dict[str, Any]]:
        """Generate parcel data for demo site"""
        site = self.get_demo_site(site_type)
        if not site:
            return []

        parcels = []
        area_hectares = site['area_hectares']
        target_units = site['target_development']['residential_units']
        
        # Generate parcels based on site type
        if site_type == 'coastal_flood':
            parcels = self._generate_coastal_parcels(area_hectares, target_units)
        elif site_type == 'brownfield_grid':
            parcels = self._generate_brownfield_parcels(area_hectares, target_units)
        elif site_type == 'greenfield_edge':
            parcels = self._generate_greenfield_parcels(area_hectares, target_units)

        return parcels

    def _generate_coastal_parcels(self, area_hectares: float, target_units: int) -> List[Dict[str, Any]]:
        """Generate parcels for coastal flood site"""
        parcels = []
        num_parcels = 60
        
        for i in range(num_parcels):
            parcel_area = (area_hectares * 10000) / num_parcels  # Convert to sq meters
            
            # Vary parcel characteristics based on location
            if i < 20:  # Waterfront parcels
                use_mix = {'residential': 0.8, 'commercial': 0.2}
                far = 2.5
                height = 45
                flood_risk = 'High'
            elif i < 40:  # Mid-block parcels
                use_mix = {'residential': 0.6, 'commercial': 0.3, 'institutional': 0.1}
                far = 3.0
                height = 60
                flood_risk = 'Medium'
            else:  # Interior parcels
                use_mix = {'residential': 0.7, 'commercial': 0.2, 'institutional': 0.1}
                far = 2.0
                height = 30
                flood_risk = 'Low'

            parcel = {
                'id': f'coastal_parcel_{i+1}',
                'area': parcel_area,
                'use_mix': use_mix,
                'far': far,
                'height': height,
                'flood_risk': flood_risk,
                'elevation': 2.5 + (i % 3) * 0.5,  # 2.5-4.0 meters
                'flood_resilient': True,
                'sustainability_features': ['elevated_construction', 'stormwater_management']
            }
            parcels.append(parcel)

        return parcels

    def _generate_brownfield_parcels(self, area_hectares: float, target_units: int) -> List[Dict[str, Any]]:
        """Generate parcels for brownfield grid site"""
        parcels = []
        num_parcels = 85
        
        for i in range(num_parcels):
            parcel_area = (area_hectares * 10000) / num_parcels
            
            # Vary parcel characteristics based on grid location
            if i < 25:  # Corner parcels (commercial)
                use_mix = {'commercial': 0.7, 'residential': 0.3}
                far = 4.0
                height = 75
                contamination = 'Low'
            elif i < 50:  # Mid-block parcels (mixed use)
                use_mix = {'residential': 0.6, 'commercial': 0.3, 'light_industrial': 0.1}
                far = 3.5
                height = 60
                contamination = 'Medium'
            else:  # Interior parcels (residential)
                use_mix = {'residential': 0.8, 'commercial': 0.2}
                far = 2.5
                height = 45
                contamination = 'High'

            parcel = {
                'id': f'brownfield_parcel_{i+1}',
                'area': parcel_area,
                'use_mix': use_mix,
                'far': far,
                'height': height,
                'contamination': contamination,
                'remediation_required': contamination != 'Low',
                'adaptive_reuse': i < 10,  # First 10 parcels for adaptive reuse
                'sustainability_features': ['brownfield_remediation', 'adaptive_reuse']
            }
            parcels.append(parcel)

        return parcels

    def _generate_greenfield_parcels(self, area_hectares: float, target_units: int) -> List[Dict[str, Any]]:
        """Generate parcels for greenfield edge site"""
        parcels = []
        num_parcels = 100
        
        for i in range(num_parcels):
            parcel_area = (area_hectares * 10000) / num_parcels
            
            # Vary parcel characteristics based on location
            if i < 30:  # Edge parcels (commercial/institutional)
                use_mix = {'commercial': 0.6, 'institutional': 0.3, 'residential': 0.1}
                far = 2.0
                height = 40
                natural_features = 'Woodland'
            elif i < 70:  # Mid parcels (residential)
                use_mix = {'residential': 0.8, 'commercial': 0.2}
                far = 1.5
                height = 25
                natural_features = 'Grassland'
            else:  # Interior parcels (agricultural preservation)
                use_mix = {'agricultural': 0.8, 'residential': 0.2}
                far = 0.5
                height = 15
                natural_features = 'Agricultural'

            parcel = {
                'id': f'greenfield_parcel_{i+1}',
                'area': parcel_area,
                'use_mix': use_mix,
                'far': far,
                'height': height,
                'natural_features': natural_features,
                'agricultural_preservation': i >= 70,
                'low_impact_development': True,
                'sustainability_features': ['habitat_corridors', 'water_conservation']
            }
            parcels.append(parcel)

        return parcels

    def generate_network_data(self, site_type: str) -> List[Dict[str, Any]]:
        """Generate network data for demo site"""
        site = self.get_demo_site(site_type)
        if not site:
            return []

        networks = []
        
        if site_type == 'coastal_flood':
            networks = self._generate_coastal_network()
        elif site_type == 'brownfield_grid':
            networks = self._generate_brownfield_network()
        elif site_type == 'greenfield_edge':
            networks = self._generate_greenfield_network()

        return networks

    def _generate_coastal_network(self) -> List[Dict[str, Any]]:
        """Generate network for coastal flood site"""
        return [
            {
                'id': 'coastal_arterial_1',
                'link_class': 'arterial',
                'length': 1200,
                'width': 15,
                'elevation': 4.0,
                'flood_protection': True,
                'stormwater_management': True
            },
            {
                'id': 'coastal_collector_1',
                'link_class': 'collector',
                'length': 800,
                'width': 12,
                'elevation': 3.5,
                'flood_protection': True,
                'stormwater_management': True
            },
            {
                'id': 'coastal_local_1',
                'link_class': 'local',
                'length': 400,
                'width': 8,
                'elevation': 3.0,
                'flood_protection': False,
                'stormwater_management': True
            }
        ]

    def _generate_brownfield_network(self) -> List[Dict[str, Any]]:
        """Generate network for brownfield grid site"""
        return [
            {
                'id': 'brownfield_arterial_1',
                'link_class': 'arterial',
                'length': 900,
                'width': 14,
                'transit_ready': True,
                'pedestrian_priority': True
            },
            {
                'id': 'brownfield_collector_1',
                'link_class': 'collector',
                'length': 600,
                'width': 10,
                'transit_ready': False,
                'pedestrian_priority': True
            },
            {
                'id': 'brownfield_local_1',
                'link_class': 'local',
                'length': 300,
                'width': 7,
                'transit_ready': False,
                'pedestrian_priority': True
            }
        ]

    def _generate_greenfield_network(self) -> List[Dict[str, Any]]:
        """Generate network for greenfield edge site"""
        return [
            {
                'id': 'greenfield_arterial_1',
                'link_class': 'arterial',
                'length': 1500,
                'width': 16,
                'natural_corridor': True,
                'bike_lanes': True
            },
            {
                'id': 'greenfield_collector_1',
                'link_class': 'collector',
                'length': 1000,
                'width': 12,
                'natural_corridor': True,
                'bike_lanes': True
            },
            {
                'id': 'greenfield_local_1',
                'link_class': 'local',
                'length': 500,
                'width': 8,
                'natural_corridor': False,
                'bike_lanes': False
            }
        ]

    def export_demo_data(self, site_type: str, format: str = 'json') -> str:
        """Export demo site data in specified format"""
        site_data = {
            'site': self.get_demo_site(site_type),
            'parcels': self.generate_parcel_data(site_type),
            'network': self.generate_network_data(site_type),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'site_type': site_type,
                'version': '1.0'
            }
        }
        
        if format == 'json':
            return json.dumps(site_data, indent=2)
        else:
            return str(site_data)
