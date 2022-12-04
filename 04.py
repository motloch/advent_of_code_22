dat = open('04.txt', 'r').read().splitlines()

full_overlap = 0
for line in dat:
    w1, w2 = line.split(',')
    x1,y1 = w1.split('-')
    x2,y2 = w2.split('-')
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    if x1 <= x2 and y1 >= y2:
        full_overlap += 1
    elif x1 >= x2 and y1 <= y2:
        full_overlap += 1

print(full_overlap)

overlap = 0
for line in dat:
    w1, w2 = line.split(',')
    x1,y1 = w1.split('-')
    x2,y2 = w2.split('-')
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    if y1 < x2 or y2 < x1:
        pass
    else:
        overlap += 1

print(overlap)

