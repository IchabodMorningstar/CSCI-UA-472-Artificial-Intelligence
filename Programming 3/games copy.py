import random
import sys
import numpy as np


# function for the first line of txt file
def read_input():
    NDice, NSides, LTarget, UTarget, NGames, M = sys.stdin.readline().strip().split()
    NDice, NSides, LTarget, UTarget, NGames, M = int(
        NDice), int(NSides), int(LTarget), int(UTarget), int(NGames), int(M)
    return NDice, NSides, LTarget, UTarget, NGames, M


# choose number by randomly selecting from given distribution
def chooseFromDist(p):
    # values = list(range(1, len(p) + 1))
    # return random.choices(values, weights=p, k=1)[0]
    arr = [i for i in range(1, len(p)+1)]
    choice = random.choices(arr, p, k=1)
    return choice[0]


# find the total of dice
def rollDice(NDice, NSides):
    # total = 0
    # for roll_trial in range(NDice):
    #     roll = random.randint(1, NSides)
    #     total += roll
    # return total
    return sum(random.randint(1, NSides) for _ in range(NDice))


# choose dice with probability
def chooseDice(X, Y, LoseCount, WinCount, NDice, M):
    K = NDice
    # X, Y = Score
    f_values = [0] * K

    # calculate the distribution of numbers of dice
    for k in range(1, K + 1):
        if WinCount[k][X][Y] + LoseCount[k][X][Y] == 0:
            f_values[k-1] = 0.5
        else:
            f_values[k-1] = WinCount[k][X][Y] / \
                (WinCount[k][X][Y] + LoseCount[k][X][Y])

    # find the needed values
    k_hat = f_values.index(max(f_values))  # Find k with highest f-value
    best_f_k = f_values[k_hat]
    s = sum(f_values) - best_f_k
    T = sum(WinCount[k][X][Y] + LoseCount[k][X][Y] for k in range(1, K + 1))

    pk_hat = (T * best_f_k + M) / (T * best_f_k + K * M)
    deno = (s * T + (K - 1) * M)
    # prob = [(1 - pk_hat) * (T * f_values[k-1] + M) /
    #         deno for k in range(1, K + 1)]
    p_k = [0] * K
    for k in range(1, NDice + 1):
        f_k = f_values[k-1]
        if k-1 == k_hat:
            p_k[k-1] = pk_hat
        else:
            p_k[k-1] = (1 - pk_hat) * (T * f_k + M) / deno

    # prob[k_hat-1] = pk_hat

    # choose dice from given distribution
    chosen = chooseFromDist(p_k)
    # chosen = chooseFromDist(prob)

    return chosen


DEBUG = False


# def chooseDice(X, Y, LoseCount, WinCount, NDice, M) -> int:

#     WinCount = np.array(WinCount)
#     LoseCount = np.array(LoseCount)
#     # return the number of dice to roll

#     # selected_total and selected_WinCount are the accounts of the number of dice to roll at state <X,Y>
#     selected_total = LoseCount[:, X, Y] + WinCount[:, X, Y]
#     selected_WinCount = WinCount[:, X, Y]

#     # initialize f_ks of the length of the dice: f_ks[0] refers to the probability of choosing 1 dice
#     f_ks = np.zeros(NDice)
#     for k in range(1, NDice + 1):
#         # if the denominator is 0, set f_k to 0.5
#         if selected_total[k] == 0:
#             f_ks[k-1] = 0.5
#         else:
#             f_ks[k-1] = selected_WinCount[k] / selected_total[k]

#     # get k^ and its index
#     best_k_index = np.argmax(f_ks)
#     best_f_k = f_ks[best_k_index]

#     # calculate s and T
#     s = np.sum(f_ks) - f_ks[best_k_index]
#     T = sum(selected_total)

#     # calculate p_k^ according to the formula
#     best_p_k = (T*best_f_k + M) / (T*best_f_k + NDice*M)

#     # calculate p_k according to the formula
#     p_k = np.empty_like(f_ks)
#     for k in range(1, NDice + 1):
#         f_k = f_ks[k-1]
#         if k-1 == best_k_index:
#             p_k[k-1] = best_p_k
#         else:
#             p_k[k-1] = (1 - best_p_k) * (T * f_k + M) / (T * s + (NDice-1) * M)

#     # give the distribution to chooseFromDist and get the number of dice to roll
#     number_of_dice = chooseFromDist(list(p_k))

