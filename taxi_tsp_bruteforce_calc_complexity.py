"""
Recursive Calculation of number of valid path
 for asymptotic complexity analysis
 for design of brute-force method
"""
import math


# def comb(waiting, inCar):
#     if waiting == 0:
#         return math.factorial(inCar)
#     if inCar == 1:
#         return waiting * comb(waiting - 1, inCar + 1)
#     return waiting * comb(waiting - 1, inCar + 1) + inCar * comb(waiting, inCar - 1)
#
#
# def comb2(waiting, inCar):
#     if waiting == 0:
#         return math.factorial(inCar) if inCar > 1 else 1
#     if inCar <= 1:
#         return waiting * comb2(waiting - 1, inCar + 1)
#     return waiting * comb2(waiting - 1, inCar + 1) + inCar * comb2(waiting, inCar - 1)


def comb3(waiting, inCar):
    if waiting == 0:
        return math.factorial(inCar) if inCar > 1 else 1

    result = waiting * comb3(waiting - 1, inCar + 1)
    if inCar > 1:
        result += inCar * comb3(waiting, inCar - 1)

    return result


nClients = 4
# z = nClients * (nClients - 1) * comb3(nClients - 2, 2)
# z = nClients*comb3(nClients-1, 1)
z = comb3(nClients, 0)

print('sum', z)


