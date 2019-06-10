import math
import Other
import BasicStructures
from Vector import Vector
import Geometry
from Quaternion import Quaternion
import time

all_cameras = []
global main_camera

class Camera():    
    def __init__(self, position, rotation = Quaternion(1,(0,0,0)), scale = (1,1,1), main = True, resolution = (1200, 600)):
        from Transform import Transform
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
        from Geometry import Surface
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.right, cam.FOV_vertical/2)
        surface = Surface.From_vectors(vector, tr.right, tr.position)
        self.top = surface
        return surface.factors
    
    def Bottom(self):
        from Geometry import Surface
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.right, -cam.FOV_vertical/2)
        surface = Surface.From_vectors(tr.right, vector, tr.position)
        self.bottom = surface
    
    def Left(self):
        from Geometry import Surface
        cam = main_camera
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.up, cam.FOV/2)
        surface = Surface.From_vectors(vector, tr.up, tr.position)
        self.left = surface
    
    def Right(self):
        from Geometry import Surface
        cam = self.cam
        tr = cam.global_transform
        vector = tr.forward
        vector = Vector.Rotate(vector, tr.up, -cam.FOV/2)
        surface = Surface.From_vectors(tr.up, vector, tr.position)
        self.right = surface
    
    def Clip(self):
        from Geometry import Surface
        cam = self.cam
        tr = cam.global_transform
        normal = tr.forward
        point = Vector.Add(tr.position, Vector.Scale(tr.forward, cam.clip_min))
        surface = Surface.From_normal(normal, point)
        self.clip = surface
        
    def Update(self):
        self.cam.global_transform = self.cam.transform.To_global()
        self.Top()
        self.Bottom()
        self.Left()
        self.Right()
        self.Clip()
        self.all_surfaces = []
        self.all_surfaces.append(self.top)
        self.all_surfaces.append(self.bottom)
        self.all_surfaces.append(self.left)
        self.all_surfaces.append(self.right)
        self.all_surfaces.append(self.clip)
    
    
"""****************************  Zmienne globalne i bufory  ***************************************"""
    

    
"""****************************  Funkcje  ***************************************"""
    
    
def World_to_screen(point):
    """Get view of the point on screen"""
    from Geometry import Surface
    tr = main_camera.global_transform
    
    screen_surface = Surface.From_normal(tr.forward, point)
    screen_middle_point = Vector.Add(tr.position, Vector.Surface_cross_point(tr.position, tr.forward, screen_surface))
        
    screen_width = math.tan(math.radians(main_camera.FOV/2))*Vector.Magnitude(Vector.Difference(screen_middle_point, tr.position))*2
    screen_height = screen_width / main_camera.aspect_ratio
    
    component_vector_scalars = Vector.Distribution_between(Vector.Difference(point, screen_middle_point), tr.right, tr.down, tr.forward)

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
    if main_camera.pyramid.top.Point_relative_pos(point) < threshold:
        return False
    elif main_camera.pyramid.bottom.Point_relative_pos(point) < threshold:
        return False
    elif main_camera.pyramid.left.Point_relative_pos(point) < threshold:
        return False
    elif main_camera.pyramid.right.Point_relative_pos(point) < threshold:
        return False
    elif main_camera.pyramid.clip.Point_relative_pos(point) < threshold:
        return False
    else:
        return True

def Is_visible2d(point):
    if point[0]<=0 or point[0]>=main_camera.resolution[0] or point[1]<=0 or point[1]>=main_camera.resolution[1]:
        return False
    else:
        return True
    
def Render():
    import Mesh
    import pyinit
#    Mesh._sort_faces_()
#    for obj in Mesh.objects:
#        Draw(obj, obj.material.color, pyinit.game_display)
    for face in Mesh.all_faces:
        Draw(face, face.material.color, pyinit.game_display)

def Draw(obj, color, display):
    import pygame
    import Mesh
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
            if Vector.Dot_product(Vector.Difference(face.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), face.normal)<=0:
                Draw(face, color, display)
