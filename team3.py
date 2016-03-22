
from __future__ import division
import copy
import time
import math
import random

class State:
    """
    class to define the characteristics of a state or node
    """
    def __init__(self, temp_board, temp_block, flag, action, depth, value, status):
        self.board = temp_board
        self.mainBlock = temp_block
        self.flag = flag
        self.action = action
        self.value = value
        self.child = []
        self.depth = depth
        self.status = status

class Player3:
    def __init__(self):
        pass

    def move(self, temp_board, temp_block, old_move, flag):
        global timestart, maxFlag, minFlag, nodeCount 
        timestart = time.time()
        maxFlag = flag
        minFlag = negateFlag(flag)
        nodeCount = 0
        if old_move == (-1,-1):
            return (4,4)
        state = State(temp_board, temp_block, flag, old_move, 0, -10000000, 'max')
        nodeCount +=1
        a = -10000000
        b = 10000000
        state.value = maxValue(state, a, b)
        for i in state.child:
            if i.value == state.value:
                return i.action


def maxValue(state, a, b):
    if checkCutoff(state):
        state.value = utility(state)
        return state.value

    state.child = successors(state)
    for i in state.child:
        state.value = max(state.value, minValue(i,a,b))

        if state.value >= b:
            return state.value

        a = max(a, state.value)
    
    return state.value

def minValue(state, a, b):
    if checkCutoff(state):
        state.value = utility(state)
        return state.value

    state.child = successors(state)
    for i in state.child:
        state.value = min(state.value, maxValue(i,a,b))

        if state.value <= a:
            return state.value

        b = min(b, state.value)

    return state.value

def checkCutoff(state):
   """
   checks the cutoff for the tree
   """
   if state.depth >= 5  or checkBoardFull(state.board,state.mainBlock):
       return True
   return False
 
def getValidBlocks(temp_board, temp_block, old_move):
    """
    function to determine which boards are valid to do a move in the bigger block. returns a list of all the valid boards
    """
    row, col = old_move[0], old_move[1]
    validOptions = [] #list to contain all the valid block positions
    #block_row
    curBlock = (row%3, col%3);
    #check centre
    if curBlock[0] == 1 and curBlock[1] == 1:
        validOptions.append(curBlock)
    #check the 2nd and 8th position
    elif curBlock[1] == 1:
        validOptions.append((curBlock[0], curBlock[1]-1));
        validOptions.append((curBlock[0], curBlock[1]+1));
    #check the 4th and 6th position
    elif curBlock[0] == 1:
        validOptions.append((curBlock[0]-1, curBlock[1]));
        validOptions.append((curBlock[0]+1, curBlock[1]));
    #check Corners
    else:
        if curBlock[0] + 1 == 1:
            validOptions.append((curBlock[0]+1, curBlock[1]));
        elif curBlock[0] -1 ==1 :
            validOptions.append((curBlock[0]-1, curBlock[1]));

        if curBlock[1] +1 == 1:
            validOptions.append((curBlock[0], curBlock[1]+1));
        elif curBlock[1] -1 == 1:
            validOptions.append((curBlock[0], curBlock[1]-1));


    #print validOptions, old_move, temp_block
    tempOptions = []
    for i in validOptions:
        if temp_block[i[0]*3 + i[1]] == '-' :
           tempOptions.append(i)
           #validOptions.remove(i)
    validOptions = tempOptions
    
    #validOptions
    if len(validOptions) != 0:
        return (validOptions, 0)
    else:
        #print "are kya batyein "
        validOptions = []
        for i in range(0, 3):
            for j in range(0,3):
                if temp_block[i*3 + j] == '-' :
                    validOptions.append((i,j))
        return (validOptions,1)
    

def checkBlockComplete(board, position):
    """
    returns the flag which is getting completed if any 
    """
    row, col = position[0]%3, position[1]%3
    char = "-"
    for i in range(0, 3):
        if board[row*3 + i][col*3] == board[row*3+i][col*3+1] == board[row*3+i][col*3+2] :
            if board[row*3+i][col*3] != '-' and board[row*3+i][col*3] != 'D':
                char= board[row*3+i][col*3]

        if board[row*3][col*3+i] == board[row*3 +1][col*3+i] == board[row*3+2][col*3+i]:
            if board[row*3][col*3+i] != '-' and board[row*3][col*3+i] != 'D':
                char = board[row*3][col*3+i]

    if board[row*3][col*3] == board[row*3+1][col*3+1] == board[row*3+2][col*3+2] :
        if board[row*3][col*3] != '-' and board[row*3][col*3]!='D':
            char = board[row*3][col*3]

    if board[row*3][col*3+2] == board[row*3+1][col*3+1] == board[row*3+2][col*3]:
        if board[row*3+1][col*3+1] != '-' and board[row*3+1][col*3+1]!='D':
            char = board[row*3+1][col*3+1]

