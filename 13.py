dat = open('13.txt', 'r').read().splitlines()

num_messages = (len(dat) // 3)
if len(dat) % 3 != 0:
    num_messages += 1

######
# Part 1
######

correct = []

WRONG_ORDER = 1
RIGHT_ORDER = -1

def process(expL, expR):
    """
    Compares the two expressions.
    """

    # apply the comparison rules
    for valL, valR in zip(expL, expR):

        # if comparing integers, we can make a decision unless equal
        if type(valL) == type(valR) == int:
            if valL > valR:
                return WRONG_ORDER
            if valL < valR:
                return RIGHT_ORDER

        # at least one list - recursion
        else:

            # if ints present, convert to array
            if type(valL) == int:
                valL = [valL]
            if type(valR) == int:
                valR = [valR]

            # unless it is draw, return
            x = process(valL, valR)
            if x in [WRONG_ORDER, RIGHT_ORDER]:
                return x

    # if we got here, all is ok so far. we have to check which list is longer
    if len(expL) <= len(expR):
        return RIGHT_ORDER
    else:
        return WRONG_ORDER

# check each pair
for idx in range(1, num_messages + 1):
    exp1 = eval(dat[3*idx - 3])
    exp2 = eval(dat[3*idx - 2])

    if process(exp1, exp2) == RIGHT_ORDER:
        correct.append(idx)

print(sum(correct))

######
# Part 2
######

DIVIDER_PACKETS = [[[2]], [[6]]]

# get the packets
all_packets = [eval(x) for i, x in enumerate(dat) if i % 3 != 2] 
all_packets += DIVIDER_PACKETS

# sort according to 'process' function
from functools import cmp_to_key
all_packets = sorted(all_packets, key = cmp_to_key(process))

# find the two special packets
idxes = []
for idx, packet in enumerate(all_packets):
    if packet in DIVIDER_PACKETS:
        idxes.append(idx + 1) # one-indexed

# return product
from math import prod
print(prod(idxes))
