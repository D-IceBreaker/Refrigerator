a = int(input())
b = int(input())

if a == b:
    print(0)
elif max(a, b) == a:
    print(1)
else:
    print(2)