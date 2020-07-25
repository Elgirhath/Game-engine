from lib.Ray import Ray
from lib.Geometry import Plane
from lib.Vector import Vector
from lib.Mesh import Edge
from lib.Geometry import Plane

def trim_edge_to_visible(origin, end, camera):
    top = camera.pyramid.top
    bottom = camera.pyramid.bottom
    right = camera.pyramid.right
    left = camera.pyramid.left
    clip = camera.pyramid.clip

    edge = Edge(origin, end)

    for plane in [top, bottom, right, left, clip]:
        edge = trim_edge(edge, plane)
        if edge == None:
            return edge

    return edge

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