import math

def f(m,k):
    if m==0:
        return math.factorial(k)
    if k==1:
        return m*f(m-1,k+1)
    return m*f(m-1, k+1) + k*f(m, k-1)

def comb(m,k):
    if m==0:
        print (k,'! permutations of destination')
        return math.factorial(k)
    if k==1:
        return m*comb(m-1,k+1)
    return m*comb(m-1, k+1) + k*comb(m, k-1)

n = 8
z = n*(n-1)*f(n-2,2)
print('sum',z)