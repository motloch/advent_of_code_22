num_cols = 9
num_rows = 8

dat = [x.replace('\n', '') for x in open('05.txt', 'r').readlines()]

def load_state():

    # keep track of letters in the column
    state = [[] for _ in range(num_cols)]

    # initialize, keep the top-most character at the end of the list
    for row in dat[:num_rows]:
        for col_idx in range(num_cols):
            current_char = row[1 + 4*col_idx]
            if current_char != ' ':
                state[col_idx].insert(0, current_char)

    return state

# Problem 1

state = load_state()

for row in dat[num_rows+2:]:
    _, num, _, from_col, _, to_col = row.split()  
    num, from_col, to_col = int(num), int(from_col), int(to_col)
    for i in range(num):
        c = state[from_col-1].pop()
        state[to_col-1].append(c)

print(''.join([x[-1] for x in state]))
    
# Part 2

state = load_state()

for row in dat[num_rows+2:]:
    _, num, _, from_col, _, to_col = row.split()  
    num, from_col, to_col = int(num), int(from_col), int(to_col)
    state[to_col-1] += state[from_col-1][-num:]
    del state[from_col-1][-num:]

print(''.join([x[-1] for x in state]))
    

