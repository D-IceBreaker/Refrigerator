# import math

# ans = 1

# if x == 0:
#     ans = 0

# for i in range(1, int(x/2 + 1)):
#     if x % i == 0:
#         ans += 1

# print(ans)

def divisor_count(n):
    return len([i for i in range(1, n + 1) if n % i == 0])

if __name__ == "__main__":
    x = int(input())
    print(divisor_count(x))