#checking for the draw condition
    if char == '-' :
        for i in range(row*3, row*3+3):
            for j in range(col*3, col*3+3):
                if board[i][j] == '-':
                    return char
        char = 'D'
        

    return char

def getProbBoard(board, position, flag):
    '''
    given a board it gives the probability like utility of the flag to win the board
    '''
    row, col = position[0]%3, position[1]%3
    val = 0
    totalVal = 0
    temp_board = [ [ board[i][j] for j in range(col*3, col*3+3) ] for i in range(row*3, row*3+3) ] 
    for i in range(0,3):
        for j in range(0,3):
            if temp_board[i][j] == '-':
                temp_board[i][j] = flag
                if checkBlockComplete(temp_board, (0,0)) == flag:
                    return 1
                elif checkBlockCompletePartial(temp_board, (0,0), negateFlag(flag), 2):
                    val -= 0.5
                elif checkBlockCompletePartial(temp_board,(0,0),flag,2):
                    val+=0.5
                totalVal += 1
                temp_board[i][j] = '-'
    try:
        return val/totalVal
    except:
        return 0

def getActionProb(board, block, position, flag):
    row, col = position[0]%3, position[1]%3
    val =0
    temp_board = [ [board[i][j] for j in range(col*3, col*3+3)] for i in range(row*3, row*3+3)]
    for i in range(0, 3):
        for j in range(0, 3):
            if temp_board[i][j] == '-':
                temp_board[i][j] = flag
                if checkBlockComplete(temp_board, (0,0)) == flag:
                    return 1
                elif checkBlockCompletePartial(temp_board, (0,0), negateFlag(flag), 2):
                    tempValBlocks = getValidBlocks(temp_board, block, (i,j))[0]
                    if position in tempValBlocks:
                        temp_board[i][j] = '-'
                        continue
                    else:
                        return 1
                temp_board[i][j]='-'
    return 0

def alternateGetProb(board, position):
    row, col = position[0]%3, position[1]%3
    val = 0
    tot_val = 200
    temp_board = [ [board[i][j] for j in range(col*3, col*3+3)] for i in range(row*3, row*3+3)]
    res = checkBlockComplete(temp_board,(0,0))
    if res == maxFlag:
        return 1.0
    elif res == minFlag:
        return -1.0
    res2 = checkBlockCompletePartial(board,(0,0),maxFlag,2)
    res1 = checkBlockCompletePartial(board,(0,0),maxFlag,1)
    if res2>0:
        val+=res2*30
    else:
        val+= res1*5
    res2 = checkBlockCompletePartial(board,(0,0),minFlag,2)
    res1 = checkBlockCompletePartial(board,(0,0),minFlag,1)
    if res2>0:
        val-=30*res2
    else:
        val-=5*res1
    try:
        #print "prob",val/tot_val
        return val/tot_val
    except:
        return 0
                        
def manipulateMySum(tempSum):
    valMap = [0, 5, 30, 500]
    temp = abs(tempSum)
    floatPart = temp - int(temp)
    intPart = int(temp)
    ceilPart = int(math.ceil(tempSum))
    
    tempVal = floatPart*valMap[ceilPart] + (1.0-floatPart)*valMap[intPart]
    if tempSum < 0:
        tempVal *= -1

    return tempVal

def finalUtility(problist):
    cntMax=0
    cntMin=0
    sumMax=0
    sumMin=0
    for i in problist:
        if i>=0.5:
            cntMax+=1;
            sumMax+=i
        elif i<=-0.5:
            cntMin+=1
            sumMin+=i
    if cntMin == 0:
        return manipulateMySum(sumMax)
    elif cntMax == 0:
        return manipulateMySum(sumMin)
    else:
        return 0

def utility(state):
    global maxFlag
    temp_board = [ [state.mainBlock[j] for j in range(i*3, 3*(i+1))] for i in range(0, 3)]
    res = checkBlockComplete(temp_board,(0,0))
    if res == maxFlag:
        return 1000
    elif res == minFlag:
        return -1000
    mainUtil = 0
    probGrid = []
    validBlocks = getValidBlocks(state.board, state.mainBlock, state.action)[0]
    
    for i in range(0,3):
        tempList = []
        for j in range(0,3):
            if state.mainBlock[3*i+j] == maxFlag:
                tempList.append(1)
            elif state.mainBlock[3*i+j] == minFlag:
                tempList.append(-1)
            elif state.mainBlock[3*i+j] == 'D':
                tempList.append(0)
            else:
                tempProb = alternateGetProb(state.board, (i,j))
                tempList.append(tempProb)

        probGrid.append(tempList)

    #now checking what should be added in the main utility on the basis of the sum of rows of probGrid
    for i in range(0,3):
        mainUtil += finalUtility(probGrid[i])

    for i in range(0,3):
        tmplist = []
        for j in range(0,3):
            tmplist.append(probGrid[j][i])
        mainUtil += finalUtility(tmplist)

    tmplist = []
    for i in range(0,3):
        tmplist.append(probGrid[i][i])
    mainUtil += finalUtility(tmplist)

    tmplist = []
    for i in range(0,3):
        tmplist.append(probGrid[i][2-i])
    mainUtil += finalUtility(tmplist)


    return mainUtil


   
