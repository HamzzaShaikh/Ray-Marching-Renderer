Welcome to the ray marching renderer.

To keep things concise, here is what you need to know!

To run the program, run the raymarch.py program and change the "scene_json_files"
 to include the json file(s) you want to render. It will then use the scenes defined in the given json files to generate and save a .png of the scene.

***
The json files used to define scenes are fairly straightforward. The easiest way to understand how to create scenes is by looking at some of the previously defines ones. The main components are

* Define a camera, (keep the position, up, and forward the same). Change the pixel width and pixel height to change the resolution of the image. This will directly impact the render time. a resolution of 3840x2160 renders a 4K image but can take up to 20 hours! While an image of resolution 300x160 renders a low-quality image in a matter of minutes. These times also depend on how many objects / light sources you have.

* Objects can be spheres, pills/cylinders, and planes. The position parameter defines the position, radius the radius, and material defines the material properties

* The material properties include ambient, diffuse, spectral, and spectral p. The ambient changes the actual color of the object, the diffuse changes the matte level of the object, and the spectral changes the reflectivity. It is recommended not to change the spectral_p value. All of these colors and coefficients must be an array of 3 floats from 0-1. To change the ambient color the first, second, and third values correspond to red, green, and blue respectively. 

* The lights include 2 types, point and directional. These require a defines light color as well as position if its a point light and a direction if its a directional light,

* The general coordinate system is x, y, z where x is the direction of the camera, y is the right to left with respect to the camera, and z is the height.
