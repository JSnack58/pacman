"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from argparse import Action
import heapq
from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue
# from ../../pacai.util.priorityQueue import PriorityQueue
# class Stack(object):
#     """
#     A container with a last-in-first-out (LIFO) queuing policy.
#     """

#     def __init__(self):
#         self.list = []

#     def push(self, item):
#         """
#         Push an item onto the stack.
#         """

#         self.list.append(item)

#     def pop(self):
#         """
#         Pop the most recently pushed item from the stack.
#         """

#         return self.list.pop()

#     def isEmpty(self):
#         """
#         Returns True if the stack is empty.
#         """

#         return len(self.list) == 0

#     def peek(self):
#         top = self.list.pop()
#         self.list.append(top)
#         return top

#     def __len__(self):
#         return len(self.list)
    
#     def __repr__(self):
#         print("[ ",end = '')
#         for i in self.list:
#             print(i," ",end = '')
#         print("]")

#     def printSuccessors(self):
#         print("[ ",end = '')
#         for i in self.list:
#             print(i," ",end = '')
#         print("]")

# class Queue(object):
#     def __init__(self):
#         self.list = []

#     def enqueue(self, item):
#         """
#         Push an item onto the stack.
#         """

#         self.list.append(item)

#     def dequeue(self):
#         """
#         Pop the most recently pushed item from the stack.
#         """

#         return self.list.pop(0)

#     def isEmpty(self):
#         """
#         Returns True if the stack is empty.
#         """

#         return len(self.list) == 0

#     def peek(self):
#         return self.list[0]

#     def __len__(self):
#         return len(self.list)

#create class to track information on the spots
class Node2(object):
    def __init__(self, loc, direction, cost):
        #loc is a string that holds action and later previous actions
        self.cornerList = None
        if isinstance(loc[0],int):
            self.position = loc
        elif isinstance(loc[0],tuple):
            self.position = loc[0]
            self.cornerList = loc[1]
            # print("self.position",self.position)
            # print("self.cornerList",self.cornerList)
        self.pathToNode = direction
        self.wasVisited = False
        self.actionCost = cost
        self.costOfPath = 0
    
    def location(self):
        return self.position

    def path(self):
        return self.pathToNode

    def pathCost(self):
        return self.costOfPath

    def updateCornerList(self,index,value):
        self.cornerList[index] = value
    
    def getCornerList(self):
        return self.cornerList

    def isCornerGoal(self):
        print("cornerList",self.cornerList)
        if self.cornerList != None:
            for i in self.cornerList:
                if i == 0:
                    return False
            return True
        else:
            return None

    def updateCost(self, cost):
        self.costOfPath = self.actionCost + cost

    def visited(self):
        return self.wasVisited
    
    def cost(self):
        return self.actionCost

    def updatePath(self,actions):
        #actions is a string of previous actions
        #actions is appended to show the paths taken to reach Node
        #print(self.pathToNode,' + ',actions)
        self.pathToNode = actions + ' ' + self.pathToNode
    
    def visit(self):
        self.wasVisited = True
    
    def __eq__(self,other):
        return ((self.actionCost) == (other.actionCost))

    def __ne__(self,other):
        return ((self.actionCost) != (other.actionCost))

    def __lt__(self,other):
        return ((self.actionCost)< (other.actionCost))

    def __gt__(self,other):
        return ((self.actionCost) > (other.actionCost))

    def __le__(self,other):
        return ((self.actionCost) < (other.actionCost)) or ((self.actionCost) == (other.actionCost))
    
    def __ge__(self,other):
        return ((self.actionCost) > (other.actionCost)) or ((self.actionCost) == (other.actionCost))
    
