import math

v = int(input()) #velocity
t = int(input()) #time
s = 109

ans = (v * t) % s

print(abs(ans))