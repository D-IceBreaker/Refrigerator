N = int(input())
a = [int(x) for x in input().split()]

ans = a[::-1]
for i in range(N):
    print(ans[i], end=" ")