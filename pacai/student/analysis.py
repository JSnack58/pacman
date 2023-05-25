"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None


def question2():
    """
    [Enter a description of what you did here.]
    """

    # answerDiscount = 0.9
    # answerNoise = 0.2
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise


def question3a():
    """
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = -0.9

    return answerDiscount, answerNoise, answerLivingReward


def question3b():
    """
    [Enter a description of what you did here.]
    """

    # answerDiscount = 0.9
    # answerNoise = 0.2
    # answerLivingReward = 0.0
    answerDiscount = 0.5
    answerNoise = 0.3
    answerLivingReward = -0.9
    return answerDiscount, answerNoise, answerLivingReward


def question3c():
    """
    [Enter a description of what you did here.]
    """

    # answerDiscount = 0.9
    # answerNoise = 0.2
    # answerLivingReward = 0.0
    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0
    return answerDiscount, answerNoise, answerLivingReward


def question3d():
    """
    [Enter a description of what you did here.]
    """

    # answerDiscount = 0.9
    # answerNoise = 0.2
    # answerLivingReward = 0.0
    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3e():
    """
    [Enter a description of what you did here.]
    """

    # answerDiscount = 0.9
    # answerNoise = 0.2
    # answerLivingReward = 0.0
    answerDiscount = 0.9
    answerNoise = 0.9
    answerLivingReward = 3.0

    return answerDiscount, answerNoise, answerLivingReward


def question6():
    """
    [Enter a description of what you did here.]
    """

    # trade off between Epsilon and learningRate
    # Increasing learning rate cause pacman to stay at start
    #   pacman stays at start
    #   would need to increase Epsilon to randomly cross bridge
    # Decreasing learning rate
    #   pacman wastes lives on cliffs
    #   needs to learn faster to choose best option
    # Increase Epsilon
    #   pacman moves to randomly to cross bridge
    #   would need to learn faster to chose right
    # Decrease Epsilon
    #   pacman stays at start, increase Epsilon
    return NOT_POSSIBLE


if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
