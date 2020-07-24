from lib.Ray import Ray
from lib.Geometry import Surface
from lib.Vector import Vector
from lib.Mesh import Edge
from lib.Geometry import Surface

def trim_edge_to_visible(origin, end, camera):
    top = camera.pyramid.top
    bottom = camera.pyramid.bottom
    right = camera.pyramid.right
    left = camera.pyramid.left
    clip = camera.pyramid.clip

    edge = Edge(origin, end)

    for surface in [top, bottom, right, left, clip]:
        edge = trim_edge(edge, surface)
        if edge == None:
            return edge

    return edge

def trim_edge(edge, surface):
    ray = Ray(edge.A, Vector.Difference(edge.B, edge.A))
    intersection = ray.Intersect_point(surface)

    if not intersection or Vector.Distance(intersection, ray.origin) > Vector.Magnitude(ray.direction):
        if surface.Point_relative_pos(edge.A) > 0:
            return edge
        else:
            return None

    if surface.Point_relative_pos(edge.A) > 0:
        edge.B = intersection
    else:
        edge.A = intersection

    return edge

def cut_edge1(origin, end, main_camera):
    ray = Ray(origin, Vector.Difference(end, origin))
    intersections = []
            
    top = main_camera.pyramid.top
    bottom = main_camera.pyramid.bottom
    right = main_camera.pyramid.right
    left = main_camera.pyramid.left
    clip = main_camera.pyramid.clip
            
    intersection = ray.Intersect_point(bottom)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                    
    intersection = ray.Intersect_point(right)
    if intersection:
        if Surface.Is_point_between_surfaces(top, bottom, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(left)
    if intersection:
        if Surface.Is_point_between_surfaces(top, bottom, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(top)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(clip)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if Surface.Is_point_between_surfaces(top, bottom, intersection):
                intersections.append(intersection)
                
    if len(intersections)<2:
        return None
    
    
    distance = Vector.Magnitude(Vector.Difference(end, origin))
    new_origin = None
    for intersection in intersections:
        inter_distance = Vector.Magnitude(Vector.Difference(intersection, origin))
        if inter_distance < distance:
            distance = inter_distance
            new_origin = intersection
    if new_origin:
        return new_origin
    else:
        return None