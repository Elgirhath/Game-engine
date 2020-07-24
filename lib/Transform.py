from lib.Vector import Vector
from lib.Quaternion import Quaternion
from lib import Screen

class Transform():
    def __init__(self, parent, position, rot, scale = (1,1,1)):
        self.obj = parent
    
        self.forward = (1,0,0)
        self.right = (0,-1,0)
        self.up = (0,0,1)
        self.backward = (-1,0,0)
        self.left = (0,1,0)
        self.down = (0,0,-1)
    
        self.position = position
        self.rotation = rot
        self.scale = scale
    
    def Translate(self, vector):
        self.position = Vector.Add(self.position, vector)
        
        self._update_mesh_()
        
        if self.obj == Screen.main_camera:
            self.obj.pyramid.Update()
            
            
    def Set_pos(self, position):
        self.position = position
        
        self._update_mesh_()
        
        if self.obj == Screen.main_camera:
            self.obj.pyramid.Update()
    
    def Rotate(self, angle = 0, axis = (0, 0, 0), rotation = Quaternion(1,(0,0,0))):
        """Rotation of the object"""
        if axis == (0,0,0):
            self.rotation = Quaternion.Rotation_compound(self.rotation, rotation)
        else:
            rotQuaternion = Quaternion.Rot_quaternion(angle, axis)
            self.rotation = Quaternion.Rotation_compound(self.rotation, rotQuaternion)
        
        self._update_mesh_()
            
        self.forward =  Quaternion.Vector_quaternion_rotate((1,0,0), self.rotation)
        self.backward =  Quaternion.Vector_quaternion_rotate((-1,0,0), self.rotation)
        self.right =  Quaternion.Vector_quaternion_rotate((0,-1,0), self.rotation)
        self.left =  Quaternion.Vector_quaternion_rotate((0,1,0), self.rotation)
        self.up =  Quaternion.Vector_quaternion_rotate((0,0,1), self.rotation)
        self.down =  Quaternion.Vector_quaternion_rotate((0,0,-1), self.rotation)
        
        if self.obj == Screen.main_camera:
            self.obj.pyramid.Update()
        
    def Scale(self, scale):
        self.scale = Vector.Scale_by_vector(self.scale, scale)
        
        self._update_mesh_()
        
    def _rotate_vertex_(self, vertex_init):
        resultant_local_pos = Quaternion.Vector_quaternion_rotate(vertex_init, self.rotation)
        resultant_global_pos = Vector.Add(resultant_local_pos, self.position)
        return resultant_global_pos
    
    def _update_mesh_(self):
        if not 'mesh' in dir(self.obj):
            return
        mesh = self.obj.mesh
        if 'vertices' in dir(mesh):
            for i in range(0,len(mesh.vertices_init)):
                vertex = Vector.Scale_by_vector(mesh.vertices_init[i], self.scale)
                mesh.vertices[i] = self._rotate_vertex_(vertex)
                
                
        if 'edges' in dir(mesh):
            for i in range(0,len(mesh.edges_init)):
                vertex_a = Vector.Scale_by_vector(mesh.edges_init[i].A, self.scale)
                vertex_b = Vector.Scale_by_vector(mesh.edges_init[i].B, self.scale)
                mesh.edges[i].A = self._rotate_vertex_(vertex_a)
                mesh.edges[i].B = self._rotate_vertex_(vertex_b)
                
        if 'faces' in dir(mesh):
            for i in range(0,len(mesh.faces_init)):
                for k in range(0, len(mesh.faces_init[i].vertex)):
                    vertex = Vector.Scale_by_vector(mesh.faces_init[i].vertex[k], self.scale)
                    mesh.faces[i].vertex[k] = self._rotate_vertex_(vertex)
                mesh.faces[i].normal = Quaternion.Vector_quaternion_rotate(mesh.faces_init[i].normal, self.rotation)
                
    def To_global(self, abc = 0):
        if self.obj.parent:
            position = Vector.Add(self.obj.parent.transform.position, Quaternion.Vector_quaternion_rotate(self.position, self.obj.parent.transform.rotation))
            rotation = Quaternion.Rotation_compound(self.rotation, self.obj.parent.transform.rotation)
            scale = Quaternion.Vector_quaternion_rotate(self.scale, self.obj.parent.transform.rotation)
            obj = self.obj
            
            transform = Transform(obj, position, rotation, scale)
            
            transform.forward =  Quaternion.Vector_quaternion_rotate(self.forward, self.obj.parent.transform.rotation)
            transform.backward =  Quaternion.Vector_quaternion_rotate(self.backward, self.obj.parent.transform.rotation)
            transform.right =  Quaternion.Vector_quaternion_rotate(self.right, self.obj.parent.transform.rotation)
            transform.left =  Quaternion.Vector_quaternion_rotate(self.left, self.obj.parent.transform.rotation)
            transform.up =  Quaternion.Vector_quaternion_rotate(self.up, self.obj.parent.transform.rotation)
            transform.down =  Quaternion.Vector_quaternion_rotate(self.down, self.obj.parent.transform.rotation)
            
            return transform
        else:
            return self