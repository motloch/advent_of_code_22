dat = open('02.txt', 'r').read().splitlines()

d = {
    'A X': 3+1,
    'B X': 0+1,
    'C X': 6+1,
    'A Y': 6+2,
    'B Y': 3+2,
    'C Y': 0+2,
    'A Z': 0+3,
    'B Z': 6+3,
    'C Z': 3+3
    }

print(sum(d[x] for x in dat))

d2 = {
    'A X': 0+3,
    'B X': 0+1,
    'C X': 0+2,
    'A Y': 3+1,
    'B Y': 3+2,
    'C Y': 3+3,
    'A Z': 6+2,
    'B Z': 6+3,
    'C Z': 6+1
    }

print(sum(d2[x] for x in dat))
