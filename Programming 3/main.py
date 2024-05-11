import random
import numpy as np

DEBUG = False

# the function to choose a number from a distribution


def chooseFromDist(p: list[float]) -> int:
    # p = [0.1, 0.2, 0.3, 0.4]
    # return 1 with 10% chance, 2 with 20% chance, 3 with 30% chance, 4 with 40% chance
    values = list(range(1, len(p) + 1))
    return random.choices(values, weights=p, k=1)[0]

# the function to roll a dice and return the sum or the rolls


def rollDice(NDice, NSides) -> int:
    total = 0
    for roll_trial in range(NDice):
        roll = random.randint(1, NSides)
        total += roll
    return total

# the function to choose the number of dice to roll


def chooseDice(X, Y, LoseCount, WinCount, NDice, M) -> int:
    # return the number of dice to roll

    # selected_total and selected_WinCount are the accounts of the number of dice to roll at state <X,Y>
    selected_total = LoseCount[:, X, Y] + WinCount[:, X, Y]
    selected_WinCount = WinCount[:, X, Y]

    # initialize f_ks of the length of the dice: f_ks[0] refers to the probability of choosing 1 dice
    f_ks = np.zeros(NDice)
    for k in range(1, NDice + 1):
        # if the denominator is 0, set f_k to 0.5
        if selected_total[k] == 0:
            f_ks[k-1] = 0.5
        else:
            f_ks[k-1] = selected_WinCount[k] / selected_total[k]

    # get k^ and its index
    best_k_index = np.argmax(f_ks)
    best_f_k = f_ks[best_k_index]

    # calculate s and T
    s = np.sum(f_ks) - f_ks[best_k_index]
    T = sum(selected_total)

    # calculate p_k^ according to the formula
    best_p_k = (T*best_f_k + M) / (T*best_f_k + NDice*M)

    # calculate p_k according to the formula
    p_k = np.empty_like(f_ks)
    for k in range(1, NDice + 1):
        f_k = f_ks[k-1]
        if k-1 == best_k_index:
            p_k[k-1] = best_p_k
        else:
            p_k[k-1] = (1 - best_p_k) * (T * f_k + M) / (T * s + (NDice-1) * M)

    # give the distribution to chooseFromDist and get the number of dice to roll
    number_of_dice = chooseFromDist(list(p_k))

    if DEBUG:
        print(
            f"choosing {number_of_dice} dices with probability {p_k[number_of_dice-1]}")
    return number_of_dice


def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):

    # initialize the scores to be 0
    A_score, B_score = 0, 0

    # used to record the step of each player
    A_record, B_record = [], []

    # a flah to indicate whose turn it is
    is_A_turn = True

    # loop until one of the player wins
    while A_score < LTarget and B_score < LTarget:

        # if it is A's turn
        if is_A_turn:

            # decide the number of dice to roll
            number_of_dice = chooseDice(
                A_score, B_score, LoseCount, WinCount, NDice, M)

            # record the step
            A_record.append([A_score, B_score, number_of_dice])

            # roll the dice
            A_roll = rollDice(number_of_dice, NSides)

            if DEBUG:
                print(f"A's turn: A_score={A_score}, B_score={B_score}")
                print(f"A_record: {A_record}")
                print(f"A rolls {A_roll}")

            # update the score and flag
            A_score += A_roll
            is_A_turn = False

        # if it is B's turn
        else:

            # decide the number of dice to roll
            number_of_dice = chooseDice(
                B_score, A_score, LoseCount, WinCount, NDice, M)

            # record the step
            B_record.append([B_score, A_score, number_of_dice])

            # roll the dice
            B_roll = rollDice(number_of_dice, NSides)

            if DEBUG:
                print(f"B's turn: A_score={A_score}, B_score={B_score}")
                print(f"B_record: {B_record}")
                print(f"B rolls {B_roll}")

            # update the score and flag
            B_score += B_roll
            is_A_turn = True

    # when one player wins, update WinCount and LoseCount
    if (A_score >= LTarget and A_score <= UTarget) or B_score > UTarget:

        if DEBUG:
            print("A wins")

        # if A wins
        for record in A_record:
            # update WinCount with A's record
            A_score, B_score, number_of_dice = record[0], record[1], record[2]
            WinCount[number_of_dice, A_score, B_score] += 1
            if DEBUG:
                print(
                    f"WinCount[{number_of_dice}, {A_score}, {B_score}] = {WinCount[number_of_dice, A_score, B_score]}")

        for record in B_record:
            # update LoseCount with B's record
            B_score, A_score, number_of_dice = record[0], record[1], record[2]
            LoseCount[number_of_dice, B_score, A_score] += 1
            if DEBUG:
                print(
                    f"LoseCount[{number_of_dice}, {B_score}, {A_score}] = {LoseCount[number_of_dice, B_score, A_score]}")
    else:
        # if B wins
        if DEBUG:
            print("B wins")

        for record in B_record:
            # update WinCount with B's record
            B_score, A_score, number_of_dice = record[0], record[1], record[2]
            WinCount[number_of_dice, B_score, A_score] += 1
            if DEBUG:
                print(
                    f"WinCount[{number_of_dice}, {B_score}, {A_score}] = {WinCount[number_of_dice, B_score, A_score]}")

        for record in A_record:
            # update LoseCount with A's record
            A_score, B_score, number_of_dice = record[0], record[1], record[2]
            LoseCount[number_of_dice, A_score, B_score] += 1
            if DEBUG:
                print(
                    f"LoseCount[{number_of_dice}, {A_score}, {B_score}] = {LoseCount[number_of_dice, A_score, B_score]}")
    # print(WinCount, LoseCount)
    return LoseCount, WinCount

# the function to extract the final answer from WinCount and LoseCount


def extractAnswer(WinCount, LoseCount):

    # get the number of dice that has highest wincount each state
    best_k_indices = np.argmax(WinCount, axis=0)

    # get the wincount and total count for these best ks
    total = WinCount + LoseCount
    x_indices, y_indices = np.indices(best_k_indices.shape)
    selected_WinCount = WinCount[best_k_indices, x_indices, y_indices]
    selected_total = total[best_k_indices, x_indices, y_indices]

    if DEBUG:
        print("selected_WinCount", selected_WinCount)
        print("selected_total", selected_total)

    # calculate the probability
    probs = np.where(selected_total > 0, selected_WinCount / selected_total, 0)
    return probs, best_k_indices


def prog3(NDice, NSides, LTarget, UTarget, NGames, M):

    # Initialize WinCount and LoseCount
    LoseCount = np.zeros((NDice + 1, LTarget, LTarget))
    WinCount = np.zeros((NDice + 1, LTarget, LTarget))

    # run the game "NGames" times
    for game_trial in range(NGames):
        if DEBUG:
            print(f"-------------Game {game_trial + 1}-------------")
        # update WinCount and LoseCount
        LoseCount, WinCount = PlayGame(
            NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

    probs, solutions = extractAnswer(WinCount, LoseCount)
    print(WinCount, '\n', LoseCount)
    print("Play =\n", probs)
    print("Prob =\n", solutions)
    return probs, solutions


if __name__ == '__main__':

    np.set_printoptions(suppress=True)  # turn off scientific notation

    # =============== parameters ===============
    # NDice = 3
    # NSides = 2
    # LTarget = 6
    # UTarget = 7
    # M = 100
    # NGames = 100000

    NDice = 2
    NSides = 2
    LTarget = 4
    UTarget = 5
    M = 100
    NGames = 100000

    random_seed = 2
    # ==========================================

    random.seed(random_seed)
    prog3(NDice, NSides, LTarget, UTarget, NGames, M)
