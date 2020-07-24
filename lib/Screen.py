import math
from lib import Other
from lib import BasicStructures
from lib.Vector import Vector
from lib import Geometry
from lib.Quaternion import Quaternion
from lib.render.edge_render_helper import trim_edge_to_visible
import time

all_cameras = []
global main_camera

class Camera():    
    def __init__(self, position, rotation = Quaternion(1,(0,0,0)), scale = (1,1,1), main = True, resolution = (1200, 600)):
        from lib.Transform import Transform
        self.transform = Transform(self, position, rotation, scale)
        self.global_transform = None
        if main == True or len(all_cameras)==0:
            for cam in all_cameras:
                cam.main = False
            self.main = True
        all_cameras.append(self)
        global main_camera
        main_camera = self
        
        self.parent = None
        
        self.clip_min = 0.1
        self.clip_max = 100
        self.resolution = resolution
        self.aspect_ratio = resolution[0]/resolution[1]
        self.FOV = 120
        
        """tg(FOV/2) = tg(FOV_vertical/2)*aspect_ratio"""
        
        self.FOV_vertical = math.degrees(math.atan((math.tan(math.radians(self.FOV/2))/self.aspect_ratio)))*2
        self.pyramid = View_pyramid(self)
        
        self.middle_pixel = (int(Vector.Scale(main_camera.resolution, (1/2))[0]), int(Vector.Scale(main_camera.resolution, (1/2))[1]))
        self.left_top_pixel = (0,0)
        self.right_top_pixel = (self.resolution[0],0)
        self.left_bottom_pixel = (0, self.resolution[1])
        self.right_bottom_pixel = (self.resolution[0], self.resolution[1])
        
class View_pyramid():
    def __init__(self, cam):
        self.cam = cam
    
    def Top(self):
        from lib.Geometry import Plane
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.right, cam.FOV_vertical/2)
        plane = Plane.From_vectors(vector, tr.right, tr.position)
        self.top = plane
        return plane.factors
    
    def Bottom(self):
        from lib.Geometry import Plane
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.right, -cam.FOV_vertical/2)
        plane = Plane.From_vectors(tr.right, vector, tr.position)
        self.bottom = plane
    
    def Left(self):
        from lib.Geometry import Plane
        cam = main_camera
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.up, cam.FOV/2)
        plane = Plane.From_vectors(vector, tr.up, tr.position)
        self.left = plane
    
    def Right(self):
        from lib.Geometry import Plane
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.up, -cam.FOV/2)
        plane = Plane.From_vectors(tr.up, vector, tr.position)
        self.right = plane
    
    def Clip(self):
        from lib.Geometry import Plane
        cam = self.cam
        tr = cam.global_transform
        normal = tr.forward
        point = Vector.Add(tr.position, Vector.Scale(tr.forward, cam.clip_min))
        plane = Plane.From_normal(normal, point)
        self.clip = plane
        
    def Update(self):
        self.cam.global_transform = self.cam.transform.To_global()
        self.Top()
        self.Bottom()
        self.Left()
        self.Right()
        self.Clip()
        self.all_planes = []
        self.all_planes.append(self.top)
        self.all_planes.append(self.bottom)
        self.all_planes.append(self.left)
        self.all_planes.append(self.right)
        self.all_planes.append(self.clip)
    
    
"""****************************  Zmienne globalne i bufory  ***************************************"""
    

    
"""****************************  Funkcje  ***************************************"""
    
    
def World_to_screen(point):
    """Get view of the point on screen"""
    from lib.Geometry import Plane
    tr = main_camera.global_transform
    
    screen_plane = Plane.From_normal(tr.forward, point)
    screen_middle_point = Vector.Add(tr.position, Vector.Plane_cross_point(tr.position, tr.forward, screen_plane))
        
    screen_width = math.tan(math.radians(main_camera.FOV/2))*Vector.Magnitude(Vector.Difference(screen_middle_point, tr.position))*2
    screen_height = screen_width / main_camera.aspect_ratio
    
    component_vector_scalars = Vector.convert_to_different_space(Vector.Difference(point, screen_middle_point), tr.right, tr.down, tr.forward)

    point_right_vector = Vector.Vector_round(Vector.Add(Vector.Scale(tr.right, screen_width/2), Vector.Scale(tr.right, component_vector_scalars[0])))
    point_down_vector = Vector.Vector_round(Vector.Add(Vector.Scale(tr.down, screen_height/2), Vector.Scale(tr.down, component_vector_scalars[1])))
    point_right = Vector.Magnitude(point_right_vector)/screen_width
    point_down = Vector.Magnitude(point_down_vector)/screen_height
    scale_right = Vector.Scale_div(point_right_vector, tr.right)
    if scale_right<0:
        point_right=-point_right
    scale_down = Vector.Scale_div(point_down_vector, tr.down)
    if scale_down<0:
        point_down=-point_down
    return (point_right * main_camera.resolution[0], point_down * main_camera.resolution[1])



def Is_visible3d(point):
    threshold = 0
    if main_camera.pyramid.top.get_signed_distance_to_point(point) < threshold:
        return False
    elif main_camera.pyramid.bottom.get_signed_distance_to_point(point) < threshold:
        return False
    elif main_camera.pyramid.left.get_signed_distance_to_point(point) < threshold:
        return False
    elif main_camera.pyramid.right.get_signed_distance_to_point(point) < threshold:
        return False
    elif main_camera.pyramid.clip.get_signed_distance_to_point(point) < threshold:
        return False
    else:
        return True

def Is_visible2d(point):
    if point[0]<=0 or point[0]>=main_camera.resolution[0] or point[1]<=0 or point[1]>=main_camera.resolution[1]:
        return False
    else:
        return True
    
