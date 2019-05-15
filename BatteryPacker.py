import sys
import time
import random



# All available cells. Size must equal to par x ser
#cellCap = [1890, 1923, 1956, 1976, 1982, 2004, 2034, 2054, 2065, 2076, 2076, 2123, 2134, 2156, 2178, 2187]

#par = 4 # Cells in parallel
#ser = 4 # Cells in series



# recursive function to be called by allCombLst / allCombInt
def allCombRec(lst, start, end, cnt):
    res = []
    if cnt == 1:
        for item in lst[start:end]:
            res.append([item])
    else:
        for index, item in enumerate(lst[start:end]):
            l = len(res)
            res += allCombRec(lst, start + index + 1, end + 1, cnt - 1)
            for i in range(l, len(res)):
                res[i].append(item)
    return res

# Returns a list with all possible combinations of length cnt of items in the list lst
def allCombLst(lst, cnt):
    return allCombRec(lst, 0, len(lst) - cnt + 1, cnt)

# Returns a list with all possible combinations of length cnt of integers from start to end (excluded)
def allCombInt(start, end, cnt):
    return allCombRec([x for x in range(start, end + 1)], start, end - start - cnt + 1, cnt)

# Get cell pack
def cellPack(cellCapacities, parallel, serial):
    if len(cellCapacities) < parallel * serial:
        print("Cell count mismatch")
        sys.exit()

    # Ideal capacity of each group of parallel cells
    idealGroupCap = sum(cellCapacities) // serial
    print("Ideal capacity:\t" + str(idealGroupCap) + "mA")

    # Get all possible strings
    allGroups = allCombInt(0, parallel * serial, parallel)

    # Add difference between string capacity and ideal capacity to each group
    for index, string in enumerate(allGroups):
        cap = 0
        for i in string:
            cap += cellCapacities[i]
        allGroups[index] = [abs(cap - idealGroupCap), string]

    # Sort by cap difference
    allGroups.sort(key = lambda x: x[0])

    # Kick the worse one of incompatible groups
    usedCells = []
    groupCount = 0
    skipped = 0
    while groupCount < serial:
        currentGroup = allGroups[groupCount]
        compatible = True
        for cell in currentGroup[1]:
            if cell in usedCells:
                compatible = False
                break
        if compatible:
            usedCells += currentGroup[1]
            groupCount += 1
        else:
            skipped += 1
            allGroups.pop(groupCount)

    print("Skipped groups:\t" + str(skipped))
    # the lowest x groups are compatible and more or less optimal
    return allGroups[:serial]


# Benchmark from 2S2P to 7S7P
serPar = 2
while serPar < 6:
    serPar += 1
    cellCaps = [random.randint(1800,2200) for i in range(serPar * serPar)]
    t = 0
    repeat = 1
    for i in range(repeat):
        start = time.process_time_ns()
        l = cellPack(cellCaps, serPar, serPar)
        end = time.process_time_ns()
        t += end - start
    print("Time: " + str(t // repeat // 1000000) + "ms")
    print("\t\t\tDiff to ideal\tCells")
    for i,g in enumerate(l):
        print("Group " + str(i+1) + ":\t" + str(g[0]), end = "\t\t\t\t")
        for cell in g[1]:
            print(cellCaps[cell], end = "\t")
        print("")
    print("")
else:
    sys.exit()