#     if DEBUG:
#         print(
#             f"choosing {number_of_dice} dices with probability {p_k[number_of_dice-1]}")
#     return number_of_dice


# a helper to update matrices
def update_matrices(player_scores, player_idx, WinCount, LoseCount, k, rsl):
    X, Y = player_scores[player_idx], player_scores[player_idx ^ 1]
    if rsl[player_idx]:
        WinCount[X][Y][k] += 1
        # print(f"{X}, {Y}, {k} wins {WinCount[X][Y][k]}")
    else:
        LoseCount[X][Y][k] += 1
        # print(f"{X}, {Y}, {k} loses {LoseCount[X][Y][k]}")


# play the game by recursion
def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M, player_scores, player_idx):
    # initialize the status
    x, y = player_scores[player_idx], player_scores[player_idx ^ 1]
    # print(player_idx, "plays at", x, y)

    k = chooseDice(x, y, LoseCount, WinCount, NDice, M)
    # print('k', k)
    roll_total = rollDice(k, NSides)

    x += roll_total
    # print("player", player_idx, "has", roll_total,
    #       "from", k, 'dice', "in total", x)

    # check current status
    # x wins
    if LTarget <= x <= UTarget:
        # print(player_idx, "wins")
        rsl = {player_idx: True, player_idx ^ 1: False}
        update_matrices(player_scores, player_idx, WinCount, LoseCount, k, rsl)
        return rsl
    # x loses
    elif x > UTarget:
        # print(player_idx, "loses")
        rsl = {player_idx: False, player_idx ^ 1: True}
        update_matrices(player_scores, player_idx, WinCount, LoseCount, k, rsl)
        return rsl
    # game goes on
    else:
        player_scores[player_idx] += roll_total

        rsl = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount,
                       WinCount, M, player_scores, player_idx ^ 1)

        player_scores[player_idx] -= roll_total

        update_matrices(player_scores, player_idx, WinCount, LoseCount, k, rsl)

        return rsl

# def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M, hh, jj):

#     # initialize the scores to be 0
#     A_score, B_score = 0, 0

#     # used to record the step of each player
#     A_record, B_record = [], []

#     # a flah to indicate whose turn it is
#     is_A_turn = True

#     # loop until one of the player wins
#     while A_score < LTarget and B_score < LTarget:

#         # if it is A's turn
#         if is_A_turn:

#             # decide the number of dice to roll
#             number_of_dice = chooseDice(
#                 A_score, B_score, LoseCount, WinCount, NDice, M)

#             # record the step
#             A_record.append([A_score, B_score, number_of_dice])

#             # roll the dice
#             A_roll = rollDice(number_of_dice, NSides)

#             # update the score and flag
#             A_score += A_roll
#             is_A_turn = False

#         # if it is B's turn
#         else:

#             # decide the number of dice to roll
#             number_of_dice = chooseDice(
#                 B_score, A_score, LoseCount, WinCount, NDice, M)

#             # record the step
#             B_record.append([B_score, A_score, number_of_dice])

#             # roll the dice
#             B_roll = rollDice(number_of_dice, NSides)

#             # update the score and flag
#             B_score += B_roll
#             is_A_turn = True

#     # when one player wins, update WinCount and LoseCount
#     if (A_score >= LTarget and A_score <= UTarget) or B_score > UTarget:

#         # if A wins
#         for record in A_record:
#             # update WinCount with A's record
#             A_score, B_score, number_of_dice = record[0], record[1], record[2]
#             WinCount[number_of_dice][A_score][B_score] += 1

#         for record in B_record:
#             # update LoseCount with B's record
#             B_score, A_score, number_of_dice = record[0], record[1], record[2]
#             LoseCount[number_of_dice][B_score][A_score] += 1
#     else:
#         # if B wins

#         for record in B_record:
#             # update WinCount with B's record
#             B_score, A_score, number_of_dice = record[0], record[1], record[2]
#             WinCount[number_of_dice][B_score][A_score] += 1

#         for record in A_record:
#             # update LoseCount with A's record
#             A_score, B_score, number_of_dice = record[0], record[1], record[2]
#             LoseCount[number_of_dice][A_score][B_score] += 1
#             # print(WinCount, LoseCount)
#     return LoseCount, WinCount


