import unittest

class TestEdgeLimitToScreen(unittest.TestCase):
    def test_left_edge(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((-20, 0), (20, 20))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (0.0, 10.0))
        self.assertEqual(limited.B, (20.0, 20.0))
        
    def test_left_edge_inverted(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((20, 20), (-20, 0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (20.0, 20.0))
        self.assertEqual(limited.B, (0.0, 10.0))
        
    def test_top_edge(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((0, -20), (20, 20))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (10.0, 0.0))
        self.assertEqual(limited.B, (20.0, 20.0))

    def test_top_edge_inverted(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((20, 20), (0, -20))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (20.0, 20.0))
        self.assertEqual(limited.B, (10.0, 0.0))

        
    def test_right_edge(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((80, 20), (120, 60))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (80.0, 20.0))
        self.assertEqual(limited.B, (100.0, 40.0))
        
    def test_right_edge_inverted(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((120, 60), (80, 20))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (100.0, 40.0))
        self.assertEqual(limited.B, (80.0, 20.0))
        
    def test_bottom_edge(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((20, 120), (60, 80))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (40.0, 100.0))
        self.assertEqual(limited.B, (60.0, 80.0))
        
    def test_bottom_edge_inverted(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((60, 80), (20, 120))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (60.0, 80.0))
        self.assertEqual(limited.B, (40.0, 100.0))

    def test_fully_visible(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((5.0, 50.0), (20.0, 20.0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (5.0, 50.0))
        self.assertEqual(limited.B, (20.0, 20.0))

    def test_combined_left_bottom_edge(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((20.0, 80.0), (-20.0, 160.0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (20.0, 80.0))
        self.assertEqual(limited.B, (10.0, 100.0))
        
    def test_combined_left_bottom_edge_inverted(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((-20.0, 160.0), (20.0, 80.0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (10.0, 100.0))
        self.assertEqual(limited.B, (20.0, 80.0))
        
    def test_edge_across_screen(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((-50.0, 20.0), (150.0, 80.0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertEqual(limited.A, (0.0, 35.0))
        self.assertEqual(limited.B, (100.0, 65.0))
        
    def test_invisible_edge_is_none(self):
        from engine.Mesh import Edge
        from engine.render.world_screen_space_converter import limit_edge_to_screen
        
        edge = Edge((-50.0, 20.0), (20.0, -30.0))

        limited = limit_edge_to_screen(edge, (100, 100))

        self.assertIsNone(limited)

if __name__ == '__main__':
    unittest.main()