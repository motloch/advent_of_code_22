# allow both options - the test case and the full problem
fname = '22.txt'
dat = open(fname, 'r').read().splitlines()

# save the board as 2D array
board = []

for row in dat[:-2]:
    board.append(list(row))

# size of the board
m = len(board)
n = max(len(row) for row in board)

# pad rows that are shorter than n with ' '
for i, row in enumerate(board):
    if len(row) < n:
        board[i] = row + [' '] * (n - len(row))

# split the instructions into (step length, rotation) tuples - if there is no rotation at
# the end, set None
instructions = dat[-1]
import re
instructions = re.findall(r'\d+[LR]{0,1}', instructions)
instructions = [(int(x[:-1]), x[-1]) if not x.isdigit() else (int(x), None) for x in instructions]

# dx, dy steps dependent on orientation
steps = [
            [1, 0],  # right
            [0, 1],  # down
            [-1, 0], # left
            [0, -1]  # up
        ]

#####
# Part 1
#####

# starting positions/orientation (y is facing downward, x to the right)
y = 0
x = 0
while board[y][x] != '.':
    x += 1
facing = 0

for num_steps, rotation in instructions:
    # make the step
    for i in range(num_steps):  
        newx = (x + steps[facing][0]) % n
        newy = (y + steps[facing][1]) % m

        # wrap around
        while board[newy][newx] == ' ':
            newx = (newx + steps[facing][0]) % n
            newy = (newy + steps[facing][1]) % m

        # either make the step, or end the move
        if board[newy][newx] == '#':
            break
        elif board[newy][newx] == '.':
            x = newx
            y = newy

    # rotate
    if rotation == 'R':
        facing = (facing + 1) % 4
    elif rotation == 'L':
        facing = (facing - 1) % 4

# output result - plus one because we index from zero, not from one
print(1000*(y + 1) + 4*(x + 1) + facing)

#####
# Part 2
#####

def extract_face(ys, xs, n):
    """
    Obtain n*n 2D array corresponding to one face of the cube, starting at (ys,xs)
    position of the full board. n is size of the cube.
    """
    res = []
    for y in range(ys, ys+n):
        res.append(board[y][xs:xs+n])
    return res

# obtain the individual faces of the cube
if fname == '22b.txt':
    # Distribution of the faces:
    #       F0   
    # F1 F2 F3   
    #       F4 F5
    n = 4
    face_starts = [[0,2*n], [n,0], [n,n], [n,2*n], [2*n,2*n], [2*n,3*n]]
else:
    # Distribution of the faces:
    #    F0 F1
    #    F2   
    # F3 F4   
    # F5      
    n = 50
    face_starts = [[0,n], [0,2*n], [n,n], [2*n,0], [2*n,n], [3*n,0]]

cube = [ extract_face(yy, xx, n) for yy, xx in face_starts ]

# starting face/positions/orientation (y is facing downward, x to the right)
face = 0
y = 0
x = 0
while cube[face][y][x] != '.':
    x += 1
facing = 0

def isWrap(x,y):
    """
    Are we switching to another face?
    """
    if x < 0 or y < 0 or x >= n or y >= n:
        return True
    else:
        return False

if fname == '22b.txt':
    # test case
    def Wrap(face, y, x, facing):
        """
        Performs the stitching of the faces.

        Return new face, y, x and facing when going to another face
        """
        if face == 0:
            if facing == 0:
                return 5, n - 1 - y, n - 1, 2
            if facing == 1:
                return 3, 0, x, 1
            if facing == 2:
                return 2, 0, n - 1 - y, 1
            if facing == 3:
                return 1, 0, n - 1 - x, 1
        if face == 1:
            if facing == 0:
                return 2, y, 0, 0
            if facing == 1:
                return 4, n - 1, n - 1 - x, 3
            if facing == 2:
                return 5, n - 1, n - 1 - y, 3
            if facing == 3:
                return 0, 0, n - 1 - x, 1
        if face == 2:
            if facing == 0:
                return 3, y, 0, 0
            if facing == 1:
                return 4, n - 1 - x, 0, 0
            if facing == 2:
                return 1, y, n - 1, 2
            if facing == 3:
                return 0, x, 0, 0
        if face == 3:
            if facing == 0:
                return 5, 0, n - 1-y, 1
            if facing == 1:
                return 4, 0, x, 1
            if facing == 2:
                return 2, y, n - 1, 2
            if facing == 3:
                return 0, n - 1, x, 3
        if face == 4:
            if facing == 0:
                return 5, y, 0, 0
            if facing == 1:
                return 1, n - 1, n - 1-x, 3
            if facing == 2:
                return 2, n - 1, n - 1-y, 3
            if facing == 3:
                return 3, n - 1, x, 3
        if face == 5:
            if facing == 0:
                return 0, y, 0, 2
            if facing == 1:
                return 1, n - 1 - x, 0, 0
            if facing == 2:
                return 4, y, n - 1, 2
            if facing == 3:
                return 3, n - 1 - x, n - 1, 2
else:
    # actual problem
    # faces:
    #    F0 F1
    #    F2   
    # F3 F4   
    # F5      
    def Wrap(face, y, x, facing):
        """
        Performs the stitching of the faces.

        Return new face, y, x and facing when going to another face
        """
        if face == 0:
            if facing == 0:
                return 1, y, 0, 0
            if facing == 1:
                return 2, 0, x, 1
            if facing == 2:
                return 3, n - 1 - y, 0, 0
            if facing == 3:
                return 5, x, 0, 0
        if face == 1:
            if facing == 0:
                return 4, n - 1 - y, n-1, 2
            if facing == 1:
                return 2, x, n - 1, 2
            if facing == 2:
                return 0, y, n - 1, 2
            if facing == 3:
                return 5, n-1, x, 3
        if face == 2: 
            if facing == 0:
                return 1, n-1, y, 3
            if facing == 1:
                return 4, 0, x, 1
            if facing == 2:
                return 3, 0, y, 1
            if facing == 3:
                return 0, n-1, x, 3
        if face == 3:
            if facing == 0:
                return 4, y, 0, 0
            if facing == 1:
                return 5, 0, x, 1
            if facing == 2:
                return 0, n-1-y, 0, 0
            if facing == 3:
                return 2, x, 0, 0
        if face == 4:
            if facing == 0:
                return 1, n-1-y, n-1, 2
            if facing == 1:
                return 5, x, n-1, 2
            if facing == 2:
                return 3, y, n - 1, 2
            if facing == 3:
                return 2, n - 1, x, 3
        if face == 5:
            if facing == 0:
                return 4, n-1, y, 3
            if facing == 1:
                return 1, 0, x, 1
            if facing == 2:
                return 0, 0, y, 1
            if facing == 3:
                return 3, n - 1, x, 3

for num_steps, rotation in instructions:
    # make the step
    for i in range(num_steps):  
        newface = face
        newx = x + steps[facing][0]
        newy = y + steps[facing][1]
        newfacing = facing

        # if we wrap around the edge
        if isWrap(newx, newy):
            newface, newy, newx, newfacing = Wrap(face, y, x, facing)

        # either make the step, or end the move
        if cube[newface][newy][newx] == '#':
            break
        elif cube[newface][newy][newx] == '.':
            face = newface
            x = newx
            y = newy
            facing = newfacing

    # rotate
    if rotation == 'R':
        facing = (facing + 1) % 4
    elif rotation == 'L':
        facing = (facing - 1) % 4

# output result - plus one because we are zero-indexed, face_starts because we 
# should use position on the flat board
print(1000*(y + 1 + face_starts[face][0]) + 4*(x+1+face_starts[face][1]) + facing)
