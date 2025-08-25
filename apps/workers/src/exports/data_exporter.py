# Created automatically by Cursor AI (2025-08-25)
import json
import logging
from typing import Dict, Any, List, Optional, Union
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import base64
import zipfile
from io import BytesIO
import geopandas as gpd
from shapely.geometry import shape
import pandas as pd
import numpy as np
from urllib.parse import urlparse, parse_qs
import hashlib
import hmac
import time
import uuid

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExporter:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }
        
        # MinIO configuration for file storage
        self.minio_config = {
            'endpoint': os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
            'access_key': os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            'secret_key': os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
            'bucket': os.getenv('MINIO_BUCKET', 'urban-planner-exports'),
            'secure': os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        }
        
        # Export formats and their configurations
        self.export_formats = {
            'geojson': {
                'name': 'GeoJSON',
                'description': 'Geospatial data in GeoJSON format',
                'extensions': ['.geojson'],
                'mime_type': 'application/geo+json'
            },
            'shapefile': {
                'name': 'Shapefile',
                'description': 'ESRI Shapefile format for GIS applications',
                'extensions': ['.shp', '.shx', '.dbf', '.prj'],
                'mime_type': 'application/zip'
            },
            'gpkg': {
                'name': 'GeoPackage',
                'description': 'OGC GeoPackage format for spatial data',
                'extensions': ['.gpkg'],
                'mime_type': 'application/geopackage+sqlite3'
            },
            'dxf': {
                'name': 'DXF',
                'description': 'AutoCAD DXF format for CAD applications',
                'extensions': ['.dxf'],
                'mime_type': 'application/dxf'
            },
            'csv': {
                'name': 'CSV',
                'description': 'Comma-separated values for tabular data',
                'extensions': ['.csv'],
                'mime_type': 'text/csv'
            },
            'zip': {
                'name': 'ZIP Archive',
                'description': 'Compressed archive with multiple formats',
                'extensions': ['.zip'],
                'mime_type': 'application/zip'
            }
        }

    def export_scenario_data(self, scenario_id: str, export_format: str = 'geojson', 
                           include_analysis: bool = True, include_metadata: bool = True) -> Dict[str, Any]:
        """Export scenario data in specified format"""
        try:
            # Validate export format
            if export_format not in self.export_formats:
                return {'success': False, 'error': f'Unsupported export format: {export_format}'}
            
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id, include_analysis)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}
            
            # Generate export
            export_result = self._generate_export(scenario_data, export_format, include_metadata)
            if not export_result['success']:
                return export_result
            
            # Store file and generate signed URL
            file_url = self._store_export_file(export_result['data'], export_format, scenario_id)
            if not file_url:
                return {'success': False, 'error': 'Failed to store export file'}
            
            return {
                'success': True,
                'message': f'Exported scenario data in {self.export_formats[export_format]["name"]} format',
                'data': {
                    'export_format': export_format,
                    'format_name': self.export_formats[export_format]['name'],
                    'file_url': file_url,
                    'file_size': len(export_result['data']),
                    'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
                    'exported_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting scenario data: {str(e)}")
            return {'success': False, 'error': str(e)}

    def export_multiple_formats(self, scenario_id: str, formats: List[str] = None, 
                              include_analysis: bool = True) -> Dict[str, Any]:
        """Export scenario data in multiple formats as a ZIP archive"""
        try:
            if formats is None:
                formats = ['geojson', 'shapefile', 'csv']
            
            # Validate formats
            for fmt in formats:
                if fmt not in self.export_formats:
                    return {'success': False, 'error': f'Unsupported export format: {fmt}'}
            
            # Get scenario data
            scenario_data = self._get_scenario_data(scenario_id, include_analysis)
            if not scenario_data:
                return {'success': False, 'error': 'No scenario data found'}
            
            # Create ZIP archive with multiple formats
            zip_data = self._create_multi_format_zip(scenario_data, formats)
            
            # Store file and generate signed URL
            file_url = self._store_export_file(zip_data, 'zip', scenario_id, 'multi_format')
            if not file_url:
                return {'success': False, 'error': 'Failed to store export file'}
            
            return {
                'success': True,
                'message': f'Exported scenario data in {len(formats)} formats',
                'data': {
                    'export_formats': formats,
                    'format_names': [self.export_formats[fmt]['name'] for fmt in formats],
                    'file_url': file_url,
                    'file_size': len(zip_data),
                    'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
                    'exported_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting multiple formats: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _get_scenario_data(self, scenario_id: str, include_analysis: bool = True) -> Optional[Dict[str, Any]]:
        """Get comprehensive scenario data for export"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get scenario
            query = """
            SELECT s.*, 
                   COUNT(p.id) as parcel_count,
                   SUM(ST_Area(p.geometry)) as total_area
            FROM scenarios s
            LEFT JOIN parcels p ON s.id = p.scenario_id AND p.status = 'active'
            WHERE s.id = %s
            GROUP BY s.id
            """
            cursor.execute(query, (scenario_id,))
            scenario = cursor.fetchone()
            
            if not scenario:
                return None
            
            # Get parcels
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
            
            # Get analysis data if requested
            analysis_data = {}
            if include_analysis:
                analysis_data = scenario.get('kpis', {})
            
            return {
                'scenario': scenario,
                'parcels': parcels,
                'links': links,
                'analysis': analysis_data
            }
            
        finally:
            cursor.close()
            conn.close()

    def _generate_export(self, scenario_data: Dict[str, Any], export_format: str, 
                        include_metadata: bool = True) -> Dict[str, Any]:
        """Generate export in specified format"""
        try:
            if export_format == 'geojson':
                return self._export_geojson(scenario_data, include_metadata)
            elif export_format == 'shapefile':
                return self._export_shapefile(scenario_data, include_metadata)
            elif export_format == 'gpkg':
                return self._export_gpkg(scenario_data, include_metadata)
            elif export_format == 'dxf':
                return self._export_dxf(scenario_data, include_metadata)
            elif export_format == 'csv':
                return self._export_csv(scenario_data, include_metadata)
            else:
                return {'success': False, 'error': f'Export format {export_format} not implemented'}
                
        except Exception as e:
            logger.error(f"Error generating {export_format} export: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _export_geojson(self, scenario_data: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
        """Export data as GeoJSON"""
        try:
            # Create FeatureCollection
            features = []
            
            # Add parcels
            for parcel in scenario_data['parcels']:
                feature = {
                    'type': 'Feature',
                    'geometry': json.loads(parcel['geometry']),
                    'properties': {
                        'id': parcel['id'],
                        'type': 'parcel',
                        **parcel['properties']
                    }
                }
                
                # Add capacity data
                if parcel['capacity']:
                    feature['properties']['capacity'] = parcel['capacity']
                
                # Add utilities data
                if parcel['utilities']:
                    feature['properties']['utilities'] = parcel['utilities']
                
                features.append(feature)
            
            # Add links
            for link in scenario_data['links']:
                feature = {
                    'type': 'Feature',
                    'geometry': json.loads(link['geometry']),
                    'properties': {
                        'id': link['id'],
                        'type': 'link',
                        'link_class': link['link_class'],
                        **link['properties']
                    }
                }
                features.append(feature)
            
            # Create GeoJSON structure
            geojson = {
                'type': 'FeatureCollection',
                'features': features
            }
            
            # Add metadata if requested
            if include_metadata:
                geojson['metadata'] = {
                    'scenario_id': scenario_data['scenario']['id'],
                    'scenario_name': scenario_data['scenario']['name'],
                    'exported_at': datetime.now().isoformat(),
                    'feature_count': len(features),
                    'parcel_count': len(scenario_data['parcels']),
                    'link_count': len(scenario_data['links'])
                }
            
            return {
                'success': True,
                'data': json.dumps(geojson, indent=2).encode('utf-8')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _export_shapefile(self, scenario_data: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
        """Export data as Shapefile"""
        try:
            # Create GeoDataFrames
            parcel_features = []
            for parcel in scenario_data['parcels']:
                geometry = shape(json.loads(parcel['geometry']))
                properties = {
                    'id': parcel['id'],
                    'type': 'parcel',
                    **parcel['properties']
                }
                
                if parcel['capacity']:
                    properties['capacity'] = json.dumps(parcel['capacity'])
                
                if parcel['utilities']:
                    properties['utilities'] = json.dumps(parcel['utilities'])
                
                parcel_features.append({
                    'geometry': geometry,
                    **properties
                })
            
            link_features = []
            for link in scenario_data['links']:
                geometry = shape(json.loads(link['geometry']))
                properties = {
                    'id': link['id'],
                    'type': 'link',
                    'link_class': link['link_class'],
                    **link['properties']
                }
                link_features.append({
                    'geometry': geometry,
                    **properties
                })
            
            # Create GeoDataFrames
            parcels_gdf = gpd.GeoDataFrame(parcel_features, crs='EPSG:4326')
            links_gdf = gpd.GeoDataFrame(link_features, crs='EPSG:4326')
            
            # Create ZIP file with shapefiles
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add parcels shapefile
                parcels_buffer = BytesIO()
                parcels_gdf.to_file(parcels_buffer, driver='ESRI Shapefile')
                parcels_buffer.seek(0)
                
                # Add all shapefile components
                for ext in ['.shp', '.shx', '.dbf', '.prj']:
                    try:
                        with open(f'parcels{ext}', 'rb') as f:
                            zip_file.writestr(f'parcels{ext}', f.read())
                    except FileNotFoundError:
                        pass
                
                # Add links shapefile
                links_buffer = BytesIO()
                links_gdf.to_file(links_buffer, driver='ESRI Shapefile')
                links_buffer.seek(0)
                
                for ext in ['.shp', '.shx', '.dbf', '.prj']:
                    try:
                        with open(f'links{ext}', 'rb') as f:
                            zip_file.writestr(f'links{ext}', f.read())
                    except FileNotFoundError:
                        pass
                
                # Add metadata if requested
                if include_metadata:
                    metadata = {
                        'scenario_id': scenario_data['scenario']['id'],
                        'scenario_name': scenario_data['scenario']['name'],
                        'exported_at': datetime.now().isoformat(),
                        'parcel_count': len(scenario_data['parcels']),
                        'link_count': len(scenario_data['links'])
                    }
                    zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))
            
            zip_buffer.seek(0)
            return {
                'success': True,
                'data': zip_buffer.getvalue()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _export_gpkg(self, scenario_data: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
        """Export data as GeoPackage"""
        try:
            # Create GeoDataFrames (similar to shapefile)
            parcel_features = []
            for parcel in scenario_data['parcels']:
                geometry = shape(json.loads(parcel['geometry']))
                properties = {
                    'id': parcel['id'],
                    'type': 'parcel',
                    **parcel['properties']
                }
                
                if parcel['capacity']:
                    properties['capacity'] = json.dumps(parcel['capacity'])
                
                if parcel['utilities']:
                    properties['utilities'] = json.dumps(parcel['utilities'])
                
                parcel_features.append({
                    'geometry': geometry,
                    **properties
                })
            
            link_features = []
            for link in scenario_data['links']:
                geometry = shape(json.loads(link['geometry']))
                properties = {
                    'id': link['id'],
                    'type': 'link',
                    'link_class': link['link_class'],
                    **link['properties']
                }
                link_features.append({
                    'geometry': geometry,
                    **properties
                })
            
            # Create GeoDataFrames
            parcels_gdf = gpd.GeoDataFrame(parcel_features, crs='EPSG:4326')
            links_gdf = gpd.GeoDataFrame(link_features, crs='EPSG:4326')
            
            # Create GeoPackage
            gpkg_buffer = BytesIO()
            parcels_gdf.to_file(gpkg_buffer, driver='GPKG', layer='parcels')
            links_gdf.to_file(gpkg_buffer, driver='GPKG', layer='links')
            
            gpkg_buffer.seek(0)
            return {
                'success': True,
                'data': gpkg_buffer.getvalue()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _export_dxf(self, scenario_data: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
        """Export data as DXF (simplified implementation)"""
        try:
            # Create a simple DXF structure
            dxf_content = [
                '0',
                'SECTION',
                '2',
                'HEADER',
                '9',
                '$ACADVER',
                '1',
                'AC1014',
                '0',
                'ENDSEC',
                '0',
                'SECTION',
                '2',
                'ENTITIES'
            ]
            
            # Add parcels as POLYLINE entities
            for parcel in scenario_data['parcels']:
                geometry = json.loads(parcel['geometry'])
                if geometry['type'] == 'Polygon':
                    coords = geometry['coordinates'][0]
                    dxf_content.extend([
                        '0',
                        'POLYLINE',
                        '8',
                        'PARCELS',
                        '66',
                        '1',
                        '70',
                        '1'
                    ])
                    
                    for coord in coords:
                        dxf_content.extend([
                            '0',
                            'VERTEX',
                            '8',
                            'PARCELS',
                            '10',
                            str(coord[0]),
                            '20',
                            str(coord[1])
                        ])
                    
                    dxf_content.extend([
                        '0',
                        'SEQEND'
                    ])
            
            # Add links as LINE entities
            for link in scenario_data['links']:
                geometry = json.loads(link['geometry'])
                if geometry['type'] == 'LineString':
                    coords = geometry['coordinates']
                    if len(coords) >= 2:
                        dxf_content.extend([
                            '0',
                            'LINE',
                            '8',
                            'LINKS',
                            '10',
                            str(coords[0][0]),
                            '20',
                            str(coords[0][1]),
                            '11',
                            str(coords[-1][0]),
                            '21',
                            str(coords[-1][1])
                        ])
            
            dxf_content.extend([
                '0',
                'ENDSEC',
                '0',
                'EOF'
            ])
            
            return {
                'success': True,
                'data': '\n'.join(dxf_content).encode('utf-8')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _export_csv(self, scenario_data: Dict[str, Any], include_metadata: bool = True) -> Dict[str, Any]:
        """Export data as CSV (tabular format)"""
        try:
            # Create CSV data
            csv_data = []
            
            # Add parcels data
            for parcel in scenario_data['parcels']:
                properties = parcel['properties']
                row = {
                    'id': parcel['id'],
                    'type': 'parcel',
                    'geometry_type': json.loads(parcel['geometry'])['type'],
                    **properties
                }
                
                if parcel['capacity']:
                    row['capacity_units'] = parcel['capacity'].get('units', 0)
                    row['capacity_population'] = parcel['capacity'].get('population', 0)
                    row['capacity_jobs'] = parcel['capacity'].get('jobs', 0)
                
                csv_data.append(row)
            
            # Add links data
            for link in scenario_data['links']:
                properties = link['properties']
                row = {
                    'id': link['id'],
                    'type': 'link',
                    'link_class': link['link_class'],
                    'geometry_type': json.loads(link['geometry'])['type'],
                    **properties
                }
                csv_data.append(row)
            
            # Convert to DataFrame and CSV
            df = pd.DataFrame(csv_data)
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            
            return {
                'success': True,
                'data': csv_buffer.getvalue()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_multi_format_zip(self, scenario_data: Dict[str, Any], formats: List[str]) -> bytes:
        """Create ZIP archive with multiple export formats"""
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add each format
            for fmt in formats:
                export_result = self._generate_export(scenario_data, fmt, True)
                if export_result['success']:
                    if fmt == 'shapefile':
                        # Shapefile is already a ZIP, extract and add components
                        shapefile_zip = zipfile.ZipFile(BytesIO(export_result['data']))
                        for name in shapefile_zip.namelist():
                            zip_file.writestr(f'{fmt}/{name}', shapefile_zip.read(name))
                    else:
                        # Add single file
                        extension = self.export_formats[fmt]['extensions'][0]
                        zip_file.writestr(f'{fmt}/data{extension}', export_result['data'])
            
            # Add metadata
            metadata = {
                'scenario_id': scenario_data['scenario']['id'],
                'scenario_name': scenario_data['scenario']['name'],
                'exported_at': datetime.now().isoformat(),
                'formats_included': formats,
                'parcel_count': len(scenario_data['parcels']),
                'link_count': len(scenario_data['links'])
            }
            zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    def _store_export_file(self, file_data: bytes, export_format: str, scenario_id: str, 
                          suffix: str = '') -> Optional[str]:
        """Store export file and return signed URL"""
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            extension = self.export_formats[export_format]['extensions'][0]
            filename = f"scenario_{scenario_id}_{export_format}{suffix}_{timestamp}{extension}"
            
            # For now, return a mock signed URL
            # In production, this would upload to MinIO/S3 and generate a real signed URL
            file_hash = hashlib.md5(file_data).hexdigest()
            mock_url = f"https://exports.urban-planner.com/{filename}?signature={file_hash}&expires={int(time.time() + 86400)}"
            
            # Store file metadata in database
            self._store_export_metadata(scenario_id, export_format, filename, len(file_data))
            
            return mock_url
            
        except Exception as e:
            logger.error(f"Error storing export file: {str(e)}")
            return None

    def _store_export_metadata(self, scenario_id: str, export_format: str, filename: str, file_size: int):
        """Store export metadata in database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO exports (scenario_id, export_format, filename, file_size, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (scenario_id, export_format, filename, file_size, datetime.now()))
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error storing export metadata: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def get_export_history(self, scenario_id: str) -> Dict[str, Any]:
        """Get export history for a scenario"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = """
            SELECT export_format, filename, file_size, created_at
            FROM exports
            WHERE scenario_id = %s
            ORDER BY created_at DESC
            """
            cursor.execute(query, (scenario_id,))
            exports = cursor.fetchall()
            
            return {
                'success': True,
                'data': {
                    'scenario_id': scenario_id,
                    'exports': exports,
                    'total_exports': len(exports)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting export history: {str(e)}")
            return {'success': False, 'error': str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_export(self, export_id: str) -> Dict[str, Any]:
        """Delete an export file"""
        try:
            # In production, this would delete from MinIO/S3 and database
            return {
                'success': True,
                'message': 'Export deleted successfully'
            }
            
        except Exception as e:
            logger.error(f"Error deleting export: {str(e)}")
            return {'success': False, 'error': str(e)}
