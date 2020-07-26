from engine.Quaternion import Quaternion
from engine.Vector import Vector
from engine.Transform import Transform
from engine.Mesh import Edge

class Cube():
    def __init__(self, position, rotation = Quaternion(1,(0,0,0)), scale = (1,1,1)):
        self.transform = Transform(self, position, rotation, scale)
        
        self.edges_init = []
        self.vertices_init = []
        
        self.vertices_init.append(Vector.Add((0.5,0.5,0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((0.5,-0.5,0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((-0.5,-0.5,0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((-0.5,0.5,0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((0.5,0.5,-0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((0.5,-0.5,-0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((-0.5,-0.5,-0.5), self.transform.position))
        self.vertices_init.append(Vector.Add((-0.5,0.5,-0.5), self.transform.position))
        
        self.edges_init.append(Edge(self.vertices_init[0], self.vertices_init[1]))
        self.edges_init.append(Edge(self.vertices_init[1], self.vertices_init[2]))
        self.edges_init.append(Edge(self.vertices_init[2], self.vertices_init[3]))
        self.edges_init.append(Edge(self.vertices_init[3], self.vertices_init[0]))
        self.edges_init.append(Edge(self.vertices_init[4], self.vertices_init[5]))
        self.edges_init.append(Edge(self.vertices_init[5], self.vertices_init[6]))
        self.edges_init.append(Edge(self.vertices_init[6], self.vertices_init[7]))
        self.edges_init.append(Edge(self.vertices_init[7], self.vertices_init[4]))
        self.edges_init.append(Edge(self.vertices_init[0], self.vertices_init[4]))
        self.edges_init.append(Edge(self.vertices_init[1], self.vertices_init[5]))
        self.edges_init.append(Edge(self.vertices_init[2], self.vertices_init[6]))
        self.edges_init.append(Edge(self.vertices_init[3], self.vertices_init[7]))
        
        self.edges = []
        self.vertices = []
        
        for edge in self.edges_init:
            A = edge.A
            B = edge.B
            self.edges.append(Edge(A, B))
            
        for vertex in self.vertices_init:
            self.vertices.append(vertex)
            
#        if rotation.struct !=(1,0,0,0):
#            self.transform.Rotate(rotation = rotation)