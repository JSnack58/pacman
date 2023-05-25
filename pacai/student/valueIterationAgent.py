from pacai.agents.learning.value import ValueEstimationAgent
# from pacai.core.mdp.MarkovDecisionProcess import getStates
# from pacai.core.mdp.MarkovDecisionProcess import getPossibleActions
# from pacai.core.mdp.MarkovDecisionProcess import getTransitionStatesAndProbs
# from pacai.core.mdp.MarkovDecisionProcess import getReward


class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate=0.9, iters=100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        # A dictionary which holds the q-values for each state.
        self.values = {}

        # Compute the values here.
        states = self.mdp.getStates()
        self.values = {state: 0 for state in states}
        for i in range(iters):

            self.valueIteration(states)

    # create empty temporary dictionary
    # iterate through the states to fill dictionary
    #   if state is terminal
    #       set dict key to state and value to 0
    #       continue
    #   else
    #       set dict key to state value to best-value
    # put all key-value pairs in the self.values
    def valueIteration(self, states):
        tmp = {}
        for state in states:
            if self.mdp.isTerminal(state):
                tmp[state] = 0
                continue
            tmp[state] = self.getBestActionAndValue(state)[1]

        self.values = {state: tmp[state] for state in states}

    # initialize value to 0
    # get successor states and state probabilites
    # iterate through successor states and probabilities
    #   find the successor state's transition reward
    #   calculate Q-value of the successor state
    #   increment value by the Q-value
    # return the value
    def getQValue(self, state, action):
        value = 0
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for stateProb in statesAndProbs:
            successorState, transitionProbability = stateProb
            transitionReward = self.mdp.getReward(
                state, action, successorState)
            discountedValue = self.discountRate * self.getValue(successorState)
            rewardValueSum = transitionReward + discountedValue
            value += transitionProbability * rewardValueSum

        return value

    # get state's possible actions
    # initialize bestValue as negative infinity
    # initialize bestAction as None
    # iterate possible actions
    #   get Q-value of each action in the state
    #   if Q-value surpasses bestValue
    #       bestValue = Q-value
    #       bestAction = action
    # return bestAction and bestValue as a tuple
    def getBestActionAndValue(self, state):
        actions = self.mdp.getPossibleActions(state)
        bestValue = -float("inf")
        bestAction = None
        for action in actions:
            qVal = self.getQValue(state, action)
            if qVal > bestValue:
                bestValue = qVal
                bestAction = action
        return (bestAction, bestValue)

    # return the bestAction from getBestActionAndValue
    def getPolicy(self, state):
        return self.getBestActionAndValue(state)[0]

    # return value from self.alues
    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        # print(self.values.keys())
        # print(state)
        return self.values[state]

    # return the action from getPolicy
    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
