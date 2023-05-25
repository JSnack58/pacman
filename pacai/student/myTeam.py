from pacai.core.directions import Directions

from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core import distanceCalculator
import logging
import random
import time


class SuperReflexAgent(ReflexCaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index)
        # self.offenseAgent = OffensiveReflexAgent(self.index)
        # self.defenseAgent = DefensiveReflexAgent(self.index)
        self.defensiveFeatures = {}
        self.offensiveFeatures = {}
        self.weights = {}

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.
        """

        self.red = gameState.isOnRedTeam(self.index)
        self.distancer = distanceCalculator.Distancer(
            gameState.getInitialLayout())
        # print("root distancer: ",self.distancer)
        self.distancer.getMazeDistances()

    def areInvaders(self, gameState):
        enemies = [gameState.getAgentState(i)
                   for i in self.getOpponents(gameState)]
        invaders = [a for a in enemies if a.isPacman(
        ) and a.getPosition() is not None]
        if len(invaders) > 0:
            return True
        return False

    def infiltrationStarted(self, gameState):
        team = self.getTeam(gameState)
        for teammate in team:
            if teammate != self.index and gameState.getAgentState(teammate).isPacman():
                return True
        return False

    def thereIsADefense(self, gameState):
        team = self.getTeam(gameState)
        for teammate in team:
            if teammate != self.index and not gameState.getAgentState(teammate).isPacman():
                return True
        return False

    def teamMateDistance(self, gameState):
        team = self.getTeam(gameState)
        teamPositions = [gameState.getAgentState(
            teammate).getPosition() for teammate in team]
        dist = self.getMazeDistance(teamPositions[0], teamPositions[1])
        return dist

    def getFeatures(self, gameState, action):
        # activate defense
        successor = self.getSuccessor(gameState, action)
        enemies = [successor.getAgentState(i)
                   for i in self.getOpponents(successor)]
        enemiesLocs = [enemyState.getPosition() for enemyState in enemies]
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        teammateDistance = self.teamMateDistance(gameState)
        if self.areInvaders(gameState) or self.infiltrationStarted(gameState):
            # Computes whether we're on defense (1) or offense (0).
            self.defensiveFeatures['onDefense'] = 1
            if (myState.isPacman()):
                self.defensiveFeatures['onDefense'] = 0

            # Computes distance to invaders we can see.

            self.defensiveFeatures['teammateDistance'] = teammateDistance
            invaders = [a for a in enemies if a.isPacman(
            ) and a.getPosition() is not None]
            self.defensiveFeatures['numInvaders'] = len(invaders)

            defendedFood = len(self.getFoodYouAreDefending(gameState).asList())

            self.defensiveFeatures['defendedFood'] = defendedFood

            if (len(invaders) > 0):
                # print("Defense: ",myPos,invaders)
                dists = [self.getMazeDistance(
                    myPos, a.getPosition()) for a in invaders]
                self.defensiveFeatures['invaderDistance'] = min(dists)

            if (action == Directions.STOP):
                self.defensiveFeatures['stop'] = 1

            rev = Directions.REVERSE[gameState.getAgentState(
                self.index).getDirection()]
            if (action == rev):
                self.defensiveFeatures['reverse'] = 1

            return self.defensiveFeatures
        # go on offense

        else:
            self.offensiveFeatures['successorScore'] = self.getScore(successor)
            self.defensiveFeatures['teammateDistance'] = teammateDistance
            # Compute distance to the nearest food.
            foodList = self.getFood(successor).asList()

            # This should always be True, but better safe than sorry.
            enemyFood = len(foodList)
            self.offensiveFeatures['enemyFood'] = enemyFood
            self.offensiveFeatures['enemyDistance'] = min(
                [self.getMazeDistance(myPos, enemy) for enemy in enemiesLocs])
            # print("length ", length)
            if (enemyFood > 0):
                myPos = successor.getAgentState(self.index).getPosition()
                # print("my list: ",myPos,foodList)
                minDistance = min([self.getMazeDistance(myPos, food)
                                  for food in foodList])
                self.offensiveFeatures['distanceToFood'] = minDistance
            return self.offensiveFeatures

    def getWeights(self, gameState, action):
        self.weights = {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -20,
            'stop': 0,
            'reverse': 0,
            'enemyFood': -100,
            'defendedFood': 150,
            'successorScore': 1.0,
            'distanceToFood': -1.0,
            'enemyDistance': .1,
            'teammateDistance': 1
        }
        return self.weights

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState, action)
        # print("features: ",features)
        weights = self.getWeights(gameState, action)
        # print("weights: ",weights)
        stateEval = sum(features[feature] * weights[feature]
                        for feature in features)

        return stateEval

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """
        actions = gameState.getLegalActions(self.index)
        # print(actions)
        start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        logging.debug('evaluate() time for agent %d: %.4f' %
                      (self.index, time.time() - start))

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        # print("values: ",values)
        # print("bestActions: ",bestActions)
        return random.choice(bestActions)


def createTeam(firstIndex, secondIndex, isRed,
               first='pacai.student.myTeam.SuperReflexAgent',
               second='pacai.student.myTeam.SuperReflexAgent'):

    return[
        SuperReflexAgent(firstIndex),
        SuperReflexAgent(secondIndex)
    ]
