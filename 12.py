arr = open('12.txt', 'r').read().splitlines()
arr = [list(row) for row in arr]

m = len(arr)
n = len(arr[0])

distance = [[None for i in range(n)] for j in range(m)]
found = [[False for i in range(n)] for j in range(m)]

# find start and finish
for i in range(m):
    for j in range(n):
        if arr[i][j] == 'E':
            end = (i, j)
            arr[i][j] = 'z'
        elif arr[i][j] == 'S':
            start = (i, j)
            arr[i][j] = 'a'

# the format is ((x,y), distance) ; start at the end because of the second part
queue = [(end, 0)]
found[end[0]][end[1]] = True

# check if position is in the array
def isIn(x,y):
    return x >= 0 and y>=0 and x < m and y < n

while queue:
    # we found the shortest path
    (x, y), d = queue.pop(0)
    distance[x][y] = d

    # check out neighbors
    for dx, dy in [[1,0], [-1,0], [0,1], [0,-1]]:
        
        # must be in the array, we have not gotten there yet
        if isIn(x+dx, y+dy) and not found[x+dx][y+dy]:
            # can only go one letter up
            if ord(arr[x+dx][y+dy]) + 1 >= ord(arr[x][y]):
                queue.append(((x+dx, y+dy), d+1))
                found[x+dx][y+dy] = True

print(distance[start[0]][start[1]])

min_dist = 10**9
for i in range(m):
    for j in range(n):
        # find the closest 'a' that can be reached from the end
        if distance[i][j] and arr[i][j] == 'a':
            min_dist = min(min_dist, distance[i][j])
print(min_dist)
