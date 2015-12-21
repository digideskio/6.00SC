# Problem Set 7: Probabilities
# Name: Shouvik Roy
# Collaborators:
# Time: 30 mins


import random


def rollDie():
    """
    Rolls a six sided die. Returns a number from 1 to 6 chosen randomly.
    """
    return random.choice([1, 2, 3, 4, 5, 6])


def roll_n_die(n):
    """
    Rolls n die. Returns a string representation of the outcome
    """
    result = ""
    for i in range(n):
        result += str(rollDie())
    return result


def simulate_yahtzee(number_of_iterations):
    yahtzee = ["11111", "22222", "33333", "44444", "55555", "66666"]
    rolled_yahtzee = 0
    for i in range(number_of_iterations):
        current_roll = roll_n_die(5)
        if current_roll in yahtzee:
            rolled_yahtzee += 1
    return rolled_yahtzee / float(number_of_iterations)

print simulate_yahtzee(10000000)
