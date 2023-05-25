# from hashlib import new
# from posixpath import supports_unicode_filenames
# import random


# from zoneinfo import available_timezones
from pacai.core.directions import Directions
from pacai.student.searchAgents import ClosestDotSearchAgent
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print("scores: ",scores)
        # print("bestIndicies: ",bestIndices)
        # chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.
        # Modification: chooses the bestscore being the safest distance
        chosenIndex = scores.index(max(scores))
        return legalMoves[chosenIndex]

    def scaredyCatPacman(self, successorGameState):
        # Avoids ghost at all costs, can get stuck on corners to avoid them
        # weakness trapped between 2 ghosts
        # get PacMan's and ghosts' positions
        newPosition = successorGameState.getPacmanPosition()
        ghostIndicies = successorGameState.getGhostIndexes()
        ghostPositions = [successorGameState.getGhostPosition(
            agentIndex) for agentIndex in ghostIndicies]

        # find distance between pacman and ghosts
        pacDist = [manhattan(newPosition, gPos) for gPos in ghostPositions]

        # return sum of pacman's score and distance between closest ghost
        safestDistance = min(pacDist)
        # safestDistance = 1/min(pacDist)
        return safestDistance

    def distanceToClosestFood(self, currentGameState, successorGameState):
        # turn the food matrix into list of coordinates
        # iterate the list
        # if coord
        oldFood = currentGameState.getFood()
        pacLoc = successorGameState.getPacmanPosition()
        dis = None
        for coord in oldFood.asList():
            x, y = coord
            if oldFood[x][y]:
                if dis is None:
                    dis = manhattan(pacLoc, (x, y))
                else:
                    dis = min(dis, manhattan(pacLoc, (x, y)))
        return dis

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # print("successorGameState = ",successorGameState)
        # print("score ", successorGameState.getScore())
        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldPosition = currentGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # ghostIndicies = successorGameState.getGhostIndexes()

        # amplifies affect of food distance
        hunger = 10

        # Scaredy-cat pacman: Focuses on avoiding ghost
        safestDistance = self.scaredyCatPacman(successorGameState)

        # Find distance to closest food
        closestFood = self.distanceToClosestFood(
            currentGameState, successorGameState)

        score = safestDistance
        score -= hunger * closestFood
        score += successorGameState.getScore()

        return score


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def maxVal(self, gameState, currentDepth, treeDepth):
        # if games state is win, loss, or treeDepth is exceed
        # return the evaluation of the state
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            return self.getEvaluationFunction()(gameState)

        # intialize variables
        # value: the largest value from the worst outcome for pacman
        value = -float("inf")  # so any number can be bigger
        # pacman has an index of 0 in agentIndex
        # ghosts have indexes 1 to numAgents-1
        pacman = 0
        firstGhost = 1
        # for all legal actions pacman can take
        # create successor from the current action
        # value <- max(value, minValue from the ghosts' positions)
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)
            value = max(value, self.minVal(
                successor, currentDepth, treeDepth, firstGhost))
        # value now is the best value out of the worst situation
        return value

    def minVal(self, gameState, currentDepth, treeDepth, agent):
        # wins, losses, or exceeding treedepth returns evaluated gameState
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            return self.getEvaluationFunction()(gameState)
        # intialize variables
        # value: the smallest value from the best outcome for pacman
        # so any number can be smaller, easily finds minimum
        value = float("inf")
        # agents are the number of agents in the game
        # agents' have unique indexes
        # pacman's index 0, ghosts are indexes 1 to agents - 1
        agents = gameState.getNumAgents()  # to find the last agentIndex
        # on the last ghost find the smallest score pacman can get in his gameState
        # increase the treeDepth because we planned for all ghosts
        if agent == agents - 1:
            value = min(value, self.maxVal(
                gameState, currentDepth + 1, treeDepth))
        # we haven't planned for all ghosts
        # find if next ghost can minimize pacman's score
        else:
            value = min(value, self.minVal(
                gameState, currentDepth, treeDepth, agent + 1))

        # value is now the least value of best situation for pacman
        return value

    # return a list of legal action excluding 'stop'
    def __getLegalActions__(self, state, agentId):
        actions = state.getLegalActions(agentId)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        return actions

    # return the best action for the worst possible situation
    def getAction(self, gameState):
        # treeDepth holds how much we want to plan ahead
        treeDepth = self.getTreeDepth()
        currentDepth = 0
        # bestscore compared to all values search for max between both
        # negative infinity because anything could be bigger
        bestscore = -float("inf")
        # bestAction: best action for worst possible situation
        # stop because its legal anywhere
        bestAction = Directions.STOP
        # pacman's agentIndex is 0
        pacman = 0
        # generate and iterate all of pacman's legal actions
        # create successor from each action
        # find highest value of each action via maxVal()
        # bestscore become max between itself and the value
        # bestAction is the action that caused the bestscore
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)
            score = self.maxVal(successor, currentDepth, treeDepth)
            if bestscore < score:
                bestscore = score
                bestAction = action
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def maxVal(self, gameState, currentDepth, treeDepth, alpha, Beta):
        # if games state is win, loss, or treeDepth is exceed
        # return the evaluation of the state
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            return self.getEvaluationFunction()(gameState)

        # intialize variables
        # value: the largest value from the worst outcome for pacman
        value = -float("inf")  # so any number can be bigger
        # pacman has an index of 0 in agentIndex
        # ghosts have indexes 1 to numAgents-1
        pacman = 0
        firstGhost = 1
        # for all legal actions pacman can take
        # create successor from the current action
        # value <- max(value, minValue from the ghosts' positions)
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)
            value = max(value, self.minVal(
                successor, currentDepth, treeDepth, firstGhost, alpha=alpha, Beta=Beta))
            if value >= Beta:
                return value
            alpha = max(alpha, value)
        # value now is the best value out of the worst situation
        return value

    def minVal(self, gameState, currentDepth, treeDepth, agent, alpha, Beta):
        # wins, losses, or exceeding treedepth returns evaluated gameState
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            return self.getEvaluationFunction()(gameState)
        # intialize variables
        # value: the smallest value from the best outcome for pacman
        # so any number can be smaller, easily finds minimum
        value = float("inf")
        # agents are the number of agents in the game
        # agents' have unique indexes
        # pacman's index 0, ghosts are indexes 1 to agents - 1
        agents = gameState.getNumAgents()  # to find the last agentIndex
        # on the last ghost find the smallest score pacman can get in his gameState
        # increase the treeDepth because we planned for all ghosts
        if agent == agents - 1:
            value = min(value, self.maxVal(
                gameState, currentDepth + 1, treeDepth, alpha=alpha, Beta=Beta))
            if value <= alpha:
                return value
            Beta = min(Beta, value)
        # we haven't planned for all ghosts
        # find if next ghost can minimize pacman's score
        else:
            value = min(value, self.minVal(
                gameState, currentDepth, treeDepth, agent + 1, alpha=alpha, Beta=Beta))
            if value <= alpha:
                return value
            Beta = min(Beta, value)
        # value is now the least value of best situation for pacman
        return value

    def __getLegalActions__(self, state, agentId):
        actions = state.getLegalActions(agentId)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        return actions

    def getAction(self, gameState):
        # treeDepth holds how much we want to plan ahead
        treeDepth = self.getTreeDepth()
        currentDepth = 0
        # bestscore compared to all values search for max between both
        # negative infinity because anything could be bigger
        bestscore = -float("inf")
        # bestAction: best action for worst possible situation
        # stop because its legal anywhere
        bestAction = Directions.STOP
        # pacman's agentIndex is 0
        pacman = 0
        # generate and iterate all of pacman's legal actions
        # create successor from each action
        # find highest value of each action via maxVal()
        # bestscore become max between itself and the value
        # bestAction is the action that caused the bestscore
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)
            score = self.maxVal(successor, currentDepth, treeDepth,
                                alpha=-float("inf"), Beta=float("inf"))
            if bestscore < score:
                bestscore = score
                bestAction = action
        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def maxVal(self, gameState, currentDepth, treeDepth):
        # if games state is win, loss, or treeDepth is exceed
        # return the evaluation of the state
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            if(gameState.isLose()):
                return -float("inf")
            return self.getEvaluationFunction()(gameState)

        # intialize variables
        # value: the largest value from the worst outcome for pacman
        value = -float("inf")  # so any number can be bigger
        # pacman has an index of 0 in agentIndex
        # ghosts have indexes 1 to numAgents-1
        pacman = 0
        firstGhost = 1
        # for all legal actions pacman can take
        # create successor from the current action
        # value <- max(value, minValue from the ghosts' positions)
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)

            maxi = max(value, self.minVal(
                successor, currentDepth, treeDepth, firstGhost))
            value = maxi

        return value

    def minVal(self, gameState, currentDepth, treeDepth, agent):
        # wins, losses, or exceeding treedepth returns evaluated gameState
        if gameState.isWin() or gameState.isLose() or currentDepth >= treeDepth:
            if(gameState.isLose()):
                return -float("inf")
            return self.getEvaluationFunction()(gameState)
        # intialize variables
        # value: the smallest value from the best outcome for pacman
        # so any number can be smaller, easily finds minimum
        # value = float("inf")
        actions = self.__getLegalActions__(agentId=agent, state=gameState)
        numActions = len(actions)
        value = float("inf")
        # agents are the number of agents in the game
        # agents' have unique indexes
        # pacman's index 0, ghosts are indexes 1 to agents - 1
        agents = gameState.getNumAgents()  # to find the last agentIndex
        # on the last ghost find the smallest score pacman can get in his gameState
        # increase the treeDepth because we planned for all ghosts
        for action in actions:
            ghostSuccessor = gameState.generateSuccessor(
                agentIndex=agent, action=action)

            if agent == agents - 1:
                # print("before-value ",value)
                mini = min(value, self.maxVal(
                    ghostSuccessor, currentDepth + 1, treeDepth))
                # print("after-Minvalue: ","min(",value,",",mini,")")
                if value == float("inf"):
                    value = mini
                else:
                    value += mini
                # print(" mini: ",mini,"after-value: ",value)
            # we haven't planned for all ghosts
            # find if next ghost can minimize pacman's score
            else:
                # print("before-value ",value)
                mini = self.minVal(
                    ghostSuccessor, currentDepth, treeDepth, agent + 1)
                if value == float("inf"):
                    value = mini
                else:
                    value += mini
                # print(" mini: ",mini,"after-value: ",value)
        # value is now the least value of best situation for pacman

        return value / numActions

    # return a list of legal action excluding 'stop'

    def __getLegalActions__(self, state, agentId):
        actions = state.getLegalActions(agentId)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        return actions

    # def findWeight(self,actions):
    #     for action in actions:
    #         value += self.maxVal
    #     return value
    def getAction(self, gameState):
        # treeDepth holds how much we want to plan ahead
        treeDepth = self.getTreeDepth()
        currentDepth = 0
        # bestscore compared to all values search for max between both
        # negative infinity because anything could be bigger
        bestscore = -float("inf")
        # bestAction: best action for worst possible situation
        # stop because its legal anywhere
        bestAction = Directions.STOP
        # pacman's agentIndex is 0
        pacman = 0
        # generate and iterate all of pacman's legal actions
        # create successor from each action
        # find highest value of each action via maxVal()
        # bestscore become max between itself and the value
        # bestAction is the action that caused the bestscore
        actions = self.__getLegalActions__(gameState, pacman)
        for action in actions:
            if action == 'Stop':
                continue
            successor = gameState.generateSuccessor(
                agentIndex=pacman, action=action)

            # value will be the maxVal of current Action
            # value gets added to the wieghtValue
            # weight+
            # track value
            # print("actions: ",action)
            score = self.maxVal(successor, currentDepth, treeDepth)
            # print(action,"'s score: ",score)
            # acc += value
            # weightVal += value * acc/numActions
            # weight = weightVal/(numActions)
            # score = weight * value

            # should we keep the bestcore
            if bestscore < score:
                bestscore = score
                bestAction = action
                # print("bestAction is now: ",bestAction,"score of",bestscore)

            # index += 1
        # print("getAction() move ",bestAction)
        return bestAction


