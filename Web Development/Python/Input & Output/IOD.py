import math

N = int(input()) #number of kids
K = int(input()) #number of apples

ans = K / N

print(K - (math.floor(ans) * N))