#        for edge in obj.edges:
#            Draw(edge, color, display)
            
    if type(obj) is Mesh.Face:
        if not Vector.Dot_product(Vector.Difference(obj.vertex[0], Vector.Local_to_world_space(main_camera.transform.position, main_camera.parent.transform)), obj.normal)<=0:
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
        
        face_surface = Geometry.Surface.From_normal(obj.normal, obj.vertex[0])
        pixels = [main_camera.left_top_pixel,
                  main_camera.left_bottom_pixel,
                  main_camera.right_top_pixel,
                  main_camera.right_bottom_pixel]
        
        for pixel in pixels:
            ray = Ray_on_pixel(pixel)
            intersection = ray.Intersect_point(face_surface)
            if intersection:
                if Geometry.Point_in_polygon(intersection, obj.vertex):
                    vertices.append(pixel)
                    
            
        if len(vertices)>2:
            center = Geometry.Center_of_mass(vertices)
            vertices = Geometry.Sort_clockwise(vertices, center)
            pygame.draw.polygon(display, color, vertices)
            
def _cut_edge_(origin, end):
    from Ray import Ray
    from Geometry import Surface
    ray = Ray(origin, Vector.Difference(end, origin))
    intersections = []
            
    top = main_camera.pyramid.top
    bottom = main_camera.pyramid.bottom
    right = main_camera.pyramid.right
    left = main_camera.pyramid.left
    clip = main_camera.pyramid.clip
            
    intersection = ray.Intersect_point(bottom)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                    
    intersection = ray.Intersect_point(right)
    if intersection:
        if Surface.Is_point_between_surfaces(top, bottom, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(left)
    if intersection:
        if Surface.Is_point_between_surfaces(top, bottom, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(top)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if clip.Point_relative_pos(intersection)>0:
                intersections.append(intersection)
                
    intersection = ray.Intersect_point(clip)
    if intersection:
        if Surface.Is_point_between_surfaces(right, left, intersection):
            if Surface.Is_point_between_surfaces(top, bottom, intersection):
                intersections.append(intersection)
                
    if len(intersections)<2:
        return None
    
    
    distance = Vector.Magnitude(Vector.Difference(end, origin))
    new_origin = None
    for intersection in intersections:
        inter_distance = Vector.Magnitude(Vector.Difference(intersection, origin))
        if inter_distance < distance:
            distance = inter_distance
            new_origin = intersection
    if new_origin:
        return new_origin
    else:
        return None
    
def World_to_screen_edge(edge):
    import Mesh
    from Ray import Ray
    
    if Is_visible3d(edge.A) and Is_visible3d(edge.B):
        origin_pos = World_to_screen(edge.A)
        end_pos = World_to_screen(edge.B)
        return Mesh.Edge(origin_pos, end_pos)
    elif Is_visible3d(edge.A) or Is_visible3d(edge.B):          
        inversed = False
        if Is_visible3d(edge.A):
            origin = edge.A
            end = edge.B
        else:
            inversed = True
            origin = edge.B
            end = edge.A
        ray = Ray(origin, Vector.Difference(end, origin))
        closest_intersection = None
        distance = None
        for surface in main_camera.pyramid.all_surfaces:
            if ray.Intersect_point(surface):
                intersection = ray.Intersect_point(surface)
                tmp_distance = Vector.Magnitude(Vector.Difference(intersection, ray.origin))
                if not distance or tmp_distance < distance:
                    distance = tmp_distance
                    closest_intersection = intersection
                    
        if not inversed:
            origin_pos = World_to_screen(origin)
            end_pos = World_to_screen(closest_intersection)
        else:
            origin_pos = World_to_screen(closest_intersection)
            end_pos = World_to_screen(origin)
        return Mesh.Edge(origin_pos, end_pos)
        
    else:
        origin = None
        end = None
        origin = _cut_edge_(edge.A, edge.B)
        end = _cut_edge_(edge.B, edge.A)
                    
        if origin and end:
            origin_pos = World_to_screen(origin)
            end_pos = World_to_screen(end)
            return Mesh.Edge(origin_pos, end_pos)
        else:
            return None

def _write_(msg, size, coordinates, bold = 0, color = (255,255,255)):
    import pygame
    import pyinit
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
    from Vector import Vector
    import math
    from Ray import Ray
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