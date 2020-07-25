import math
from lib import Other
from lib import BasicStructures
from lib.Vector import Vector
from lib import Geometry
from lib.Quaternion import Quaternion
import time
import pygame
from lib import Mesh
from lib.render.world_screen_space_converter import world_to_screen_edge_unclamped
from lib.render.world_to_screen_face_converter import world_to_screen_face

all_cameras = []
global main_camera

class Camera():    
    def __init__(self, position, rotation = Quaternion.identity(), scale = (1,1,1), main = True, resolution = (1200, 600)):
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
    from lib import pyinit
    for face in Mesh.all_faces:
        draw_face(face, face.material.color, pyinit.game_display)

def draw_mesh(mesh, color, display):
    for face in mesh.faces:
        if Vector.dot(Vector.Difference(face.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), face.normal)<=0:
            draw_face(face, color, display)

def draw_edge(edge, color, display):
    edge2d = world_to_screen_edge_unclamped(edge, main_camera)
    if edge2d:
        pygame.draw.line(display, color, edge2d.A, edge2d.B, 3)

def draw_face(face, color, display):
    if should_face_be_backwards_culled(face):
        return

    vertices = world_to_screen_face(face, main_camera)

    if vertices:
        pygame.draw.polygon(display, color, vertices)

def should_face_be_backwards_culled(face):
    return Vector.dot(Vector.Difference(face.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), face.normal) > 0

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