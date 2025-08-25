# Created automatically by Cursor AI (2025-08-25)
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union
import json
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GISIngestWorker:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DB', 'urban_planner'),
            'user': os.getenv('POSTGRES_USER', 'planner'),
            'password': os.getenv('POSTGRES_PASSWORD', 'dev_password')
        }

    def process_geojson(self, geojson_data: Dict[str, Any], scenario_id: str) -> Dict[str, Any]:
        """Process GeoJSON data and store in PostGIS"""
        try:
            # Load GeoJSON into GeoDataFrame
            gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
            
            # Ensure CRS is WGS84 (EPSG:4326)
            if gdf.crs is None:
                gdf.set_crs(epsg=4326, inplace=True)
            elif gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)

            # Validate and clean geometries
            gdf = self._clean_geometries(gdf)
            
            # Store in database
            result = self._store_geometries(gdf, scenario_id, geojson_data.get('type', 'FeatureCollection'))
            
            return {
                'success': True,
                'message': f'Processed {len(gdf)} features',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Error processing GeoJSON: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def process_shapefile(self, file_path: str, scenario_id: str) -> Dict[str, Any]:
        """Process Shapefile and store in PostGIS"""
        try:
            # Load Shapefile
            gdf = gpd.read_file(file_path)
            
            # Ensure CRS is WGS84
            if gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)

            # Validate and clean geometries
            gdf = self._clean_geometries(gdf)
            
            # Store in database
            result = self._store_geometries(gdf, scenario_id, 'shapefile')
            
            return {
                'success': True,
                'message': f'Processed {len(gdf)} features from shapefile',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Error processing shapefile: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _clean_geometries(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Clean and validate geometries"""
        # Remove invalid geometries
        gdf = gdf[gdf.geometry.is_valid]
        
        # Fix geometries if needed
        gdf.geometry = gdf.geometry.buffer(0)
        
        # Ensure single polygons (not multipolygons for parcels)
        if 'parcel' in gdf.columns or 'type' in gdf.columns:
            gdf.geometry = gdf.geometry.apply(self._ensure_single_polygon)
        
        return gdf

    def _ensure_single_polygon(self, geom):
        """Convert MultiPolygon to single Polygon if possible"""
        if geom.geom_type == 'MultiPolygon':
            if len(geom.geoms) == 1:
                return geom.geoms[0]
            else:
                # Union all polygons
                return unary_union(geom.geoms)
        return geom

    def _store_geometries(self, gdf: gpd.GeoDataFrame, scenario_id: str, source_type: str) -> Dict[str, Any]:
        """Store geometries in PostGIS database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Determine table based on geometry type
            if gdf.geometry.iloc[0].geom_type in ['Polygon', 'MultiPolygon']:
                if source_type == 'FeatureCollection' and 'parcel' in gdf.columns:
                    table_name = 'parcels'
                else:
                    table_name = 'site_boundaries'
            elif gdf.geometry.iloc[0].geom_type == 'LineString':
                table_name = 'links'
            else:
                raise ValueError(f"Unsupported geometry type: {gdf.geometry.iloc[0].geom_type}")

            # Insert geometries
            for idx, row in gdf.iterrows():
                geom_wkt = row.geometry.wkt
                properties = row.drop('geometry').to_dict()
                
                if table_name == 'parcels':
                    self._insert_parcel(cursor, scenario_id, geom_wkt, properties)
                elif table_name == 'site_boundaries':
                    self._insert_site_boundary(cursor, scenario_id, geom_wkt, properties)
                elif table_name == 'links':
                    self._insert_link(cursor, scenario_id, geom_wkt, properties)

            conn.commit()
            
            return {
                'table': table_name,
                'features_count': len(gdf),
                'scenario_id': scenario_id
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def _insert_parcel(self, cursor, scenario_id: str, geom_wkt: str, properties: Dict[str, Any]):
        """Insert parcel into database"""
        query = """
        INSERT INTO parcels (scenario_id, geometry, properties, created_at, updated_at)
        VALUES (%s, ST_GeomFromText(%s, 4326), %s, NOW(), NOW())
        """
        cursor.execute(query, (scenario_id, geom_wkt, json.dumps(properties)))

    def _insert_site_boundary(self, cursor, scenario_id: str, geom_wkt: str, properties: Dict[str, Any]):
        """Insert site boundary into database"""
        query = """
        INSERT INTO site_boundaries (scenario_id, geometry, properties, created_at, updated_at)
        VALUES (%s, ST_GeomFromText(%s, 4326), %s, NOW(), NOW())
        """
        cursor.execute(query, (scenario_id, geom_wkt, json.dumps(properties)))

    def _insert_link(self, cursor, scenario_id: str, geom_wkt: str, properties: Dict[str, Any]):
        """Insert link into database"""
        query = """
        INSERT INTO links (scenario_id, geometry, properties, created_at, updated_at)
        VALUES (%s, ST_GeomFromText(%s, 4326), %s, NOW(), NOW())
        """
        cursor.execute(query, (scenario_id, geom_wkt, json.dumps(properties)))

    def validate_upload(self, file_path: str) -> Dict[str, Any]:
        """Validate uploaded file before processing"""
        try:
            if file_path.endswith('.geojson') or file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    geojson_data = json.load(f)
                
                gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
            else:
                gdf = gpd.read_file(file_path)
            
            # Basic validation
            validation_result = {
                'valid': True,
                'feature_count': len(gdf),
                'geometry_types': gdf.geometry.geom_type.unique().tolist(),
                'crs': str(gdf.crs),
                'bounds': gdf.total_bounds.tolist(),
                'area': gdf.geometry.area.sum() if gdf.geometry.iloc[0].geom_type in ['Polygon', 'MultiPolygon'] else None
            }
            
            # Check for potential issues
            issues = []
            if len(gdf) == 0:
                issues.append("No features found")
                validation_result['valid'] = False
            
            if not gdf.geometry.is_valid.all():
                issues.append("Some geometries are invalid")
                validation_result['valid'] = False
            
            if gdf.geometry.area.sum() > 1000000000:  # 1000 km²
                issues.append("Area seems very large, check CRS")
            
            validation_result['issues'] = issues
            return validation_result
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
