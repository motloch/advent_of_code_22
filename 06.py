dat = open('06.txt', 'r').read().splitlines()[0]

for i in range(len(dat)-4):
    if len(set(dat[i:i+4])) == 4:
        print(i + 4)
        break

for i in range(len(dat)-14):
    if len(set(dat[i:i+14])) == 14:
        print(i + 14)
        break
