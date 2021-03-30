a = int(input())
b = int(input())
ans = ""

if a % 2 == 0:
    for i in range(a, b + 1, 2):
        ans += str(i) + " "
else:
    for i in range(a + 1, b + 1, 2):
        ans += str(i) + " "

print(ans)