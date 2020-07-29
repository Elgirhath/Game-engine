from engine.math import vector3

def convert_to_different_space(vector, component_vector1, component_vector2, component_vector3):
    """
        Returns scalars of the new R3 basis describing vector
    """
    x = vector3.dot(vector, component_vector1) / vector3.dot(component_vector1, component_vector1)
    y = vector3.dot(vector, component_vector2) / vector3.dot(component_vector2, component_vector2)
    z = vector3.dot(vector, component_vector3) / vector3.dot(component_vector3, component_vector3)

    return (x, y, z)