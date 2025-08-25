# Created automatically by Cursor AI (2025-08-25)
import unittest
import json
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from shapely.validation import make_valid
import geopandas as gpd
from apps.workers.src.gis.geometry_validator import GeometryValidator

class TestGeometryValidation(unittest.TestCase):
    def setUp(self):
        self.validator = GeometryValidator()

    def test_valid_polygon(self):
        """Test that valid polygons pass validation"""
        valid_polygon = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
        
        result = self.validator.validate_geometry(valid_polygon)
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['geometry_type'], 'Polygon')

    def test_invalid_polygon_self_intersection(self):
        """Test that self-intersecting polygons are detected and repaired"""
        invalid_polygon = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 1], [0, 1], [1, 0], [0, 0]]]
        }
        
        result = self.validator.validate_geometry(invalid_polygon)
        self.assertFalse(result['is_valid'])
        self.assertTrue(result['can_repair'])
        
        repaired = self.validator.repair_geometry(invalid_polygon)
        self.assertTrue(repaired['is_valid'])

    def test_invalid_polygon_holes(self):
        """Test that polygons with invalid holes are repaired"""
        invalid_polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]],
                [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]]
            ]
        }
        
        result = self.validator.validate_geometry(invalid_polygon)
        self.assertTrue(result['is_valid'])  # This should be valid
        
        # Test with invalid hole
        invalid_hole_polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]],
                [[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]  # Hole outside polygon
            ]
        }
        
        result = self.validator.validate_geometry(invalid_hole_polygon)
        self.assertFalse(result['is_valid'])

    def test_multipolygon_validation(self):
        """Test MultiPolygon validation"""
        valid_multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]]
            ]
        }
        
        result = self.validator.validate_geometry(valid_multipolygon)
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['geometry_type'], 'MultiPolygon')

    def test_linestring_validation(self):
        """Test LineString validation"""
        valid_linestring = {
            "type": "LineString",
            "coordinates": [[0, 0], [1, 1], [2, 2]]
        }
        
        result = self.validator.validate_geometry(valid_linestring)
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['geometry_type'], 'LineString')

    def test_point_validation(self):
        """Test Point validation"""
        valid_point = {
            "type": "Point",
            "coordinates": [0, 0]
        }
        
        result = self.validator.validate_geometry(valid_point)
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['geometry_type'], 'Point')

    def test_geometry_repair(self):
        """Test geometry repair functionality"""
        # Create a bowtie polygon (self-intersecting)
        bowtie_coords = [[0, 0], [2, 2], [0, 2], [2, 0], [0, 0]]
        invalid_polygon = {
            "type": "Polygon",
            "coordinates": [bowtie_coords]
        }
        
        repaired = self.validator.repair_geometry(invalid_polygon)
        self.assertTrue(repaired['is_valid'])
        self.assertIsNotNone(repaired['geometry'])

    def test_area_calculation(self):
        """Test area calculation for valid geometries"""
        polygon = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
        
        area = self.validator.calculate_area(polygon)
        self.assertGreater(area, 0)
        self.assertAlmostEqual(area, 1.0, places=6)

    def test_bounds_calculation(self):
        """Test bounds calculation"""
        polygon = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [2, 0], [2, 3], [0, 3], [0, 0]]]
        }
        
        bounds = self.validator.calculate_bounds(polygon)
        expected_bounds = [0, 0, 2, 3]  # [minx, miny, maxx, maxy]
        self.assertEqual(bounds, expected_bounds)

    def test_topology_fixing(self):
        """Test topology fixing for complex geometries"""
        # Create overlapping polygons
        overlapping_polygons = [
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]
            },
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [3, 1], [3, 3], [1, 3], [1, 1]]]
            }
        ]
        
        fixed = self.validator.fix_topology(overlapping_polygons)
        self.assertTrue(len(fixed) > 0)
        
        # Check that fixed geometries are valid
        for geom in fixed:
            result = self.validator.validate_geometry(geom)
            self.assertTrue(result['is_valid'])

if __name__ == '__main__':
    unittest.main()
