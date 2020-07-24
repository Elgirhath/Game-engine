import unittest

class TestEdgeRenderHelper(unittest.TestCase):
    def test_trim_edge_only_origin_visible(self):
        from lib.render.edge_render_helper import trim_edge
        from lib.Mesh import Edge
        from lib.Geometry import Plane

        edge = Edge((0.0, 0.0, 0.0), (0.0, 2.0, 0.0))
        plane = Plane.From_normal((0.0, -1.0, 0.0), (0.0, 1.0, 0.0))

        trimmed_edge = trim_edge(edge, plane)

        self.assertEqual(trimmed_edge.A, (0.0, 0.0, 0.0))
        self.assertEqual(trimmed_edge.B, (0.0, 1.0, 0.0))
        
    def test_trim_edge_only_end_visible(self):
        from lib.render.edge_render_helper import trim_edge
        from lib.Mesh import Edge
        from lib.Geometry import Plane

        edge = Edge((0.0, 2.0, 0.0), (0.0, 0.0, 0.0))
        plane = Plane.From_normal((0.0, -1.0, 0.0), (0.0, 1.0, 0.0))

        trimmed_edge = trim_edge(edge, plane)

        self.assertEqual(trimmed_edge.A, (0.0, 1.0, 0.0))
        self.assertEqual(trimmed_edge.B, (0.0, 0.0, 0.0))
        
    def test_trim_edge_not_visible(self):
        from lib.render.edge_render_helper import trim_edge
        from lib.Mesh import Edge
        from lib.Geometry import Plane

        edge = Edge((0.0, 0.0, 0.0), (0.0, 2.0, 0.0))
        plane = Plane.From_normal((0.0, -1.0, 0.0), (0.0, -1.0, 0.0))

        trimmed_edge = trim_edge(edge, plane)

        self.assertIsNone(trimmed_edge)
        
    def test_trim_edge_fully_visible(self):
        from lib.render.edge_render_helper import trim_edge
        from lib.Mesh import Edge
        from lib.Geometry import Plane

        edge = Edge((0.0, 0.0, 0.0), (0.0, 2.0, 0.0))
        plane = Plane.From_normal((0.0, 1.0, 0.0), (0.0, -1.0, 0.0))

        trimmed_edge = trim_edge(edge, plane)

        self.assertEqual(trimmed_edge.A, (0.0, 0.0, 0.0))
        self.assertEqual(trimmed_edge.B, (0.0, 2.0, 0.0))
        
        
    def test_trim_edge_fully_visible_directed_towards_plane(self):
        from lib.render.edge_render_helper import trim_edge
        from lib.Mesh import Edge
        from lib.Geometry import Plane

        edge = Edge((0.0, 2.0, 0.0), (0.0, 0.0, 0.0))
        plane = Plane.From_normal((0.0, 1.0, 0.0), (0.0, -1.0, 0.0))

        trimmed_edge = trim_edge(edge, plane)

        self.assertEqual(trimmed_edge.A, (0.0, 2.0, 0.0))
        self.assertEqual(trimmed_edge.B, (0.0, 0.0, 0.0))

if __name__ == '__main__':
    unittest.main()