def scaredyCatPacman(successorGameState):
    # Avoids ghost at all costs, can get stuck on corners to avoid them
    # weakness trapped between 2 ghosts
    # get PacMan's and ghosts' positions
    newPosition = successorGameState.getPacmanPosition()
    ghostIndicies = successorGameState.getGhostIndexes()
    ghostPositions = [successorGameState.getGhostPosition(
        agentIndex) for agentIndex in ghostIndicies]

    # find distance between pacman and ghosts
    pacDist = [manhattan(newPosition, gPos) for gPos in ghostPositions]

    # return sum of pacman's score and distance between closest ghost
    safestDistance = min(pacDist)
    # safestDistance = 1/min(pacDist)
    # safestDistance = safestDistance
    return safestDistance


def distanceToClosestFood(currentGameState, successorGameState):
    # turn the food matrix into list of coordinates
    # iterate the list
    # if coord
    pacman = 0
    actions = currentGameState.getLegalActions(pacman)
    oldFood = currentGameState.getFood()
    dis = float("inf")
    for action in actions:
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacLoc = successorGameState.getPacmanPosition()
        for coord in oldFood.asList():
            x, y = coord
            if oldFood[x][y]:
                dis = min(dis, manhattan(pacLoc, (x, y)))
    if dis > 3:
        return float("inf")

    return dis
