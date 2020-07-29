from engine.math import vector3
from engine.Quaternion import Quaternion

class Transform():
    def __init__(self, obj, position, rot, scale = (1,1,1)):
        self.object = obj
        self.children = set()
        self.parent = None
    
        self.forward = (1,0,0)
        self.right = (0,-1,0)
        self.up = (0,0,1)
        self.backward = (-1,0,0)
        self.left = (0,1,0)
        self.down = (0,0,-1)
    
        self.position = position
        self.rotation = rot
        self.scale = scale

        self._calculate_global_tranform()
    
    def Translate(self, vector):
        self.Set_pos(vector3.add(self.position, vector))
            
    def Set_pos(self, position):
        self.position = position
        
        self._update_mesh_()

        for child in self.children:
            child.global_transform = child._calculate_global_tranform()
    
    def Rotate(self, angle = 0, axis = (0, 0, 0), rotation = Quaternion(1,(0,0,0))):
        """Rotation of the object"""
        if axis == (0,0,0):
            self.rotation = Quaternion.composite_rotations(self.rotation, rotation)
        else:
            rotQuaternion = Quaternion.from_angle_axis(angle, axis)
            self.rotation = Quaternion.composite_rotations(self.rotation, rotQuaternion)
        
        self._update_mesh_()
            
        self.forward =  Quaternion.rotate_vector((1,0,0), self.rotation)
        self.backward =  vector3.scale(self.forward, -1)
        self.right =  Quaternion.rotate_vector((0,-1,0), self.rotation)
        self.left =  vector3.scale(self.right, -1)
        self.up =  Quaternion.rotate_vector((0,0,1), self.rotation)
        self.down =  vector3.scale(self.up, -1)

    def set_parent(self, parent_transform):
        self.parent = parent_transform
        parent_transform.children.add(self)
        
    def scale(self, scale):
        self.scale = vector3.scale_by_vector(self.scale, scale)
        
        self._update_mesh_()
        
    def _rotate_vertex_(self, vertex_init):
        resultant_local_pos = Quaternion.rotate_vector(vertex_init, self.rotation)
        resultant_global_pos = vector3.add(resultant_local_pos, self.position)
        return resultant_global_pos
    
    def _update_mesh_(self):
        if not 'mesh' in dir(self.object):
            return
        mesh = self.object.mesh
        if 'vertices' in dir(mesh):
            for i in range(0,len(mesh.vertices_init)):
                vertex = vector3.scale_by_vector(mesh.vertices_init[i], self.scale)
                mesh.vertices[i] = self._rotate_vertex_(vertex)
                
                
        if 'edges' in dir(mesh):
            for i in range(0,len(mesh.edges_init)):
                vertex_a = vector3.scale_by_vector(mesh.edges_init[i].A, self.scale)
                vertex_b = vector3.scale_by_vector(mesh.edges_init[i].B, self.scale)
                mesh.edges[i].A = self._rotate_vertex_(vertex_a)
                mesh.edges[i].B = self._rotate_vertex_(vertex_b)
                
        if 'faces' in dir(mesh):
            for i in range(0,len(mesh.faces_init)):
                for k in range(0, len(mesh.faces_init[i].vertex)):
                    vertex = vector3.scale_by_vector(mesh.faces_init[i].vertex[k], self.scale)
                    mesh.faces[i].vertex[k] = self._rotate_vertex_(vertex)
                mesh.faces[i].normal = Quaternion.rotate_vector(mesh.faces_init[i].normal, self.rotation)
                
    def get_global_transform(self):
        return self._global_transform

    def _calculate_global_tranform(self):
        if not self.parent:
            self._global_transform = self
            return

        parent_global_transform = self.parent.get_global_transform()

        position = vector3.add(parent_global_transform.position, Quaternion.rotate_vector(self.position, parent_global_transform.rotation))
        rotation = Quaternion.composite_rotations(self.rotation, parent_global_transform.rotation)
        scale = Quaternion.rotate_vector(self.scale, parent_global_transform.rotation)
        obj = self.object
        
        transform = Transform(obj, position, rotation, scale)
        
        transform.forward =  Quaternion.rotate_vector(self.forward, parent_global_transform.rotation)
        transform.backward =  Quaternion.rotate_vector(self.backward, parent_global_transform.rotation)
        transform.right =  Quaternion.rotate_vector(self.right, parent_global_transform.rotation)
        transform.left =  Quaternion.rotate_vector(self.left, parent_global_transform.rotation)
        transform.up =  Quaternion.rotate_vector(self.up, parent_global_transform.rotation)
        transform.down =  Quaternion.rotate_vector(self.down, parent_global_transform.rotation)
        
        self._global_transform = transform