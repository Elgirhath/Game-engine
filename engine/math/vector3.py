import math
from engine import settings
from engine.Other import Digits


def divide(vector_1, vector_2):
    return (vector_1[0]/vector_2[0],vector_1[1]/vector_2[1],vector_1[2]/vector_2[2])
        
def magnitude(vector):
    return math.sqrt(dot(vector, vector))

def dot(vector_1, vector_2):
    a = vector_1[0]*vector_2[0]
    b = vector_1[1]*vector_2[1]
    c = vector_1[2]*vector_2[2]

    return a + b + c

def scale(vector, scalar):
    return (vector[0]*scalar, vector[1]*scalar, vector[2]*scalar)

def add(vector_1, vector_2):
    return (vector_1[0] + vector_2[0], vector_1[1] + vector_2[1], vector_1[2] + vector_2[2])

def scale_div(vector_1, vector_2):
    if vector_2[0] != 0:
        return vector_1[0]/vector_2[0]
    elif vector_2[1] != 0:
        return vector_1[1]/vector_2[1]
    elif vector_2[2] != 0:
        return vector_1[2]/vector_2[2]
    else:
        raise ValueError("Division by zero vector")
    
def cross(vector_1, vector_2):
    return (vector_1[1]*vector_2[2]-vector_1[2]*vector_2[1], vector_1[2]*vector_2[0]-vector_1[0]*vector_2[2], vector_1[0]*vector_2[1]-vector_1[1]*vector_2[0])


def normalize(vector_1):
    """
        scales vector_1 so that its magnitude is equal to 1
    """
    if magnitude(vector_1)!=0:
        v_scale = 1/magnitude(vector_1)
        vector_1 = scale(vector_1, v_scale)
    return vector_1

def subtract(vector_1, vector_2):
    return (vector_1[0]-vector_2[0], vector_1[1] - vector_2[1], vector_1[2] - vector_2[2])
    
def get_angle(vector_1, vector_2):
    cos_a = dot(vector_1, vector_2)/(magnitude(vector_1) * magnitude(vector_2))
    if cos_a > 1.0:
        cos_a = 1.0
    if cos_a < -1.0:
        cos_a = -1.0
        
    return math.degrees(math.acos(cos_a))

def to_2d(vector):
    return (vector[0], vector[1])
        
def distance(point1, point2):
    return magnitude(subtract(point2, point1))

def scale_by_vector(vector1, vector2):
    result = []
    for i in range(0, len(vector1)):
        result.append(vector1[i] * vector2[i])
    return tuple(result)
    
def compare_magnitudes(vector1, vector2):
    """
        Returns:
            positive number if vector1's magnitude is greater than vector2
            0 if vector1's magnitude is equal to vector2's
            negative number otherwise
    """
    return vector1[0] ** 2 + vector1[1] ** 2 + vector1[2] ** 2 - vector2[0] ** 2 - vector2[1] ** 2 - vector2[2] ** 2