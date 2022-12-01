import numpy as np
import json

from objects import Sphere, Plane, Material, Cylinder
from lights import DirectionalLight, PointLight
from utils import normalize, reflect, Ray

class Camera:
    def __init__(self, position, up, forward, width, height, fov):
        self.position = position
        self.up = normalize(up)
        self.forward = normalize(forward)
        self.right = normalize(np.cross(up, forward))
        self.transform = np.matrix([self.forward, self.right, self.up])
        self.width = width
        self.height = height
        self.fov = fov
        self.fov_ratio = height / width

class Scene:    
    def __init__(self, json_file):
        with open(json_file, "r") as file:
            json_data = json.load(file)
            
            try:
                self.camera = Camera(
                    np.array(json_data["camera"]["position"]),
                    np.array(json_data["camera"]["up"]),
                    np.array(json_data["camera"]["forward"]),
                    int(json_data["camera"]["pixel_width"]),
                    int(json_data["camera"]["pixel_height"]),
                    int(json_data["camera"]["fov"])
                )
            except:
                print("Error parsing camera")
                exit(-1)
            
            self.objects = []
            for i, object in enumerate(json_data["objects"]):
                try:
                    material = Material (
                        np.array(object["material"]["ambient"]),
                        np.array(object["material"]["diffuse"]),
                        np.array(object["material"]["spectral"]),
                        float(object["material"]["spectral_p"])
                    )
                                            
                    if object["type"] == "sphere":
                        self.objects.append(
                            Sphere(
                                np.array(object["position"]),
                                float(object["radius"]), 
                                material
                            )
                        )
                    elif object["type"] == "plane":
                        self.objects.append(
                            Plane(
                                np.array(object["position"]),
                                np.array(object["normal"]),
                                material
                            )
                        )
                    elif object["type"] == "cylinder":
                        self.objects.append(
                            Cylinder(
                                np.array(object["position1"]),
                                np.array(object["position2"]),
                                float(object["radius"]),
                                material
                            )
                        )
                    else:
                        raise Exception
                except:
                    print(f"Error parsing object at index {i}")
                    exit(-1)
                    
            self.lights = []
            for light in json_data["lights"]:
                try:
                    if light["type"] == "point":
                        self.lights.append(
                            PointLight(
                                np.array(light["position"]),
                                np.array(light["color"])
                            )
                        )
                    elif light["type"] == "directional":
                        self.lights.append(
                            DirectionalLight(
                                np.array(light["direction"]),
                                np.array(light["color"])
                            )
                        )
                    else:
                        raise Exception
                except:
                    print(f"Error parsing light at index {i}")
                    exit(-1)
    
    def ray_march(self, ray):        
        # Does this ray hit anything
        object_hit = None
        hit_location = None
        
        current_ray_traveled = 0
        for _ in range(1000):
            current_ray = current_ray_traveled*ray.ray_direction + ray.ray_position
            
            min_distance = float('inf')
            min_object = -1
            for i, object in enumerate(self.objects):
                this_distance = object.get_distance(current_ray)
                if this_distance < min_distance:
                    min_distance = this_distance
                    min_object = i
                    
            if min_distance < 0.001:
                object_hit = self.objects[min_object]
                hit_location = current_ray
                break
            elif min_distance > (2**32):
                break
            else:
                current_ray_traveled += min_distance
                
        return object_hit, hit_location
        
    def get_pixel_color(self, x, y):
        # what is the ray coming from this pixel
        theta = np.radians(((x - (self.camera.width/2)) / self.camera.width) * self.camera.fov)
        rho =  np.radians(((y - (self.camera.height/2)) / self.camera.height) * self.camera.fov * self.camera.fov_ratio)
        x_rotation = np.matrix([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0            ,  0            , 1]
        ])
        y_rotation = np.matrix([
            [ np.cos(rho), 0, np.sin(rho)],
            [ 0          , 1, 0          ],
            [-np.sin(rho), 0, np.cos(rho)]
        ])
        direction_transform = self.camera.transform * x_rotation * y_rotation * np.linalg.inv(self.camera.transform)
        ray_direction = np.resize(direction_transform @ self.camera.forward, (3,))
        camera_ray = Ray(self.camera.position, ray_direction)
        
        hit_object, hit_location = self.ray_march(camera_ray)
        
        pixel_color = np.array((0.0, 0.0, 0.0), dtype=np.float64)
        if hit_object is not None:
                    
            # Ambient Shading
            pixel_color += hit_object.material.get_ambient_coef()
            
            diffuse_color = np.array([0.0, 0.0, 0.0])
            spectral_color = np.array([0.0, 0.0, 0.0])
            for light in self.lights:
                
                light_direction = normalize(light.get_ray(hit_location))
                light_distance = np.linalg.norm(hit_location - light.get_position())
                shadow_ray = Ray(hit_location + 0.002*hit_object.get_surface_normal(hit_location), -light_direction)
                shadow_hit_object, shadow_hit_location = self.ray_march(shadow_ray)                
                
                if shadow_hit_object is not None:
                    hit_distance = np.linalg.norm(hit_location - shadow_hit_location)
                    if light_distance > hit_distance:
                        continue
                
                # Diffuse Shading
                diffuse_brightness = max(light.get_ray(hit_location) @ -normalize(hit_object.get_surface_normal(hit_location)), 0)
                diffuse_color += hit_object.material.get_diffuse_coef() * (diffuse_brightness * np.array(light.color))
            
                # Spectral Shading
                spectral_brightness = max(
                        -(normalize(reflect(light.get_ray(hit_location), hit_object.get_surface_normal(hit_location))) @ camera_ray.ray_direction),
                        0
                    ) ** hit_object.material.get_spectral_p_coef()
                spectral_color += hit_object.material.get_spectral_coef() * (spectral_brightness * np.array(light.color))
            
            pixel_color += diffuse_color
            pixel_color += spectral_color
                
            
        return pixel_color