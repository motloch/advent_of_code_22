# load the jet patterns, count how many jets there are
jet_pattern = open('17.txt', 'r').read().splitlines()[0]
num_jets = len(jet_pattern)

# various shapes, count how many there are
shapes = [['@'*4], ['.@.', '@@@', '.@.'], ['..@', '..@', '@@@'], ['@']*4, ['@@']*2]
num_shapes = len(shapes)

# We will store the tower of rocks as a list of strings. For convenience, the "top of the
# tower" will be at the end of the array. So the rocks fall from the end of the array
# towards the beginning.

def process_shape(tower_state, jet_idx, shape_idx):
    """
    Given a tower of rocks as a list of strings, index of the next jet and index of the
    next shape, return these three after the next rock has fallend down and stopped.

    """

    current_shape = shapes[shape_idx]
    current_height = len(current_shape)

    # add the three empty spaces plus however many are necessary for the shape
    tower_state += ['.......']*(3 + current_height)

    # current shape position (position of its top left corner)
    x = 2
    y = len(tower_state) - 1

    # move until we get stuck
    while True:

        # Left/right move
        if jet_pattern[jet_idx] == '>':
            shift = 1
        else:
            shift = - 1

        can_move = True

        # check if '#' characters can move
        for i, row in enumerate(current_shape):
            for j, c in enumerate(row):
                xc = x + j
                yc = y - i 
                if c == '.':
                    pass
                else:
                    if xc+shift > 6 or xc+shift < 0 or tower_state[yc][xc+shift] == '#':
                        can_move = False

        if can_move:
            x += shift

        jet_idx = (jet_idx + 1) % num_jets

        # Down
        can_move = True

        # check if '#' characters can move
        for i, row in enumerate(current_shape):
            for j, c in enumerate(row):
                xc = x + j
                yc = y - i
                if c == '.':
                    pass
                else:
                    if tower_state[yc - 1][xc] == '#':
                        can_move = False

        if can_move:
            # moving down means towards the beginning of the list
            y -= 1
        else:
            # get stuck
            for i, row in enumerate(current_shape):
                for j, c in enumerate(row):
                    xc = x + j
                    yc = y - i
                    if c == '.':
                        pass
                    else:
                        tower_state[yc] = tower_state[yc][:xc] + '#' + tower_state[yc][xc+1:]

            # erase empty lines at the top
            while tower_state[-1] == '.......':
                del tower_state[-1]

            # new shape
            shape_idx = (shape_idx + 1) % num_shapes
                
            break

    return tower_state, jet_idx, shape_idx

#####
# Problem 1
#####

# initialize with only the floor, first jet stream, first shape
tower_state = ['#######']
jet_idx = 0
shape_idx = 0

# drop 2022 rocks
for idx in range(2022):
    tower_state, jet_idx, shape_idx = process_shape(tower_state, jet_idx, shape_idx)

print(len(tower_state) - 1) # minus one for the floor

#####
# Problem 2
#####

NUM_ROCKS = 1000000000000

# Given the large number of rocks to simulate, we will search for periodicity. This means we
# want to have the same shape (e.g. '####') falling under the influence of the same jet
# pattern (e.g. starting with second jet) into effectively the same configuration of
# stopped rocks.

# We only describe the state of fallen rocks using the top LINES_TO_KEEP rows. For one it
# saves memory, also we assume no rock can fall for more than 100 rows so it does not
# really matter what happens deep under the current top of the tower.
LINES_TO_KEEP = 100

# initialize the simulation with only the floor
tower_state = ['#######']

# we start with the first jet and shape
jet_idx = 0
shape_idx = 0

# we have not discarded any rows from the bottom yet
discarded_lines = 0

# keep track of full configurations in the form (tower state, jet index, shape index) that we have
# encountered
seen_configurations = set()

# for each such configuration, keep track of number of rocks already deposited and height
# of the tower at that time
seen_idxs_heights = {}

# run the simulation until we find a period
for idx in range(NUM_ROCKS):

    # run one step of the simulation
    tower_state, jet_idx, shape_idx = process_shape(tower_state, jet_idx, shape_idx)

    # only keep the top X lines. If possible, drop the bottom of the tower (beginning of
    # the list). But remember how many rows we have discarded.
    if len(tower_state) > LINES_TO_KEEP:
        discarded_lines += len(tower_state) - LINES_TO_KEEP
        tower_state = tower_state[-LINES_TO_KEEP:]

    # convert state to tuples, such that we can use hash
    tuple_state = tuple(tuple(x) for x in tower_state)

    # full configuration, including which jet and shape to use next
    new_configuration = (tuple_state, jet_idx, shape_idx)

    # did we find a period?
    if new_configuration in seen_configurations:
        old_idx, old_height = seen_idxs_heights[new_configuration]
        period = idx - old_idx

        # for simplicity, only consider the case where the period can get us exactly to
        # the desired number of deposited rocks. Otherwise we would have to deal with the
        # last few rocks separately.
        if (NUM_ROCKS - 1 - idx) % period == 0: # -1 for indexing starting with zero
            num_periods_left = (NUM_ROCKS - 1 - idx) // period
            current_height = len(tower_state) + discarded_lines - 1 # -1 for floor
            discarded_lines += num_periods_left * (current_height - old_height)
            break
    else:
       seen_configurations.add(new_configuration) 
       seen_idxs_heights[new_configuration] = (idx, len(tower_state) + discarded_lines - 1) #-1 for floor

print(len(tower_state) + discarded_lines - 1) # minus one for the floor
