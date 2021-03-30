a = int(input())
i = 0
b = 1

while i <= a:
    if b >= a:
        print(i)
        break
    b *= 2
    i += 1