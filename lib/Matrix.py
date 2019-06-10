import math

class Matrix():
    def __init__(self, values):
        self.struct = values
        
        for verse in values:
            if len(verse) !=len(values[0]) or len(values)<1:
                print ("Matrix is wrong format")
                return 0
            
    def x_rot (angle):
        x_rot_matrix = Matrix([[1,0,0], [0, math.cos(math.radians(angle)), -math.sin(math.radians(angle))], [0, math.sin(math.radians(angle)), math.cos(math.radians(angle))]])
        return x_rot_matrix
    
    def y_rot (angle):
        y_rot_matrix = Matrix([[math.cos(math.radians(angle)),0,math.sin(math.radians(angle))], [0, 1, 0], [-math.sin(math.radians(angle)), 0, math.cos(math.radians(angle))]])
        return y_rot_matrix
            
    def z_rot (angle):
        z_rot_matrix = Matrix([[math.cos(math.radians(angle)),-math.sin(math.radians(angle)),0], [math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0], [0, 0, 1]])
        return z_rot_matrix
    
    def I(dimension):
        result_mat = []
        for i in range(0,dimension):
            verse = []
            for k in range(0,dimension):
                if i==k:
                    verse.append(1)
                else:
                    verse.append(0)
            result_mat.append(verse)
        return Matrix(result_mat)
    
    def axis_rot (axis, angle):
        from Vector import Vector
        axis = Vector.Normalize(axis)
        angle = math.radians(angle)
        axis_mat = Matrix.From_vector(axis)
        a = Matrix.I(3).Scale(math.cos(angle))
        b = Matrix.Cross_product_matrix(axis_mat).Scale(math.sin(angle))
        c = Matrix.Scale(axis_mat.Multiply(axis_mat.Transposed()), (1-math.cos(angle)))
        R = Matrix.Sum((a,b,c))
        return R
    
    def From_vector(vector):
        result = []
        for i in range(0, len(vector)):
            result.append([vector[i]])
        return Matrix(result)
        
    def Sum(list_of_matrices):
        result = list_of_matrices[0].struct
        for i in range(1, len(list_of_matrices)):
            for j in range(0,len(list_of_matrices[i].struct)):
                for k in range(0, len(list_of_matrices[i].struct[j])):
                    result[j][k] += list_of_matrices[i].struct[j][k]
        mat = Matrix(result)
        return mat
            
    def Det(self):
#        m - determined matrix
        m=self.struct
        if len(m) <= 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]
        
        else:
            first_row = list(m[0])
            deter = 0
            for i in range(0, len(m[0])):
                temp_matrix = []
                for row in m:
                    temp_matrix.append(list(row))
                temp_matrix.pop(0)
                for row in temp_matrix:
                    row.pop(i)
                algebraic_complement = Matrix(temp_matrix)
                deter += first_row[i] * (-1)**(i+2) * algebraic_complement.Det()
            return deter
        
    def Square_solutions(mat, constant_terms):
        dets = []
        for i in range(0,len(mat.struct)):
            swapped_struct = []
            for verse in mat.struct:
                swapped_struct.append(list(verse))
            
            k=0
            for verse in swapped_struct:
                verse.pop(i)
                verse.insert(i, constant_terms[k])
                k+=1
            swapped_matrix = Matrix(swapped_struct)
            dets.append(swapped_matrix.Det())
        solutions = []
        for det in dets:
            solutions.append(det/mat.Det())
        return solutions
    
    def Solutions(self, constant_terms):
#        constant_terms - wyrazy wolne
        if len(self.struct) == len(self.struct[0]):
            if self.Det()== 0:
                print("Determinant equal to 0")
            else:
                return Matrix.Square_solutions(self, constant_terms)
        elif len(self.struct) > len(self.struct[0]):
            for l in range(0, len(self.struct)-1):
                for k in range (l+1, len(self.struct)):
                    struct = []
                    struct.append(self.struct[l])
                    struct.append(self.struct[k])
                    frag_matrix = Matrix(struct)
                    if frag_matrix.Det()!=0:
                        return frag_matrix.Square_solutions((constant_terms[l], constant_terms[k]))
                        
        else:
            print("Za duzo niewiadomych")
            return 0
    
    def Vector_product(self, vector):
        m = self.struct
        results = []
        for i in range(0, len(m)):
            result = 0
            for k in range(0, len(m[i])):
                result += m[i][k] * vector[k]
            results.append(result)
        return results
    
    def Multiply(self, matrix):
        if len(self.struct) == len(matrix.struct[0]) and len(self.struct[0]) == len(matrix.struct):
            new_struct = []
            for i in range (0, len(self.struct)):
                new_row = []
                for j in range(0, len(self.struct[i])):
                    var = 0
                    for k in range(0, len(matrix.struct)):
                        var += self.struct[i][k]*matrix.struct[k][j]
                    new_row.append(var)
                new_struct.append(new_row)
            return Matrix(new_struct)
        
    def Cross_product_matrix(vector_mat):
        if len(vector_mat.struct) == 3:
            mat = Matrix([[0, -vector_mat.struct[2][0], vector_mat.struct[1][0]], [vector_mat.struct[2][0], 0, -vector_mat.struct[0][0]], [-vector_mat.struct[1][0], vector_mat.struct[0][0], 0]])
            return mat
        
    def Scale(self, scalar):
        result = []
        for verse in self.struct:
            new_verse = []
            for field in verse:
                new_verse.append(field*scalar)
            result.append(new_verse)
        return Matrix(result)
                
    def Tensor_product(self, mat):
        result_mat = []
        for n in range(0,len(self.struct)):
            for k in range(0, len(mat.struct)):
                verse = []
                for i in range(0, len(self.struct[n])):
                    for j in range(0, len(mat.struct[k])):
                        verse.append(self.struct[n][i]*mat.struct[k][j])
                result_mat.append(verse)
        return result_mat
    
    def Transposed(self):
        result = []
        for j in range(0, len(self.struct[0])):
            verse = []
            for i in range(0, len(self.struct)):
                verse.append(self.struct[i][j])
            result.append(verse)
        mat = Matrix(result)
        return mat