class Node(object):
    def __init__(self, state):
        #loc is a string that holds action and later previous actions
        loc = state[0]
        direction = state[1]
        cost = state[2]
        
        self.cornerList = None
        if isinstance(loc[0],int):
            self.position = loc
        elif isinstance(loc[0],tuple):
            self.position = loc[0]
            self.cornerList = loc[1]
            # print("self.position",self.position)
            # print("self.cornerList",self.cornerList)
        self.pathToNode = direction
        self.wasVisited = False
        self.actionCost = cost
        self.costOfPath = 0
    
    def location(self):
        return self.position

    def path(self):
        return self.pathToNode

    def pathCost(self):
        return self.costOfPath

    def updateCornerList(self,index,value):
        self.cornerList[index] = value
    
    def getCornerList(self):
        return self.cornerList

    def makeState(self):
        if self.cornerList == None:
            return (self.position,self.pathToNode,self.actionCost)
        else:
            return ((self.position,self.cornerList),self.pathToNode,self.actionCost)
    
    def isCornerGoal(self):
        print("cornerList",self.cornerList)
        if self.cornerList != None:
            for i in self.cornerList:
                if i == 0:
                    return False
            return True
        else:
            return None

    def updateCost(self, cost):
        self.costOfPath = self.actionCost + cost

    def visited(self):
        return self.wasVisited
    
    def cost(self):
        return self.actionCost

    def updatePath(self,actions):
        #actions is a string of previous actions
        #actions is appended to show the paths taken to reach Node
        #print(self.pathToNode,' + ',actions)
        self.pathToNode = actions + ' ' + self.pathToNode
        print(self.pathToNode)
        print()
        print()
    
    def visit(self):
        self.wasVisited = True
    
    def __eq__(self,other):
        return ((self.actionCost) == (other.actionCost))

    def __ne__(self,other):
        return ((self.actionCost) != (other.actionCost))

    def __lt__(self,other):
        return ((self.actionCost)< (other.actionCost))

    def __gt__(self,other):
        return ((self.actionCost) > (other.actionCost))

    def __le__(self,other):
        return ((self.actionCost) < (other.actionCost)) or ((self.actionCost) == (other.actionCost))
    
    def __ge__(self,other):
        return ((self.actionCost) > (other.actionCost)) or ((self.actionCost) == (other.actionCost))
    
def visit(loc, stack, discovered, problem):
    successors = list(reversed(problem.successorStates(loc[0])))
    #print("discovered: ", discovered)
    visitedNode = discovered[loc[0]]

    for  successor in successors:
       stack.push(successor)
       if successor[0] not in discovered:
           #create Node from successor: stateNode
           #append the visitedNode's path
           #log stateNode as value for successor's location within 'visited'
        #    print(successor)
           stateNode = Node(successor[0],successor[1],successor[2])
           stateNode.updatePath(visitedNode.path())
           discovered[successor[0]] = stateNode

    #set visitedNode visited variable to True
    visitedNode.visit()

def startDFS(loc, stack, discovered, problem):
    #find the successors of the location
    successors = list(reversed(problem.successorStates(loc)))
    #create node from start pathToNode is empty string
    startNode = Node("",0)
    startNode.visit()

    #print("loc: ",loc,": ",successors)
    for  successor in successors:
        #push sucessor to stack
        stack.push(successor)
        #if successor isn't visited
        if successor[0] not in discovered:
            #create node from sucessor
            #log node as value for successor's location within discovered
            stateNode = Node(successor[0],successor[1],successor[2])
            discovered[successor[0]] = stateNode

    discovered[loc] = startNode 

def depthFirstSearch(problem):
    stack = Stack()
    discovered = {}
    start = problem.startingState()
    startDFS(start, stack, discovered, problem)
    while not stack.isEmpty():
       target = stack.pop()
       targetLoc = target[0]

       if not discovered[targetLoc].visited():
        #    print("target: ",target)
           #visit(targetLoc,stack,visited,problem)
           visit(target,stack,discovered,problem)
           #visited[targetLoc] = True

       if problem.isGoal(targetLoc):
            visit(target,stack,discovered,problem)
            print("direction: ",discovered[targetLoc].path().split(' '))
            directions = discovered[targetLoc].path().split(' ')
            return directions
    print("Found nothing")
    return ["West"]

