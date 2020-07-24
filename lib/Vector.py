import math

class Vector():
    def Division(vector_1, vector_2):
        if vector_2[0]!=0 and vector_2[1]!=0 and vector_2[2]!=0:
            return (vector_1[0]/vector_2[0],vector_1[1]/vector_2[1],vector_1[2]/vector_2[2])
        else:
            print("vector.division - dzielenie przez 0")
            
    def Magnitude(vector):
        if len(vector) == 2:
            return math.sqrt(vector[0]**2+vector[1]**2)
        elif len(vector) == 3:
            return math.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
        else:
            print("Blad rozmiaru wektora:   ", str(vector))
            return 0
    
    def Dot_product(vector_1, vector_2):
        a =vector_1[0]*vector_2[0]
        b = vector_1[1]*vector_2[1]
        c = vector_1[2]*vector_2[2]
        
        result = a + b + c
        return result
    
    def Scale(vector, scalar):
        result_list = []
        for i in range(0, len(vector)):
            result_list.append(vector[i]*scalar)
        result = tuple(result_list)
        return result
    
    def Add(vector_1, vector_2):
        if len(vector_1)== 2 and len(vector_2)== 2:
            summary = (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1])
        elif len(vector_1)== 3 and len(vector_2)== 3:
            summary = (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1], vector_1[2] + vector_2[2])
        else:
            print("Blad rozmiaru wektora")
            return 0
        return summary
    
    def Scale_div(vector_1, vector_2):
        if len(vector_1) == 3 and len(vector_2) == 3:
            if vector_2[0] != 0:
                return vector_1[0]/vector_2[0]
            elif vector_2[1] != 0:
                return vector_1[1]/vector_2[1]
            elif vector_2[2] != 0:
                return vector_1[2]/vector_2[2]
            else:
                print("Scale_div divides by 0! Vector_2 = ", vector_2)
        
    def Cross_product(vector_1, vector_2):
        return (vector_1[1]*vector_2[2]-vector_1[2]*vector_2[1], vector_1[2]*vector_2[0]-vector_1[0]*vector_2[2], vector_1[0]*vector_2[1]-vector_1[1]*vector_2[0])
    
    def Cross_product_2d(vector_1, vector_2):
        return vector_1[0]*vector_2[1]-vector_1[1]*vector_2[0]

    
    def Normalize(vector_1):
        """
            Scales vector_1 so that its magnitude is equal to 1
        """
        if Vector.Magnitude(vector_1)!=0:
            scale = 1/Vector.Magnitude(vector_1)
            vector_1 = Vector.Scale(vector_1, scale)
        return vector_1
    
    def Difference(vector_1, vector_2):
        if len(vector_1)== 2 and len(vector_2)== 2:
            diff = (vector_1[0]-vector_2[0], vector_1[1] - vector_2[1])
        elif len(vector_1)== 3 and len(vector_2)== 3:
            diff = (vector_1[0]-vector_2[0], vector_1[1] - vector_2[1], vector_1[2] - vector_2[2])
        else:
            print("Blad rozmiaru wektora")
            return 0
        return diff
    
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
        rot_quat = Quaternion.Rot_quaternion(angle, axis)
        rotated_vector = Quaternion.Vector_quaternion_rotate(vector, rot_quat)
        return rotated_vector
        
    def Vector_round(vec):
        from lib import settings
        from lib.Other import Digits
        var1 = vec[0]
        var2 = vec[1]
        var3 = vec[2]
        if var1 % 1 <settings.threshold or (1-var1%1)<settings.threshold:
            var1 = round(var1, Digits(settings.threshold))
        if var2 % 1 <settings.threshold or (1-var2%1)<settings.threshold:
            var2 = round(var2, Digits(settings.threshold))
        if var3 % 1 <settings.threshold or (1-var3%1)<settings.threshold:
            var3 = round(var3, Digits(settings.threshold))
        return (var1, var2, var3)
        
    def Plane_cross_point(vector_origin, vector, plane):
        """
            Scales the vector so that it ends on the plane
        """
        scalar = (- vector_origin[0] * plane.factors[0] - vector_origin[1] * plane.factors[1] - vector_origin[2] * plane.factors[2] - plane.factors[3])/(vector[0] * plane.factors[0] + vector[1] * plane.factors[1] + vector[2] * plane.factors[2])
        return (vector[0]*scalar,vector[1]*scalar,vector[2]*scalar)
        
    def Angle_between_vectors(vector_1, vector_2):
        cos_a = Vector.Dot_product(vector_1, vector_2)/(Vector.Magnitude(vector_1) * Vector.Magnitude(vector_2))
        return math.degrees(math.acos(cos_a))
    
    def Distribution_between(vector, component_vector1, component_vector2, component_vector3):
        """
            Returns scalars of the new R3 basis describing vector
        """
        from lib.Matrix import Matrix
        mat = Matrix([
                [component_vector1[0], component_vector2[0], component_vector3[0]],
                [component_vector1[1], component_vector2[1], component_vector3[1]],
                [component_vector1[2], component_vector2[2], component_vector3[2]],])
    
        a = (vector[0])
        b = (vector[1])
        c = (vector[2])
        scalars = mat.Solutions((a, b, c)) #the scalars of component vectors
        return scalars
    
    def World_to_local_space(point, transform):
        from lib.Quaternion import Quaternion
        x = point
        x = Vector.Difference(point, transform.position)
        if transform.rotation.norm>0:
            x = Quaternion.Vector_quaternion_rotate(x, transform.rotation.inverse())
        return x
    
    def Local_to_world_space(point, transform):
        from lib.Quaternion import Quaternion
        point_in_local = point
        if transform.rotation.norm>0:
            point_rotated = Quaternion.Vector_quaternion_rotate(point_in_local, transform.rotation)
        point_rotated_and_translated = Vector.Add(point_rotated, transform.position)
        return point_rotated_and_translated
    
    def To_2d(vector3d):
        if len(vector3d) == 2:
            return vector3d
        elif len(vector3d) == 3:
            return (vector3d[0], vector3d[1])
        else:
            print("Podany vector3d ma zly rozmiar")
    
    def To_3d(vector2d):
        if len(vector2d) == 3:
            return vector2d
        elif len(vector2d) == 2:
            return (vector2d[0], vector2d[1], 0)
        else:
            print("Podany vector2d ma zly rozmiar")
            
    def Distance(point1, point2):
        return Vector.Magnitude(Vector.Difference(point2, point1))
    
    def Scale_by_vector(vector1, vector2):
        result = []
        for i in range(0, len(vector1)):
            result.append(vector1[i] * vector2[i])
        return tuple(result)