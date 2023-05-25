import random
from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection, probability


class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.values = {}

    # if (state, action) pair in values
    #   return the value
    # else
    #   return 0.0
    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        # set qval = 0
        # check if state/action are in self.values
        # if so put in self.values and return qval = value
        # self.values[(state, action)] = qval
        if (state, action) in self.values:
            # print("Found self.values[",state,"] = ",self.values[(state,action)])
            return self.values[(state, action)]
        # print("self.values[",state,"] = 0.0")
        return 0.0

    # get list of actions
    # create list of Q-values from each action
    # if Q-value list is empty
    #   return 0.0
    # else return max value of list
    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        # get action for action in actions
        # append qval from list
        actions = self.getLegalActions(state)
        qVals = [self.getQValue(state, action) for action in actions]
        if len(qVals) == 0:
            return 0.0
        maxQVal = max(qVals)
        # print("maxQVal",maxQVal)
        return maxQVal
        # return 0.0

    # initialize bestAction as None
    # intiallize bestActions as empty array
    # iterate state's actions from possibleActions
    #   returnAction = None
    #   create an array of Q-values from the actions and state
    #   record length of Q-value array
    #   if array is empty
    #       return returnAction
    # initialize bestQ-value as negative infinity
    # iterate the indicies of Q-value array
    #   if q-value at index is greater than bestQ-value
    #       means a better path is found
    #       bestAction = action at index in action
    #       reset bestActions to empty array then append bestAction
    #   else if q-value is equal to bestQVal
    #        append action to the bestActions
    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """

        # iterate state's actions from possibleActions
        #   returnAction = STOP
        #   getQValue on each action on the state
        #   compare val = getValue() to q = getQValue()
        #       if val == q
        #           append action to list
        #   action = random.choice(list)
        #   return action
        # bestAction = Directions.STOP

        # bestAction is None
        # array of bestActions
        # qVals array of QValues
        bestAction = None
        bestActions = []
        actions = self.getLegalActions(state)
        qVals = [self.getQValue(state, action) for action in actions]
        qValsLen = len(qVals)

        if qValsLen == 0:
            return bestAction

        bestQVal = -float("inf")
        for index in range(qValsLen):
            if qVals[index] > bestQVal:
                bestQVal = qVals[index]
                bestAction = actions[index]
                # reset bestActions to start a new set of bestActions
                bestActions = [bestAction]
            elif qVals[index] == bestQVal:
                bestActions.append(actions[index])

        # if bestActions isn't empty
        #   return random action
        # else
        #   return None
        if len(bestActions) != 0:
            return random.choice(bestActions)
        else:
            return None

    # get alpha, discount-rate, and future-value
    # caculate sample
    # caculate value
    # put value in self.values indexed by state-action tuple
    def update(self, state, action, nextState, reward):
        # getAlpha
        # getdiscountRate
        # futureVal = getValue(nextState)
        alpha = self.getAlpha()
        discountRate = self.getDiscountRate()
        futureVal = self.getValue(nextState)
        qVal = self.getQValue(state, action)
        sample = reward + discountRate * futureVal

        self.values[(state, action)] = (1 - alpha) * qVal + alpha * sample

    # if flipCoin is True
    #   return a random action
    # else
    #   return best action via getPolicy()
    def getAction(self, state):
        if probability.flipCoin(self.getEpsilon()):
            return random.choice(self.getLegalActions(state))
        return self.getPolicy(state)


class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action


class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
                 extractor='pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            print(self.weights.values())
            # raise NotImplementedError()

    # get the discountRate, future-value, and QValue
    # calculate and return correction value
    def getCorrection(self, state, action, nextState, reward):
        discountRate = self.getDiscountRate()
        futureVal = self.getValue(nextState)
        qVal = self.getQValue(state, action)

        return (reward + discountRate * futureVal) - qVal

    # get the features dictionary
    # iterate the features dictionary
    #   if feature is in the weight vector
    #       get alpha, feature weight and value, and correction value
    #       calculate the new weight
    #       put new weight into weight dictionary at feature
    #   else
    #       initialize feature weight as 0.0 in weight vector
    def update(self, state, action, nextState, reward):
        features = self.featExtractor().getFeatures(state, action)
        for feature in features:
            if feature in self.weights:
                correction = self.getCorrection(
                    state, action, nextState, reward)
                self.weights[feature] = self.weights[feature] + \
                    self.getAlpha() * correction * features[feature]
            else:
                self.weights[feature] = 0.0

    # get the features dictionary
    # intialize Q-value as 0
    # iterate the feature dictionary
    #   if feature in weight vector
    #       multiply feature value by feature weight
    #       increment Q-value by product
    def getQValue(self, state, action):
        features = self.featExtractor().getFeatures(state, action)
        qVal = 0

        for feature in features:
            if feature in self.weights:
                qVal += features[feature] * self.weights[feature]

        return qVal
