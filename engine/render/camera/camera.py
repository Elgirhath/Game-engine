from engine.Quaternion import Quaternion
from engine.Transform import Transform
from engine.Vector import Vector
from engine.Geometry import Plane
import math

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
        
        # tg(FOV/2) = tg(FOV_vertical/2)*aspect_ratio
        self.FOV_vertical = math.degrees(math.atan((math.tan(math.radians(self.FOV/2))/self.aspect_ratio)))*2
        
        self.middle_pixel = (int(Vector.Scale(main_camera.resolution, (1/2))[0]), int(Vector.Scale(main_camera.resolution, (1/2))[1]))
        self.left_top_pixel = (0,0)
        self.right_top_pixel = (self.resolution[0],0)
        self.left_bottom_pixel = (0, self.resolution[1])
        self.right_bottom_pixel = (self.resolution[0], self.resolution[1])

        self._clipping_plane_manager = ClippingPlaneManager(self)

    def get_clipping_plane(self):
        return self._clipping_plane_manager.get_clipping_plane()


class ClippingPlaneManager():
    def __init__(self, camera):
        self.camera = camera
        self.previous_position = camera.transform.position
        self.previous_rotation = camera.transform.rotation
        self.previous_scale = camera.transform.scale
        self.clipping_plane = self.recalculate()

    def get_clipping_plane(self):
        if self.was_transform_changed():
            self.recalculate()

        return self.clipping_plane

    def was_transform_changed(self):
        tr = self.camera.transform.get_global_transform()
        if self.previous_position != tr.position:
            return True
        
        if self.previous_rotation != tr.rotation:
            return True
            
        if self.previous_scale != tr.scale:
            return True

        return False
        
    def recalculate(self):
        tr = self.camera.transform.get_global_transform()
        normal = tr.forward
        point = Vector.Add(tr.position, Vector.Scale(tr.forward, self.camera.clip_min))
        self.clipping_plane = Plane.From_normal(normal, point)

        self.previous_position = tr.position
        self.previous_rotation = tr.rotation
        self.previous_scale = tr.scale