import random
import sys
# import numpy as np


# function for the first line of txt file
def read_input():
    NDice, NSides, LTarget, UTarget, NGames, M = sys.stdin.readline().strip().split()
    NDice, NSides, LTarget, UTarget, NGames, M = int(
        NDice), int(NSides), int(LTarget), int(UTarget), int(NGames), int(M)
    return NDice, NSides, LTarget, UTarget, NGames, M


# choose number by randomly selecting from given distribution
def chooseFromDist(p):
    arr = [i for i in range(1, len(p)+1)]
    choice = random.choices(arr, p, k=1)
    return choice[0]


# find the total of dice
def rollDice(NDice, NSides):
    return sum(random.randint(1, NSides) for _ in range(NDice))


# choose dice with probability
def chooseDice(Score, LoseCount, WinCount, NDice, M):
    K = NDice
    X, Y = Score
    f_values = [0] * (K + 1)

    # calculate the distribution of numbers of dice
    for k in range(1, K + 1):
        if WinCount[X][Y][k] + LoseCount[X][Y][k] == 0:
            f_values[k] = 0.5
        else:
            f_values[k] = WinCount[X][Y][k] / \
                (WinCount[X][Y][k] + LoseCount[X][Y][k])

    # find the needed values
    k_hat = f_values.index(max(f_values[1:]))  # Find k with highest f-value
    s = sum(f_values) - f_values[k_hat]
    T = sum(WinCount[X][Y][k] + LoseCount[X][Y][k] for k in range(1, K + 1))

    pk_hat = (T * f_values[k_hat] + M) / (T * f_values[k_hat] + K * M)
    deno = (s * T + (K - 1) * M)
    prob = [(1 - pk_hat) * (T * f_values[k] + M) /
            deno for k in range(1, K + 1)]

    prob[k_hat-1] = pk_hat

    # choose dice from given distribution
    return chooseFromDist(prob)


# game play function
def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    # initialize
    A_score, B_score = 0, 0
    A_record, B_record = [], []
    flg = True

    # loop until one of the player wins/loses
    while A_score < LTarget and B_score < LTarget:
        # A's turn
        if flg:
            # find number of dice to roll
            number_of_dice = chooseDice(
                [A_score, B_score], LoseCount, WinCount, NDice, M)

            # record the step
            A_record.append([A_score, B_score, number_of_dice])

            # roll the dice
            total_dice = rollDice(number_of_dice, NSides)

            # update the score
            A_score += total_dice
        # B's turn
        else:
            # find number of dice to roll
            number_of_dice = chooseDice(
                [B_score, A_score], LoseCount, WinCount, NDice, M)

            # record the step
            B_record.append([B_score, A_score, number_of_dice])

            # roll the dice
            total_dice = rollDice(number_of_dice, NSides)

            # update the score
            B_score += total_dice

        # flag change
        flg ^= 1

    # update WinCount and LoseCount
    if (LTarget <= A_score <= UTarget) or B_score > UTarget:
        # A wins
        X, Y = WinCount, LoseCount
    else:
        # B wins
        X, Y = LoseCount, WinCount

    for record in A_record:
        # update WinCount with A's record
        A_score, B_score, number_of_dice = record[0], record[1], record[2]
        X[A_score][B_score][number_of_dice] += 1

    for record in B_record:
        # update LoseCount with B's record
        B_score, A_score, number_of_dice = record[0], record[1], record[2]
        Y[B_score][A_score][number_of_dice] += 1

    return LoseCount, WinCount


# explain the result
def extractAnswer(WinCount, LoseCount):
    # import numpy as np
    # print(np.array(WinCount))
    # print(np.array(LoseCount))

    # interpret the count matrices into decision and prob
    result = []
    for i in range(len(WinCount)):
        for j in range(len(WinCount[i])):
            best_ratio = 0
            best_move = 0
            for k in range(1, len(WinCount[i][j])):
                deno = (WinCount[i][j][k] + LoseCount[i][j][k])
                if deno == 0:
                    ratio = 0
                else:
                    ratio = WinCount[i][j][k] / deno

                if ratio > best_ratio:
                    best_ratio = ratio
                    best_move = k

            if WinCount[i][j][best_move] + LoseCount[i][j][best_move] == 0:
                probability = 0
            else:
                probability = WinCount[i][j][best_move] / \
                    (WinCount[i][j][best_move] + LoseCount[i][j][best_move])
            result.append((i, j, best_move, probability))

    # print the readable lines
    ind = 0
    print("PLAY = ")
    for i in result:
        if ind != i[0]:
            print()
            ind = i[0]
        print(i[2], end=" ")

    ind = 0
    print("\n\nPROB = ")
    for i in result:
        if ind != i[0]:
            print()
            ind = i[0]
        print(f"{i[3]:.4f}", end=" ")


# summarizing function
def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    LoseCount = [[[0] * (NDice + 1) for _ in range(LTarget)]
                 for _ in range(LTarget)]
    WinCount = [[[0] * (NDice + 1) for _ in range(LTarget)]
                for _ in range(LTarget)]

    # print(len(WinCount), len(WinCount[0]), len(WinCount[0][0]))
    # to play NGames times
    for _ in range(NGames):
        PlayGame(NDice, NSides, LTarget, UTarget, LoseCount,
                 WinCount, M)

    extractAnswer(WinCount, LoseCount)


if __name__ == "__main__":
    # random.seed(2)
    # prog3(3, 2, 6, 7, 100000, 100)
    # prog3(2, 3, 6, 7, 100000, 100)
    # prog3(2, 2, 4, 5, 100000, 100)
    NDice, NSides, LTarget, UTarget, NGames, M = read_input()
    prog3(NDice, NSides, LTarget, UTarget, NGames, M)