def Render():
    from lib import Mesh
    from lib import pyinit
    for face in Mesh.all_faces:
        Draw(face, face.material.color, pyinit.game_display)

def Draw(obj, color, display):
    import pygame
    from lib import Mesh
    if type(obj) is Mesh.Edge:
        edge2d = World_to_screen_edge(obj)
        if edge2d:
            pygame.draw.line(display, color, edge2d.A, edge2d.B, 3)
                    
    if type(obj) is BasicStructures.Cube:
        for edge in obj.edges:
            Draw(edge, color, display)
            
    if type(obj) is Mesh.Object:
        if 'mesh' in dir(obj):
            Draw(obj.mesh, color, display)
            
    if type(obj) is Mesh.Mesh:
        for face in obj.faces:
            if Vector.dot(Vector.Difference(face.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), face.normal)<=0:
                Draw(face, color, display)
#        for edge in obj.edges:
#            Draw(edge, color, display)
            
    if type(obj) is Mesh.Face:
        if not Vector.dot(Vector.Difference(obj.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), obj.normal)<=0:
            return
        edges = []
        if len(obj.vertex) == 3:
            edges.append(Mesh.Edge(obj.vertex[0], obj.vertex[1]))
            edges.append(Mesh.Edge(obj.vertex[1], obj.vertex[2]))
            edges.append(Mesh.Edge(obj.vertex[2], obj.vertex[0]))
        elif len(obj.vertex) == 4:
            edges.append(Mesh.Edge(obj.vertex[0], obj.vertex[1]))
            edges.append(Mesh.Edge(obj.vertex[1], obj.vertex[2]))
            edges.append(Mesh.Edge(obj.vertex[2], obj.vertex[3]))
            edges.append(Mesh.Edge(obj.vertex[3], obj.vertex[0]))
        vertices = []
        for edge in edges:
            screen_edge = World_to_screen_edge(edge)
            if screen_edge:
                exists = False
                for i in range(0, len(vertices)):
                    if vertices[i] == screen_edge.A:
                        exists = True
                if not exists:
                    vertices.append(screen_edge.A)
                exists = False
                for i in range(0, len(vertices)):
                    if vertices[i] == screen_edge.B:
                        exists = True
                if not exists:
                    vertices.append(screen_edge.B)
        
        face_plane = Geometry.Plane.From_normal(obj.normal, obj.vertex[0])
        pixels = [main_camera.left_top_pixel,
                  main_camera.left_bottom_pixel,
                  main_camera.right_top_pixel,
                  main_camera.right_bottom_pixel]
        
        for pixel in pixels:
            ray = Ray_on_pixel(pixel)
            intersection = ray.Intersect_point(face_plane)
            if intersection:
                if Geometry.Point_in_polygon(intersection, obj.vertex):
                    vertices.append(pixel)
                    
            
        if len(vertices)>2:
            center = Geometry.Center_of_mass(vertices)
            vertices = Geometry.Sort_clockwise(vertices, center)
            pygame.draw.polygon(display, color, vertices)
    
def World_to_screen_edge(edge):
    from lib import Mesh
    from lib.Ray import Ray

    trimmed_edge = trim_edge_to_visible(edge.A, edge.B, main_camera)
                
    if trimmed_edge:
        origin_pos = World_to_screen(trimmed_edge.A)
        end_pos = World_to_screen(trimmed_edge.B)
        return Mesh.Edge(origin_pos, end_pos)
    else:
        return None

def _write_(msg, size, coordinates, bold = 0, color = (255,255,255)):
    import pygame
    from lib import pyinit
    font = pygame.font.SysFont("Arial", size)
    if bold:
        font.set_bold(bold)
    label = font.render(str(msg), 1, color)
    pyinit.game_display.blit(label, coordinates)
    
    
def log(*arg):
    import settings
    if len(arg)<2:
        print("No kind of log function receives ", len(arg), " arguments")
    elif type(arg[len(arg)-1]) is tuple:
        coordinates = arg[len(arg)-1]
        msg = ""
        for i in range(0, len(arg)-1):
            
            if type(arg[i]) is str:
                msg += arg[i]
                
            elif type(arg[i]) is int or type(arg[i]) is float or type(arg[i]) is complex:
                msg+=str(round(arg[i], settings.round_digits))
                
            elif type(arg[i]) is tuple:
                msg+="("
                for j in range(0,len(arg[i])):
                    if j != 0:
                        msg+=", "
                    msg+=str(round(arg[i][j], settings.round_digits))
                msg += ")"
                    
            elif type(arg[i]) is bool:
                msg += str(arg[i])
            elif type(arg[i]) is list:
                msg+="["
                for j in range(0,len(arg[i])):
                    if j != 0:
                        msg+=", "
                    msg+=str(round(arg[i][j], settings.round_digits))
                msg += "]"
        _write_(msg, 15, coordinates)

def Ray_on_pixel(point2d):
    from lib.Vector import Vector
    import math
    from lib.Ray import Ray
    tr = main_camera.global_transform
    dist_from_mid = Vector.Difference(point2d, main_camera.middle_pixel)
    tg_alfa = math.tan(math.radians(main_camera.FOV/2))*dist_from_mid[0]/(main_camera.resolution[0]/2)
    tg_beta = math.tan(math.radians(main_camera.FOV_vertical/2))*dist_from_mid[1]/(main_camera.resolution[1]/2)
    direction = Vector.Add(Vector.Add(tr.forward, Vector.Scale(tr.right, tg_alfa)), Vector.Scale(tr.down, tg_beta))
    direction = Vector.Normalize(direction)
    ray = Ray(tr.position, direction)
    return ray

def Screen_to_world(point2d, distance):
    ray = Ray_on_pixel(point2d)
    point = Vector.Add(ray.origin, Vector.Scale(ray.direction, distance))
    return point