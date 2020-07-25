import unittest

class TestVector(unittest.TestCase):
    def test_vector_distribution_case1(self):
        from lib.Vector import Vector

        v = (0.4, 1.4, 9.3)

        v1 = (5.0, 0.0, 0.0)
        v2 = (0.0, 1.0, 0.0)
        v3 = (0.0, 0.0, 1.0)

        converted = Vector.convert_to_different_space(v, v1, v2, v3)

        self.assertEqual(converted, (0.08, 1.4, 9.3))
        
    def test_vector_distribution_case2(self):
        from lib.Vector import Vector

        v = (0.4, 1.4, 9.3)
        v1 = (1.0, 0.0, 0.0)
        v2 = (0.0, 1.0, 0.0)
        v3 = (0.0, 0.0, 1.0)

        converted = Vector.convert_to_different_space(v, v1, v2, v3)

        self.assertEqual(converted, (0.4, 1.4, 9.3))
        
    def test_vector_distribution_case3(self):
        from lib.Vector import Vector

        v = (0.4, 1.4, 9.3)
        v1 = (0.0, 0.0, 1.0)
        v2 = (0.0, 1.0, 0.0)
        v3 = (1.0, 0.0, 0.0)

        converted = Vector.convert_to_different_space(v, v1, v2, v3)

        self.assertEqual(converted, (9.3, 1.4, 0.4))

if __name__ == '__main__':
    unittest.main()