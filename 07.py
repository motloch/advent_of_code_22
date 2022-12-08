# Nodes to build the tree out of
class Node:
    def __init__(self, parent, size = None, isDir = True):
        self.isDir = isDir
        self.size = size
        self.children = {}
        self.parent = parent

# Load the data
dat = open('07.txt', 'r').read().splitlines()

######
# Build the filesystem structure
######

# Structure describing the filesystem
tree = Node(parent = None)

# Pointer to where user is as we go through the commands
pointer = tree

# Build the filesystem line by one
line_no = 0
while line_no < len(dat):

    # read the next instruction
    instruction = dat[line_no].split()
    assert '$' == instruction[0]

    # process the instruction
    if instruction[1] == 'cd' and instruction[2] == '..':
        assert pointer.parent
        pointer = pointer.parent
        line_no += 1
    elif instruction[1] == 'cd' and instruction[2] == '/':
        pointer = tree
        line_no += 1
    elif instruction[1] == 'cd':
        pointer = pointer.children[instruction[2]]
        line_no += 1
    elif instruction[1] == 'ls':

        if pointer.children != {}:
            revisited = True
        else:
            revisited = False

        line_no += 1

        while line_no < len(dat) and '$' not in dat[line_no]:
            size, name = dat[line_no].split() 
            if not revisited:
                if size == 'dir':
                    pointer.children[name] = Node(parent = pointer, isDir = True)
                else:
                    pointer.children[name] = Node(parent = pointer, isDir = False, size = int(size))
            line_no += 1
    else:
        print('Unknown command')
        exit()

#####
# Fill in folder sizes
#####

def getSize(folder: Node):
    size = 0 

    # sum over children, recursion if necessary
    for name, child in folder.children.items():

        if not child.size:
            assert child.isDir
            getSize(child)

        size += child.size

    folder.size = size

getSize(tree)

#####
# Problem 1
#####

result = 0
queue = [tree]

while queue:
    current = queue.pop()
    if current.size <= 100000:
        result += current.size

    for name, child in current.children.items():
        if child.isDir:
            queue.append(child)

print(result)

#####
# Problem 2
#####
unused = 70000000 - tree.size
needs = 30000000 - unused

optimal_size = 1e9
queue = [tree]

while queue:
    current = queue.pop()

    if current.size < optimal_size and current.size >= needs:
        optimal_size = current.size

    for name, child in current.children.items():
        if child.isDir:
            queue.append(child)

print(optimal_size)
