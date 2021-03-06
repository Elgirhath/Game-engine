from engine.util.is_point_in_polygon_resolver import is_point_in_polygon
from engine import Mesh
from engine.Quaternion import Quaternion
from engine.math import vector3
from engine import Collider

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
        
    def intersect_plane(self, plane):
        """
            pivot = (xp, yp, zp)
            direction = (xd, yd, zd)
            a(xp + kxd) + b(yp + kyd) + c(zp + kzd) + d = 0
            k(axd + byd + czd) = - axp - byp - czp - d
            1* - axp - byp - czp - d = 0
                pivot lays on the plane
            2* - axp - byp - czp - d != 0
                a) axd + byd + czd = 0
                    no intersection
                b) axd + byd + czd != 0
                    k = -(axp + byp + czp + d)/(axd + byd + czd)
                    ***** If k<0 - Ray doesn't really intersect!!! *****
        """
        a = plane.factors[0]
        b = plane.factors[1]
        c = plane.factors[2]
        d = plane.factors[3]
        xp = self.origin[0]
        yp = self.origin[1]
        zp = self.origin[2]
        xd = self.direction[0]
        yd = self.direction[1]
        zd = self.direction[2]
        if a*xp + b*yp + c*zp + d == 0:
            return (xp, yp, zp)
        else:
            if a*xd + b*yd + c*zd == 0:
                return None
            else:
                k = -(a*xp + b*yp + c*zp + d)/(a*xd + b*yd + c*zd)
#                print("k = ", k)
                if k>0:
                    return (xp + k*xd, yp + k*yd, zp + k*zd)
                else:
#                    print("no intersection")
                    return None
                
    def Face_intersection(self, face):
        intersection = self.intersect_plane(face.Plane())
        if intersection and is_point_in_polygon(intersection, face.vertex):
            return intersection
        else:
            return None
    
    def Collide(self, chosen_obj = None, ignore = None):
        k_min = None
        collider = None
        for obj in Mesh.objects:
            if ignore:
                if obj in ignore:
                    continue
            if chosen_obj:
                if chosen_obj != obj:
                    continue

            if 'collider' in dir(obj):
                if obj.collider:
                    if not chosen_obj and Collider.Point_collision(obj.collider, self.origin):
                        continue
                    
                    global_box_center = vector3.add(Quaternion.rotate_vector(obj.collider.center, obj.transform.rotation), obj.transform.position)
                    global_difference = vector3.subtract(self.origin, global_box_center)
                    local_ray_origin = Quaternion.rotate_vector(global_difference, obj.transform.rotation.conjugate())
                    local_ray_dir = Quaternion.rotate_vector(self.direction, obj.transform.rotation.conjugate())
                    
#                    size = (obj.collider.size[0] * obj.transform.scale[0], obj.collider.size[1] * obj.transform.scale[1], obj.collider.size[2] * obj.transform.scale[2])
                    size = obj.collider.size
                    for i in range(0, 3):
                        if local_ray_dir[i]!=0:
                            k = (-size[i] - local_ray_origin[i])/local_ray_dir[i]
                            if k>=0:
                                intersection = vector3.add(local_ray_origin, vector3.scale(local_ray_dir, k))
                                inside = True
                                for j in range(0, 3):
                                    if j!=i and abs(intersection[j])>size[j]:
                                        inside = False
                                if inside:
                                    if k_min == None or k_min > k:
                                        k_min = k
                                        collider = obj.collider
                                        
                            k = (size[i] - local_ray_origin[i])/local_ray_dir[i]
                            if k>=0:
                                intersection = vector3.add(local_ray_origin, vector3.scale(local_ray_dir, k))
                                inside = True
                                for j in range(0, 3):
                                    if j!=i and abs(intersection[j])>size[j]:
                                        inside = False
                                if inside:
                                    if k_min == None or k_min > k:
                                        k_min = k
                                        collider = obj.collider
                                    
        if k_min != None and collider != None:
            point = vector3.add(self.origin, vector3.scale(self.direction, k_min))
        else:
            point = None
            
        return Collider.Collision(collider, point)