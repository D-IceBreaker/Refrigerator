def second_max(arr):
    minimum = -101
    first, second = minimum, minimum
    for n in arr:
        if n > first:
            first, second = n, first
        elif first > n > second:
            second = n
    return second if second != minimum else None

if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())

    print(second_max(arr))