def getCoordinates(loc):
    coordinates = loc #((3,5),[0,0,0,0])
    # print("coordinate: ",coordinates,"suc: ",successor)
    if type(coordinates[0]) != 'tuple':#((3,5))
        coordinates = coordinates[0]#3
    return coordinates

def startBFS(loc, queue, discovered, problem):
    #find the successors of the location
    
    #create node from start pathToNode is empty string
    startNode = Node((loc,"",0))
    # successors = list(reversed(problem.successorStates(startNode.location())))
    successors = list(reversed(problem.successorStates((loc,"",0))))
   
    startNode.visit()

    for  successor in successors:
        #push sucessor to stack
        queue.enqueue(successor)
        # queue.push(successor)
        #if successor isn't visited
        coordinates = getCoordinates(successor[0])

        if coordinates not in discovered:
            #create node from sucessor
            #log node as value for successor's location within discovered
            # print("successor: ",successor[0],successor[1],successor[2])
            stateNode = Node(successor)
            discovered[coordinates] = stateNode

    discovered[startNode.location()] = startNode 

def visitBFS(targetState, queue, discovered, problem):
    temp = Node(targetState)
    visitedNode = discovered[temp.location()]
    del(temp)
    print("targetState: ",targetState)
    # print("location: ",visitedNode.location())
    # successors = list(reversed(problem.successorStates(visitedNode.location())))
    successors = list(reversed(problem.successorStates(targetState)))
    for  successor in successors:
       queue.enqueue(successor)
    #    queue.push(successor)
       coordinates = getCoordinates(successor[0])
       
       if coordinates not in discovered:
           #create Node from successor: stateNode
           #append the visitedNode's path
           #log stateNode as value for successor's location within 'visited'
           #print(successor)
           stateNode = Node(successor)
           stateNode.updatePath(visitedNode.path())
        #    discovered[successor[0]] = stateNode
           discovered[coordinates] = stateNode
           

    #set visitedNode visited variable to True
    # cornerGoal = visitedNode.isCornerGoal()
    # if cornerGoal == True or cornerGoal == None:
    #     print("cornerGoal: ",cornerGoal)
    visitedNode.visit()

def depthFirstSearch(problem):
    queue = Stack()
    visitedList = []
    startState = problem.startingState()
    
    queue.push((startState,[],0))
    while not queue.isEmpty():
        target = queue.pop()#state path cost
        # if problem.isGoal(target[0]):
        #     print("return: ",target[1])
        #     return target[1]
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        successors = problem.successorStates(target[0])
        for successor in successors:
            
            queue.push((successor[0],
            target[1] + [successor[1]],
            0))
        if problem.isGoal(target[0]):
            print("return: ",target[1])
            return target[1]
    return None
def breadthFirstSearch(problem):
    queue = Queue()
    visitedList = []
    startState = problem.startingState()
    
    queue.push((startState,[],0))
    while not queue.isEmpty():
        target = queue.pop()#state path cost
        # if problem.isGoal(target[0]):
        #     print("return: ",target[1])
        #     return target[1]
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        successors = problem.successorStates(target[0])
        for successor in successors:
            
            queue.push((successor[0],
            target[1] + [successor[1]],
            0))
        if problem.isGoal(target[0]):
            print("return: ",target[1])
            return target[1]
    return None
def visitUCS(problem,state):
    
    location = state[0]
    corners = None
    if isinstance(location[0],tuple):
        corners = gameState[1]
        location = gameState[0]
    action = state[1]
    print(action)
    cost = state[2]
    for  successor in problem.successorStates(location):
        successorState = (successor[0],
            action + [successor[1]],
            successor[2]+cost)
        yield  successorState
    # for  successor in problem.successorStates(location):
    #     stateNode = Node((successor[0],successor[1],successor[2]))
    #     stateNode.updatePath(visitedNode.path())
    #     stateNode.updateCost(visitedNode.pathCost())
    
    #     # stateNode.actionCost = visitedNode.pathCost() + successor[2]
    #     yield stateNode
        # children.append(stateNode)
        # queue.push(stateNode,1)
        # discovered[successor[0]] = stateNode

    #set visitedNode visited variable to True
    # visitedNode.visit()
    # return children
