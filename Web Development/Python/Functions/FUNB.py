def my_power(a, b):
    if b == 0:
        return 1
    ans = a
    for i in range(1, b):
        ans *= a
        i += 1
    return ans

if __name__ == "__main__":
    a = [int(x) for x in input().split()]
    ans = my_power(a[0], a[1])
    print(ans)