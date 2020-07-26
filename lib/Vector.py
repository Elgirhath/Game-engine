import math

class Vector():
    def divide(vector_1, vector_2):
        if len(vector_1) == 3:
            return (vector_1[0]/vector_2[0],vector_1[1]/vector_2[1],vector_1[2]/vector_2[2])
        else:
            return (vector_1[0]/vector_2[0],vector_1[1]/vector_2[1])
            
    def Magnitude(vector):
        return math.sqrt(Vector.dot(vector, vector))
    
    def dot(vector_1, vector_2):
        a = vector_1[0]*vector_2[0]
        b = vector_1[1]*vector_2[1]

        if len(vector_1) == 2:
            return a + b

        c = vector_1[2]*vector_2[2]

        return a + b + c
    
    def Scale(vector, scalar):
        if len(vector) == 2:
            return (vector[0]*scalar, vector[1]*scalar)
        else:
            return (vector[0]*scalar, vector[1]*scalar, vector[2]*scalar)
    
    def Add(vector_1, vector_2):
        if len(vector_1) == 2:
            return (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1])
        else:
            return (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1], vector_1[2] + vector_2[2])
    
    def Scale_div(vector_1, vector_2):
        if len(vector_1) == 3:
            if vector_2[0] != 0:
                return vector_1[0]/vector_2[0]
            elif vector_2[1] != 0:
                return vector_1[1]/vector_2[1]
            elif vector_2[2] != 0:
                return vector_1[2]/vector_2[2]
            else:
                print("Scale_div divides by 0! Vector_2 = ", vector_2)
        
    def cross(vector_1, vector_2):
        if len(vector_1) == 2:
            return vector_1[0]*vector_2[1]-vector_1[1]*vector_2[0]
        else:
            return (vector_1[1]*vector_2[2]-vector_1[2]*vector_2[1], vector_1[2]*vector_2[0]-vector_1[0]*vector_2[2], vector_1[0]*vector_2[1]-vector_1[1]*vector_2[0])

    
    def Normalize(vector_1):
        """
            Scales vector_1 so that its magnitude is equal to 1
        """
        if Vector.Magnitude(vector_1)!=0:
            scale = 1/Vector.Magnitude(vector_1)
            vector_1 = Vector.Scale(vector_1, scale)
        return vector_1
    
    def Difference(vector_1, vector_2):
        if len(vector_1) == 2:
            return (vector_1[0]-vector_2[0], vector_1[1] - vector_2[1])
        else:
            return (vector_1[0]-vector_2[0], vector_1[1] - vector_2[1], vector_1[2] - vector_2[2])
    
    def Homothety(point, origin, scalar):
        """
            Transforms the point by homothety around the origin about the scalar
        """
        vec_origin_to_point = Vector.Difference(point, origin)
        x = scalar
        point = Vector.Add(Vector.Scale(vec_origin_to_point, x), origin)
        return point;
        
    def Rotate(vector, axis, angle):
        from lib.Quaternion import Quaternion
        rot_quat = Quaternion.from_angle_axis(angle, axis)
        rotated_vector = Quaternion.rotate_vector(vector, rot_quat)
        return rotated_vector
        
    def Vector_round(vec):
        from lib import settings
        from lib.Other import Digits

        digit_number = Digits(settings.threshold)

        var1 = round(vec[0], digit_number)
        var2 = round(vec[1], digit_number)
        var3 = round(vec[2], digit_number)
        return (var1, var2, var3)
        
    def Plane_cross_point(vector_origin, vector, plane):
        """
            Scales the vector so that it ends on the plane
        """
        scalar = (- vector_origin[0] * plane.factors[0] - vector_origin[1] * plane.factors[1] - vector_origin[2] * plane.factors[2] - plane.factors[3])/(vector[0] * plane.factors[0] + vector[1] * plane.factors[1] + vector[2] * plane.factors[2])
        return (vector[0]*scalar,vector[1]*scalar,vector[2]*scalar)
        
    def Angle_between_vectors(vector_1, vector_2):
        cos_a = Vector.dot(vector_1, vector_2)/(Vector.Magnitude(vector_1) * Vector.Magnitude(vector_2))
        if cos_a > 1.0:
            cos_a = 1.0
        if cos_a < -1.0:
            cos_a = -1.0
            
        return math.degrees(math.acos(cos_a))
    
    def To_2d(vector):
        return (vector[0], vector[1])
    
    def To_3d(vector):
        if len(vector) == 3:
            return vector
            
        return (vector[0], vector[1], 0)
            
    def Distance(point1, point2):
        return Vector.Magnitude(Vector.Difference(point2, point1))
    
    def Scale_by_vector(vector1, vector2):
        result = []
        for i in range(0, len(vector1)):
            result.append(vector1[i] * vector2[i])
        return tuple(result)

    @staticmethod
    def compare_magnitudes(vector1, vector2):
        """
            Returns:
                positive number if vector1's magnitude is greater than vector2
                0 if vector1's magnitude is equal to vector2's
                negative number otherwise
        """
        return vector1[0] ** 2 + vector1[1] ** 2 + vector1[2] ** 2 - vector2[0] ** 2 - vector2[1] ** 2 - vector2[2] ** 2