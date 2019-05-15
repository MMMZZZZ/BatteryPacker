import sys



# All available cells. Size must equal to par x ser
cellCap = [1890, 1923, 1956, 1976, 1982, 2004, 2034, 2054, 2065, 2076, 2076, 2123, 2134, 2156, 2178, 2187]

par = 4 # Cells in parallel
ser = 4 # Cells in series



# recursive function to be called by allCombisLst / allCombisInt
def allCombRec(lst, start, end, cnt):
    res = []
    if cnt == 1:
        for item in lst[start:end]:
            res.append([item])
    else:
        for index, item in enumerate(lst[start:end]):
            restPoss = allCombRec(lst, start + index + 1, end + 1, cnt - 1)
            for i in range(len(restPoss)):
                restPoss[i].insert(0, item)
            res += restPoss
    return res

# Returns a list with all possible combinations of length cnt of items in the list lst
def allCombLst(lst, cnt):
    return allCombRec(lst, 0, len(lst) - cnt + 1, cnt)

# Returns a list with all possible combinations of length cnt of integers from start to end (excluded)
def allCombInt(start, end, cnt):
    return allCombRec([x for x in range(start, end + 1)], start, end - start - cnt + 1, cnt)



if len(cellCap) != par * ser:
    print("Cell count mismatch")
    sys.exit()

# Ideal capacity of each group of parallel cells
idealGroupCap = sum(cellCap) / ser

# Get all possible strings
allGroups = allCombInt(0, par * ser, par)

# Add difference between string capacity and ideal capacity to each group
for index, string in enumerate(allGroups):
    cap = 0
    for i in string:
        cap += cellCap[i]
    allGroups[index] = [abs(cap - idealGroupCap), string]

# Sort by cap difference
allGroups.sort(key = lambda x: x[0])

# Kick the worse one of incompatible groups
usedCells = []
groupCount = 0
while groupCount < ser:
    currentGroup = allGroups[groupCount]
    compatible = True
    for cell in currentGroup[1]:
        if cell in usedCells:
            compatible = False
            break
    if compatible:
        usedCells += currentGroup[1]
        groupCount += 1
        print(currentGroup)
    else:
        allGroups.pop(groupCount)