def xor(x, y):
    if x != y:
        return 1
    else:
        return 0

if __name__ == "__main__":
    a = [int(x) for x in input().split()]
    ans = xor(a[0], a[1])
    print(ans)