from engine.math import vector3

class Plane():
    def __init__(self, factor_tupple):
        self.factors = factor_tupple
        
    def normal(self):
        return (self.factors[0], self.factors[1], self.factors[2])
    
    def normalize(self):
        normal = self.normal()
        if vector3.magnitude(normal)!=0:
            scale = 1/vector3.magnitude(normal)
            normal = vector3.scale(normal, scale)
            d = self.factors[3]*scale
            self.factors = (normal[0], normal[1], normal[2], d)
            
    def Invert_normal(self):
        self.factors = vector3.scale(self.factors, -1)
        
    def Switch_normal_by_vector(self, vector):
        if vector3.dot(self.normal(), vector)<0:
            self.Invert_normal()
        
    def From_points(vertex1, vertex2, vertex3):
        plane_vector1 = vector3.subtract(vertex1, vertex2)
        plane_vector2 = vector3.subtract(vertex2, vertex3)
        normal = vector3.cross(plane_vector1, plane_vector2)
        normal = vector3.normalize(normal)
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*vertex1[0]-normal[1]*vertex1[1]-normal[2]*vertex1[2]
        plane = Plane((a,b,c,d))
        return plane

    def From_normal(normal, point):
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*point[0]-normal[1]*point[1]-normal[2]*point[2]
        plane = Plane((a,b,c,d))
        return plane
    
    def From_vectors(vector1, vector2, origin_point):
        normal = vector3.cross(vector1, vector2)
        normal = vector3.normalize(normal)
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*origin_point[0]-normal[1]*origin_point[1]-normal[2]*origin_point[2]
        plane = Plane((a,b,c,d))
        return plane
    
    def Contains_point(self, point):
        a = self.factors[0]
        b = self.factors[1]
        c = self.factors[2]
        d = self.factors[3]
        
        x = point[0]
        y = point[1]
        z = point[2]
        
        return abs(a*x + b*y + c*z + d) < 1e-6
    
    def get_signed_distance_to_point(self, point):
        """
            Returns:
                0 if point lays on the plane
                distance from the plane if point is on positive side of plane
                Negative distance if point is on negative side of plane
        """
        if self.factors[2] != 0.0:
            plane_point = (0.0, 0.0, -self.factors[3] / self.factors[2])
        elif self.factors[1] != 0.0:
            plane_point = (0.0, -self.factors[3] / self.factors[1], 0.0)
        else:
            plane_point = (-self.factors[3] / self.factors[0], 0.0, 0.0)

        points_diff = vector3.subtract(point, plane_point)
        return vector3.dot(points_diff, self.normal())
        
    def string(self):
        return str(self.factors[0]) + "*x + " + str(self.factors[1]) + "*y + " + str(self.factors[2]) + "*z + " + str(self.factors[3]) + " = 0"

    def string_z(self):
        return "z = " + "(-"+str(self.factors[0]) + "*x - " + str(self.factors[1]) + "*y - " + str(self.factors[3])+ ") / " + str(self.factors[2])

    def Is_point_between_planes(plane1, plane2, point):
        rel_pos1 = plane1.get_signed_distance_to_point(point)
        rel_pos2 = plane2.get_signed_distance_to_point(point)
        if rel_pos1 < 0 or rel_pos2 < 0:
            return False
        else:
            return True
    
def Axis_view(point, axis):
    k = vector3.dot(point, axis)/vector3.magnitude(point)**2
    return k