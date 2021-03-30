N = int(input())
a = [int(x) for x in input().split()]
ans = 0

for i in range(N):
    if a[i] > 0:
        ans += 1

print(ans)