def uniformCostSearch(problem):
    queue = PriorityQueue()
    visitedList = []
    startState = problem.startingState()
    
    queue.push((startState,[],0),0)
    while not queue.isEmpty():
        target = queue.pop()#state path cost
        # if problem.isGoal(target[0]):
        #     print("return: ",target[1])
        #     return target[1]
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        # successors = problem.successorStates(target[0])
        print("target: ",target)
        # for successor in successors:
        for successor in visitUCS(problem,target):
            print("successor: ",successor)
            # queue.push((successor[0],
            # target[1] + [successor[1]],
            # 0),1)
            queue.push(successor,successor[2])
        if problem.isGoal(target[0]):
            print("return: ",target[1])
            return target[1]
    return None

def aStarSearch(problem, heuristic):
    queue = PriorityQueue()
    visitedList = []
    startState = problem.startingState()
    distance = heuristic(problem.startingState(),problem)
    queue.push((startState,[],0),1+distance)
    while not queue.isEmpty():
        target = queue.pop()#state path cost
        # if problem.isGoal(target[0]):
        #     print("return: ",target[1])
        #     return target[1]
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        for successor in visitUCS(problem,target):
            distance = heuristic(problem.startingState(),problem)
            # queue.push((successor[0],
            # target[1] + [successor[1]],
            # 0),distance)
            queue.push(successor,successor[2] + distance)
        if problem.isGoal(target[0]):
            print("return: ",target[1])
            return target[1]
    return None


