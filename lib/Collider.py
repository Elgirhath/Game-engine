class Sphere_collider():
    def __init__ (self, parent, center, radius):
        self.parent = parent
        self.center = center
        self.radius = radius
        
    def Collide(self, other):
        from lib.Vector import Vector
        if type(other) is Sphere_collider:
            if Vector.Distance(other.center, self.center) <= self.radius + other.radius:
                return True
        return False
            
class Box_collider():
    from lib.Quaternion import Quaternion
    def __init__(self, parent, center, size_tuple, rotation = Quaternion(1, (0,0,0))):
        from lib import Mesh
        self.parent = parent
        self.center = center
        self.size = size_tuple
        self.rotation = rotation
    
        self.normals = [(1,0,0),
                        (0,-1,0),
                        (0,0,1),
                        (-1,0,0),
                        (0,1,0),
                        (0,0,-1)]
        self.points = [(self.size[0], self.size[1], self.size[2]),
                       (self.size[0], self.size[1], -self.size[2]),
                       (self.size[0], -self.size[1], self.size[2]),
                       (self.size[0], -self.size[1], -self.size[2]),
                       (-self.size[0], self.size[1], self.size[2]),
                       (-self.size[0], self.size[1], -self.size[2]),
                       (-self.size[0], -self.size[1], self.size[2]),
                       (-self.size[0], -self.size[1], -self.size[2])]
        
        self.faces = [Mesh.Face((self.points[0], self.points[1], self.points[2], self.points[3])),
                      Mesh.Face((self.points[4], self.points[5], self.points[6], self.points[7])),
                      Mesh.Face((self.points[0], self.points[1], self.points[4], self.points[5])),
                      Mesh.Face((self.points[2], self.points[3], self.points[6], self.points[7])),
                      Mesh.Face((self.points[0], self.points[2], self.points[4], self.points[6])),
                      Mesh.Face((self.points[1], self.points[3], self.points[5], self.points[7])),
                      ]
        
    def Collide(self, other):
        if type(other) is Box_collider:
            if SAT_collision(self, other):
                return True
        return False
            
class Collision():
    def __init__ (self, other, point):
        self.other = other
        self.point = point
        
def SAT_collision(collider1, collider2):
    from lib.Vector import Vector
    from lib.Quaternion import Quaternion
    points1 = list(collider1.points)
    center1 = Vector.Add(collider1.parent.transform.position, Quaternion.Vector_quaternion_rotate(collider1.center, collider1.parent.transform.rotation))
    for i in range(0, len(points1)):
        points1[i] = Quaternion.Vector_quaternion_rotate(points1[i], collider1.parent.transform.rotation)
        points1[i] = Vector.Add(points1[i], center1)
        
        
    points2 = list(collider2.points)
    center2 = Vector.Add(collider2.parent.transform.position, Quaternion.Vector_quaternion_rotate(collider2.center, collider2.parent.transform.rotation))
    for i in range(0, len(points2)):
        points2[i] = Quaternion.Vector_quaternion_rotate(points2[i], collider2.parent.transform.rotation)
        points2[i] = Vector.Add(points2[i], center2)
    
    
    for normal in collider1.normals:
        rotated_normal = Quaternion.Vector_quaternion_rotate(Quaternion.Vector_quaternion_rotate(normal, collider1.rotation), collider1.parent.transform.rotation)
        min1 = None
        max1 = None
        for point in points1:
            axis_view = Vector.dot(rotated_normal, point)
            if min1 == None or min1 > axis_view:
                min1 = axis_view
            if max1 == None or max1 < axis_view:
                max1 = axis_view
                
        min2 = None
        max2 = None
        for point in points2:
            axis_view = Vector.dot(rotated_normal, point)
            if min2 == None or min2 > axis_view:
                min2 = axis_view
            if max2 == None or max2 < axis_view:
                max2 = axis_view
                
        if min1>max2 or max1<min2:
            return False
        
    for normal in collider2.normals:
        rotated_normal = Quaternion.Vector_quaternion_rotate(Quaternion.Vector_quaternion_rotate(normal, collider2.rotation), collider2.parent.transform.rotation)
        min1 = None
        max1 = None
        for point in points1:
            axis_view = Vector.dot(rotated_normal, point)
            if min1 == None or min1 > axis_view:
                min1 = axis_view
            if max1 == None or max1 < axis_view:
                max1 = axis_view
                
        min2 = None
        max2 = None
        for point in points2:
            axis_view = Vector.dot(rotated_normal, point)
            if min2 == None or min2 > axis_view:
                min2 = axis_view
            if max2 == None or max2 < axis_view:
                max2 = axis_view
                
        if max1<min2 or min1>max2:
            return False
    return True

def Point_collision(box, point):
    from lib.Quaternion import Quaternion
    from lib.Vector import Vector
    box_center = Vector.Add(box.parent.transform.position, Quaternion.Vector_quaternion_rotate(box.center, box.parent.transform.rotation))
    rotated_point = Quaternion.Vector_quaternion_rotate(Vector.Difference(point, box_center), box.parent.transform.rotation.conjugate())
    if abs(rotated_point[0]) > box.size[0]*box.parent.transform.scale[0]:
        return False
    if abs(rotated_point[1]) > box.size[1]*box.parent.transform.scale[1]:
        return False
    if abs(rotated_point[2]) > box.size[2]*box.parent.transform.scale[2]:
        return False
    return True