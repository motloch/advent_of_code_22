dat = open('18.txt', 'r').read().splitlines()

positions = set()
for row in dat:
    x,y,z = map(int, row.split(','))
    positions.add((x,y,z))

neighbors = [ [ 1,0,0], [-1,0,0], [0, 1,0], [0,-1,0], [0,0, 1], [0,0,-1]]

#####
# Problem 1
#####

surface_area = 0

for x,y,z in positions:
    for dx, dy, dz in neighbors:
        if (x+dx, y+dy, z+dz) not in positions:
            surface_area += 1

print(surface_area)

#####
# Problem 2
#####

# find min and max
min_xyz = 10**6
max_xyz = -10**6

for x,y,z in positions:
    min_xyz = min(min_xyz, x, y, z)
    max_xyz = max(max_xyz, x, y, z)

# generate a 3D array with 1 at lava positions
import numpy as np
arr = np.zeros((max_xyz+1, max_xyz+1, max_xyz+1), dtype = int)

for x,y,z in positions:
    arr[x,y,z] = 1

# find the water cubes and fill them with 2 - everything we can reach starting from
# (0,0,0)
def isIn(x,y,z):
    return x >= 0 and y >= 0 and z >= 0 and x <= max_xyz and y <= max_xyz and z <= max_xyz

queue = [(0,0,0)]
arr[0,0,0] = 2

while queue:
    x,y,z = queue.pop()
    for dx, dy, dz in neighbors:
        if isIn(x+dx,y+dy,z+dz) and arr[x+dx,y+dy,z+dz] == 0:
           queue.append((x+dx, y+dy, z+dz)) 
           arr[x+dx,y+dy,z+dz] = 2

# count the surface area
surface_area = 0
for x in range(max_xyz + 1):
    for y in range(max_xyz + 1):
        for z in range(max_xyz + 1):
            if arr[x,y,z] == 1:
                for dx, dy, dz in neighbors:
                    if not isIn(x+dx,y+dy,z+dz) or arr[x+dx,y+dy,z+dz] == 2:
                        surface_area += 1

print(surface_area)
                
