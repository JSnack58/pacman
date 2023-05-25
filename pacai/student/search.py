"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue


def depthFirstSearch(problem):
    queue = Stack()
    visitedList = []
    startState = problem.startingState()
    target = (startState, [], 0)
    queue.push(target)
    # visitedList.append(startState)
    if problem.isGoal(target[0]):
        return target[1]
    while not queue.isEmpty():
        target = queue.pop()
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        # print(len(visitedList), target)
        if problem.isGoal(target[0]):
            return target[1]
        successors = problem.successorStates(target[0])

        for successor in successors:

            queue.push((successor[0],
                        target[1] + [successor[1]],
                        0))
        # if problem.isGoal(target[0]):
        #     return target[1]
    return None


def breadthFirstSearch(problem):
    queue = Queue()
    visitedList = []
    startState = problem.startingState()
    target = (startState, [], 0)
    if problem.isGoal(target[0]):
        return target[1]
    queue.push(target)
    while not queue.isEmpty():
        target = queue.pop()  # state path cost
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        if problem.isGoal(target[0]):
            # print(target[1])
            return target[1]
        successors = problem.successorStates(target[0])
        for successor in successors:

            queue.push((successor[0],
                        target[1] + [successor[1]],
                        0))
        if problem.isGoal(target[0]):
            # print(target[1])
            return target[1]
    return None


def visitUCS(problem, state):

    location = state[0]
    action = state[1]
    cost = state[2]
    for successor in problem.successorStates(location):
        successorState = (successor[0],
                          action + [successor[1]],
                          successor[2] + cost)
        # successorState = (successor[0],
        #                   action + [successor[1]],
        #                   successor[2])
        yield successorState


def uniformCostSearch(problem):
    queue = PriorityQueue()
    visitedList = []
    startState = problem.startingState()
    # print("startState: ",startState)c
    target = (startState, [], 0)

    if problem.isGoal(target[0]):
        return target[1]
    queue.push(target, 0)

    while not queue.isEmpty():
        target = queue.pop()  # state path cost

        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        # print("target",target)
        for successor in visitUCS(problem, target):
            queue.push(successor, successor[2])
        if problem.isGoal(target[0]):
            return target[1]
    return None

def visitAS(problem, state):

    location = state[0]
    action = state[1]
    cost = state[2]
    for successor in problem.successorStates(location):
        successorState = (successor[0],
                          action + [successor[1]],
                          successor[2] + cost)
        yield successorState
def aStarSearch(problem, heuristic):
    queue = PriorityQueue()
    visitedList = []
    startState = problem.startingState()
    distance = heuristic(problem.startingState(), problem)
    target = (startState, [], 0)

    if problem.isGoal(target[0]):
        return target[1]

    # queue.push(target, 1 + distance)
    aStar = 1 + distance
    queue.push(target, aStar)
    while not queue.isEmpty():
        target = queue.pop()  # state path cost
        if target[0] in visitedList:
            continue
        visitedList.append(target[0])
        for successor in visitUCS(problem, target):
            distance = heuristic(target[0], problem)
            aStar = target[2] + distance
            queue.push(successor, aStar)
            # queue.push(successor, 1 + distance)
        if problem.isGoal(target[0]):
            # print(target[1])
            return target[1]
    return None
