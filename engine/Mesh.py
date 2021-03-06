from engine import Collider, Color, Geometry
from engine.Quaternion import Quaternion
from engine.Rigidbody import Rigidbody
from engine.Transform import Transform
from engine.math import vector3

global all_faces
all_faces = []
objects = []

class Object():
    def __init__(self, position, rotation = Quaternion(1, (0,0,0)), scale = (1,1,1), mesh = None, collider = None, name = "Default", material = None, parent = None):
        self.parent = parent
        self.transform = Transform(self, position, rotation, scale)
        if not material:
            self.material = Color.default_material
        else:
            self.material = material
        
        self.mesh = mesh
        if self.mesh:
            self.mesh.parent = self
            for face in self.mesh.faces_init:
                face.material = self.material
            for face in self.mesh.faces:
                face.material = self.material
                
        self.collider = collider
        if mesh and not collider:
            self.Calculate_collider()
            
        self.transform._update_mesh_()
        self.rigidbody = Rigidbody(self)
        
        if self.mesh == None:
            name = "Empty"
            
        self.name = None
        for obj in objects:
            if obj.name == name:
                i = 1
                name = name + "[" + str(i) + "]"
                self.name = name
                
        if not self.name:
            self.name = name
        
        objects.append(self)
            
    def Calculate_collider(self):
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        min_z = None
        max_z = None
        for vertex in self.mesh.vertices_init:
            if not min_x or min_x > vertex[0]:
                min_x = vertex[0]
            if not max_x or max_x < vertex[0]:
                max_x = vertex[0]
            if not min_y or min_y > vertex[1]:
                min_y = vertex[1]
            if not max_y or max_y < vertex[1]:
                max_y = vertex[1]
            if not min_z or min_z > vertex[2]:
                min_z = vertex[2]
            if not max_z or max_z < vertex[2]:
                max_z = vertex[2]
                
        collider_center = ((max_x+min_x)/2, (max_y+min_y)/2, (max_z+min_z)/2)
        collider_size = ((max_x-min_x)/2, (max_y-min_y)/2, (max_z-min_z)/2)
        self.collider = Collider.Box_collider(self, collider_center, collider_size)
        
    def Set_collider(self, center, size, rotation = Quaternion(1, (0,0,0))):
        self.collider = Collider.Box_collider(self, center, size, rotation)
        
    def Set_mesh(self, mesh):
        self.mesh = mesh
        self.mesh.parent = self
        
    def add_camera(self, camera):
        self.camera = camera
        camera.transform.set_parent(self.transform)
        camera.parent = self
    
    def Destroy(self):
        if self == None:
            return
        print(self.mesh)
        for face in self.mesh.faces:
            for i in range(0, len(all_faces)):
                if all_faces[i] == face:
                    all_faces.pop(i)
                    break
        for i in range(0, len(objects)):
            if objects[i] == self:
                objects.pop(i)
                return
            
    def Set_material(self, material):
        if not material:
            return
        else:
            self.material = material
            if self.mesh:
                self.mesh.parent = self
                for face in self.mesh.faces_init:
                    face.material = self.material
                for face in self.mesh.faces:
                    face.material = self.material

class Mesh():
    def __init__(self, parent, vertex_list, edge_list, face_list, material = None):
        self.parent = parent
        self.vertices_init = vertex_list
        self.edges_init = edge_list
        self.faces_init = face_list
        
        self.vertices = []
        self.edges = []
        self.faces = []
        
        for vertex_init in self.vertices_init:    
            self.vertices.append(vertex_init)
        for edge_init in self.edges_init:    
            vertex_a = edge_init.A
            vertex_b = edge_init.B
            self.edges.append(Edge(vertex_a, vertex_b))
        for face_init in self.faces_init:    
            vertex_list = []
            for vertex in face_init.vertex:
                vertex_list.append(vertex)
            face = Face(vertex_list, face_init.normal)
            self.faces.append(face)
            
            global all_faces
            all_faces.append(face)

