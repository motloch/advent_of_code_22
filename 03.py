dat = open('03.txt', 'r').read().splitlines()

def score_char(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

score = 0
for s in dat:
    l = len(s) // 2
    c = list((set(s[:l]) & set(s[l:])))[0]
    score += score_char(c)

print(score)

score = 0
l = len(dat)
for i in range(l//3):
    c = list(set(dat[3*i]) & set(dat[3*i+1]) & set(dat[3*i+2]))[0]
    score += score_char(c)

print(score)
