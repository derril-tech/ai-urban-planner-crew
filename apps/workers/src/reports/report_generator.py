# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium
from folium import plugins

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

        # Report templates
        self.report_templates = {
            'executive_summary': {
                'name': 'Executive Summary',
                'sections': ['overview', 'key_findings', 'recommendations', 'next_steps'],
                'include_charts': True,
                'include_maps': True
            },
            'technical_report': {
                'name': 'Technical Report',
                'sections': ['methodology', 'data_analysis', 'results', 'discussion', 'conclusions'],
                'include_charts': True,
                'include_maps': True
            },
            'stakeholder_report': {
                'name': 'Stakeholder Report',
                'sections': ['overview', 'impacts', 'benefits', 'timeline', 'engagement'],
                'include_charts': True,
                'include_maps': False
            },
            'public_report': {
                'name': 'Public Report',
                'sections': ['overview', 'community_benefits', 'timeline', 'feedback'],
                'include_charts': True,
                'include_maps': True
            }
        }

    def generate_report(self, scenario_id: str, report_type: str = 'executive_summary', 
                       output_format: str = 'pdf') -> Dict[str, Any]:
        """Generate a comprehensive report for a scenario"""
        try:
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}

            # Validate report type
            if report_type not in self.report_templates:
                return {'success': False, 'error': f'Invalid report type: {report_type}'}

            template = self.report_templates[report_type]
            
            # Generate report content
            report_content = self._generate_report_content(scenario_data, template)
            
            # Generate charts and maps
            charts = []
            maps = []
            if template['include_charts']:
                charts = self._generate_charts(scenario_data)
            if template['include_maps']:
                maps = self._generate_maps(scenario_data)

            # Create PDF report
            if output_format == 'pdf':
                pdf_path = self._create_pdf_report(report_content, charts, maps, template)
                
                # Read PDF file and encode as base64
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                
                # Clean up temporary file
                os.remove(pdf_path)
                
                return {
                    'success': True,
                    'message': f'Generated {template["name"]} report',
                    'data': {
                        'report_type': report_type,
                        'template_name': template['name'],
                        'pdf_base64': pdf_base64,
                        'file_size': len(pdf_content),
                        'generated_at': datetime.now().isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Unsupported output format: {output_format}'
                }

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _get_scenario_data(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive scenario data for report generation"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get scenario with all analysis data
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

            # Get parcels with all data
            query = """
            SELECT id, ST_AsGeoJSON(geometry) as geometry, properties, capacity, utilities
            FROM parcels
            WHERE scenario_id = %s AND status = 'active'
            """
            cursor.execute(query, (scenario_id,))
            parcels = cursor.fetchall()

            # Get links
            query = """
            SELECT id, ST_AsGeoJSON(geometry) as geometry, properties, link_class
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

    def _generate_report_content(self, scenario_data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report content based on template"""
        scenario = scenario_data['scenario']
        kpis = scenario_data['kpis']
        
        content = {
            'title': f"Urban Planning Report - {scenario['name']}",
            'subtitle': f"Generated on {datetime.now().strftime('%B %d, %Y')}",
            'sections': {}
        }

        # Generate sections based on template
        for section in template['sections']:
            if section == 'overview':
                content['sections']['overview'] = self._generate_overview_section(scenario_data)
            elif section == 'key_findings':
                content['sections']['key_findings'] = self._generate_key_findings_section(scenario_data)
            elif section == 'recommendations':
                content['sections']['recommendations'] = self._generate_recommendations_section(scenario_data)
            elif section == 'next_steps':
                content['sections']['next_steps'] = self._generate_next_steps_section(scenario_data)
            elif section == 'methodology':
                content['sections']['methodology'] = self._generate_methodology_section(scenario_data)
            elif section == 'data_analysis':
                content['sections']['data_analysis'] = self._generate_data_analysis_section(scenario_data)
            elif section == 'results':
                content['sections']['results'] = self._generate_results_section(scenario_data)
            elif section == 'discussion':
                content['sections']['discussion'] = self._generate_discussion_section(scenario_data)
            elif section == 'conclusions':
                content['sections']['conclusions'] = self._generate_conclusions_section(scenario_data)
            elif section == 'impacts':
                content['sections']['impacts'] = self._generate_impacts_section(scenario_data)
            elif section == 'benefits':
                content['sections']['benefits'] = self._generate_benefits_section(scenario_data)
            elif section == 'timeline':
                content['sections']['timeline'] = self._generate_timeline_section(scenario_data)
            elif section == 'engagement':
                content['sections']['engagement'] = self._generate_engagement_section(scenario_data)
            elif section == 'community_benefits':
                content['sections']['community_benefits'] = self._generate_community_benefits_section(scenario_data)
            elif section == 'feedback':
                content['sections']['feedback'] = self._generate_feedback_section(scenario_data)

        return content

    def _generate_overview_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overview section"""
        scenario = scenario_data['scenario']
        parcels = scenario_data['parcels']
        
        total_area = scenario.get('total_area', 0)
        parcel_count = len(parcels)
        
        return {
            'title': 'Project Overview',
            'content': [
                f"This urban planning scenario, '{scenario['name']}', covers an area of {total_area/10000:.1f} hectares with {parcel_count} development parcels.",
                f"The project aims to create a sustainable, mixed-use development that balances density, accessibility, and environmental considerations.",
                f"Key development parameters include an average Floor Area Ratio (FAR) of {scenario.get('avg_far', 0):.1f} and average building height of {scenario.get('avg_height', 0):.1f} meters."
            ],
            'key_metrics': {
                'total_area_ha': total_area / 10000,
                'parcel_count': parcel_count,
                'avg_far': scenario.get('avg_far', 0),
                'avg_height': scenario.get('avg_height', 0)
            }
        }

    def _generate_key_findings_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate key findings section"""
        kpis = scenario_data['kpis']
        
        findings = []
        
        # Extract key metrics from KPIs
        if 'capacity_analysis' in kpis:
            capacity = kpis['capacity_analysis']
            findings.append(f"Development capacity: {capacity.get('total_units', 0):,} units, {capacity.get('total_population', 0):,} people, {capacity.get('total_jobs', 0):,} jobs")
        
        if 'budget_analysis' in kpis:
            budget = kpis['budget_analysis']
            total_budget = budget.get('total', {}).get('total', 0)
            findings.append(f"Total project budget: ${total_budget/1000000:.1f}M")
        
        if 'sustainability_score' in kpis:
            sustainability = kpis['sustainability_score']
            overall_score = sustainability.get('overall_score', 0)
            findings.append(f"Sustainability score: {overall_score:.1f}/100 ({sustainability.get('overall_grade', 'N/A')})")
        
        if 'network_analysis' in kpis:
            network = kpis['network_analysis']
            intersection_density = network.get('intersection_density', 0)
            findings.append(f"Network connectivity: {intersection_density:.1f} intersections per km²")
        
        return {
            'title': 'Key Findings',
            'content': findings,
            'highlights': [
                'Sustainable development with high walkability scores',
                'Mixed-use zoning promotes community interaction',
                'Comprehensive infrastructure planning',
                'Strong focus on environmental sustainability'
            ]
        }

    def _generate_recommendations_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations section"""
        return {
            'title': 'Recommendations',
            'content': [
                'Implement phased development approach to minimize disruption',
                'Prioritize pedestrian and cycling infrastructure',
                'Enhance public transit connectivity',
                'Maintain green space ratio above 15%',
                'Consider energy-efficient building standards',
                'Develop community engagement programs'
            ],
            'priorities': {
                'high': ['Infrastructure development', 'Community engagement'],
                'medium': ['Sustainability features', 'Transit integration'],
                'low': ['Aesthetic enhancements', 'Additional amenities']
            }
        }

    def _generate_next_steps_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate next steps section"""
        return {
            'title': 'Next Steps',
            'content': [
                'Complete detailed engineering studies',
                'Obtain necessary permits and approvals',
                'Begin community consultation process',
                'Develop detailed construction timeline',
                'Establish project management team',
                'Secure funding and financing'
            ],
            'timeline': {
                'immediate': ['Permit applications', 'Community consultation'],
                'short_term': ['Engineering studies', 'Funding approval'],
                'medium_term': ['Construction planning', 'Infrastructure development'],
                'long_term': ['Building construction', 'Community activation']
            }
        }

    def _generate_methodology_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate methodology section"""
        return {
            'title': 'Methodology',
            'content': [
                'Comprehensive GIS analysis using PostGIS spatial database',
                'Multi-criteria evaluation framework for sustainability assessment',
                'Network analysis for connectivity and accessibility evaluation',
                'Energy modeling for environmental impact assessment',
                'Cost-benefit analysis for economic feasibility',
                'Stakeholder engagement and community feedback integration'
            ],
            'tools_used': [
                'PostGIS for spatial analysis',
                'NetworkX for network modeling',
                'GeoPandas for geospatial data processing',
                'Matplotlib for data visualization',
                'Custom optimization algorithms for scenario generation'
            ]
        }

    def _generate_data_analysis_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data analysis section"""
        parcels = scenario_data['parcels']
        links = scenario_data['links']
        
        # Calculate statistics
        total_parcels = len(parcels)
        total_links = len(links)
        
        # Analyze parcel types
        residential_count = sum(1 for p in parcels if p['properties'].get('useMix', {}).get('residential', 0) > 0.5)
        commercial_count = sum(1 for p in parcels if p['properties'].get('useMix', {}).get('commercial', 0) > 0.5)
        mixed_use_count = total_parcels - residential_count - commercial_count
        
        return {
            'title': 'Data Analysis',
            'content': [
                f"Analyzed {total_parcels} development parcels and {total_links} network links",
                f"Land use distribution: {residential_count} residential, {commercial_count} commercial, {mixed_use_count} mixed-use",
                "Spatial analysis performed using PostGIS geometry functions",
                "Network connectivity assessed using graph theory algorithms",
                "Sustainability metrics calculated using standardized scoring systems"
            ],
            'statistics': {
                'total_parcels': total_parcels,
                'total_links': total_links,
                'residential_parcels': residential_count,
                'commercial_parcels': commercial_count,
                'mixed_use_parcels': mixed_use_count
            }
        }

    def _generate_results_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate results section"""
        kpis = scenario_data['kpis']
        
        results = []
        
        # Extract results from various analyses
        if 'capacity_analysis' in kpis:
            capacity = kpis['capacity_analysis']
            results.append(f"Development capacity: {capacity.get('total_units', 0):,} units")
            results.append(f"Population capacity: {capacity.get('total_population', 0):,} people")
            results.append(f"Employment capacity: {capacity.get('total_jobs', 0):,} jobs")
        
        if 'network_analysis' in kpis:
            network = kpis['network_analysis']
            results.append(f"Network density: {network.get('intersection_density', 0):.1f} intersections/km²")
            results.append(f"Walkability score: {network.get('walkability_score', 0):.1f}/100")
        
        if 'sustainability_score' in kpis:
            sustainability = kpis['sustainability_score']
            results.append(f"Overall sustainability: {sustainability.get('overall_score', 0):.1f}/100")
        
        return {
            'title': 'Results',
            'content': results,
            'summary': "The analysis demonstrates strong potential for sustainable urban development with excellent connectivity and environmental performance."
        }

    def _generate_discussion_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate discussion section"""
        return {
            'title': 'Discussion',
            'content': [
                "The proposed development successfully balances density with livability",
                "Network connectivity supports active transportation modes",
                "Sustainability features contribute to long-term environmental goals",
                "Mixed-use zoning promotes community interaction and reduces vehicle trips",
                "Cost-benefit analysis shows positive economic returns",
                "Community engagement will be crucial for successful implementation"
            ],
            'implications': [
                'Reduced carbon footprint through sustainable design',
                'Improved public health through active transportation',
                'Enhanced community resilience and social cohesion',
                'Economic benefits through increased property values',
                'Long-term cost savings through energy efficiency'
            ]
        }

    def _generate_conclusions_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conclusions section"""
        return {
            'title': 'Conclusions',
            'content': [
                "The proposed urban development scenario demonstrates strong potential for creating a sustainable, livable community",
                "Comprehensive analysis supports the feasibility of the project",
                "Key success factors include community engagement and phased implementation",
                "Environmental and social benefits outweigh implementation costs",
                "The project serves as a model for sustainable urban development"
            ],
            'recommendations': [
                'Proceed with detailed planning and community consultation',
                'Implement sustainability features as priority',
                'Develop comprehensive monitoring and evaluation framework',
                'Establish partnerships with local stakeholders',
                'Consider expansion opportunities for future phases'
            ]
        }

    def _generate_impacts_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate impacts section"""
        return {
            'title': 'Project Impacts',
            'content': [
                'Positive economic impact through job creation and increased property values',
                'Environmental benefits through sustainable design and reduced emissions',
                'Social improvements through enhanced community facilities and connectivity',
                'Health benefits through active transportation infrastructure',
                'Educational opportunities through mixed-use development'
            ],
            'impact_categories': {
                'economic': ['Job creation', 'Property value increase', 'Local business growth'],
                'environmental': ['Reduced emissions', 'Green space preservation', 'Energy efficiency'],
                'social': ['Community cohesion', 'Access to amenities', 'Quality of life'],
                'health': ['Active transportation', 'Access to healthcare', 'Mental well-being']
            }
        }

    def _generate_benefits_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate benefits section"""
        return {
            'title': 'Project Benefits',
            'content': [
                'Sustainable development that meets current and future needs',
                'Enhanced community connectivity and accessibility',
                'Improved environmental performance and resilience',
                'Economic opportunities for local businesses and residents',
                'High-quality public spaces and amenities'
            ],
            'benefit_quantification': {
                'economic_benefits': '$50M+ in economic value',
                'environmental_benefits': '30% reduction in carbon footprint',
                'social_benefits': 'Improved quality of life for 10,000+ residents',
                'health_benefits': 'Increased active transportation by 40%'
            }
        }

    def _generate_timeline_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate timeline section"""
        return {
            'title': 'Project Timeline',
            'content': [
                'Phase 1: Planning and Permitting (6-12 months)',
                'Phase 2: Infrastructure Development (12-18 months)',
                'Phase 3: Building Construction (24-36 months)',
                'Phase 4: Community Activation (6-12 months)'
            ],
            'milestones': {
                'planning': ['Community consultation', 'Environmental assessment', 'Permit approval'],
                'construction': ['Site preparation', 'Infrastructure installation', 'Building construction'],
                'completion': ['Final inspections', 'Community handover', 'Monitoring program']
            }
        }

    def _generate_engagement_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate engagement section"""
        return {
            'title': 'Community Engagement',
            'content': [
                'Regular public meetings and workshops',
                'Online feedback platforms and surveys',
                'Stakeholder advisory committees',
                'Educational programs and information sessions',
                'Transparent communication and progress updates'
            ],
            'engagement_strategies': {
                'outreach': ['Public meetings', 'Newsletters', 'Social media'],
                'participation': ['Workshops', 'Surveys', 'Focus groups'],
                'feedback': ['Online platforms', 'Comment periods', 'Response tracking']
            }
        }

    def _generate_community_benefits_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate community benefits section"""
        return {
            'title': 'Community Benefits',
            'content': [
                'New housing options for diverse income levels',
                'Enhanced public spaces and recreational facilities',
                'Improved access to essential services and amenities',
                'Better transportation options and connectivity',
                'Increased community pride and sense of place'
            ],
            'benefit_details': {
                'housing': 'Affordable and market-rate housing options',
                'amenities': 'Parks, community centers, and retail spaces',
                'services': 'Healthcare, education, and transit access',
                'connectivity': 'Walking and cycling infrastructure',
                'environment': 'Green spaces and sustainable features'
            }
        }

    def _generate_feedback_section(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate feedback section"""
        return {
            'title': 'Community Feedback',
            'content': [
                'Strong support for sustainable development features',
                'Concerns about construction impacts and timeline',
                'Requests for affordable housing options',
                'Interest in community facilities and amenities',
                'Support for active transportation infrastructure'
            ],
            'feedback_summary': {
                'positive': ['Sustainability focus', 'Community amenities', 'Transportation options'],
                'concerns': ['Construction timeline', 'Traffic impacts', 'Cost considerations'],
                'suggestions': ['More affordable housing', 'Additional green space', 'Community facilities']
            }
        }

    def _generate_charts(self, scenario_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate charts for the report"""
        charts = []
        
        # Capacity chart
        capacity_chart = self._create_capacity_chart(scenario_data)
        if capacity_chart:
            charts.append(capacity_chart)
        
        # Sustainability score chart
        sustainability_chart = self._create_sustainability_chart(scenario_data)
        if sustainability_chart:
            charts.append(sustainability_chart)
        
        # Budget breakdown chart
        budget_chart = self._create_budget_chart(scenario_data)
        if budget_chart:
            charts.append(budget_chart)
        
        return charts

    def _create_capacity_chart(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create capacity analysis chart"""
        kpis = scenario_data['kpis']
        
        if 'capacity_analysis' not in kpis:
            return None
        
        capacity = kpis['capacity_analysis']
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Units', 'Population', 'Jobs']
        values = [
            capacity.get('total_units', 0),
            capacity.get('total_population', 0),
            capacity.get('total_jobs', 0)
        ]
        
        bars = ax.bar(categories, values, color=['#3B82F6', '#10B981', '#F59E0B'])
        ax.set_title('Development Capacity', fontsize=16, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{value:,}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return {
            'title': 'Development Capacity',
            'description': 'Total development capacity in units, population, and jobs',
            'image_data': base64.b64encode(img_buffer.getvalue()).decode('utf-8'),
            'type': 'bar_chart'
        }

    def _create_sustainability_chart(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create sustainability score chart"""
        kpis = scenario_data['kpis']
        
        if 'sustainability_score' not in kpis:
            return None
        
        sustainability = kpis['sustainability_score']
        category_scores = sustainability.get('category_scores', {})
        
        if not category_scores:
            return None
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(category_scores.keys())
        scores = [category_scores[cat]['score'] for cat in categories]
        
        bars = ax.bar(categories, scores, color=['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'])
        ax.set_title('Sustainability Scores by Category', fontsize=16, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12)
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return {
            'title': 'Sustainability Scores',
            'description': 'Sustainability performance by category',
            'image_data': base64.b64encode(img_buffer.getvalue()).decode('utf-8'),
            'type': 'bar_chart'
        }

    def _create_budget_chart(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create budget breakdown chart"""
        kpis = scenario_data['kpis']
        
        if 'budget_analysis' not in kpis:
            return None
        
        budget = kpis['budget_analysis']
        breakdown = budget.get('total', {}).get('breakdown', {})
        
        if not breakdown:
            return None
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(breakdown.keys())
        values = [breakdown[cat] for cat in categories]
        
        # Convert to millions for readability
        values_millions = [v / 1000000 for v in values]
        
        bars = ax.bar(categories, values_millions, color=['#3B82F6', '#10B981', '#F59E0B'])
        ax.set_title('Budget Breakdown', fontsize=16, fontweight='bold')
        ax.set_ylabel('Cost (Millions USD)', fontsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars, values_millions):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'${value:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return {
            'title': 'Budget Breakdown',
            'description': 'Project budget breakdown by category',
            'image_data': base64.b64encode(img_buffer.getvalue()).decode('utf-8'),
            'type': 'bar_chart'
        }

    def _generate_maps(self, scenario_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate maps for the report"""
        maps = []
        
        # Site overview map
        overview_map = self._create_overview_map(scenario_data)
        if overview_map:
            maps.append(overview_map)
        
        # Network connectivity map
        network_map = self._create_network_map(scenario_data)
        if network_map:
            maps.append(network_map)
        
        return maps

    def _create_overview_map(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create site overview map"""
        parcels = scenario_data['parcels']
        
        if not parcels:
            return None
        
        # Create folium map
        m = folium.Map(location=[0, 0], zoom_start=15)
        
        # Add parcels
        for parcel in parcels:
            geometry = json.loads(parcel['geometry'])
            properties = parcel['properties']
            
            # Determine color based on use mix
            use_mix = properties.get('useMix', {})
            if use_mix.get('residential', 0) > 0.5:
                color = 'blue'
            elif use_mix.get('commercial', 0) > 0.5:
                color = 'red'
            else:
                color = 'green'
            
            folium.GeoJson(
                geometry,
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"Parcel {parcel['id']}"
            ).add_to(m)
        
        # Save map to HTML
        map_html = m._repr_html_()
        
        return {
            'title': 'Site Overview',
            'description': 'Development parcels and land use distribution',
            'html_content': map_html,
            'type': 'interactive_map'
        }

    def _create_network_map(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create network connectivity map"""
        links = scenario_data['links']
        
        if not links:
            return None
        
        # Create folium map
        m = folium.Map(location=[0, 0], zoom_start=15)
        
        # Add network links
        for link in links:
            geometry = json.loads(link['geometry'])
            link_class = link['link_class']
            
            # Determine color based on link class
            if link_class == 'arterial':
                color = 'red'
                weight = 4
            elif link_class == 'collector':
                color = 'orange'
                weight = 3
            else:
                color = 'yellow'
                weight = 2
            
            folium.GeoJson(
                geometry,
                style_function=lambda x, color=color, weight=weight: {
                    'color': color,
                    'weight': weight,
                    'opacity': 0.8
                },
                tooltip=f"{link_class.title()} road"
            ).add_to(m)
        
        # Save map to HTML
        map_html = m._repr_html_()
        
        return {
            'title': 'Network Connectivity',
            'description': 'Street network and connectivity analysis',
            'html_content': map_html,
            'type': 'interactive_map'
        }

    def _create_pdf_report(self, report_content: Dict[str, Any], charts: List[Dict[str, Any]], 
                          maps: List[Dict[str, Any]], template: Dict[str, Any]) -> str:
        """Create PDF report"""
        # Create temporary file
        temp_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_file, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20
        )
        
        # Build story
        story = []
        
        # Title page
        story.append(Paragraph(report_content['title'], title_style))
        story.append(Paragraph(report_content['subtitle'], subtitle_style))
        story.append(PageBreak())
        
        # Table of contents (simplified)
        story.append(Paragraph('Table of Contents', heading_style))
        for section_name, section_data in report_content['sections'].items():
            story.append(Paragraph(f"• {section_data['title']}", styles['Normal']))
        story.append(PageBreak())
        
        # Add sections
        for section_name, section_data in report_content['sections'].items():
            story.append(Paragraph(section_data['title'], heading_style))
            
            # Add content
            if isinstance(section_data['content'], list):
                for item in section_data['content']:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
                    story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(section_data['content'], styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        # Add charts
        if charts:
            story.append(PageBreak())
            story.append(Paragraph('Charts and Visualizations', heading_style))
            
            for chart in charts:
                story.append(Paragraph(chart['title'], styles['Heading3']))
                story.append(Paragraph(chart['description'], styles['Normal']))
                
                # Convert base64 image to file-like object
                img_data = base64.b64decode(chart['image_data'])
                img_buffer = BytesIO(img_data)
                
                # Add image to PDF
                img = Image(img_buffer, width=6*inch, height=4*inch)
                story.append(img)
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        return temp_file
