dat = open('01.txt', 'r').read().splitlines()

calories = []

current = 0
for x in dat:
    if x == '':
        calories.append(current)
        current = 0
    else:
        current += int(x)
calories.append(current)

calories = sorted(calories)

print(calories[-1])
print(sum(calories[-3:]))
