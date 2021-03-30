def min_of_four(a, b, c, d):
    if a < b and a < c and a < d:
        return a
    elif b < c and b < d:
        return b
    elif c < d:
        return c
    else:
        return d

if __name__ == "__main__":
    a = [int(x) for x in input().split()]
    ans = min_of_four(a[0], a[1], a[2], a[3])
    print(ans)