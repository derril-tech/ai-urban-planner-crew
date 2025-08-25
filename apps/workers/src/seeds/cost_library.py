# Created automatically by Cursor AI (2025-08-25)
import json
from typing import Dict, Any, List
from datetime import datetime

class CostLibrary:
    def __init__(self):
        self.cost_data = {
            'infrastructure': self._create_infrastructure_costs(),
            'buildings': self._create_building_costs(),
            'sustainability': self._create_sustainability_costs(),
            'soft_costs': self._create_soft_costs(),
            'utilities': self._create_utility_costs(),
            'landscaping': self._create_landscaping_costs()
        }

    def get_cost_data(self, category: str = None) -> Dict[str, Any]:
        """Get cost data by category or all costs"""
        if category:
            return self.cost_data.get(category, {})
        return self.cost_data

    def calculate_total_cost(self, quantities: Dict[str, float], location: str = 'national') -> Dict[str, Any]:
        """Calculate total cost based on quantities and location"""
        total_cost = 0
        cost_breakdown = {}
        
        for category, items in quantities.items():
            category_cost = 0
            category_data = self.cost_data.get(category, {})
            
            for item, quantity in items.items():
                if item in category_data:
                    base_cost = category_data[item]['base_cost']
                    location_factor = self._get_location_factor(location)
                    item_cost = base_cost * quantity * location_factor
                    category_cost += item_cost
                    
                    cost_breakdown[f"{category}_{item}"] = {
                        'quantity': quantity,
                        'unit_cost': base_cost * location_factor,
                        'total_cost': item_cost
                    }
            
            total_cost += category_cost
            cost_breakdown[category] = {
                'total': category_cost,
                'items': {k: v for k, v in cost_breakdown.items() if k.startswith(f"{category}_")}
            }
        
        return {
            'total_cost': total_cost,
            'cost_breakdown': cost_breakdown,
            'location_factor': self._get_location_factor(location),
            'calculated_at': datetime.now().isoformat()
        }

    def _create_infrastructure_costs(self) -> Dict[str, Any]:
        """Create infrastructure cost data"""
        return {
            'road_construction': {
                'base_cost': 250,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Standard road construction including base, asphalt, and drainage',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.2,
                    'southeast': 1.0,
                    'midwest': 0.9,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'sidewalk_construction': {
                'base_cost': 45,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Concrete sidewalk with base preparation',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.15,
                    'southeast': 0.95,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'stormwater_system': {
                'base_cost': 180,  # $/linear meter
                'unit': 'linear_meter',
                'description': 'Underground stormwater drainage system',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 1.0,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'water_main': {
                'base_cost': 220,  # $/linear meter
                'unit': 'linear_meter',
                'description': 'Water main installation including pipe and fittings',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.2,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'sanitary_sewer': {
                'base_cost': 200,  # $/linear meter
                'unit': 'linear_meter',
                'description': 'Sanitary sewer installation',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.15,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'electrical_underground': {
                'base_cost': 150,  # $/linear meter
                'unit': 'linear_meter',
                'description': 'Underground electrical distribution',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'street_lighting': {
                'base_cost': 8500,  # $/unit
                'unit': 'unit',
                'description': 'LED street light with pole and foundation',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            }
        }

    def _create_building_costs(self) -> Dict[str, Any]:
        """Create building cost data"""
        return {
            'residential_single_family': {
                'base_cost': 1800,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Single-family residential construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.25,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.15,
                    'national': 1.0
                }
            },
            'residential_multifamily': {
                'base_cost': 2200,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Multi-family residential construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.3,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.2,
                    'national': 1.0
                }
            },
            'commercial_office': {
                'base_cost': 2800,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Commercial office building construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.35,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.25,
                    'national': 1.0
                }
            },
            'commercial_retail': {
                'base_cost': 2400,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Commercial retail building construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.3,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.2,
                    'national': 1.0
                }
            },
            'institutional_school': {
                'base_cost': 3200,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'School building construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.4,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.3,
                    'national': 1.0
                }
            },
            'institutional_healthcare': {
                'base_cost': 4500,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Healthcare facility construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.45,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.35,
                    'national': 1.0
                }
            },
            'industrial_warehouse': {
                'base_cost': 1200,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Industrial warehouse construction',
                'source': 'RSMeans 2024',
                'location_factors': {
                    'northeast': 1.2,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.1,
                    'national': 1.0
                }
            }
        }

    def _create_sustainability_costs(self) -> Dict[str, Any]:
        """Create sustainability feature cost data"""
        return {
            'solar_pv_rooftop': {
                'base_cost': 1800,  # $/kW
                'unit': 'kW',
                'description': 'Rooftop solar PV system installation',
                'source': 'NREL 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 0.95,
                    'national': 1.0
                }
            },
            'solar_pv_ground': {
                'base_cost': 1200,  # $/kW
                'unit': 'kW',
                'description': 'Ground-mounted solar PV system',
                'source': 'NREL 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 0.95,
                    'national': 1.0
                }
            },
            'battery_storage': {
                'base_cost': 800,  # $/kWh
                'unit': 'kWh',
                'description': 'Battery energy storage system',
                'source': 'NREL 2024',
                'location_factors': {
                    'northeast': 1.05,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.0,
                    'national': 1.0
                }
            },
            'green_roof': {
                'base_cost': 180,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Extensive green roof system',
                'source': 'Green Roofs for Healthy Cities 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'rainwater_harvesting': {
                'base_cost': 120,  # $/cubic meter
                'unit': 'cubic_meter',
                'description': 'Rainwater harvesting system',
                'source': 'American Rainwater Catchment Systems 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'geothermal_heating': {
                'base_cost': 4500,  # $/ton
                'unit': 'ton',
                'description': 'Geothermal heat pump system',
                'source': 'International Ground Source Heat Pump Association 2024',
                'location_factors': {
                    'northeast': 1.15,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'ev_charging_station': {
                'base_cost': 3500,  # $/station
                'unit': 'station',
                'description': 'Level 2 EV charging station',
                'source': 'DOE Alternative Fuels Data Center 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            }
        }

    def _create_soft_costs(self) -> Dict[str, Any]:
        """Create soft cost data"""
        return {
            'architectural_design': {
                'base_cost': 0.08,  # 8% of construction cost
                'unit': 'percentage',
                'description': 'Architectural design and engineering',
                'source': 'AIA 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'permits_and_fees': {
                'base_cost': 0.03,  # 3% of construction cost
                'unit': 'percentage',
                'description': 'Building permits and regulatory fees',
                'source': 'Building Codes and Standards 2024',
                'location_factors': {
                    'northeast': 1.2,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'legal_and_insurance': {
                'base_cost': 0.02,  # 2% of construction cost
                'unit': 'percentage',
                'description': 'Legal services and insurance',
                'source': 'Construction Industry Institute 2024',
                'location_factors': {
                    'northeast': 1.15,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'project_management': {
                'base_cost': 0.05,  # 5% of construction cost
                'unit': 'percentage',
                'description': 'Project management and oversight',
                'source': 'Project Management Institute 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'financing_costs': {
                'base_cost': 0.04,  # 4% of total project cost
                'unit': 'percentage',
                'description': 'Financing and interest costs',
                'source': 'Urban Land Institute 2024',
                'location_factors': {
                    'northeast': 1.05,
                    'southeast': 0.95,
                    'midwest': 0.9,
                    'west': 1.0,
                    'national': 1.0
                }
            }
        }

    def _create_utility_costs(self) -> Dict[str, Any]:
        """Create utility cost data"""
        return {
            'water_treatment_plant': {
                'base_cost': 2500,  # $/cubic meter per day
                'unit': 'cubic_meter_per_day',
                'description': 'Water treatment plant construction',
                'source': 'American Water Works Association 2024',
                'location_factors': {
                    'northeast': 1.2,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'wastewater_treatment': {
                'base_cost': 3000,  # $/cubic meter per day
                'unit': 'cubic_meter_per_day',
                'description': 'Wastewater treatment plant construction',
                'source': 'Water Environment Federation 2024',
                'location_factors': {
                    'northeast': 1.25,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.15,
                    'national': 1.0
                }
            },
            'electrical_substation': {
                'base_cost': 500000,  # $/MVA
                'unit': 'MVA',
                'description': 'Electrical substation construction',
                'source': 'IEEE 2024',
                'location_factors': {
                    'northeast': 1.15,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.1,
                    'national': 1.0
                }
            },
            'natural_gas_distribution': {
                'base_cost': 150,  # $/linear meter
                'unit': 'linear_meter',
                'description': 'Natural gas distribution system',
                'source': 'American Gas Association 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            }
        }

    def _create_landscaping_costs(self) -> Dict[str, Any]:
        """Create landscaping cost data"""
        return {
            'park_development': {
                'base_cost': 85,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Public park development including amenities',
                'source': 'National Recreation and Park Association 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'tree_planting': {
                'base_cost': 450,  # $/tree
                'unit': 'tree',
                'description': 'Tree planting including materials and installation',
                'source': 'International Society of Arboriculture 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'bioswale': {
                'base_cost': 120,  # $/sq meter
                'unit': 'sq_meter',
                'description': 'Bioswale construction for stormwater management',
                'source': 'American Society of Civil Engineers 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            },
            'playground_equipment': {
                'base_cost': 25000,  # $/playground
                'unit': 'playground',
                'description': 'Complete playground equipment and surfacing',
                'source': 'National Recreation and Park Association 2024',
                'location_factors': {
                    'northeast': 1.1,
                    'southeast': 0.9,
                    'midwest': 0.85,
                    'west': 1.05,
                    'national': 1.0
                }
            }
        }

    def _get_location_factor(self, location: str) -> float:
        """Get location factor for cost adjustment"""
        location_factors = {
            'northeast': 1.2,
            'southeast': 0.9,
            'midwest': 0.85,
            'west': 1.1,
            'national': 1.0
        }
        return location_factors.get(location.lower(), 1.0)

    def get_cost_escalation(self, base_year: int, target_year: int) -> float:
        """Get cost escalation factor between years"""
        # Simplified escalation factors (in practice, these would come from industry indices)
        escalation_rates = {
            2020: 0.02,  # 2% per year
            2021: 0.03,  # 3% per year
            2022: 0.05,  # 5% per year
            2023: 0.04,  # 4% per year
            2024: 0.03,  # 3% per year
            2025: 0.025  # 2.5% per year
        }
        
        escalation_factor = 1.0
        for year in range(base_year, target_year):
            rate = escalation_rates.get(year, 0.025)  # Default 2.5%
            escalation_factor *= (1 + rate)
        
        return escalation_factor

    def export_cost_library(self, format: str = 'json') -> str:
        """Export cost library data"""
        export_data = {
            'cost_library': self.cost_data,
            'metadata': {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'sources': 'RSMeans, NREL, AIA, and industry standards 2024',
                'notes': 'Costs are base costs and should be adjusted for location and time'
            }
        }
        
        if format == 'json':
            return json.dumps(export_data, indent=2)
        else:
            return str(export_data)
