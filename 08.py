dat = open('08.txt', 'r').read().splitlines()
arr = [list(map(int, line)) for line in dat]

m, n = len(arr), len(arr[0])

######
# Problem 1
######

is_visible = [[False for i in range(n)] for j in range(m)]

# rows
for i in range(m):
    
    # from the left
    highest = -1
    for j in range(n):
        if arr[i][j] > highest:
            is_visible[i][j] = True
            highest = arr[i][j]

    # from the right
    highest = -1
    for j in range(n-1,-1,-1):
        if arr[i][j] > highest:
            is_visible[i][j] = True
            highest = arr[i][j]

# columns
for j in range(n):
    
    # from the left
    highest = -1
    for i in range(m):
        if arr[i][j] > highest:
            is_visible[i][j] = True
            highest = arr[i][j]

    # from the right
    highest = -1
    for i in range(m-1,-1,-1):
        if arr[i][j] > highest:
            is_visible[i][j] = True
            highest = arr[i][j]

num_visible = 0
for i in range(m):
    num_visible += sum(is_visible[i])
print(num_visible)

######
# Problem 2
######

# Number of trees we can see when looking up/down/left/right
view_u = [[0 for i in range(n)] for j in range(m)]
view_d = [[0 for i in range(n)] for j in range(m)]
view_l = [[0 for i in range(n)] for j in range(m)]
view_r = [[0 for i in range(n)] for j in range(m)]

# rows
for i in range(m):

    # how far is the tree of height at least x?
    distance_to_height = [0 for i in range(10)]
    
    # from the left
    for j in range(n):
        view_l[i][j] = distance_to_height[arr[i][j]]

        # if we have tree of height 3, then we should end up with
        # [1, 1, 1, 1, x+1, y+1, z+1, ...]
        for k in range(arr[i][j] + 1):
            distance_to_height[k] = 1
        for k in range(arr[i][j] + 1, 10):
            distance_to_height[k] += 1

    # from the right
    distance_to_height = [0 for i in range(10)]
    for j in range(n-1,-1,-1):
        view_r[i][j] = distance_to_height[arr[i][j]]
        for k in range(arr[i][j] + 1):
            distance_to_height[k] = 1
        for k in range(arr[i][j] + 1, 10):
            distance_to_height[k] += 1

# columns
for j in range(n):

    # how far is the tree of height at least x?
    distance_to_height = [0 for i in range(10)]
    
    # from the top
    for i in range(m):
        view_u[i][j] = distance_to_height[arr[i][j]]
        for k in range(arr[i][j] + 1):
            distance_to_height[k] = 1
        for k in range(arr[i][j] + 1, 10):
            distance_to_height[k] += 1

    # from the bottom
    distance_to_height = [0 for i in range(10)]
    for i in range(m-1,-1,-1):
        view_d[i][j] = distance_to_height[arr[i][j]]
        for k in range(arr[i][j] + 1):
            distance_to_height[k] = 1
        for k in range(arr[i][j] + 1, 10):
            distance_to_height[k] += 1

# find the max
result = 0
for i in range(m):
    for j in range(n):
        result = max(result, view_u[i][j] * view_d[i][j] * view_r[i][j] * view_l[i][j])

print(result)
