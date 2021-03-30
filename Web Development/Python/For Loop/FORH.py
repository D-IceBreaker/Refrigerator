x = int(input())
ans = ""

for i in range(1, x + 1):
    if x % i == 0:
        ans += str(i) + " "

print(ans)