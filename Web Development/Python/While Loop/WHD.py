a = int(input())

while a > 0:
    if a == 1:
        print('YES')
        break
    elif a % 2 != 0:
        print('NO')
        break
    a /= 2