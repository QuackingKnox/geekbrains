import math

n = 2236938
x = list(range(1, n+1))
new_list = []
for i in x:
    new_list.append(i**(1/n))
E = 10**-6
a = 1
for i in x:
    a *= new_list[i-1]
    func = i / a
print(func, math.e - func, E)
