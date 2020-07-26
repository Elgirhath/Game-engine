from lib.Mesh import Face
from lib.render.world_screen_space_converter import world_to_screen_edge_unclamped, limit_edge_to_screen
from lib import Geometry
from lib import Screen
from lib.util.is_point_in_polygon_resolver import is_point_in_polygon
from lib import Input
from lib.render.vertex_sorter import sort_vertices

def world_to_screen_face(face, camera):
    edges_unclamped = get_screen_edges_unclamped(face, camera)

    if len(edges_unclamped) < 2:
        return None

    vertices_unclamped = sort_vertices(extract_vertices_from_edges(edges_unclamped))
    corner_pixels = [camera.left_top_pixel,
                camera.left_bottom_pixel,
                camera.right_top_pixel,
                camera.right_bottom_pixel]
    vertices = []
    for pixel in corner_pixels:
        if is_point_in_polygon(pixel, vertices_unclamped):
            vertices.append(pixel)

    clamped_edges = clamp_edges(edges_unclamped, camera)
    vertices.extend(extract_vertices_from_edges(clamped_edges))

    if len(vertices)>2:
        vertices = sort_vertices(vertices)
        return vertices

    return None

def get_screen_edges_unclamped(face, camera):
    edges = []
    for edge in face.get_edges():
        screen_edge = world_to_screen_edge_unclamped(edge, camera)
        if screen_edge:
            edges.append(screen_edge)

    return edges

def extract_vertices_from_edges(edge_list):
    vertices = set()
    for edge in edge_list:
        vertices.add(edge.A)
        vertices.add(edge.B)
    return list(vertices)

def clamp_edges(edge_list, camera):
    clamped_edges = []
    for edge in edge_list:
        edge = limit_edge_to_screen(edge, camera.resolution)
        if edge != None:
            clamped_edges.append(edge)

    return clamped_edges