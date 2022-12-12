from copy import deepcopy

dat = open('11.txt', 'r').read().splitlines()

num_monkeys = sum('Monkey' in line for line in dat)

state = []
operations = []
divisibles = []
if_true = []
if_false = []

for monkey in range(num_monkeys):
    # read in the initial state
    items = dat[1 + 7*monkey].split(': ')[-1].split(',')
    items = list(map(int, items))
    state.append(items)

    # read in the operations
    current = dat[2 + 7*monkey].split('=')[-1]
    operations.append(current)

    # read in the test criterios
    current = int(dat[3 + 7*monkey].split(' ')[-1])
    divisibles.append(current)

    # read in the next if true
    current = int(dat[4 + 7*monkey].split(' ')[-1])
    if_true.append(current)

    # read in the next if false
    current = int(dat[5 + 7*monkey].split(' ')[-1])
    if_false.append(current)

# preserve the original state for the second problem
original_state = deepcopy(state)

#####
# Problem 1
#####

# Perform the monkey dance
num_inspections = [0 for monkey in range(num_monkeys)]

for turn in range(20):
    for monkey in range(num_monkeys):
        while len(state[monkey]):
            old = state[monkey].pop()

            # inspection
            num_inspections[monkey] += 1
            new = eval(operations[monkey])

            # bored
            new = new // 3

            # check where next
            if new % divisibles[monkey] == 0:
                state[if_true[monkey]].append(new)
            else:
                state[if_false[monkey]].append(new)

num_inspections = sorted(num_inspections)
print(num_inspections[-1] * num_inspections[-2])

#####
# Problem 2
#####

state = original_state
from math import prod
K = prod(divisibles) # we only need keep track of the worry level modulo K

# Perform the monkey dance
num_inspections = [0 for monkey in range(num_monkeys)]

for turn in range(10000):
    for monkey in range(num_monkeys):
        while len(state[monkey]):
            old = state[monkey].pop(0)

            # inspection
            num_inspections[monkey] += 1
            new = eval(operations[monkey]) % K

            # check where next
            if new % divisibles[monkey] == 0:
                state[if_true[monkey]].append(new)
            else:
                state[if_false[monkey]].append(new)

num_inspections = sorted(num_inspections)
print(num_inspections[-1] * num_inspections[-2])
