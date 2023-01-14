dat = open('23.txt', 'r').read().splitlines()

# (x,y) of the elves' positions
positions = []
for y, row in enumerate(dat):
    for x, c in enumerate(row):
        if c == '#':
            positions.append((x,y))

# which dx, dy we try, in the proper order
to_try = [
   [(-1,-1), ( 0, -1), (+1,-1)], 
   [(-1,+1), ( 0, +1), (+1,+1)], 
   [(-1,-1), (-1,  0), (-1,+1)], 
   [(+1,-1), (+1,  0), (+1,+1)], 
]

from collections import Counter

def update(positions, to_try):

    is_change = False
    proposals = [(0,0) for _ in positions]
    cntr = Counter()

    # proposed positions
    for i, (x, y) in enumerate(positions):
        
        # check all directions in the correct order - is the given direction available?
        is_empty = [
                    all(
                        (x+dx,y+dy) not in positions 
                        for dx,dy in steps
                       ) 
                    for steps in to_try
                   ]

        # no need to move
        if all(is_empty):
            dx = 0
            dy = 0
        # otherwise we move into the middle position of the first available direction
        elif is_empty[0]:
            dx = to_try[0][1][0]
            dy = to_try[0][1][1]
        elif is_empty[1]:
            dx = to_try[1][1][0]
            dy = to_try[1][1][1]
        elif is_empty[2]:
            dx = to_try[2][1][0]
            dy = to_try[2][1][1]
        elif is_empty[3]:
            dx = to_try[3][1][0]
            dy = to_try[3][1][1]
        # nowhere to move
        else:
            dx = 0
            dy = 0

        # update given elf
        proposals[i] = (x+dx, y+dy)
        cntr.update([(x+dx, y+dy)])

    # decide if we move - check for collisions
    newpositions = [(0,0) for _ in positions]
    for i, (x, y) in enumerate(positions):
        if cntr[proposals[i]] == 1:
            if proposals[i] != (x,y):
                is_change = True
            newpositions[i] = proposals[i]
        else:
            newpositions[i] = (x,y)

    # rotate order of directions in which we test
    new_to_try = to_try[1:] + [to_try[0]]

    return newpositions, new_to_try, is_change

for round_no in range(10):
    positions, to_try, _ = update(positions, to_try)

minx = min(pos[0] for pos in positions)
maxx = max(pos[0] for pos in positions)
miny = min(pos[1] for pos in positions)
maxy = max(pos[1] for pos in positions)

print((maxx - minx + 1)*(maxy - miny + 1) - len(positions))

#####
# Problem 2
#####

positions = []
for y, row in enumerate(dat):
    for x, c in enumerate(row):
        if c == '#':
            positions.append((x,y))

# which dx, dy we try
to_try = [
   [(-1,-1), ( 0, -1), (+1,-1)], 
   [(-1,+1), ( 0, +1), (+1,+1)], 
   [(-1,-1), (-1,  0), (-1,+1)], 
   [(+1,-1), (+1,  0), (+1,+1)], 
]

round_no = 0

while True:
    round_no += 1
    positions, to_try, is_change = update(positions, to_try)
    if not is_change:
        print(round_no)
        break
