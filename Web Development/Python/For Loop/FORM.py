N = int(input())
ans = 0

for i in range(N):
    if int(input()) == 0:
        ans += 1

print(ans)