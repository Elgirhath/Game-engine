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
from engine.math import vector3, vector2
from engine.render import text_renderer
from engine.render.camera import camera
    
"""****************************  Funkcje  ***************************************"""

def Is_visible2d(point):
    return point[0] > 0 and point[0] < camera.main_camera.resolution[0] and point[1] > 0 and point[1] < camera.main_camera.resolution[1]
    
def Render():
    for face in Mesh.all_faces:
        draw_face(face, face.material.color, pyinit.game_display)

def render_text():
    text_renderer.render()

def draw_edge(edge, color, display):
    edge2d = world_to_screen_edge_unclamped(edge, main_camera)
    if edge2d:
        pygame.draw.line(display, color, edge2d.A, edge2d.B, 3)

def draw_face(face, color, display):
    if should_face_be_backwards_culled(face):
        return

    vertices = world_to_screen_face(face, camera.main_camera)

    if vertices:
        pygame.draw.polygon(display, color, vertices)

def should_face_be_backwards_culled(face):
    return vector3.dot(vector3.subtract(face.vertex[0], Local_to_world_space(camera.main_camera.transform.position, camera.main_camera.parent.transform)), face.normal) > 0
    
    
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
        text_renderer.write(msg, 15, coordinates)

def Ray_on_pixel(point2d):
    cam = camera.main_camera
    tr = cam.transform.get_global_transform()
    dist_from_mid = vector2.subtract(point2d, cam.middle_pixel)
    tg_alfa = math.tan(math.radians(cam.FOV/2))*dist_from_mid[0]/(cam.resolution[0]/2)
    tg_beta = math.tan(math.radians(cam.FOV_vertical/2))*dist_from_mid[1]/(cam.resolution[1]/2)
    direction = vector3.add(vector3.add(tr.forward, vector3.scale(tr.right, tg_alfa)), vector3.scale(tr.down, tg_beta))
    direction = vector3.normalize(direction)
    ray = Ray(tr.position, direction)
    return ray

def Screen_to_world(point2d, distance):
    ray = Ray_on_pixel(point2d)
    point = vector3.add(ray.origin, vector3.scale(ray.direction, distance))
    return point
