import sys
from PIL import Image

def parse_image(image_path):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    pixel_arr = [[img.getpixel((x,y)) for x in range(w)] for y in range(h)]

    return pixel_arr

def arr_to_image(pixel_arr):
    h = len(pixel_arr)
    w = len(pixel_arr[0])
    img = Image.new("RGB", (w, h))
    for y in range(h):
        for x in range(w):
            img.putpixel((x,y), pixel_arr[y][x])
    return img






if __name__ == "__main__":
    image_path = sys.argv[1]
    pixel_arr = parse_image(image_path)
    img = arr_to_image(pixel_arr)
    img.show()
