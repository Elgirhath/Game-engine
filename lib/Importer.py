from lib.Quaternion import Quaternion
from lib import Mesh

def Import_obj(obj_file, position, rotation = Quaternion(1, (0,0,0)), scale = (1,1,1)):
    path = "models/" + obj_file
    obj_lines = open(path, "r").readlines()
    vertices = []
    edges = []
    normals = []
    faces = []
    for line in obj_lines:
        if line[0] == "v" and line[1] == " ":
            vertex_coords = []
            value = ""
            for sign in line:
                if ord(sign) == 45 or (ord(sign)>=48 and ord(sign)<=57) or ord(sign) == 46:
                    value += sign
                if ord(sign) == 32 and len(value)>0:
                    vertex_coords.append(float(value))
                    value = ""
            vertex_coords.append(float(value))
            vertex = tuple(vertex_coords)
            vertices.append(vertex)
            
        if line[0] == "v" and line[1] == "n" and line[2] == " ":
            normal_coords = []
            value = ""
            for sign in line:
                if ord(sign) == 45 or (ord(sign)>=48 and ord(sign)<=57) or ord(sign) == 46:
                    value += sign
                if ord(sign) == 32 and len(value)>0:
                    normal_coords.append(float(value))
                    value = ""
            normal_coords.append(float(value))
            normal = tuple(normal_coords)
            normals.append(normal)
            
        if line[0] == "f" and line[1] == " ":
            vertex_list = []
            value = ""
            slash_passed = False
            for sign in line:
                if ord(sign) == 45 or (ord(sign)>=48 and ord(sign)<=57) or ord(sign) == 46:
                    value += sign
                if ord(sign) == 47 and len(value)>0:
                    if not slash_passed:
                        vertex_list.append(vertices[int(value)-1])
                    slash_passed = True
                    value = ""
                if ord(sign) == 32 and len(value)>0:
                    slash_passed = False
                    normal = normals[int(value)-1]
                    value = ""
            
            
            faces.append(Mesh.Face(vertex_list, normal))
            face_edges = []
            
            if len(vertex_list) == 4:
                face_edges.append(Mesh.Edge(vertex_list[0], vertex_list[1]))
                face_edges.append(Mesh.Edge(vertex_list[1], vertex_list[2]))
                face_edges.append(Mesh.Edge(vertex_list[2], vertex_list[3]))
                face_edges.append(Mesh.Edge(vertex_list[3], vertex_list[0]))
#                print("Only triangles accepted")
            else:
                face_edges.append(Mesh.Edge(vertex_list[0], vertex_list[1]))
                face_edges.append(Mesh.Edge(vertex_list[1], vertex_list[2]))
                face_edges.append(Mesh.Edge(vertex_list[2], vertex_list[0]))
                
            for face_edge in face_edges:
                already_exists = False
                for edge in edges:
                    if edge.A == face_edge.A and edge.B == face_edge.B:
                        already_exists = True
                        break
                    if edge.A == face_edge.B and edge.B == face_edge.A:
                        already_exists = True
                        break
                    
                if not already_exists:
                    edges.append(face_edge)
            
    mesh = Mesh.Mesh(None, vertices, edges, faces)
    obj = Mesh.Object(position, rotation, scale, mesh)
    name = ""
    for i in range(0, len(obj_file)-4):
        name += obj_file[i]
    obj.name = name
    return obj