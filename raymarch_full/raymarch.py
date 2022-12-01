import numpy as np
import matplotlib.pyplot as plt
from scene import Scene


if __name__ == '__main__':
    from multiprocessing import Pool
    from datetime import datetime
    
    # scene_json_files = ["scene1.json", "scene2.json"]
    # scene_json_files = ["scene7.json"]
    """"
    IMPORTANT_NOTE: DO NOT RERUN ANY OF THE OLD FILES, ITLL GET RID OF THE CURRENT SAVED IMAGES
    MAKE A NEW JSON AND RUN THAT TO TEST NEW SCENES / REDO OLD SCENES
    """
    scene_json_files = ["scenedir.json"]
    for scene_json in scene_json_files:
        N_THREADS = 16
        SATURATION = 1
        scene = Scene(scene_json)
        WIDTH = scene.camera.width
        HEIGHT = scene.camera.height
        
        pixel_coords = [(x, y) for y in range(HEIGHT) for x in range(WIDTH)]
        image_array = None
        
        start_time = datetime.now()
        with Pool(N_THREADS) as pool:
            image_array = pool.starmap(scene.get_pixel_color, pixel_coords)
        stop_time = datetime.now()
        
        image = (np.resize(np.array(image_array), (HEIGHT, WIDTH, 3)) / ((np.max(image_array)/SATURATION) if np.max(image_array) > 1 else 1)).clip(0, 1)

        print(f"Raymarch for {'.'.join(scene_json.split('.')[:-1])} took {stop_time-start_time}")
        plt.imsave(f"{'.'.join(scene_json.split('.')[:-1])}.png", image)