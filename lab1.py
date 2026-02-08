import sys
import heapq
import math
from PIL import Image

terrain = {
    (71, 51, 3): 0.45, # Paved Road
    (0, 0, 0): 0.56, # Footpath
    (248, 148, 18): 0.67, # Open Land
    (255, 255, 255): 0.83, # Eazy Forest
    (255, 192, 0): 1.00, # Rough Meadow
    (2, 208, 60): 1.25, # Slow Run Forest
    (2, 136, 40): 1.67, # Walk Forest
    (5, 73, 24): float('inf'), # Vegetation
    (0, 0, 255): float('inf'), # Lake
    (205, 0, 101): float('inf') # Out of Bounds
}

DX = 10.29
DY = 7.55

def distance(a, b, elev_arr):
    x1, y1 = a
    x2, y2 = b

    dx = abs(x1 - x2) * DX
    dy = abs(y1 - y2) * DY
    dz = abs(elev_arr[y1][x1] - elev_arr[y2][x2])

    return math.sqrt(dx*dx + dy*dy + dz*dz)

def neighbors(x, y, width, height):
    n = []
    if x > 0:
        n.append((x-1, y))
    if x < width-1:
        n.append((x+1, y))
    if y > 0:
        n.append((x, y-1))
    if y < height-1:
        n.append((x, y+1))

    return n

def astar(start, goal, pixel_arr, elev_arr):
    h = len(pixel_arr)
    w = len(pixel_arr[0])

    min_mult = 0.45

    queue = []
    heapq.heappush(queue, (0.0, start))
    g = {start: 0.0}
    parent = {start: None}

    while queue:
        cur = heapq.heappop(queue)[1]
        if cur == goal:
            break
        
        cx, cy = cur
        for x, y in neighbors(cx, cy, w, h):
            if terrain[pixel_arr[y][x]] == float('inf'):
                continue
            
            neighbor = (x, y)
            terrain_mult = terrain[pixel_arr[cy][cx]]
            cost = distance(cur, neighbor, elev_arr) * terrain_mult
            ng = g[cur] + cost

            if neighbor not in g or ng < g[neighbor]:
                g[neighbor] = ng
                parent[neighbor] = cur
                heur = distance(neighbor, goal, elev_arr) * min_mult
                f = ng + heur
                heapq.heappush(queue, (f, neighbor))
    return parent

def build_path(parent, goal, elev_arr):
    dist = 0.0
    path = []
    cur = goal

    while cur is not None:
        path.append(cur)
        cur = parent[cur]


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

def parse_elevation(elev_file):
    elev = []
    with open(elev_file) as f:
        for line in f:
            val = [float(e) for e in line.split()]
            elev.append(val[:-5])
    return elev

def parse_path(path_file):
    path = []
    with open(path_file) as f:
        for line in f:
            coord = line.split()
            x = int(coord[0])
            y = int(coord[1])
            path.append((x, y))
    return path


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit()
    image_path = sys.argv[1]
    elev_file = sys.argv[2]
    path_file = sys.argv[3]
    output_image = sys.argv[4]

    pixel_arr = parse_image(image_path)
    elev_arr = parse_elevation(elev_file)
    path_arr = parse_path(path_file)
    img = arr_to_image(pixel_arr)
