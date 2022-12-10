dat = open('10.txt', 'r').read().splitlines()

#####
# Problem #1
#####

X = 1
cycles_to_use = [20, 60, 100, 140, 180, 220]
cycle_no = 1

result = 0

for line in dat:
    if cycle_no in cycles_to_use:
        result += X*cycle_no

    if line == 'noop':
         
        cycle_no += 1
    else:
        addition = int(line.split()[1])
        if cycle_no + 1 in cycles_to_use:
            result += X*(cycle_no+1)
        X += addition
        cycle_no += 2

print(result)
        
#####
# Problem #2
#####

WIDTH = 40
HEIGHT = 6

X = 1
pixel_pos = 0

result = []

for line in dat:
    if line == 'noop':

        # decide if pixel is dark or lit, shift pixel
        if abs(X - pixel_pos) <= 1:
            result.append('#')
        else:
            result.append('.')

        pixel_pos = (pixel_pos + 1) % WIDTH

    else:

        # with addition, we decide about two pixels
        for cycle in range(2):
            if abs(X - pixel_pos) <= 1:
                result.append('#')
            else:
                result.append('.')
        
            pixel_pos = (pixel_pos + 1) % WIDTH

        # and then shift
        addition = int(line.split()[1])
        X += addition

for k in range(HEIGHT):
    print(''.join(result[k*WIDTH:(k+1)*WIDTH]))
        
