dat = open('09.txt', 'r').read().splitlines()

# separate direction and length of step
dat = [x.split() for x in dat]

steps = {
    'R': [ 1, 0],
    'L': [-1, 0],
    'D': [0, -1],
    'U': [0, 1]
}

def solve_for_chain(N):

    positions = [(0,0) for i in range(N)]

    visited = set([(0,0)])

    for direction, length in dat:
        dhx, dhy = steps[direction]

        for step_no in range(int(length)):
            for part in range(N):
                if part == 0:
                    positions[part] = (positions[part][0] + dhx, positions[part][1] + dhy)
                else:
                    dx = positions[part-1][0] - positions[part][0]
                    dy = positions[part-1][1] - positions[part][1]

                    if dx == 2 and dy == 2:
                        positions[part] = (positions[part-1][0]-1, positions[part-1][1]-1)
                    elif dx == 2 and dy == -2:
                        positions[part] = (positions[part-1][0]-1, positions[part-1][1]+1)
                    elif dx == -2 and dy == 2:
                        positions[part] = (positions[part-1][0]+1, positions[part-1][1]-1)
                    elif dx == -2 and dy == -2:
                        positions[part] = (positions[part-1][0]+1, positions[part-1][1]+1)
                    elif dx == 2:
                        positions[part] = (positions[part-1][0]-1, positions[part-1][1])
                    elif dx == -2:
                        positions[part] = (positions[part-1][0]+1, positions[part-1][1])
                    elif dy == 2:
                        positions[part] = (positions[part-1][0], positions[part-1][1]-1)
                    elif dy == -2:
                        positions[part] = (positions[part-1][0], positions[part-1][1]+1)

            visited.add(positions[-1])

    return len(visited)

print(solve_for_chain(2))
print(solve_for_chain(10))
