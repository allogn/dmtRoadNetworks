from itertools import permutations

trips = ['A', 'B', 'C', 'D']
points = trips + trips
perm = permutations(points)
pset = set(perm)

for permut in pset.copy():
    dic = dict.fromkeys(trips, 0)

    for index, point in enumerate(permut[:-1]):
        in_car = 0
        empty_car = 0
        for val in dic.values():
            if val == 1:
                in_car = 1
                break

        if dic[point] == 0:
            dic[point] += 1
        else:
            dic[point] = 0

        if sum(dic.values()) == 0:
            empty_car = 1

        if index > 0 and empty_car > 0:
            print('empty car')
            print('permutation removed on step ', index)
            print(dic.values())
            pset.remove(permut)
            break

        if point == permut[index+1]:
            print('check it')
            if in_car == 0:
                print('permutation removed on step ', index)
                print(dic.values())
                pset.remove(permut)
                break

    print(permut)
    print()

print(len(pset))
