from lib.Vector import Vector

def are_2_points_on_the_same_side_of_line(point1, point2, line_origin, line_end):
    line_vector = Vector.Difference(line_end, line_origin)
    line_to_point_vector = Vector.Difference(point1, line_origin)
    line_to_opposite_vertex_vector = Vector.Difference(point2, line_origin)

    cp1 = Vector.cross(line_vector, line_to_point_vector)
    cp2 = Vector.cross(line_vector, line_to_opposite_vertex_vector)

    if len(point1) == 2:
        return cp1 * cp2 >= 0
    else:
        return Vector.dot(cp1, cp2) >= 0

def Point_in_triangle(point, vertex_list):
    a = are_2_points_on_the_same_side_of_line(point, vertex_list[2], vertex_list[0], vertex_list[1])
    if not a:
        return False
    b = are_2_points_on_the_same_side_of_line(point, vertex_list[0], vertex_list[1], vertex_list[2])
    if not b:
        return False
    c = are_2_points_on_the_same_side_of_line(point, vertex_list[1], vertex_list[2], vertex_list[0])
    if not c:
        return False
    else:
        return True
    
def is_point_in_polygon(point, vertex_list):
    origin = vertex_list[0]
    for i in range(1, len(vertex_list)-1):
        triangle = [origin, vertex_list[i], vertex_list[i+1]]
        if Point_in_triangle(point, triangle):
            return True
    return False