import pdb, pathlib, sys, time

p = pathlib.Path('.')
pathzip = zip(range(1, len(list(p.glob('*.lay')))+1), list(p.glob('*.lay')))
pathdict = dict(pathzip)
print("Enter a path number: (1, 2, 3 ...)")
for i in range(len(list(p.glob('*.lay')))):
    print(f"{i+1}: {list(p.glob('*.lay'))[i]}")

pathnum = int(input())

if pathnum not in range(1, len(list(p.glob('*.lay')))+1):
    print("Invalid path number")
    sys.exit(-1)

with pathdict[pathnum].open() as f:
    lines = f.readlines()

#find p
for y in range(len(lines)):
    if 'P' not in lines[y]:
        continue
    for x in range(len(lines[y])):
        if 'P' not in lines[y][x]:
            continue
        else:
            startingIndex = (y, x)
            break
    break
    
y = startingIndex[0]
x = startingIndex[1]

def checkGoal(y, x):
    if '.' in lines[y][x]:
        return True
    return False

def checkSurroundingSquaresForGoalSquare(y, x):
    if checkLeft(y, x) == 0:
        return(y, x-1)
    if checkUp(y, x) == 0:
        return(y-1, x)
    if checkRight(y, x) == 0:
        return(y, x+1)
    if checkDown(y, x) == 0:
        return(y+1, x)
    else:
        return False
    

def checkEmpty(y, x):
    if ' ' in lines[y][x]:
        return True
    return False

def checkLeft(y, x):
    if checkGoal(y, x - 1):
        return 0 #Goal found
    elif checkEmpty(y, x - 1):
        return 1 #Empty space found
    else:
        return -1

def checkUp(y, x):
    if checkGoal(y - 1, x):
        return 0 #Goal found
    elif checkEmpty(y - 1, x):
        return 1 #Empty space found
    else:
        return -1

def checkRight(y, x):
    if checkGoal(y, x + 1):
        return 0 #Goal found
    elif checkEmpty(y, x + 1):
        return 1 #Empty space found
    else:
        return -1

def checkDown(y, x):
    if checkGoal(y + 1, x):
        return 0 #Goal found
    elif checkEmpty(y + 1, x):
        return 1 #Empty space found
    else:
        return -1

def leaveTrail(y, x):
    lines[y] = lines[y][:x] + '!' + lines[y][x+1:]

def drawStart(y, x):
    lines[y] = lines[y][:x] + 'P' + lines[y][x+1:]
    

def printMap():
    for line in lines:
        print(line[:-1])

def clearMap(startSquare):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("!", " ")
    drawStart(startSquare[0], startSquare[1])
    

def checkTreeDepth(maxtreedepth, stack):
    if len(stack) > maxtreedepth:
        return len(stack)
    return maxtreedepth


def depthFirstTraversal(y, x):
    stack = [[y, x, []]]
    nodesExpanded = 0
    maxTreeDepth = 0
    pathSolutionCost = 0
    maxFringeSize = 0
    while stack:
        index = stack.pop()
        if checkSurroundingSquaresForGoalSquare(index[0], index[1]):
            leaveTrail(index[0], index[1])
            nodesExpanded += 1
            maxTreeDepth = checkTreeDepth(maxTreeDepth, stack)
            for square in stack:
                if (square[0], square[1]) != (y, x):
                    pathSolutionCost += 1
                    leaveTrail(square[0], square[1])
            print(f"Goal square at {checkSurroundingSquaresForGoalSquare(index[0], index[1])}")
            print(f"Path solution cost: {pathSolutionCost}")
            print(f"Nodes expanded: {nodesExpanded}")
            print(f"Max tree depth: {maxTreeDepth}")
            print(f"Max size of fringe: {maxFringeSize}")
            printMap()
            return
        if "left" not in index[2] and checkLeft(index[0], index[1]) == 1:
            nodesExpanded += 1
            index[2].append("left")
            stack.append(index)
            stack.append([index[0], index[1]-1, ["right"]])
            maxTreeDepth = checkTreeDepth(maxTreeDepth, stack)
            continue
        if "up" not in index[2] and checkUp(index[0], index[1]) == 1:
            nodesExpanded += 1
            index[2].append("up")
            stack.append(index)
            stack.append([index[0]-1, index[1], ["down"]])
            maxTreeDepth = checkTreeDepth(maxTreeDepth, stack)
            continue
        if "right" not in index[2] and checkRight(index[0], index[1]) == 1:
            nodesExpanded += 1
            index[2].append("right")
            stack.append(index)
            stack.append([index[0], index[1]+1, ["left"]])
            maxTreeDepth = checkTreeDepth(maxTreeDepth, stack)
            continue
        if "down" not in index[2] and checkDown(index[0], index[1]) == 1:
            nodesExpanded += 1
            index[2].append("down")
            stack.append(index)
            stack.append([index[0]+1, index[1], ["up"]])
            maxTreeDepth = checkTreeDepth(maxTreeDepth, stack)
            continue
        if maxFringeSize < len(stack):
            maxFringeSize = len(stack)
    printMap()
    print("Goal not reachable")
    return

def getBreadthFirstTraversalTrail(index):
    trail = [index]
    while index[3] != "root":
        trail.append(index[3])
        index = index[3]
    return trail

def breadthFirstTraversal(y, x):
    nodesExpanded = 0
    maxFringeSize = 0
    pathSolutionCost = 0
    queue = [[y, x, [], "root"]]
    while queue:
        index = queue[0]
        if checkSurroundingSquaresForGoalSquare(index[0], index[1]):
            clearMap((y, x))
            leaveTrail(index[0], index[1])
            nodesExpanded += 1
            for square in getBreadthFirstTraversalTrail(index):
                if (square[0], square[1]) != (y, x):
                    leaveTrail(square[0], square[1])
                    pathSolutionCost += 1
            print(f"Goal square at {checkSurroundingSquaresForGoalSquare(index[0], index[1])}")
            print(f"Path solution cost: {pathSolutionCost}")
            print(f"Nodes expanded: {nodesExpanded}")
            print(f"Max depth: {len(getBreadthFirstTraversalTrail(index))}")
            print(f"Max size of fringe: {maxFringeSize}")
            printMap()
            return
        if checkLeft(index[0], index[1]) == 1:
            nodesExpanded += 1
            queue.append([index[0], index[1]-1, ["right"], index])
            leaveTrail(index[0], index[1]-1)
        if checkUp(index[0], index[1]) == 1:
            nodesExpanded += 1
            queue.append([index[0]-1, index[1], ["down"], index])
            leaveTrail(index[0]-1, index[1])
        if checkRight(index[0], index[1]) == 1:
            nodesExpanded += 1
            queue.append([index[0], index[1]+1, ["left"], index])
            leaveTrail(index[0], index[1]+1)
        if checkDown(index[0], index[1]) == 1:
            nodesExpanded += 1
            queue.append([index[0]+1, index[1], ["up"], index])
            leaveTrail(index[0]+1, index[1])
        if len(queue) > maxFringeSize: 
            maxFringeSize = len(queue)
        queue.pop(0)
        leaveTrail(index[0], index[1])
    printMap()
    print("Goal not reachable")
    return
        
breadthFirstTraversal(y, x)  



