# load data
dat = open('14.txt', 'r').read().splitlines()

# whether we want to inspect the crated 2D array
plot = False

# split into lists of lists of integers
rocks = [[list(map(int,point.split(','))) for point in rock.split(' -> ')] for rock in dat]

# find ranges of x and y positions
xpos = set()
ypos = set()

for rock in rocks:
    for point in rock:
        xpos.add(point[0])
        ypos.add(point[1])

xmin, xmax = min(xpos), max(xpos)
ymin, ymax = min(ypos), max(ypos)

# create a 2D array describing the situation - shift everything such that xmin corresponds to 0
arr = [['.' for i in range(xmax - xmin + 1)] for j in range(ymax + 1)]

for rock in rocks:
    for (xA, yA), (xB, yB) in zip(rock, rock[1:]):
        xA = xA - xmin
        xB = xB - xmin
        if xA == xB:
            for i in range(min(yA,yB), max(yA,yB)+1):
                arr[i][xA] = '#'
        else:
            for i in range(min(xA,xB), max(xA,xB)+1):
                arr[yA][i] = '#'

# sand source position
x_source = 500 - xmin
y_source = 0
arr[y_source][x_source] = '+'

# check we filled in the array properly
if plot:
    for a in arr:
        print(''.join(a))

#####
# PART 1
#####

# simulate
num_sand = 0

while True:
    # source position
    num_sand += 1
    x = x_source
    y = y_source
    stuck = False

    # move while we can
    while not stuck and y < ymax and x >= 0 and x <= xmax - xmin:
        if arr[y+1][x] == '.':
            y += 1
        elif arr[y+1][x-1] == '.':
            y += 1
            x -= 1
        elif arr[y+1][x+1] == '.':
            y += 1
            x += 1
        else:
            arr[y][x] = 'O'
            stuck = True

    # did we get out?
    if y >= ymax or x < 0 or x > xmax:
        break

# minus one because the last one escaped
print(num_sand - 1)

#####
# PART 2
#####

# extra padding on the left/right
extraL = ymax + 2 - x_source
extraR = ymax + (xmax - xmin - x_source) - 3

# copy rocks from part 1
arr2 = [['.' for i in range(xmax - xmin + 1 + extraL + extraR)] for j in range(ymax + 3)]
for x in range(xmax - xmin + 1):
    for y in range(ymax + 1):
        arr2[y][x + extraL] = arr[y][x].replace('O', '.')

# add the floor
for x in range(xmax - xmin + 1 + extraL + extraR):
    arr2[-1][x] = '#'

if plot:
    print('\n\n\n')
    for a in arr2:
        print(''.join(a))

# simulate
num_sand = 0

while True:
    # initial position
    x = x_source + extraL
    y = y_source
    stuck = False
    num_sand += 1

    # are we done?
    if arr2[y+1][x-1] == arr2[y+1][x] == arr2[y+1][x+1] == 'O':
        break

    # move while we can
    while not stuck:
        if arr2[y+1][x] == '.':
            y += 1
        elif arr2[y+1][x-1] == '.':
            y += 1
            x -= 1
        elif arr2[y+1][x+1] == '.':
            y += 1
            x += 1
        else:
            arr2[y][x] = 'O'
            stuck = True

print(num_sand)
