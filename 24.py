import numpy as np

dat = open('24.txt', 'r').read().splitlines()

# size of the valley (ignoring the walls)
m = len(dat) - 2
n = len(dat[0]) - 2

# collect the starting positions of the blizzards
left = []
right = []
down = []
up = []

for y, row in enumerate(dat[1:-1]):
    for x, c in enumerate(row[1:-1]):
        if c == '>':
            right.append((x,y))
        if c == '<':
            left.append((x,y))
        if c == '^':
            up.append((x,y))
        if c == 'v':
            down.append((x,y))

# directions of the neighbors + we can also wait
steps = [(1,0), (-1,0), (0,1), (0,-1), (0,0)]

# check if inside the valley
def isIn(y,x):
    return x>= 0 and y>=0 and x < n and y < m

def time_of_travel(initial_time, start, end):
    """
    How long it will take us from start to end, if we start at some initial time
    """

    # at the beginning, we can not get anywhere
    is_accessible = np.zeros((m,n), dtype = bool)

    time = initial_time

    while True:
        # which positions we can get to after this round - start with all as accessible
        new_is_accessible = np.ones((m,n), dtype = bool)

        # where the blizzards are = not accessible
        for x,y in left:
            new_is_accessible[y, (x - time) % n] = False
        for x,y in right:
            new_is_accessible[y, (x + time) % n] = False
        for x,y in up:
            new_is_accessible[(y - time) % m, x] = False
        for x,y in down:
            new_is_accessible[(y + time) % m, x] = False

        # check if we could have ended up on any of the neighbors (or here) previous
        # round. If not, not accessible.
        for y in range(m):
            for x in range(n):
                has_ok_neighbor = False

                for dx, dy in steps:
                    if isIn(y+dy,x+dx) and is_accessible[y+dy,x+dx]:
                        has_ok_neighbor = True

                # we can always wait outside of the valley
                if y == start[0] and x == start[1]:
                    has_ok_neighbor = True

                if not has_ok_neighbor:
                    new_is_accessible[y,x] = False

        is_accessible = new_is_accessible

        time += 1

        # check the end
        if is_accessible[end[0], end[1]]:
            return(time)
            break


# travel there
t1 = time_of_travel(0, (0,0), (m-1,n-1))
# travel back to beginning
t2 = time_of_travel(t1, (m-1,n-1), (0,0))
# travel back to the elves
t3 = time_of_travel(t2, (0,0), (m-1,n-1))

print(t1)
print(t3)
