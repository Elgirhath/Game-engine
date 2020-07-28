from engine.Vector import Vector

    
def is_point_in_polygon(point, vertex_list):
    n_of_edge_intersections = 0

    vertex_number = len(vertex_list)
    for i in range(vertex_number):
        y_offset = point[1]
        a = (vertex_list[i][0], vertex_list[i][1] - y_offset)
        b = (vertex_list[(i+1)%vertex_number][0], vertex_list[(i+1)%vertex_number][1] - y_offset)
        if a[1] * b[1] > 0:
            continue

        x = b[0] - (b[1] * (b[0] - a[0]))/(b[1] - a[1])
        if x >= point[0]:
            n_of_edge_intersections += 1

    return n_of_edge_intersections % 2 == 1