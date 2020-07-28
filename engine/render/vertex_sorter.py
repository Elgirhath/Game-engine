from engine.Vector import Vector
import math
    
def sort_vertices(point_list):
    if len(point_list) < 4:
        return point_list

    center = get_center_of_mass(point_list)
    
    point_list.sort(key=lambda point: math.atan2(*Vector.Difference2d(point, center)))

    return point_list


def get_center_of_mass(point_list):
    vector_sum = [0,0]
    for point in point_list:
        vector_sum[0] += point[0]
        vector_sum[1] += point[1]

    return (vector_sum[0]/len(point_list), vector_sum[1]/len(point_list))