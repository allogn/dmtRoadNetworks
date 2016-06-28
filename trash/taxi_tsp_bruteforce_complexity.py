"""
Recursive Calculation of number of valid path
 for asymptotic complexity analysis
 for design of brute-force method
"""
import math
import doctest


def combinations(passengers_waiting, passengers_in_car):
    """
    >>> combinations(2,0)
    4
    >>> combinations(3,0)
    60
    >>> combinations(4,0)
    1776
    >>> combinations(5,0)
    84720
    """
    if passengers_waiting == 0:
        return math.factorial(passengers_in_car) if passengers_in_car > 1 else 1
    result = passengers_waiting * combinations(passengers_waiting - 1, passengers_in_car + 1)
    if passengers_in_car > 1:
        result += passengers_in_car * combinations(passengers_waiting, passengers_in_car - 1)
    return result


doctest.testmod()

nClients = 5
z = combinations(nClients, 0)
# z = nClients * (nClients - 1) * comb(nClients - 2, 2)
# z = nClients*comb(nClients-1, 1)

print('sum', z)


