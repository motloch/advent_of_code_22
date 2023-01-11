dat = open('21.txt', 'r').read().splitlines()

# dictionary with monkey:job pairs
d = {}
for pair in dat:
    monkey, job = pair.split(': ')
    d[monkey] = job

# to speed up repeated calculations
from functools import lru_cache

@lru_cache
def evaluate(monkey):
    """
    Recursively evaluates what given monkey yells
    """
    job = d[monkey] 

    if '+' in job:
        m1, m2 = job.split(' + ')
        return evaluate(m1) + evaluate(m2)
    elif '-' in job:
        m1, m2 = job.split(' - ')
        return evaluate(m1) - evaluate(m2)
    elif '*' in job:
        m1, m2 = job.split(' * ')
        return evaluate(m1) * evaluate(m2)
    elif '/' in job:
        m1, m2 = job.split(' / ')
        return evaluate(m1) / evaluate(m2)
    else:
        return int(job)

print(evaluate('root'))
print('---')

######
# Problem 2
######

# two monkeys that have to yell the same result
root1, root2 = d['root'].split(' + ')

# define a function that inputs humn and returns the difference yelled by these two
# monkeys. We want it to be zero.
def diff(humn):

    evaluate.cache_clear()
    d['humn'] = str(humn)

    return evaluate(root1) - evaluate(root2)

# binary search
low = 0         # leads to 58446040296627.2
high = 2**60    # leads to -1.878208097446397e+19

while low < high:
    mid = (low + high) // 2
    if diff(mid) < 0:
        high = mid - 1
    elif diff(mid) > 0:
        low = mid + 1
    else:
        print(mid) 
        break
