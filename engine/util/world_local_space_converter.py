from engine.Quaternion import Quaternion
from engine.Vector import Vector
    
def World_to_local_space(point, transform):
    point_translated = Vector.Difference(point, transform.position)
    point_translated_and_rotated = Quaternion.rotate_vector(point_translated, transform.rotation.inverse())
    return point_translated_and_rotated

def Local_to_world_space(point, transform):
    point_rotated = Quaternion.rotate_vector(point, transform.rotation)
    point_rotated_and_translated = Vector.Add(point_rotated, transform.position)
    return point_rotated_and_translated