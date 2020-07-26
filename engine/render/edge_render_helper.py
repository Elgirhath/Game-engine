from engine.Ray import Ray
from engine.Geometry import Plane
from engine.Vector import Vector
from engine.Mesh import Edge
from engine.Geometry import Plane

def trim_edge(edge, plane):
    ray = Ray(edge.A, Vector.Difference(edge.B, edge.A))
    intersection = ray.intersect_plane(plane)

    if not intersection or Vector.compare_magnitudes(Vector.Difference(intersection, ray.origin), ray.direction) > 0:
        if plane.get_signed_distance_to_point(edge.A) > 0:
            return edge
        else:
            return None

    if plane.get_signed_distance_to_point(edge.A) > 0:
        edge.B = intersection
    else:
        edge.A = intersection

    return edge