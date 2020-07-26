from engine.Vector import Vector

def convert_to_different_space(vector, component_vector1, component_vector2, component_vector3):
    """
        Returns scalars of the new R3 basis describing vector
    """
    x = Vector.dot(vector, component_vector1) / Vector.dot(component_vector1, component_vector1)
    y = Vector.dot(vector, component_vector2) / Vector.dot(component_vector2, component_vector2)
    z = Vector.dot(vector, component_vector3) / Vector.dot(component_vector3, component_vector3)

    return (x, y, z)