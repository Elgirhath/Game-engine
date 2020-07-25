from lib.Mesh import Edge
from lib.Ray import Ray
from lib.Geometry import Plane
from lib.Vector import Vector
import math
from lib.render.edge_render_helper import trim_edge_to_visible
    
def world_to_screen_point(point, camera):
    """Get view of the point on screen"""
    tr = camera.global_transform
    
    screen_plane = Plane.From_normal(tr.forward, point)
    screen_middle_point = Vector.Add(tr.position, Vector.Plane_cross_point(tr.position, tr.forward, screen_plane))
        
    screen_width = math.tan(math.radians(camera.FOV/2))*Vector.Magnitude(Vector.Difference(screen_middle_point, tr.position))*2
    screen_height = screen_width / camera.aspect_ratio
    
    point_in_camera_space = Vector.convert_to_different_space(Vector.Difference(point, screen_middle_point), tr.right, tr.down, tr.forward)

    point_right_vector = Vector.Add(Vector.Scale(tr.right, screen_width/2), Vector.Scale(tr.right, point_in_camera_space[0]))
    point_down_vector = Vector.Add(Vector.Scale(tr.down, screen_height/2), Vector.Scale(tr.down, point_in_camera_space[1]))
    point_right = Vector.Magnitude(point_right_vector)/screen_width
    point_down = Vector.Magnitude(point_down_vector)/screen_height
    scale_right = Vector.Scale_div(point_right_vector, tr.right)
    if scale_right<0:
        point_right=-point_right
    scale_down = Vector.Scale_div(point_down_vector, tr.down)
    if scale_down<0:
        point_down=-point_down
    return (point_right * camera.resolution[0], point_down * camera.resolution[1])
        

def world_to_screen_edge(edge, camera):
    if is_point_behind_camera_clip(edge.A, camera) and is_point_behind_camera_clip(edge.B, camera):
        return None

    edge = limit_edge_to_camera_clip(edge, camera)

    origin_pos = world_to_screen_point(edge.A, camera)
    end_pos = world_to_screen_point(edge.B, camera)
    edge = Edge(origin_pos, end_pos)

    return limit_edge_to_screen(edge, camera.resolution)

def limit_edge_to_camera_clip(edge, camera):
    if is_point_behind_camera_clip(edge.A, camera):
        ray = Ray(edge.B, Vector.Difference(edge.A, edge.B))
        edge.A = ray.intersect_plane(camera.pyramid.clip)

    if is_point_behind_camera_clip(edge.B, camera):
        ray = Ray(edge.A, Vector.Difference(edge.B, edge.A))
        edge.B = ray.intersect_plane(camera.pyramid.clip)

    return edge

def is_point_behind_camera_clip(point, camera):
    tr = camera.global_transform
    clip_position = Vector.Add(tr.position, Vector.Scale(tr.forward, camera.clip_min))
    return Vector.dot(Vector.Difference(point, clip_position), tr.forward) < 0.0

def limit_edge_to_screen(edge, resolution):
    if edge.A[0] < 0.0:
        if edge.B[0] < 0.0:
            return None
        edge.A = _limit_edge_left(edge.A, edge.B)

    if edge.B[0] < 0.0:
        if edge.A[0] < 0.0:
            return None
        edge.B = _limit_edge_left(edge.B, edge.A)
        
    if edge.A[1] < 0.0:
        if edge.B[1] < 0.0:
            return None
        edge.A = _limit_edge_top(edge.A, edge.B)
        
    if edge.B[1] < 0.0:
        if edge.A[1] < 0.0:
            return None
        edge.B = _limit_edge_top(edge.B, edge.A)

    if edge.A[0] > resolution[0]:
        if edge.B[0] > resolution[0]:
            return None
        edge.A = _limit_edge_right(edge.A, edge.B, resolution)
        
    if edge.B[0] > resolution[0]:
        if edge.A[0] > resolution[0]:
            return None
        edge.B = _limit_edge_right(edge.B, edge.A, resolution)
        
    if edge.A[1] > resolution[1]:
        if edge.B[1] > resolution[1]:
            return None
        edge.A = _limit_edge_bottom(edge.A, edge.B, resolution)
        
    if edge.B[1] > resolution[1]:
        if edge.A[1] > resolution[1]:
            return None
        edge.B = _limit_edge_bottom(edge.B, edge.A, resolution)

    return edge

def _limit_edge_left(outside_point, inside_point):
    aligned_point1 = inside_point[1] - (inside_point[0] * (inside_point[1] - outside_point[1]))/(inside_point[0] - outside_point[0])
    aligned_point0 = 0.0
    return (aligned_point0, aligned_point1)
    
def _limit_edge_top(outside_point, inside_point):
    aligned_point0 = inside_point[0] - (inside_point[1] * (inside_point[0] - outside_point[0]))/(inside_point[1] - outside_point[1])
    aligned_point1 = 0.0
    return (aligned_point0, aligned_point1)

def _limit_edge_right(outside_point, inside_point, resolution):
    aligned_point1 = inside_point[1] - (resolution[0] - inside_point[0]) * (inside_point[1] - outside_point[1]) / (outside_point[0] - inside_point[0])
    aligned_point0 = resolution[0]
    return (aligned_point0, aligned_point1)
    
def _limit_edge_bottom(outside_point, inside_point, resolution):
    aligned_point0 = inside_point[0] - (resolution[1] - inside_point[1]) * (inside_point[0] - outside_point[0]) / (outside_point[1] - inside_point[1])
    aligned_point1 = resolution[1]
    return (aligned_point0, aligned_point1)