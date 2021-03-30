import math

a = int(input())
i = 1

while i <= math.sqrt(a):
    if i*i <= a:
        print(i*i)
    i += 1