# def filter(childs):
#     ret = []
#     childUtilities = []
#     l = len(childs)
#     if l==1:
#         return childs
#     for i in range(0,l):
#         childUtilities.append((utility(childs[i]),i))
#     childUtilities.sort()
#     childUtilities.reverse()
#     for i in range(0,int(l/2)):
#         k = childUtilities[i][1]
#         ret.append(childs[k])
#     return ret
def checkBlockCompletePartial(board, position, flag, req):
    """
    returns the count of the two complete position in any row, col or diag
    """
    count =0
    row , col = position[0]%3, position[1]%3
    
    for i in range(0,3):
        tempCount = countInRow(board, flag, i, row, col)
        if tempCount == req:
            count += 1

    for j in range(0,3):
        tempCount = countInCol(board, flag, j, row, col)
        if tempCount == req:
            count += 1
    
    tempCount = countInOnDiag(board,flag, row, col)
    if tempCount == req:
        count += 1

    tempCount = countInOffDiag(board, flag, row, col)
    if tempCount == req:
        count += 1

    return count 


def countInRow(board, flag, i, row, col):
    tempCount =0
    for j in range(0, 3):
        if board[row*3 + i][col*3 + j] == flag :
            tempCount += 1
        elif board[row*3+i][col*3+j] == negateFlag(flag):
            tempCount -= 1
    return tempCount

def countInCol(board, flag, j, row, col):   
    tempCount = 0
    for i in range(0,3):
        if board[row*3 + i][col*3+j] == flag:
            tempCount += 1
        elif board[row*3 +i][col*3+j] == negateFlag(flag):
            tempCount -= 1

    return tempCount

def countInOnDiag(board, flag, row, col): 
    tempCount = 0
    for i in range(0,3):
        if board[row*3+i][col*3+i] == flag:
            tempCount += 1
        elif board[row*3 +i][col*3+ i] == negateFlag(flag):
            tempCount -= 1

    return tempCount

def countInOffDiag(board, flag, row, col):
    tempCount = 0
    for i in range(0,3):
        if board[row*3+2-i][col*3+i] == flag :
            tempCount += 1
        elif board[row*3+2-i][col*3+i] == negateFlag(flag):
            tempCount -= 1
    
    return tempCount
            
def negateFlag(flag):
    if flag == 'x':
        return 'o'
    else :
        return 'x'


def checkBlockFill( board, block , position):
    row, col = position[0]%3, position[1]%3
    char = checkBlockComplete(board, position)
    returnBlock = copy.deepcopy(block)
    returnBlock[row*3 + col] = char

    return returnBlock


def successors(state):
    """
    returns the list of all the possible childs of a given state
    """
    global nodeCount
    if len(state.child) != 0:
        return state.child

    #list of all the valid boards
    validBoards = getValidBlocks(state.board, state.mainBlock, state.action)[0]
    #result list to be returned
    childs = []

    for k in validBoards:
        row, col = k[0], k[1]
        for i in range(row*3, row*3+3):
            for j in range(col*3, col*3+3):
                if state.board[i][j] == '-':
                    tempCopyBoard = copy.deepcopy(state.board)
                    tempCopyBoard[i][j] = state.flag
                    tempCopyBlock = checkBlockFill(tempCopyBoard, state.mainBlock, (row,col))
                    
                    if state.status == 'max':
                        temp = State(tempCopyBoard, tempCopyBlock, negateFlag(state.flag), (i,j), state.depth + 1, 10000000, 'min')
                    elif state.status == 'min':
                        temp = State(tempCopyBoard, tempCopyBlock, negateFlag(state.flag), (i,j), state.depth + 1, -10000000, 'max')

                    childs.append(temp)
                    nodeCount += 1
    return childs

def checkBoardFull(board,block):
    allowed = ['x','o']
    temp_board = [ [block[j] for j in range(i*3, 3*(i+1))] for i in range(0, 3)]
    if checkBlockComplete(temp_board,(0,0)) in allowed:
        return True
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] =='-':
                return False
    else:
        return True

