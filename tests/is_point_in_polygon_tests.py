import unittest

class TestPointInPolygon(unittest.TestCase):
    def test_point_in_polygon(self):
        from engine.util.is_point_in_polygon_resolver import is_point_in_polygon
        from engine.Geometry import sort_vertices

        point = (0, -8)

        vertices = [
            (-10, -10),
            (-10, 10),
            (10, 10),
            (10, -10)
        ]

        self.assertTrue(is_point_in_polygon(point, vertices))

if __name__ == '__main__':
    unittest.main()