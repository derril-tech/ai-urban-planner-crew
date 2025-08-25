# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SustainabilityScore:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Default scoring weights (sum to 1.0)
        self.scoring_weights = {
            'energy': 0.25,
            'mobility': 0.20,
            'land_use': 0.20,
            'water': 0.15,
            'materials': 0.10,
            'resilience': 0.10
        }

        # Scoring criteria and thresholds
        self.scoring_criteria = {
            'energy': {
                'self_sufficiency': {
                    'excellent': 0.8,  # 80%+
                    'good': 0.6,       # 60-79%
                    'fair': 0.4,       # 40-59%
                    'poor': 0.2        # <40%
                },
                'emissions_reduction': {
                    'excellent': 0.7,  # 70%+
                    'good': 0.5,       # 50-69%
                    'fair': 0.3,       # 30-49%
                    'poor': 0.1        # <30%
                },
                'renewable_ratio': {
                    'excellent': 0.9,  # 90%+
                    'good': 0.7,       # 70-89%
                    'fair': 0.5,       # 50-69%
                    'poor': 0.3        # <50%
                }
            },
            'mobility': {
                'walkability': {
                    'excellent': 0.9,  # 90%+
                    'good': 0.7,       # 70-89%
                    'fair': 0.5,       # 50-69%
                    'poor': 0.3        # <50%
                },
                'transit_access': {
                    'excellent': 0.8,  # 80%+
                    'good': 0.6,       # 60-79%
                    'fair': 0.4,       # 40-59%
                    'poor': 0.2        # <40%
                },
                'bike_infrastructure': {
                    'excellent': 0.8,  # 80%+
                    'good': 0.6,       # 60-79%
                    'fair': 0.4,       # 40-59%
                    'poor': 0.2        # <40%
                }
            },
            'land_use': {
                'density': {
                    'excellent': 150,  # 150+ people/ha
                    'good': 100,       # 100-149 people/ha
                    'fair': 50,        # 50-99 people/ha
                    'poor': 25         # <50 people/ha
                },
                'mixed_use': {
                    'excellent': 0.8,  # 80%+ mixed use
                    'good': 0.6,       # 60-79% mixed use
                    'fair': 0.4,       # 40-59% mixed use
                    'poor': 0.2        # <40% mixed use
                },
                'green_space': {
                    'excellent': 0.3,  # 30%+ green space
                    'good': 0.2,       # 20-29% green space
                    'fair': 0.1,       # 10-19% green space
                    'poor': 0.05       # <10% green space
                }
            },
            'water': {
                'stormwater_management': {
                    'excellent': 0.9,  # 90%+ managed
                    'good': 0.7,       # 70-89% managed
                    'fair': 0.5,       # 50-69% managed
                    'poor': 0.3        # <50% managed
                },
                'water_efficiency': {
                    'excellent': 0.8,  # 80%+ efficient
                    'good': 0.6,       # 60-79% efficient
                    'fair': 0.4,       # 40-59% efficient
                    'poor': 0.2        # <40% efficient
                },
                'water_reuse': {
                    'excellent': 0.7,  # 70%+ reused
                    'good': 0.5,       # 50-69% reused
                    'fair': 0.3,       # 30-49% reused
                    'poor': 0.1        # <30% reused
                }
            },
            'materials': {
                'recycled_content': {
                    'excellent': 0.8,  # 80%+ recycled
                    'good': 0.6,       # 60-79% recycled
                    'fair': 0.4,       # 40-59% recycled
                    'poor': 0.2        # <40% recycled
                },
                'local_sourcing': {
                    'excellent': 0.9,  # 90%+ local
                    'good': 0.7,       # 70-89% local
                    'fair': 0.5,       # 50-69% local
                    'poor': 0.3        # <50% local
                },
                'embodied_carbon': {
                    'excellent': 0.3,  # 30%+ reduction
                    'good': 0.2,       # 20-29% reduction
                    'fair': 0.1,       # 10-19% reduction
                    'poor': 0.05       # <10% reduction
                }
            },
            'resilience': {
                'climate_adaptation': {
                    'excellent': 0.9,  # 90%+ adapted
                    'good': 0.7,       # 70-89% adapted
                    'fair': 0.5,       # 50-69% adapted
                    'poor': 0.3        # <50% adapted
                },
                'disaster_preparedness': {
                    'excellent': 0.8,  # 80%+ prepared
                    'good': 0.6,       # 60-79% prepared
                    'fair': 0.4,       # 40-59% prepared
                    'poor': 0.2        # <40% prepared
                },
                'social_equity': {
                    'excellent': 0.8,  # 80%+ equitable
                    'good': 0.6,       # 60-79% equitable
                    'fair': 0.4,       # 40-59% equitable
                    'poor': 0.2        # <40% equitable
                }
            }
        }

    def calculate_sustainability_score(self, scenario_id: str, weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Calculate comprehensive sustainability score for a scenario"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Update weights if provided
            if weights:
                self._validate_weights(weights)
                self.scoring_weights.update(weights)

            # Calculate category scores
            category_scores = {}
            total_score = 0

            # Energy Score
            energy_score = self._calculate_energy_score(scenario_data)
            category_scores['energy'] = energy_score
            total_score += energy_score['score'] * self.scoring_weights['energy']

            # Mobility Score
            mobility_score = self._calculate_mobility_score(scenario_data)
            category_scores['mobility'] = mobility_score
            total_score += mobility_score['score'] * self.scoring_weights['mobility']

            # Land Use Score
            land_use_score = self._calculate_land_use_score(scenario_data)
            category_scores['land_use'] = land_use_score
            total_score += land_use_score['score'] * self.scoring_weights['land_use']

            # Water Score
            water_score = self._calculate_water_score(scenario_data)
            category_scores['water'] = water_score
            total_score += water_score['score'] * self.scoring_weights['water']

            # Materials Score
            materials_score = self._calculate_materials_score(scenario_data)
            category_scores['materials'] = materials_score
            total_score += materials_score['score'] * self.scoring_weights['materials']

            # Resilience Score
            resilience_score = self._calculate_resilience_score(scenario_data)
            category_scores['resilience'] = resilience_score
            total_score += resilience_score['score'] * self.scoring_weights['resilience']

            # Calculate overall grade
            overall_grade = self._calculate_grade(total_score)

            # Store results
            results = {
                'overall_score': total_score,
                'overall_grade': overall_grade,
                'category_scores': category_scores,
                'weights': self.scoring_weights
            }

            self._store_sustainability_score(scenario_id, results)

            return {
                'success': True,
                'message': f'Calculated sustainability score: {overall_grade} ({total_score:.1f}/100)',
                'data': results
            }

        except Exception as e:
            logger.error(f"Error calculating sustainability score: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _validate_weights(self, weights: Dict[str, float]):
        """Validate that weights sum to 1.0"""
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

    def _get_scenario_data(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get all scenario data needed for scoring"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get scenario with KPIs
            query = """
            SELECT s.*, 
                   COUNT(p.id) as parcel_count,
                   SUM(ST_Area(p.geometry)) as total_area,
                   AVG(p.properties->>'far')::float as avg_far,
                   AVG(p.properties->>'height')::float as avg_height
            FROM scenarios s
            LEFT JOIN parcels p ON s.id = p.scenario_id AND p.status = 'active'
            WHERE s.id = %s
            GROUP BY s.id
            """
            cursor.execute(query, (scenario_id,))
            scenario = cursor.fetchone()
            
            if not scenario:
                return None

            # Get parcels with capacity data
            query = """
            SELECT properties, capacity
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            parcels = cursor.fetchall()

            # Get links for mobility analysis
            query = """
            SELECT properties, link_class
            FROM links
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            links = cursor.fetchall()

            return {
                'scenario': scenario,
                'parcels': parcels,
                'links': links,
                'kpis': scenario.get('kpis', {})
            }
            
        finally:
            cursor.close()
            conn.close()

    def _calculate_energy_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate energy sustainability score"""
        kpis = scenario_data['kpis']
        energy_data = kpis.get('energy_analysis', {})
        
        # Get energy metrics
        self_sufficiency = energy_data.get('demand', {}).get('self_sufficiency_ratio', 0)
        emissions_reduction = energy_data.get('emissions', {}).get('reduction_percent', 0)
        renewable_ratio = energy_data.get('solar', {}).get('renewable_ratio', 0)

        # Calculate subscores
        self_sufficiency_score = self._score_metric(self_sufficiency, self.scoring_criteria['energy']['self_sufficiency'])
        emissions_score = self._score_metric(emissions_reduction, self.scoring_criteria['energy']['emissions_reduction'])
        renewable_score = self._score_metric(renewable_ratio, self.scoring_criteria['energy']['renewable_ratio'])

        # Calculate weighted average
        energy_score = (self_sufficiency_score * 0.4 + emissions_score * 0.4 + renewable_score * 0.2) * 100

        return {
            'score': energy_score,
            'grade': self._calculate_grade(energy_score),
            'metrics': {
                'self_sufficiency': {'value': self_sufficiency, 'score': self_sufficiency_score * 100},
                'emissions_reduction': {'value': emissions_reduction, 'score': emissions_score * 100},
                'renewable_ratio': {'value': renewable_ratio, 'score': renewable_score * 100}
            }
        }

    def _calculate_mobility_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate mobility sustainability score"""
        kpis = scenario_data['kpis']
        network_data = kpis.get('network_analysis', {})
        
        # Get mobility metrics (simplified - would need more detailed analysis)
        walkability = network_data.get('intersection_density', 0) / 100  # Normalize to 0-1
        transit_access = 0.6  # Placeholder - would need transit data
        bike_infrastructure = 0.5  # Placeholder - would need bike lane data

        # Calculate subscores
        walkability_score = self._score_metric(walkability, self.scoring_criteria['mobility']['walkability'])
        transit_score = self._score_metric(transit_access, self.scoring_criteria['mobility']['transit_access'])
        bike_score = self._score_metric(bike_infrastructure, self.scoring_criteria['mobility']['bike_infrastructure'])

        # Calculate weighted average
        mobility_score = (walkability_score * 0.4 + transit_score * 0.4 + bike_score * 0.2) * 100

        return {
            'score': mobility_score,
            'grade': self._calculate_grade(mobility_score),
            'metrics': {
                'walkability': {'value': walkability, 'score': walkability_score * 100},
                'transit_access': {'value': transit_access, 'score': transit_score * 100},
                'bike_infrastructure': {'value': bike_infrastructure, 'score': bike_score * 100}
            }
        }

    def _calculate_land_use_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate land use sustainability score"""
        scenario = scenario_data['scenario']
        parcels = scenario_data['parcels']
        
        # Calculate density (people per hectare)
        total_population = sum(p.get('capacity', {}).get('population', 0) for p in parcels)
        total_area_ha = scenario['total_area'] / 10000  # Convert m² to hectares
        density = total_population / total_area_ha if total_area_ha > 0 else 0

        # Calculate mixed use ratio
        mixed_use_parcels = sum(1 for p in parcels if len(p.get('properties', {}).get('useMix', {})) > 1)
        mixed_use_ratio = mixed_use_parcels / len(parcels) if parcels else 0

        # Calculate green space ratio (simplified)
        green_space_ratio = 0.15  # Placeholder - would need actual green space data

        # Calculate subscores
        density_score = self._score_metric(density, self.scoring_criteria['land_use']['density'], reverse=True)
        mixed_use_score = self._score_metric(mixed_use_ratio, self.scoring_criteria['land_use']['mixed_use'])
        green_space_score = self._score_metric(green_space_ratio, self.scoring_criteria['land_use']['green_space'])

        # Calculate weighted average
        land_use_score = (density_score * 0.4 + mixed_use_score * 0.4 + green_space_score * 0.2) * 100

        return {
            'score': land_use_score,
            'grade': self._calculate_grade(land_use_score),
            'metrics': {
                'density': {'value': density, 'score': density_score * 100},
                'mixed_use': {'value': mixed_use_ratio, 'score': mixed_use_score * 100},
                'green_space': {'value': green_space_ratio, 'score': green_space_score * 100}
            }
        }

    def _calculate_water_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate water sustainability score"""
        # Placeholder values - would need actual water analysis data
        stormwater_management = 0.6
        water_efficiency = 0.7
        water_reuse = 0.3

        # Calculate subscores
        stormwater_score = self._score_metric(stormwater_management, self.scoring_criteria['water']['stormwater_management'])
        efficiency_score = self._score_metric(water_efficiency, self.scoring_criteria['water']['water_efficiency'])
        reuse_score = self._score_metric(water_reuse, self.scoring_criteria['water']['water_reuse'])

        # Calculate weighted average
        water_score = (stormwater_score * 0.4 + efficiency_score * 0.4 + reuse_score * 0.2) * 100

        return {
            'score': water_score,
            'grade': self._calculate_grade(water_score),
            'metrics': {
                'stormwater_management': {'value': stormwater_management, 'score': stormwater_score * 100},
                'water_efficiency': {'value': water_efficiency, 'score': efficiency_score * 100},
                'water_reuse': {'value': water_reuse, 'score': reuse_score * 100}
            }
        }

    def _calculate_materials_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate materials sustainability score"""
        # Placeholder values - would need actual materials analysis
        recycled_content = 0.5
        local_sourcing = 0.6
        embodied_carbon_reduction = 0.2

        # Calculate subscores
        recycled_score = self._score_metric(recycled_content, self.scoring_criteria['materials']['recycled_content'])
        local_score = self._score_metric(local_sourcing, self.scoring_criteria['materials']['local_sourcing'])
        carbon_score = self._score_metric(embodied_carbon_reduction, self.scoring_criteria['materials']['embodied_carbon'])

        # Calculate weighted average
        materials_score = (recycled_score * 0.4 + local_score * 0.4 + carbon_score * 0.2) * 100

        return {
            'score': materials_score,
            'grade': self._calculate_grade(materials_score),
            'metrics': {
                'recycled_content': {'value': recycled_content, 'score': recycled_score * 100},
                'local_sourcing': {'value': local_sourcing, 'score': local_score * 100},
                'embodied_carbon': {'value': embodied_carbon_reduction, 'score': carbon_score * 100}
            }
        }

    def _calculate_resilience_score(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate resilience sustainability score"""
        # Placeholder values - would need actual resilience analysis
        climate_adaptation = 0.6
        disaster_preparedness = 0.5
        social_equity = 0.7

        # Calculate subscores
        adaptation_score = self._score_metric(climate_adaptation, self.scoring_criteria['resilience']['climate_adaptation'])
        preparedness_score = self._score_metric(disaster_preparedness, self.scoring_criteria['resilience']['disaster_preparedness'])
        equity_score = self._score_metric(social_equity, self.scoring_criteria['resilience']['social_equity'])

        # Calculate weighted average
        resilience_score = (adaptation_score * 0.4 + preparedness_score * 0.3 + equity_score * 0.3) * 100

        return {
            'score': resilience_score,
            'grade': self._calculate_grade(resilience_score),
            'metrics': {
                'climate_adaptation': {'value': climate_adaptation, 'score': adaptation_score * 100},
                'disaster_preparedness': {'value': disaster_preparedness, 'score': preparedness_score * 100},
                'social_equity': {'value': social_equity, 'score': equity_score * 100}
            }
        }

    def _score_metric(self, value: float, criteria: Dict[str, float], reverse: bool = False) -> float:
        """Score a metric based on criteria thresholds"""
        if reverse:
            # For metrics where lower is better (like embodied carbon)
            if value <= criteria['excellent']:
                return 1.0
            elif value <= criteria['good']:
                return 0.8
            elif value <= criteria['fair']:
                return 0.6
            elif value <= criteria['poor']:
                return 0.4
            else:
                return 0.2
        else:
            # For metrics where higher is better
            if value >= criteria['excellent']:
                return 1.0
            elif value >= criteria['good']:
                return 0.8
            elif value >= criteria['fair']:
                return 0.6
            elif value >= criteria['poor']:
                return 0.4
            else:
                return 0.2

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D+'
        elif score >= 40:
            return 'D'
        else:
            return 'F'

    def _store_sustainability_score(self, scenario_id: str, score_data: Dict[str, Any]):
        """Store sustainability score results in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            # Update scenario with sustainability score data
            query = """
            UPDATE scenarios 
            SET kpis = jsonb_set(
                COALESCE(kpis, '{}'::jsonb),
                '{sustainability_score}',
                %s::jsonb
            ),
            updated_at = NOW()
            WHERE id = %s
            """
            cursor.execute(query, (json.dumps(score_data), scenario_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_sustainability_summary(self, scenario_id: str) -> Dict[str, Any]:
        """Get sustainability score summary for a scenario"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                query = """
                SELECT kpis->'sustainability_score' as sustainability_score
                FROM scenarios
                WHERE id = %s
                """
                cursor.execute(query, (scenario_id,))
                result = cursor.fetchone()
                
                if result and result['sustainability_score']:
                    return {
                        'success': True,
                        'data': result['sustainability_score']
                    }
                else:
                    return {'success': False, 'error': 'No sustainability score data found'}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Error getting sustainability summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
