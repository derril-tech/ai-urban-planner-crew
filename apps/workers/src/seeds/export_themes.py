# Created automatically by Cursor AI (2025-08-25)

import json
from typing import Dict, Any, List
from datetime import datetime

class ExportThemes:
    def __init__(self):
        self.themes = {
            'professional': self._create_professional_theme(),
            'executive': self._create_executive_theme(),
            'technical': self._create_technical_theme(),
            'public': self._create_public_theme(),
            'stakeholder': self._create_stakeholder_theme(),
            'academic': self._create_academic_theme(),
            'creative': self._create_creative_theme(),
            'minimal': self._create_minimal_theme()
        }
        
        self.sample_bundles = self._create_sample_bundles()
        self.layout_templates = self._create_layout_templates()

    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get a specific theme by name"""
        return self.themes.get(theme_name, {})

    def get_all_themes(self) -> Dict[str, Any]:
        """Get all available themes"""
        return self.themes

    def get_sample_bundle(self, bundle_name: str) -> Dict[str, Any]:
        """Get a specific sample bundle by name"""
        return self.sample_bundles.get(bundle_name, {})

    def get_all_sample_bundles(self) -> Dict[str, Any]:
        """Get all available sample bundles"""
        return self.sample_bundles

    def customize_theme(self, base_theme: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Create a customized theme based on a base theme"""
        base = self.get_theme(base_theme)
        if not base:
            return {}
        
        customized = base.copy()
        customized.update(customizations)
        customized['customized_from'] = base_theme
        customized['customization_date'] = datetime.now().isoformat()
        
        return customized

    def generate_export_config(self, theme_name: str, bundle_name: str = None) -> Dict[str, Any]:
        """Generate export configuration combining theme and bundle"""
        theme = self.get_theme(theme_name)
        bundle = self.get_sample_bundle(bundle_name) if bundle_name else {}
        
        config = {
            'theme': theme,
            'bundle': bundle,
            'export_settings': {
                'format': 'pdf',
                'quality': 'high',
                'include_metadata': True,
                'include_charts': True,
                'include_maps': True,
                'page_size': 'A4',
                'orientation': 'portrait'
            },
            'generated_at': datetime.now().isoformat()
        }
        
        return config

    def _create_professional_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Professional',
            'description': 'Clean, corporate-style theme suitable for business presentations',
            'colors': {
                'primary': '#2C3E50',
                'secondary': '#3498DB',
                'accent': '#E74C3C',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#7F8C8D',
                'border': '#BDC3C7',
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Arial, sans-serif',
                'heading_font': 'Georgia, serif',
                'font_size_base': '12pt',
                'font_size_heading1': '24pt',
                'font_size_heading2': '18pt',
                'font_size_heading3': '14pt',
                'line_height': 1.5,
                'font_weight_normal': 400,
                'font_weight_bold': 700
            },
            'layout': {
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
                'header_height': 60,
                'footer_height': 40,
                'section_spacing': 15,
                'paragraph_spacing': 8,
                'column_gap': 10
            },
            'elements': {
                'header_style': 'corporate',
                'footer_style': 'minimal',
                'chart_style': 'clean',
                'table_style': 'professional',
                'map_style': 'neutral',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_right',
                'logo_size': {'width': 120, 'height': 40},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Sustainable Development Solutions'
            }
        }

    def _create_executive_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Executive',
            'description': 'High-end theme for executive presentations and board reports',
            'colors': {
                'primary': '#1A1A1A',
                'secondary': '#4A90E2',
                'accent': '#D4AF37',
                'background': '#FFFFFF',
                'text': '#1A1A1A',
                'text_secondary': '#666666',
                'border': '#E0E0E0',
                'success': '#2ECC71',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Helvetica, Arial, sans-serif',
                'heading_font': 'Times New Roman, serif',
                'font_size_base': '11pt',
                'font_size_heading1': '28pt',
                'font_size_heading2': '20pt',
                'font_size_heading3': '16pt',
                'line_height': 1.4,
                'font_weight_normal': 400,
                'font_weight_bold': 600
            },
            'layout': {
                'margins': {'top': 25, 'right': 25, 'bottom': 25, 'left': 25},
                'header_height': 80,
                'footer_height': 50,
                'section_spacing': 20,
                'paragraph_spacing': 10,
                'column_gap': 15
            },
            'elements': {
                'header_style': 'elegant',
                'footer_style': 'executive',
                'chart_style': 'sophisticated',
                'table_style': 'executive',
                'map_style': 'premium',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_center',
                'logo_size': {'width': 150, 'height': 50},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Excellence in Urban Development'
            }
        }

    def _create_technical_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Technical',
            'description': 'Detailed technical theme for engineering and planning documents',
            'colors': {
                'primary': '#34495E',
                'secondary': '#2980B9',
                'accent': '#E67E22',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#5D6D7E',
                'border': '#AEB6BF',
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Courier New, monospace',
                'heading_font': 'Arial, sans-serif',
                'font_size_base': '10pt',
                'font_size_heading1': '22pt',
                'font_size_heading2': '16pt',
                'font_size_heading3': '12pt',
                'line_height': 1.6,
                'font_weight_normal': 400,
                'font_weight_bold': 700
            },
            'layout': {
                'margins': {'top': 15, 'right': 15, 'bottom': 15, 'left': 15},
                'header_height': 50,
                'footer_height': 30,
                'section_spacing': 12,
                'paragraph_spacing': 6,
                'column_gap': 8
            },
            'elements': {
                'header_style': 'technical',
                'footer_style': 'data_rich',
                'chart_style': 'detailed',
                'table_style': 'technical',
                'map_style': 'analytical',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_left',
                'logo_size': {'width': 100, 'height': 30},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Technical Excellence in Planning'
            }
        }

    def _create_public_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Public',
            'description': 'Accessible theme for public engagement and community presentations',
            'colors': {
                'primary': '#2ECC71',
                'secondary': '#3498DB',
                'accent': '#F39C12',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#7F8C8D',
                'border': '#BDC3C7',
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Verdana, Arial, sans-serif',
                'heading_font': 'Arial, sans-serif',
                'font_size_base': '14pt',
                'font_size_heading1': '26pt',
                'font_size_heading2': '20pt',
                'font_size_heading3': '16pt',
                'line_height': 1.8,
                'font_weight_normal': 400,
                'font_weight_bold': 600
            },
            'layout': {
                'margins': {'top': 30, 'right': 30, 'bottom': 30, 'left': 30},
                'header_height': 100,
                'footer_height': 60,
                'section_spacing': 25,
                'paragraph_spacing': 12,
                'column_gap': 20
            },
            'elements': {
                'header_style': 'friendly',
                'footer_style': 'informative',
                'chart_style': 'simple',
                'table_style': 'clear',
                'map_style': 'accessible',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_center',
                'logo_size': {'width': 180, 'height': 60},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Building Better Communities Together'
            }
        }

    def _create_stakeholder_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Stakeholder',
            'description': 'Balanced theme for stakeholder presentations and partnership reports',
            'colors': {
                'primary': '#8E44AD',
                'secondary': '#3498DB',
                'accent': '#E67E22',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#7F8C8D',
                'border': '#BDC3C7',
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Calibri, Arial, sans-serif',
                'heading_font': 'Cambria, Georgia, serif',
                'font_size_base': '12pt',
                'font_size_heading1': '24pt',
                'font_size_heading2': '18pt',
                'font_size_heading3': '14pt',
                'line_height': 1.6,
                'font_weight_normal': 400,
                'font_weight_bold': 600
            },
            'layout': {
                'margins': {'top': 25, 'right': 25, 'bottom': 25, 'left': 25},
                'header_height': 70,
                'footer_height': 45,
                'section_spacing': 18,
                'paragraph_spacing': 10,
                'column_gap': 12
            },
            'elements': {
                'header_style': 'collaborative',
                'footer_style': 'partnership',
                'chart_style': 'balanced',
                'table_style': 'stakeholder',
                'map_style': 'collaborative',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_right',
                'logo_size': {'width': 130, 'height': 45},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Collaborative Planning Solutions'
            }
        }

    def _create_academic_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Academic',
            'description': 'Scholarly theme for research papers and academic presentations',
            'colors': {
                'primary': '#2C3E50',
                'secondary': '#34495E',
                'accent': '#E74C3C',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#5D6D7E',
                'border': '#AEB6BF',
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Times New Roman, serif',
                'heading_font': 'Times New Roman, serif',
                'font_size_base': '12pt',
                'font_size_heading1': '18pt',
                'font_size_heading2': '14pt',
                'font_size_heading3': '12pt',
                'line_height': 2.0,
                'font_weight_normal': 400,
                'font_weight_bold': 700
            },
            'layout': {
                'margins': {'top': 25, 'right': 25, 'bottom': 25, 'left': 25},
                'header_height': 60,
                'footer_height': 40,
                'section_spacing': 20,
                'paragraph_spacing': 12,
                'column_gap': 15
            },
            'elements': {
                'header_style': 'academic',
                'footer_style': 'scholarly',
                'chart_style': 'research',
                'table_style': 'academic',
                'map_style': 'analytical',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_left',
                'logo_size': {'width': 120, 'height': 40},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Research-Driven Planning'
            }
        }

    def _create_creative_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Creative',
            'description': 'Innovative theme for creative presentations and design proposals',
            'colors': {
                'primary': '#9B59B6',
                'secondary': '#3498DB',
                'accent': '#F1C40F',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'text_secondary': '#7F8C8D',
                'border': '#BDC3C7',
                'success': '#2ECC71',
                'warning': '#F39C12',
                'error': '#E74C3C'
            },
            'typography': {
                'font_family': 'Segoe UI, Arial, sans-serif',
                'heading_font': 'Segoe UI, Arial, sans-serif',
                'font_size_base': '12pt',
                'font_size_heading1': '32pt',
                'font_size_heading2': '24pt',
                'font_size_heading3': '18pt',
                'line_height': 1.4,
                'font_weight_normal': 400,
                'font_weight_bold': 600
            },
            'layout': {
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
                'header_height': 90,
                'footer_height': 50,
                'section_spacing': 25,
                'paragraph_spacing': 10,
                'column_gap': 15
            },
            'elements': {
                'header_style': 'creative',
                'footer_style': 'innovative',
                'chart_style': 'dynamic',
                'table_style': 'modern',
                'map_style': 'creative',
                'page_numbers': True,
                'table_of_contents': True
            },
            'branding': {
                'logo_position': 'header_center',
                'logo_size': {'width': 160, 'height': 55},
                'company_name': 'Urban Planning Studio',
                'tagline': 'Innovative Urban Solutions'
            }
        }

    def _create_minimal_theme(self) -> Dict[str, Any]:
        return {
            'name': 'Minimal',
            'description': 'Clean, minimal theme focusing on content over decoration',
            'colors': {
                'primary': '#000000',
                'secondary': '#666666',
                'accent': '#333333',
                'background': '#FFFFFF',
                'text': '#000000',
                'text_secondary': '#666666',
                'border': '#CCCCCC',
                'success': '#000000',
                'warning': '#666666',
                'error': '#000000'
            },
            'typography': {
                'font_family': 'Arial, sans-serif',
                'heading_font': 'Arial, sans-serif',
                'font_size_base': '11pt',
                'font_size_heading1': '20pt',
                'font_size_heading2': '16pt',
                'font_size_heading3': '12pt',
                'line_height': 1.5,
                'font_weight_normal': 400,
                'font_weight_bold': 600
            },
            'layout': {
                'margins': {'top': 30, 'right': 30, 'bottom': 30, 'left': 30},
                'header_height': 40,
                'footer_height': 30,
                'section_spacing': 20,
                'paragraph_spacing': 8,
                'column_gap': 20
            },
            'elements': {
                'header_style': 'minimal',
                'footer_style': 'minimal',
                'chart_style': 'clean',
                'table_style': 'simple',
                'map_style': 'minimal',
                'page_numbers': True,
                'table_of_contents': False
            },
            'branding': {
                'logo_position': 'header_left',
                'logo_size': {'width': 80, 'height': 25},
                'company_name': 'Urban Planning Studio',
                'tagline': ''
            }
        }

    def _create_sample_bundles(self) -> Dict[str, Any]:
        return {
            'executive_summary': {
                'name': 'Executive Summary Bundle',
                'description': 'Comprehensive executive summary with key findings and recommendations',
                'sections': [
                    'executive_summary',
                    'key_findings',
                    'financial_summary',
                    'sustainability_metrics',
                    'recommendations',
                    'next_steps'
                ],
                'charts': [
                    'financial_overview',
                    'sustainability_score',
                    'capacity_summary',
                    'timeline'
                ],
                'maps': [
                    'site_overview',
                    'development_plan'
                ],
                'tables': [
                    'key_metrics',
                    'cost_breakdown',
                    'sustainability_breakdown'
                ],
                'appendix': [
                    'detailed_methodology',
                    'supporting_data',
                    'references'
                ]
            },
            'technical_report': {
                'name': 'Technical Report Bundle',
                'description': 'Detailed technical report with comprehensive analysis',
                'sections': [
                    'executive_summary',
                    'introduction',
                    'methodology',
                    'site_analysis',
                    'capacity_analysis',
                    'energy_analysis',
                    'budget_analysis',
                    'sustainability_analysis',
                    'network_analysis',
                    'optimization_results',
                    'conclusions',
                    'recommendations'
                ],
                'charts': [
                    'capacity_breakdown',
                    'energy_analysis',
                    'budget_waterfall',
                    'sustainability_scores',
                    'network_metrics',
                    'optimization_pareto',
                    'sensitivity_analysis'
                ],
                'maps': [
                    'site_boundary',
                    'parcel_layout',
                    'network_connectivity',
                    'energy_infrastructure',
                    'sustainability_features'
                ],
                'tables': [
                    'parcel_inventory',
                    'capacity_calculations',
                    'energy_calculations',
                    'budget_details',
                    'sustainability_metrics',
                    'network_statistics'
                ],
                'appendix': [
                    'detailed_calculations',
                    'data_sources',
                    'methodology_details',
                    'references'
                ]
            },
            'stakeholder_presentation': {
                'name': 'Stakeholder Presentation Bundle',
                'description': 'Engaging presentation for stakeholder meetings and public engagement',
                'sections': [
                    'project_overview',
                    'community_benefits',
                    'development_concept',
                    'sustainability_features',
                    'economic_impact',
                    'community_engagement',
                    'next_steps'
                ],
                'charts': [
                    'community_benefits',
                    'sustainability_highlights',
                    'economic_impact',
                    'timeline'
                ],
                'maps': [
                    'site_location',
                    'development_concept',
                    'community_amenities'
                ],
                'tables': [
                    'key_benefits',
                    'sustainability_features',
                    'community_engagement_plan'
                ],
                'appendix': [
                    'detailed_benefits',
                    'engagement_summary',
                    'contact_information'
                ]
            },
            'public_engagement': {
                'name': 'Public Engagement Bundle',
                'description': 'Accessible materials for public meetings and community feedback',
                'sections': [
                    'project_introduction',
                    'what_we_heard',
                    'proposed_plan',
                    'community_benefits',
                    'how_to_get_involved',
                    'contact_information'
                ],
                'charts': [
                    'community_feedback',
                    'benefits_summary',
                    'timeline'
                ],
                'maps': [
                    'project_area',
                    'proposed_development',
                    'nearby_amenities'
                ],
                'tables': [
                    'community_benefits',
                    'engagement_opportunities',
                    'contact_list'
                ],
                'appendix': [
                    'feedback_summary',
                    'technical_details',
                    'frequently_asked_questions'
                ]
            },
            'academic_paper': {
                'name': 'Academic Paper Bundle',
                'description': 'Scholarly format for research papers and academic publications',
                'sections': [
                    'abstract',
                    'introduction',
                    'literature_review',
                    'methodology',
                    'results',
                    'discussion',
                    'conclusions',
                    'references'
                ],
                'charts': [
                    'research_findings',
                    'statistical_analysis',
                    'comparison_studies'
                ],
                'maps': [
                    'study_area',
                    'analysis_results',
                    'spatial_distribution'
                ],
                'tables': [
                    'data_summary',
                    'statistical_results',
                    'comparison_analysis'
                ],
                'appendix': [
                    'detailed_methodology',
                    'raw_data',
                    'statistical_tests',
                    'additional_analysis'
                ]
            },
            'development_proposal': {
                'name': 'Development Proposal Bundle',
                'description': 'Comprehensive development proposal for investors and partners',
                'sections': [
                    'executive_summary',
                    'market_analysis',
                    'development_concept',
                    'financial_projection',
                    'sustainability_strategy',
                    'risk_assessment',
                    'implementation_plan',
                    'investment_opportunity'
                ],
                'charts': [
                    'market_analysis',
                    'financial_projection',
                    'sustainability_benefits',
                    'risk_assessment',
                    'return_on_investment'
                ],
                'maps': [
                    'market_area',
                    'development_concept',
                    'competitive_analysis'
                ],
                'tables': [
                    'financial_summary',
                    'market_data',
                    'sustainability_metrics',
                    'risk_matrix'
                ],
                'appendix': [
                    'detailed_financials',
                    'market_research',
                    'technical_specifications',
                    'legal_considerations'
                ]
            }
        }

    def _create_layout_templates(self) -> Dict[str, Any]:
        return {
            'single_column': {
                'name': 'Single Column',
                'description': 'Traditional single-column layout',
                'columns': 1,
                'column_widths': [1.0],
                'column_gaps': [0],
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20}
            },
            'two_column': {
                'name': 'Two Column',
                'description': 'Two-column layout for better space utilization',
                'columns': 2,
                'column_widths': [0.6, 0.4],
                'column_gaps': [15],
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20}
            },
            'three_column': {
                'name': 'Three Column',
                'description': 'Three-column layout for detailed comparisons',
                'columns': 3,
                'column_widths': [0.4, 0.3, 0.3],
                'column_gaps': [10, 10],
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20}
            },
            'sidebar': {
                'name': 'Sidebar Layout',
                'description': 'Main content with sidebar for navigation or highlights',
                'columns': 2,
                'column_widths': [0.7, 0.3],
                'column_gaps': [20],
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20}
            },
            'full_width': {
                'name': 'Full Width',
                'description': 'Full-width layout for maximum content space',
                'columns': 1,
                'column_widths': [1.0],
                'column_gaps': [0],
                'margins': {'top': 15, 'right': 15, 'bottom': 15, 'left': 15}
            }
        }

    def export_theme_data(self, format: str = 'json') -> str:
        """Export theme data in specified format"""
        if format == 'json':
            return json.dumps({
                'themes': self.themes,
                'sample_bundles': self.sample_bundles,
                'layout_templates': self.layout_templates
            }, indent=2)
        elif format == 'css':
            # Generate CSS for themes
            css_output = []
            for theme_name, theme in self.themes.items():
                css_output.append(f"/* {theme['name']} Theme */")
                css_output.append(f".theme-{theme_name} {{")
                css_output.append(f"  --primary-color: {theme['colors']['primary']};")
                css_output.append(f"  --secondary-color: {theme['colors']['secondary']};")
                css_output.append(f"  --accent-color: {theme['colors']['accent']};")
                css_output.append(f"  --background-color: {theme['colors']['background']};")
                css_output.append(f"  --text-color: {theme['colors']['text']};")
                css_output.append(f"  --text-secondary-color: {theme['colors']['text_secondary']};")
                css_output.append(f"  --border-color: {theme['colors']['border']};")
                css_output.append(f"  font-family: {theme['typography']['font_family']};")
                css_output.append(f"  font-size: {theme['typography']['font_size_base']};")
                css_output.append(f"  line-height: {theme['typography']['line_height']};")
                css_output.append("}")
                css_output.append("")
            return "\n".join(css_output)
        else:
            return json.dumps({
                'themes': self.themes,
                'sample_bundles': self.sample_bundles,
                'layout_templates': self.layout_templates
            }, indent=2)
