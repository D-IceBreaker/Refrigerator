a = int(input())
b = int(input())
ans = ""

for i in range(b + 1):
    if i*i >= a and i*i <= b:
        ans += str(i*i) + " "

print(ans)