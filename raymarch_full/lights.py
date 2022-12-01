from utils import normalize

class DirectionalLight:
    def __init__(self, direction, color):
        self.direction = normalize(direction)
        self.color = color
        
    def get_ray(self, location=None):
        return self.direction
    
    def get_position(self):
        return (2**32) * (-self.direction)
        
class PointLight:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        
    def get_ray(self, location):
        return normalize(location - self.position)
    
    def get_position(self):
        return self.position