def breadthFirstSearch2(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # *** Your Code Here ***
    queue = Queue()
    discovered = {}
    visited = []
    start = problem.startingState()
    startBFS(start, queue, discovered, problem)
    while not queue.isEmpty():
       targetState = queue.dequeue()
    #    targetState = queue.pop()
       tempNode = Node(targetState)
       targetLoc = tempNode.location()
       del(tempNode)
    #    print("targetLoc", targetLoc)
       if not discovered[targetLoc].visited():
        #    print("target: ",target)
           #visit(targetLoc,stack,visited,problem)
           visitBFS(targetState,queue,discovered,problem)
           #visited[targetLoc] = True
       if problem.isGoal(targetLoc):
            # print(targetLoc,"is goal")
            visitBFS(targetState,queue,discovered,problem)
            directions = discovered[targetLoc].path().split(' ')
            print("direction: ",discovered[targetLoc].path().split(' '))
            return directions
    print("Found nothing")
    return ["West"]
# def breadthFirstSearch(problem):
#     """
#     Search the shallowest nodes in the search tree first. [p 81]
#     """
#     # *** Your Code Here ***
#     queue = Queue()
#     discovered = {}
#     start = problem.startingState()
#     startBFS(start, queue, discovered, problem)
#     while not queue.isEmpty():
#        targetState = queue.dequeue()
#     #    targetState = queue.pop()
#        tempNode = Node(targetState)
#        targetLoc = tempNode.location()
#        del(tempNode)
#     #    print("targetLoc", targetLoc)
#        if not discovered[targetLoc].visited():
#         #    print("target: ",target)
#            #visit(targetLoc,stack,visited,problem)
#            visitBFS(targetState,queue,discovered,problem)
#            #visited[targetLoc] = True
#        if problem.isGoal(targetLoc):
#             # print(targetLoc,"is goal")
#             visitBFS(targetState,queue,discovered,problem)
#             directions = discovered[targetLoc].path().split(' ')
#             print("direction: ",discovered[targetLoc].path().split(' '))
#             return directions
#     print("Found nothing")
#     return ["West"]


def startUSC(loc, queue, discovered, problem):
    #find the successors of the location
    # successors = list(reversed(problem.successorStates(loc)))
    #create node from start pathToNode is empty string
    startNode = Node((loc,"",0))
    queue.push(startNode,1)
    startNode.visit()

    # for  successor in successors:
    #     #push sucessor to stack
    #     # queue.push(successor,successor[2])
    #     #if successor isn't visited
    #     if successor[0] not in discovered:
    #         #create node from sucessor
    #         #log node as value for successor's location within discovered
    #         stateNode = Node(successor[0],successor[1],successor[2])
    #         queue.push(stateNode,successor[2])
    #         discovered[successor[0]] = stateNode

    discovered[loc] = startNode

def visitUCS2(node, queue, discovered, problem):
    # successors = list(reversed(problem.successorStates(loc)))
    #print("discovered: ", discovered)
    # visitedNode = discovered[loc]
    visitedNode = node
    # children = []
    for  successor in problem.successorStates(visitedNode.location()):
    #    queue.push(successor,1)
    #    if successor[0] not in discovered:
           #create Node from successor: stateNode
           #append the visitedNode's path
           #log stateNode as value for successor's location within 'visited'
        #    print(successor)
        stateNode = Node((successor[0],successor[1],successor[2]))
        stateNode.updatePath(visitedNode.path())
        stateNode.updateCost(visitedNode.pathCost())
    
        # stateNode.actionCost = visitedNode.pathCost() + successor[2]
        yield stateNode
        # children.append(stateNode)
        # queue.push(stateNode,1)
        # discovered[successor[0]] = stateNode

    #set visitedNode visited variable to True
    # visitedNode.visit()
    # return children

def uniformCostSearch2(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    queue = PriorityQueue()
    discovered = {}
    loc = problem.startingState()
    
    # startUSC(start,queue,discovered,problem)
    startNode = Node((loc,"",0))
    queue.push(startNode,1)
    startNode.visit()
    discovered[loc] = True
    # print(queue.pop().location)
    while queue.isEmpty() == False:
       target = queue.pop()
       targetLoc = target.location()
       if problem.isGoal(targetLoc):
            # visitUCS(targetLoc,queue,discovered,problem)
            # print("direction: ",discovered[targetLoc].path().split(' '))
            directions = target.path().split(' ')
            directions.pop(0)
            print(directions)
            return directions
    #    if not discovered[targetLoc].visited():
       print("target: ",target.pathCost())
       for child in visitUCS(target,queue,discovered,problem):
            print()
            childLoc = child.location()
            # if (childLoc not in discovered) or (child.pathCost() < discovered[childLoc].pathCost()):
            if not childLoc in discovered:
                print(childLoc, child.path())
                child.visit()
                discovered[childLoc] = True
                queue.push(child,1)
                
    return ['West']
           #visited[targetLoc] = True

    
  

def aStarSearch2(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    queue = PriorityQueue()
    discovered = {}
    loc = problem.startingState()
    
    # startUSC(start,queue,discovered,problem)
    startNode = Node(loc,"",0)
    distance = heuristic(problem.startingState(),problem)
    queue.push(startNode,1+distance)
    startNode.visit()
    discovered[loc] = True
    # print(queue.pop().location)
    while queue.isEmpty() == False:
       target = queue.pop()
       targetLoc = target.location()
       if problem.isGoal(targetLoc):
            # visitUCS(targetLoc,queue,discovered,problem)
            # print("direction: ",discovered[targetLoc].path().split(' '))
            directions = target.path().split(' ')
            directions.pop(0)
            return directions
    #    if not discovered[targetLoc].visited():
       for child in visitUCS(target,queue,discovered,problem):
            childLoc = child.location()
            # if (childLoc not in discovered) or (child.pathCost() < discovered[childLoc].pathCost()):
            if not childLoc in discovered:
                child.visit()
                discovered[childLoc] = True
                distance = heuristic(problem.startingState(),problem)
                queue.push(child,1+distance)
                
    return ['West']
    # *** Your Code Here ***
    raise NotImplementedError()
