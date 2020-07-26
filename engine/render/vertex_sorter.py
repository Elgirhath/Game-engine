from engine.Vector import Vector
    
def sort_vertices(point_list):
    if len(point_list) < 3:
        return point_list

    center = get_center_of_mass(point_list)
    
    point_angle_list = assign_polar_coordinate_angles(point_list, center)
    
    point_angle_list.sort(key=lambda point_angle_kvp: point_angle_kvp[1])

    return [point for point, _ in point_angle_list]

def assign_polar_coordinate_angles(point_list, origin):
    reference_direction = Vector.Difference(point_list[0], origin)
    angles = [(point_list[0], 0.0)]
    for i in range(1, len(point_list)):
        p = Vector.Difference(point_list[i], origin)
        angle = Vector.Angle_between_vectors(p, reference_direction)
        if Vector.cross(p, reference_direction) < 0:
            angle = 360 - angle

        angles.append((point_list[i], angle))

    return angles


def get_center_of_mass(point_list):
    if len(point_list[0])==2:
        vector_sum = (0,0)
        for i in range(0, len(point_list)):
            vector_sum = Vector.Add(vector_sum, point_list[i])
        average = Vector.Scale(vector_sum, (1/len(point_list)))
        return average
    elif len(point_list[0])==3:
        vector_sum = (0,0, 0)
        for i in range(0, len(point_list)):
            vector_sum = Vector.Add(vector_sum, point_list[i])
        average = Vector.Scale(vector_sum, (1/len(point_list)))
        return average