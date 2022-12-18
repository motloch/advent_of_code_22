import re

filename = '15.txt'
dat = open(filename, 'r').read().splitlines()

if filename == '15.txt':
    y_test = 2000000
else:
    y_test = 10

sensors = []
beacons = []

# where beacon can not be - brute force using set
cannot = set()
beacons_on_test = set()

for line in dat:
    sx, sy, bx, by = map(int, re.findall(r'-*\d+', line))
    sensors.append([sx, sy])
    beacons.append([bx, by])

    if by == y_test:
        beacons_on_test.add(bx)

    # distance to closest beacon
    dist = abs(sx - bx) + abs(sy - by)

    # vertical distance from the test row
    dy = abs(y_test - sy)

    # are there blind spots?
    if dy <= dist:
        for dx in range(dist + 1 - dy):
            cannot.add(sx + dx)
            cannot.add(sx - dx)

print(len(cannot) - len(beacons_on_test))


## plot what is going on
#import matplotlib.pyplot as plt
#plt.figure(figsize = (5,5))
#for (sx, sy), (bx, by) in zip(sensors, beacons):
#    dist = abs(sx - bx) + abs(sy - by)
#    plt.plot([sx - dist, sx, sx + dist, sx, sx-dist], [sy, sy+dist, sy, sy-dist, sy])
#plt.plot([0, 4e6, 4e6, 0,0], [0,0,4e6,4e6,0],c='k')
#plt.show()




# we know there is a single solution. If it is inside the area, then it is between two
# pairs of diagonals that are separated by distance two. Let's see if we can find them..

# check which diagonals form the boundaries - these are the values of x+y, x-y on the diamonds
x_plus_y = set()
x_minus_y = set()
for (sx, sy), (bx, by) in zip(sensors, beacons):
    dist = abs(sx - bx) + abs(sy - by)
    x_plus_y.add(sx+sy+dist)
    x_plus_y.add(sx+sy-dist)
    x_minus_y.add(sx-sy+dist)
    x_minus_y.add(sx-sy-dist)

x_plus_y = sorted(x_plus_y)
x_minus_y = sorted(x_minus_y)

# see if there are two with a single space in between
found_x_plus_y = []
found_x_minus_y = []

for i in range(len(x_plus_y) - 1):
    if x_plus_y[i] + 2 == x_plus_y[i+1]:
        found_x_plus_y.append(x_plus_y[i] + 1)

for i in range(len(x_minus_y) - 1):
    if x_minus_y[i] + 2 == x_minus_y[i+1]:
        found_x_minus_y.append(x_minus_y[i] + 1)

# calculate x,y of the distress beacon
assert len(found_x_plus_y) == len(found_x_minus_y) == 1

found_x_plus_y, found_x_minus_y = found_x_plus_y[0], found_x_minus_y[0]

x = (found_x_plus_y + found_x_minus_y) // 2
y = (found_x_plus_y - found_x_minus_y) // 2

# result
print(4000000 * x + y)
