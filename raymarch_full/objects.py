import numpy as np
from utils import normalize, proj

class Material:
    def __init__(self, ambient, diffuse, spectral, spectral_p):
        self.ambient = np.array(ambient)
        self.diffuse = np.array(diffuse)
        self.spectral = np.array(spectral)
        self.spectral_p = spectral_p
        
    def get_ambient_coef(self):
        return self.ambient
    
    def get_diffuse_coef(self):
        return self.diffuse
    
    def get_spectral_coef(self):
        return self.spectral
    
    def get_spectral_p_coef(self):
        return self.spectral_p

class Sphere:
    def __init__(self, position, radius, material):
        self.position = position
        self.radius = radius
        self.material = material
        
    def get_distance(self, location):
        return np.linalg.norm(location-self.position) - self.radius
    
    def get_surface_normal(self, location):
         return normalize(location-self.position)

class Cylinder:
    def __init__ (self, position1, position2, radius, material):
        self.position1 = position1
        self.position2 = position2
        self.radius = radius
        self.material = material
        self.one_two = self.position2 - self.position1
        # self.one_two_norm = np.linalg.norm(self.one_two)

    def get_vert(self, location):
        pos_Diff = location - self.position1
        td = np.dot(self.one_two, pos_Diff) / np.dot(self.one_two, self.one_two)
        # td = np.clip(td, 0, self.one_two_norm)
        td = np.clip(td, 0, 1)
        vert = self.position1 + td*self.one_two
        return vert

    def get_distance(self, location):
        vert = self.get_vert(location)
        dist = np.linalg.norm(location - vert) - self.radius
        # print(f"td:{td} and test:{test}")
        return dist
    
    def get_surface_normal(self, location):
        vert = self.get_vert(location)
        return normalize(location-vert)

class Plane:
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normalize(normal)
        self.material = material
        
    def get_distance(self, location):
        return np.linalg.norm(proj((location - self.position), self.normal))
    
    def get_surface_normal(self, location):
        return self.normal