def getGroup(index):
    group = []
    for i in range(0, N):
        if(index & 1 == 1):
            group.append(i + 1)
        index = index >> 1
    return group

def desire(group):
    return len(getGroup(group))

def maxValue():
    global groups, values
    return groups.pop()

def hasThreeOrLessBits(number):
    nob = 0
    while(number != 0):
        if(number & 1 == 1):
            nob = nob + 1
        number = number >> 1
    return (nob < 4)
        
def kickGroups(group):
    global groups
    groups = [g for g in groups if (g & group) == 0]

def init(threshold):
    global groups, values
    for i in range(0, gN):
        group = i + 1
        if hasThreeOrLessBits(group):
            value = desire(group)
            if(value >= threshold):
                groups.append(group)
                values.append(value)
    groups = [x for (y, x) in sorted(zip(values, groups))]
    values = sorted(values)


import numpy as np    
N = 10;
gN = pow(2, N) - 1
groups = []
values = []
init(0)
output = []

while(len(groups) != 0):
    max = maxValue()
    output.append(getGroup(max))
    kickGroups(max)

for i in range(1, N + 1):
    isHere = False
    for g in output:
        if i in g:
            isHere = True
    if(not isHere):        
        output.append([i])
        
print(output)