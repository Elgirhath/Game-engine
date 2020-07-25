from lib.Mesh import Face
from lib.render.world_screen_space_converter import world_to_screen_edge
from lib import Geometry
from lib import Screen

def world_to_screen_face(face, camera):
    edges = face.get_edges()
    
    vertices = []
    for edge in edges:
        screen_edge = world_to_screen_edge(edge, camera)
        if screen_edge:
            if not screen_edge.A in vertices:
                vertices.append(screen_edge.A)
            if not screen_edge.B in vertices:
                vertices.append(screen_edge.B)

    if len(vertices) < 2:
        return None
    
    face_plane = Geometry.Plane.From_normal(face.normal, face.vertex[0])
    pixels = [camera.left_top_pixel,
                camera.left_bottom_pixel,
                camera.right_top_pixel,
                camera.right_bottom_pixel]
    
    for pixel in pixels:
        ray = Screen.Ray_on_pixel(pixel)
        intersection = ray.intersect_plane(face_plane)
        if intersection:
            if Geometry.Point_in_polygon(intersection, face.vertex):
                vertices.append(pixel)

    if len(vertices)>2:
        center = Geometry.Center_of_mass(vertices)
        vertices = Geometry.sort_vertices(vertices, center)
        return vertices

    return None