N = int(input())
a = [str(x) for x in input().split()]
ans = ""

for i in range(0, N, 2):
    ans += a[i] + " "

print(ans)