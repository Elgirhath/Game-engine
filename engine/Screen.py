import math
import time

import pygame
from engine import BasicStructures, Geometry, Mesh, Other, pyinit, settings
from engine.Geometry import Plane
from engine.Quaternion import Quaternion
from engine.Ray import Ray
from engine.render.world_screen_space_converter import world_to_screen_edge_unclamped
from engine.render.world_to_screen_face_converter import world_to_screen_face
from engine.Transform import Transform
from engine.util.world_local_space_converter import Local_to_world_space
from engine.Vector import Vector

all_cameras = []
global main_camera

class Camera():    
    def __init__(self, position, rotation = Quaternion.identity(), scale = (1,1,1), main = True, resolution = (1200, 600)):
        self.transform = Transform(self, position, rotation, scale)
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
        
        self.middle_pixel = (int(Vector.Scale(main_camera.resolution, (1/2))[0]), int(Vector.Scale(main_camera.resolution, (1/2))[1]))
        self.left_top_pixel = (0,0)
        self.right_top_pixel = (self.resolution[0],0)
        self.left_bottom_pixel = (0, self.resolution[1])
        self.right_bottom_pixel = (self.resolution[0], self.resolution[1])

    def get_clipping_plane(self):
        tr = self.transform.get_global_transform()
        normal = tr.forward
        point = Vector.Add(tr.position, Vector.Scale(tr.forward, self.clip_min))
        return Plane.From_normal(normal, point)

    
"""****************************  Funkcje  ***************************************"""

def Is_visible2d(point):
    if point[0]<=0 or point[0]>=main_camera.resolution[0] or point[1]<=0 or point[1]>=main_camera.resolution[1]:
        return False
    else:
        return True
    
def Render():
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
    return Vector.dot(Vector.Difference(face.vertex[0], Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), face.normal) > 0

def _write_(msg, size, coordinates, bold = 0, color = (255,255,255)):
    font = pygame.font.SysFont("Arial", size)
    if bold:
        font.set_bold(bold)
    label = font.render(str(msg), 1, color)
    pyinit.game_display.blit(label, coordinates)
    
    
def log(*arg):
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
    tr = main_camera.transform.get_global_transform()
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