# # explain the result
# def extractAnswer(WinCount, LoseCount):
#     import numpy as np
#     print(np.array(WinCount))
#     print(np.array(LoseCount))
#     # interpret the count matrices into decision and prob
#     result = []
#     for i in range(len(WinCount)):
#         for j in range(len(WinCount[i])):
#             best_ratio = 0
#             best_move = 0
#             for k in range(1, len(WinCount[i][j])):
#                 deno = (WinCount[i][j][k] + LoseCount[i][j][k])
#                 if deno == 0:
#                     ratio = 0
#                 else:
#                     ratio = WinCount[i][j][k] / deno

#                 if ratio > best_ratio:
#                     best_ratio = ratio
#                     best_move = k

#             if WinCount[i][j][best_move] + LoseCount[i][j][best_move] == 0:
#                 probability = 0
#             else:
#                 probability = WinCount[i][j][best_move] / \
#                     (WinCount[i][j][best_move] + LoseCount[i][j][best_move])
#             result.append((i, j, best_move, probability))

#     # print the readable lines
#     ind = 0
#     print("PLAY = ")
#     for i in result:
#         if ind != i[0]:
#             print()
#             ind = i[0]
#         print(i[2], end=" ")

#     ind = 0
#     print("\n\nPROB = ")
#     for i in result:
#         if ind != i[0]:
#             print()
#             ind = i[0]
#         print(f"{i[3]:.4f}", end=" ")

def extractAnswer(WinCount, LoseCount):
    WinCount = np.array(WinCount)
    LoseCount = np.array(LoseCount)

    # print(WinCount)
    # print(LoseCount)

    # get the number of dice that has highest wincount each state
    best_k_indices = np.argmax(WinCount, axis=0)

    # get the wincount and total count for these best ks
    total = WinCount + LoseCount
    x_indices, y_indices = np.indices(best_k_indices.shape)
    selected_WinCount = WinCount[best_k_indices, x_indices, y_indices]
    selected_total = total[best_k_indices, x_indices, y_indices]

    # calculate the probability
    probs = np.where(selected_total > 0, selected_WinCount / selected_total, 0)
    print(probs)
    print(best_k_indices)


# summarizing function
def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    # LoseCount = [[[0] * (LTarget) for _ in range(LTarget)]
    #              for _ in range(NDice + 1)]
    # WinCount = [[[0] * (LTarget) for _ in range(LTarget)]
    #             for _ in range(NDice + 1)]

    LoseCount = np.zeros((NDice + 1, LTarget, LTarget))
    WinCount = np.zeros((NDice + 1, LTarget, LTarget))

    # to play NGames times
    for _ in range(NGames):
        playerscore = [0, 0]
        player_id = 0
        LoseCount, WinCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount,
                                       WinCount, M, playerscore, player_id)

    extractAnswer(WinCount, LoseCount)


# def prog3_1(NDice, NSides, LTarget, UTarget, NGames, M):

#     # Initialize WinCount and LoseCount
#     LoseCount = np.zeros((NDice + 1, LTarget, LTarget))
#     WinCount = np.zeros((NDice + 1, LTarget, LTarget))

#     # run the game "NGames" times
#     for _ in range(NGames):
#         # if DEBUG:
#         #     print(f"-------------Game {game_trial + 1}-------------")
#         # update WinCount and LoseCount
#         LoseCount, WinCount = PlayGame(
#             NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M, 0, 0)

#     extractAnswer(WinCount, LoseCount)


if __name__ == "__main__":
    # NDice, NSides, LTarget, UTarget, NGames, M = read_input()
    random.seed(2)
    # prog3(3, 2, 6, 7, 100000, 100)
    # prog3_1(3, 2, 6, 7, 100000, 100)
    # prog3(3, 2, 6, 7, 100000, 100)
    # prog3(3, 2, 6, 7, 10, 5)
    prog3(2, 2, 4, 5, 100000, 100)
    # prog3_1(2, 2, 4, 5, 100000, 100)
    # prog3(NDice, NSides, LTarget, UTarget, NGames, M)
    # NDice, LTarget = 3, 10
    # LoseCount = [[[0] * (NDice + 1) for _ in range(LTarget)]
    #              for _ in range(LTarget)]
    # WinCount = [[[0] * (NDice + 1) for _ in range(LTarget)]
    #             for _ in range(LTarget)]
    # WinCount[2][3][1] = 0
    # LoseCount[2][3][1] = 2
    # WinCount[2][3][2] = 3
    # LoseCount[2][3][2] = 1
    # WinCount[2][3][3] = 1
    # LoseCount[2][3][3] = 1

    # rsl = chooseDice((2, 3), LoseCount, WinCount, NDice, 4)

    # print(rsl)
