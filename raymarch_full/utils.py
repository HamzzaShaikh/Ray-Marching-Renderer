import numpy as np

def normalize(v):
    return v / np.linalg.norm(v)

def proj(u, v):
    return np.dot(u, v) * normalize(v)

def reflect(v, n):
    return v - (np.dot(2*v, n) * n)

class Ray:
    def __init__(self, ray_position, ray_direction):
        self.ray_position = ray_position
        self.ray_direction = ray_direction
        self.time = 1
    
    def get_next_pos(self, distance):
        self.time += distance
        return (self.time * self.ray_direction) + self.ray_position