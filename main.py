"""
v1.0: Current logic Find boundary get any starting point and find nearest for first time create line and next time onwards check if near if near continue line or create new line
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
import math

STEP = 1

def create_laser_image(image_path, threshold=128):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    width, height = grayscale_image.size
    binary_image = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            if grayscale_image.getpixel((x, y)) > threshold:
                binary_image[y, x] = 255

    boundary_elems = []
    x_cord,y_cord=[],[]
    visited={}
    for y in range(height):
      for x in range(width):
        if binary_image[y, x] == 0:
          if ((x-1>=0 and binary_image[y, x-1] == 255) or 
              (y-1 >=0 and binary_image[y-1, x] == 255) or 
              (x+1< width and binary_image[y, x+1] == 255) or 
              (y+1 <height and binary_image[y+1, x] == 255) or 
              (x==0 or x==width-1 or y==0 or y==height-1)):
            boundary_elems.append((x,y))
            visited[(x,y)]=False
    
    # Show scatter points at the beginning
    fig, ax = plt.subplots()

    # Show scatter points at the beginning
    x_cord = [-ele[0] for ele in boundary_elems]
    y_cord = [ele[1] for ele in boundary_elems]
    scatter = ax.scatter(x_cord, y_cord, c="blue", s=1)

    my_queue=Queue()
    my_queue.put(boundary_elems[0])
    
    # def update(frame):
    #     nonlocal my_queue
    #     nonlocal visited
        
    #     top_item = my_queue.get()
    #     if top_item is not None:
    #       visited[top_item]=True
    #       neb=findclosestelem(top_item,boundary_elems,visited)
    #       my_queue.put(neb)
    #       line = ax.plot([-top_item[0], -neb[0]], [top_item[1], neb[1]], c="red", linewidth=1)
        
    # anim = FuncAnimation(fig, update,cache_frame_data=False,interval=1)
    # plt.show()
    
    x_cord_line=[]
    y_cord_line=[]
    
    while not my_queue.empty():
      top_item = my_queue.get()
      if top_item is not None:
        visited[top_item]=True
        neb=findclosestelem(top_item,boundary_elems,visited)
        my_queue.put(neb)
        x_cord_line.append(-top_item[0])
        y_cord_line.append(top_item[1])
    
    plt.plot(x_cord_line, y_cord_line,c="red",linewidth=1)
    plt.show()
    
    
def findclosestelem(src,boundary_elems,visited):
    min_distance = float('inf')
    closest_elem = None

    for elem in boundary_elems:
        if elem!=src and visited[elem]==False:
          distance = math.sqrt((elem[0] - src[0]) ** 2 + (elem[1] - src[1]) ** 2)
          if distance < min_distance:
              min_distance = distance
              closest_elem = elem

    return closest_elem

def getblackgroups(binary_image, height, width):
    groups = []
    start = None

    for x in range(width):
      if binary_image[height, x] == 0 and start is None:
          start = x
      elif binary_image[height, x] != 0 and start is not None:
          groups.append((start, x))
          start = None

    if start is not None:
        groups.append((start, width - 1))

    return groups

# Example usage
input_path = 'flashImage.png'
create_laser_image(input_path)