def distanceToWall(currentGameState):
    # turn the food matrix into list of coordinates
    # iterate the list
    # if coord
    pacman = 0
    actions = currentGameState.getLegalActions(pacman)
    walls = currentGameState.getWalls()
    dis = float("inf")
    for action in actions:
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacLoc = successorGameState.getPacmanPosition()
        for coord in walls.asList():
            x, y = coord
            if walls[x][y]:
                dis = min(dis, manhattan(pacLoc, (x, y)))
    return dis

def moveOptions(currentGameState):
    moves = len(currentGameState.getLegalActions(0))
    return moves


def adjecentFood(currentGameState):
    pacman = 0
    actions = currentGameState.getLegalActions(pacman)
    oldFood = currentGameState.getFood()
    food = 0
    for action in actions:
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        x, y = successorGameState.getPacmanPosition()
        if oldFood[x][y]:
            food += 1
    return food

def nearbyCapsule(currentGameState):
    pacman = 0
    actions = currentGameState.getLegalActions(pacman)
    for action in actions:
        successor = currentGameState.generateSuccessor(pacman, action)
        x, y = successor.getPacmanPosition()
        if currentGameState.hasCapsule(x, y):
            return float("inf")
    return 0

closet = ClosestDotSearchAgent(0)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    successorGameState = currentGameState
    # print("successorGameState = ",successorGameState)
    # print("score ", successorGameState.getScore())
    # Useful information you can extract.
    # newPosition = successorGameState.getPacmanPosition()
    # oldPosition = currentGameState.getPacmanPosition()
    # oldFood = currentGameState.getFood()
    # newGhostStates = successorGameState.getGhostStates()
    # ghostIndicies = successorGameState.getGhostIndexes()
    # amplifies affect of food distance
    hunger = 10
    numMoves = moveOptions(currentGameState)
    # Scaredy-cat pacman: Focuses on avoiding ghost
    safestDistance = scaredyCatPacman(successorGameState)
    # Find distance to closest food
    closestFood = distanceToClosestFood(
        currentGameState, successorGameState)
    numFood = currentGameState.getNumFood()
    if numFood == 0:
        numFood = float("inf")
    else:
        numFood = 1 / numFood
    # numMoves = moveOptions(currentGameState)
    # foodNextToPacman = adjecentFood(currentGameState)
    # safe distance from ghost +(increase distance to ghost)
    # distance from food -(decrease distance to food)
    # eating where there's no food -(decrease the amount of no food)
    # movement options +(increase movement options)
    # getScore()
    # score = fear * safestDistance
    # if safestDistance > 2:
    #     score = fear * safestDistance
    #     score -= hunger * closestFood * numFood
    # score += nearbyCapsule(currentGameState)
    # score += foodNextToPacman * hunger
    # score *= numMoves
    score = successorGameState.getScore()
    score += numMoves * safestDistance
    if safestDistance > 2:
        # score -= distanceToWall(currentGameState)
        score -= hunger * closestFood * numFood
    # score = 0
    # print(score)
    return score
    # return currentGameState.getScore()


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
