import math

N = int(input())
a = [int(x) for x in input().split()]
ans = False

for i in range(1, N):
    if a[i] == math.copysign(a[i], a[i - 1]):
        ans = True
        break

if ans:
    print('YES')
else:
    print('NO')