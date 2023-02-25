dat = open('25.txt', 'r').read().splitlines()

decimal_total = 0

def snafu_to_decimal(snafu):
    decimal = 0

    for c in snafu:
        decimal *= 5
        if c == '1':
            decimal += 1
        if c == '2':
            decimal += 2
        if c == '-':
            decimal -= 1
        if c == '=':
            decimal -= 2

    return decimal
    

# sum decimal values
decimal_total = sum(snafu_to_decimal(row) for row in dat)

# convert to snafu
def decimal_to_snafu(decimal):
    reminder = decimal
    snafu = ''

    while reminder > 0:
        current = reminder % 5
        reminder = reminder // 5

        if current == 0 and reminder > 0:
            snafu = '0' + snafu
        elif current == 1:
            snafu = '1' + snafu
        elif current == 2:
            snafu = '2' + snafu
        elif current == 3:
            snafu = '=' + snafu
            reminder += 1
        elif current == 4:
            snafu = '-' + snafu
            reminder += 1

    return snafu

print(decimal_to_snafu(decimal_total))
