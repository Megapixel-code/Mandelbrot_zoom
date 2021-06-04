import time

from PIL import Image
import os
import glob
import numpy as np
import math


def process(pos, iterations):
    i = 0
    z = pos
    while i < iterations:
        if abs(z) > 2:
            return i
        z = z ** 2 + pos
        i += 1
    return 0


def render(iterations, center, zoom):
    values = np.zeros((1000, 1000), np.int8)
    for x in range(1000):
        print(f"\r{x/10}%", end="")
        for y in range(1000):
            val = process(complex((center[0] - (3.5 / zoom) / 2) + (3.5 / zoom) / 999 * x,
                                  (center[1] - (3.5 / zoom) / 2) + (3.5 / zoom) / 999 * y), iterations)
            values[y][x] = (val * 60) % 255

    return values


def create_to(final_iterations, pos, end_zoom, starting_frame=0, delete=False):
    if delete:
        img = Image.fromarray(np.zeros((10, 10), np.int8), 'L')
        img.save(f"Imgs/Null.jpg")
        files = glob.glob("Imgs/*.jpg")
        for f in files:
            try:
                os.unlink(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

    it_vect = int((final_iterations - 100) / math.log(end_zoom * 2, 1.01)) + 1
    it = 100
    x = starting_frame
    while 0.5 * 1.01 ** x < end_zoom:
        start_time = time.perf_counter()

        values = render(it + x * it_vect, pos, 0.5 * 1.01 ** x)
        img = Image.fromarray(values, 'L')
        img.save(f"Imgs/{x}.jpg")

        total_time = (time.perf_counter() - start_time)/60
        print(f"\rImage n°{x}",
              f"\t\tProgression : {str(int((it + x * it_vect) / final_iterations * 10000) / 100)}%",
              "\t\tIterations :", str(it + x * it_vect),
              "\t\tZoom :", str(0.5 * 1.01 ** x),
              f"\t\tTime taken : {round(total_time, 2)}min")
        x += 1


def make_video(fps=30, delete=False, opening_pause=0):
    import cv2

    if delete:
        try:
            os.unlink("Video.mp4")
        except OSError as e:
            print("Error: (%s) %s" % ("Video.mp4", e.strerror))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("Video.mp4", fourcc, fps, (1000, 1000))

    for i in range(fps * opening_pause):
        video.write(cv2.imread(f"Imgs/0.jpg"))
    nb_imgs = len(glob.glob("Imgs/*jpg"))
    for i in range(nb_imgs):
        video.write(cv2.imread(f"Imgs/{i}.jpg"))

    video.release()


# to get gray variation paste the line below in main>render by remplacing this line -> (values[y][x] = (val * 60) % 255)
# values[y][x] = int((val / (iterations - 1)) * 255)

# mandelbro_center : (-0.75, 0)
# mandelbro_size : 3.5x3.5

if __name__ == '__main__':
    # This is if you want to render a single image (works the same way as create_to below
    # Image.fromarray(render(150000, (-1.941571999362835, 0.000143 41225180058430), 5**19), 'L').show()
    
    # Max iterations / (x, y) / end zoom / frame you are starting at (if you close the program so you dont start from the beginning everytime)
    create_to(150000, (-1.941571999362835, 0.00014341225180058430), 5**19, 0)
    make_video(delete=True, opening_pause=2)
    input("press enter to exit ...")
