import math
from lib.Vector import Vector

class Quaternion():
    def __init__(self, w, vector, struct = None):
        self.w = w
        self.vector = vector
        self.struct = (w, vector[0], vector[1], vector[2])
        self.norm = math.sqrt(w**2 + vector[0]**2 + vector[1]**2 + vector[2]**2)
        
    def conjugate(self):
        #kwaternion przeciwny
        return Quaternion(self.w, Vector.Scale(self.vector, -1))
    
    def inverse(self):
        #kwaternion odwrotny
        return Quaternion.Scale(self.conjugate(), 1/(self.norm**2))
    
    def Scale(quaternion, scalar):
        w = quaternion.w * scalar
        vector= (quaternion.vector[0] * scalar, quaternion.vector[1] * scalar, quaternion.vector[2] * scalar)
        return Quaternion(w, vector)
        
    def Add(quaternion_1, quaternion_2):
        return Quaternion(quaternion_1.w + quaternion_2.w, quaternion_1.vector, quaternion_2.vector)
    
    def Multiply(quaternion_1, quaternion_2):
        s_1 = quaternion_1.w
        s_2 = quaternion_2.w
        v = quaternion_1.vector
        w = quaternion_2.vector
        return Quaternion(s_1 * s_2 - Vector.dot(v, w), Vector.Add(Vector.Add(Vector.Scale(w, s_1), Vector.Scale(v, s_2)), Vector.cross(v, w)))
    
    def Rot_quaternion(angle, axis):
        axis = Vector.Normalize(axis)
        cos = math.cos(math.radians(angle)/2)
        sin = math.sin(math.radians(angle)/2)
        q = Quaternion(cos, Vector.Scale(axis, sin))
        return q
    
    def Vector_quaternion_rotate(vector, quaternion):
        if quaternion == Quaternion.identity():
            return vector

        q = quaternion
        q_inversed = q.inverse()
        Qp = Quaternion(0, vector)
        Qpu = Quaternion.Multiply(Quaternion.Multiply(q, Qp), q_inversed)
        return Qpu.vector
    
    def Rotation_compound(init_rot_quaternion, additional_rot_quaternion):
        return Quaternion.Multiply(additional_rot_quaternion, init_rot_quaternion)
    
    def Face_rotate(face, quaternion):
        from lib import Mesh
        new_vertices = []
        for vertex in face.vertex:
            new_vertices.append(Quaternion.Vector_quaternion_rotate(vertex, quaternion))
        normal = Quaternion.Vector_quaternion_rotate(face.normal, quaternion)
        return Mesh.Face(new_vertices, normal)

    @staticmethod
    def identity():
        return Quaternion(1, (0, 0, 0))

    def __eq__(self, other):
        return self.struct == other.struct