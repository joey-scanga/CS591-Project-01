import pdb
with open("bigMaze.lay", "r") as f:
    lines = f.readlines()

#find p
for y in range(len(lines)):
    if 'P' not in lines[y]:
        continue
    for x in range(len(lines[y])):
        if 'P' not in lines[y][x]:
            continue
        else:
            index = (y, x)
            break
    break
    
y = index[0]
x = index[1]

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

def checkUp(y, x):
    if checkGoal(y - 1, x):
        return 0 #Goal found
    elif checkEmpty(y - 1, x):
        return 1 #Empty space found

def checkRight(y, x):
    if checkGoal(y, x + 1):
        return 0 #Goal found
    elif checkEmpty(y, x + 1):
        return 1 #Empty space found

def checkDown(y, x):
    if checkGoal(y + 1, x):
        return 0 #Goal found
    elif checkEmpty(y + 1, x):
        return 1 #Empty space found

def leaveTrail(y, x):
    lines[y] = lines[y][:x] + '!' + lines[y][x+1:]

def printMap():
    for line in lines:
        print(line[:-1])

def depthFirstTraversal(y, x):
    stack = [[y, x, []]]
    while stack:
        index = stack.pop()
        if (index[0], index[1]) != (y, x):
            leaveTrail(index[0], index[1])
        if checkSurroundingSquaresForGoalSquare(index[0], index[1]):
            print(f"Goal square at {checkSurroundingSquaresForGoalSquare(index[0], index[1])}")
            printMap()
            return
        if "left" not in index[2] and checkLeft(index[0], index[1]) == 1:
            index[2].append("left")
            stack.append(index)
            stack.append([index[0], index[1]-1, ["right"]])
            continue
        if "up" not in index[2] and checkUp(index[0], index[1]) == 1:
            index[2].append("up")
            stack.append(index)
            stack.append([index[0]-1, index[1], ["down"]])
            continue
        if "right" not in index[2] and checkRight(index[0], index[1]) == 1:
            index[2].append("right")
            stack.append(index)
            stack.append([index[0], index[1]+1, ["left"]])
            continue
        if "down" not in index[2] and checkDown(index[0], index[1]) == 1:
            index[2].append("down")
            stack.append(index)
            stack.append([index[0]+1, index[1], ["up"]])
            continue
    printMap()
    print("Goal not reachable")
    return

def breadthFirstTraversal(y, x):
    queue = [[y, x, []]]
    while queue:
        index = queue[0]
        if (index[0], index[1]) != (y, x):
            leaveTrail(index[0], index[1])
        if checkSurroundingSquaresForGoalSquare(index[0], index[1]):
            print(f"Goal square at {checkSurroundingSquaresForGoalSquare(index[0], index[1])}")
            printMap()
            return
        if "left" not in index[2] and checkLeft(index[0], index[1]) == 1:
            queue.append([index[0], index[1]-1, ["right"]])
        if "up" not in index[2] and checkUp(index[0], index[1]) == 1:
            queue.append([index[0]-1, index[1], ["down"]])
        if "right" not in index[2] and checkRight(index[0], index[1]) == 1:
            queue.append([index[0], index[1]+1, ["left"]])
        if "down" not in index[2] and checkDown(index[0], index[1]) == 1:
            queue.append([index[0]+1, index[1], ["up"]])
        queue.pop(0)
    printMap()
    print("Goal not reachable")
    return
        
        

breadthFirstTraversal(y, x)



