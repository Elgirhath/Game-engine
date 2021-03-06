import math
from engine.math import vector3
import numpy as np
import quaternion

class Quaternion():
    def __init__(self, w, vector, struct = None):
        self.q = np.quaternion(w, vector[0], vector[1], vector[2])

    @classmethod
    def from_np_quaternion(cls, quaternion):
        return cls(quaternion.w, (quaternion.x, quaternion.y, quaternion.z))
        
    @classmethod
    def from_angle_axis(cls, angle, axis):
        axis = vector3.normalize(axis)
        v = vector3.scale(axis, math.radians(angle))
        q = quaternion.from_rotation_vector(v)
        return cls.from_np_quaternion(q)
        
    def conjugate(self):
        return Quaternion.from_np_quaternion(self.q.conjugate())
    
    def inverse(self):
        return Quaternion.from_np_quaternion(self.q.inverse())

    def norm(self):
        return self.q.norm()
    
    @staticmethod
    def rotate_vector(vector, q):
        if q.q.w == 1:
            return vector

        q_inversed = q.q.inverse()
        Qp = np.quaternion(0, vector[0], vector[1], vector[2])
        Qpu = (q.q * Qp) * q_inversed
        return (Qpu.x, Qpu.y, Qpu.z)

    @staticmethod
    def rotate_vector_by_angle(vector, axis, angle):
        rotation_quaternion = Quaternion.from_angle_axis(angle, axis)
        return Quaternion.rotate_vector(vector, rotation_quaternion)
    
    @staticmethod
    def composite_rotations(init_rot_quaternion, additional_rot_quaternion):
        return Quaternion.from_np_quaternion(additional_rot_quaternion.q * init_rot_quaternion.q)
    

    @staticmethod
    def identity():
        return Quaternion(1, (0, 0, 0))

    def __eq__(self, other):
        return self.q == other.q