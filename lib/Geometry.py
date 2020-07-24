from lib.Vector import Vector

class Surface():
    def __init__(self, factor_tupple):
        self.factors = factor_tupple
        
    def normal(self):
        return (self.factors[0], self.factors[1], self.factors[2])
    
    def Normalize(self):
        normal = self.normal()
        if Vector.Magnitude(normal)!=0:
            scale = 1/Vector.Magnitude(normal)
            normal = Vector.Scale(normal, scale)
            d = self.factors[3]*scale
            self.factors = (normal[0], normal[1], normal[2], d)
            
    def Invert_normal(self):
        self.factors = Vector.Scale(self.factors, -1)
        
    def Switch_normal_by_vector(self, vector):
        if Vector.Dot_product(self.normal(), vector)<0:
            self.Invert_normal()
        
    def From_points(vertex1, vertex2, vertex3):
        plane_vector1 = Vector.Difference(vertex1, vertex2)
        plane_vector2 = Vector.Difference(vertex2, vertex3)
        normal = Vector.Cross_product(plane_vector1, plane_vector2)
        normal = Vector.Normalize(normal)
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*vertex1[0]-normal[1]*vertex1[1]-normal[2]*vertex1[2]
        surface = Surface((a,b,c,d))
        return surface

    def From_normal(normal, point):
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*point[0]-normal[1]*point[1]-normal[2]*point[2]
        surface = Surface((a,b,c,d))
        return surface
    
    def From_vectors(vector1, vector2, origin_point):
        normal = Vector.Cross_product(vector1, vector2)
        normal = Vector.Normalize(normal)
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -normal[0]*origin_point[0]-normal[1]*origin_point[1]-normal[2]*origin_point[2]
        surface = Surface((a,b,c,d))
        return surface
    
    def Contains_point(self, point):
        a = self.factors[0]
        b = self.factors[1]
        c = self.factors[2]
        d = self.factors[3]
        
        x = point[0]
        y = point[1]
        z = point[2]
        
        if a*x + b*y + c*z + d == 0:
            return True
        else:
            return False
        
    def Perpen_vector_to_point(self, point):
        """
            Returns vector perpendicular to the surface with origin on the surface and the ending on the point
        """
        from lib.Ray import Ray
        if Ray(point, Vector.Scale(self.normal(), -1)).Intersect_point(self):
            ray = Ray(point, Vector.Scale(self.normal(), -1))
        else:
            ray = Ray(point, Vector.Scale(self.normal(), 1))
        intersection = ray.Intersect_point(self)
        vector = Vector.Difference(point, intersection)
        return vector
    
    def Point_relative_pos(self, point):
        """
            Returns:
                0 if point lays on the surface
                Distance from the surface if point is on positive side of surface
                Negative distance if point is on negative side of surface
        """
        vector = self.Perpen_vector_to_point(point)
        if Vector.Dot_product(vector, self.normal()) == 0:
            return 0
        elif Vector.Dot_product(vector, self.normal()) > 0:
            return Vector.Magnitude(vector)
        else:
            return -Vector.Magnitude(vector)
        
    def string(self):
        return str(self.factors[0]) + "*x + " + str(self.factors[1]) + "*y + " + str(self.factors[2]) + "*z + " + str(self.factors[3]) + " = 0"

    def string_z(self):
        return "z = " + "(-"+str(self.factors[0]) + "*x - " + str(self.factors[1]) + "*y - " + str(self.factors[3])+ ") / " + str(self.factors[2])

    def Is_point_between_surfaces(surface1, surface2, point):
        rel_pos1 = surface1.Point_relative_pos(point)
        rel_pos2 = surface2.Point_relative_pos(point)
        if rel_pos1 < 0 or rel_pos2 < 0:
            return False
        else:
            return True

def _sign_(point, vertex, line_origin, line_end):
    cp1 = Vector.Cross_product(Vector.To_3d(Vector.Difference(line_end, line_origin)), Vector.To_3d(Vector.Difference(point, line_origin)))
    cp2 = Vector.Cross_product(Vector.To_3d(Vector.Difference(line_end, line_origin)), Vector.To_3d(Vector.Difference(vertex, line_origin)))
    if Vector.Dot_product(cp1, cp2) >= 0:
        return True
    else:
        return False

def Point_in_triangle(point, vertex_list):
    a = _sign_(point, vertex_list[2], vertex_list[0], vertex_list[1])
    if not a:
        return False
    b = _sign_(point, vertex_list[0], vertex_list[1], vertex_list[2])
    if not b:
        return False
    c = _sign_(point, vertex_list[1], vertex_list[2], vertex_list[0])
    if not c:
        return False
    else:
        return True
    
def Point_in_polygon(point, vertex_list):
    origin = vertex_list[0]
    for i in range(1, len(vertex_list)-1):
        triangle = [origin, vertex_list[i], vertex_list[i+1]]
        if Point_in_triangle(point, triangle):
            return True
    return False
    
def Sort_clockwise(point_list, center):
    if len(point_list) < 3:
        print("Sort_clockwise przyjal ", len(point_list), "punkt/y/ow")
        return point_list
    for i in range(0, len(point_list)):
        point_list[i] = Vector.Difference(point_list[i], center)
    
    switch = True
    while switch:
        switch = False
        for i in range(0, len(point_list)):
            if i == 0:
                if Vector.Cross_product_2d(point_list[i], point_list[len(point_list)-1]) < 0:
                    point_list[i], point_list[len(point_list)-1] = point_list[len(point_list)-1], point_list[i]
                    switch = True
                
            elif Vector.Cross_product_2d(point_list[i], point_list[i-1]) < 0:
                point_list[i], point_list[i-1] = point_list[i-1], point_list[i]
                switch = True
    for i in range(0, len(point_list)):
        point_list[i] = Vector.Add(point_list[i], center)

    return point_list

def Center_of_mass(point_list):
    if len(point_list[0])==2:
        vector_sum = (0,0)
        for i in range(0, len(point_list)):
            vector_sum = Vector.Add(vector_sum, point_list[i])
        average = Vector.Scale(vector_sum, (1/len(point_list)))
        return average
    elif len(point_list[0])==3:
        vector_sum = (0,0, 0)
        for i in range(0, len(point_list)):
            vector_sum = Vector.Add(vector_sum, point_list[i])
        average = Vector.Scale(vector_sum, (1/len(point_list)))
        return average
    
def Axis_view(point, axis):
    k = Vector.Dot_product(point, axis)/Vector.Magnitude(point)**2
    return k