class Face():
    def __init__(self, vertex_list, normal = (0,0,0), mesh = None, material = Color.default_material):
        self.mesh = mesh
        self.vertex = vertex_list
        if normal == (0,0,0):
            self.normal = self.Calculate_normal()
        else:
            self.normal = normal
        
        self.material = material
    
    def Plane(self):
        a = self.normal[0]
        b = self.normal[1]
        c = self.normal[2]
        d = -self.normal[0]*self.vertex[0][0]-self.normal[1]*self.vertex[0][1]-self.normal[2]*self.vertex[0][2]
        return Geometry.Plane((a,b,c,d))
    
    def Calculate_normal(self, inverted = False):
        plane_vector1 = vector3.subtract(self.vertex[0], self.vertex[1])
        plane_vector2 = vector3.subtract(self.vertex[1], self.vertex[2])
        normal = vector3.cross(plane_vector1, plane_vector2)
        normal = vector3.normalize(normal)
        if not inverted:
            return normal
        else:
            return vector3.scale(normal, -1)

    def get_edges(self):
        edges = []
        if len(self.vertex) == 3:
            edges.append(Edge(self.vertex[0], self.vertex[1]))
            edges.append(Edge(self.vertex[1], self.vertex[2]))
            edges.append(Edge(self.vertex[2], self.vertex[0]))
        elif len(self.vertex) == 4:
            edges.append(Edge(self.vertex[0], self.vertex[1]))
            edges.append(Edge(self.vertex[1], self.vertex[2]))
            edges.append(Edge(self.vertex[2], self.vertex[3]))
            edges.append(Edge(self.vertex[3], self.vertex[0]))
        else:
            raise Exception("Invalid number of vertices. Should equal to 3 or 4")

        return edges

        
class Edge():
    def __init__(self, start_pos, end_pos):
        self.A = start_pos
        self.B = end_pos

def _sort_faces_():
    #TODO: FIX THIS
    switch = True
    while switch:
        switch = False
        for i in range(0, len(all_faces)-1):
            if vector3.dot(all_faces[i].normal, Screen.main_camera.global_transform.forward)<0:
                vc = all_faces[i].normal
            else:
                vc = vector3.scale(all_faces[i].normal, -1)
            above = True
            below = True
            for vertex in all_faces[i+1].vertex:
                if Geometry.Axis_view(vc, vector3.subtract(vertex, all_faces[i].vertex[0]))>=0:
                    below = False
                else:
                    above = False
            if not above and not below:
                if vector3.dot(all_faces[i+1].normal, Screen.main_camera.global_transform.forward)<0:
                    vc = all_faces[i+1].normal
                else:
                    vc = vector3.scale(all_faces[i+1].normal, -1)
                above = True
                below = True
                for vertex in all_faces[i].vertex:
                    if Geometry.Axis_view(vc, vector3.subtract(vertex, all_faces[i+1].vertex[0]))>=0:
                        below = False
                    else:
                        above = False
                if above:
                    all_faces[i], all_faces[i+1] = all_faces[i+1], all_faces[i]
                    switch = True
            elif below:
                all_faces[i], all_faces[i+1] = all_faces[i+1], all_faces[i]
                switch = True
                
#def _sort_better_():
#    import Screen
#    from engine.Ray import Ray
#    tr = Screen.main_camera.global_transform
#    sorted_list = []
#    for face in all_faces:
#        for vertex in face.vertex:
#            distance = vector3.distance(vertex, tr.position)
#            ray_dir = vector3.subtract(vertex, tr.position)
#            ray_ori = tr.position
#            ray = Ray(ray_ori, vector3.normalize(ray_dir))
#            for i in range(0, len(sorted_list)):
#                intersection = ray.Face_intersection(sorted_list[i])
#                if not intersection:
#                    continue
#                if vector3.distance(intersection, tr.position)<distance and vector3.distance(intersection, tr.position)>0
