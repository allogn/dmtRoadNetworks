"""
Recursive Calculation of number of valid path
 for asymptotic complexity analysis
 for design of brute-force method
"""
import math
import doctest


def comb(waiting, inCar):
    """
    >>> comb(2,0)
    4
    >>> comb(3,0)
    60
    >>> comb(4,0)
    1776
    >>> comb(5,0)
    84720
    """
    if waiting == 0:
        return math.factorial(inCar) if inCar > 1 else 1

    result = waiting * comb(waiting - 1, inCar + 1)
    if inCar > 1:
        result += inCar * comb(waiting, inCar - 1)

    return result


doctest.testmod()

nClients = 5
# z = nClients * (nClients - 1) * comb3(nClients - 2, 2)
# z = nClients*comb3(nClients-1, 1)
z = comb(nClients, 0)

print('sum', z)


