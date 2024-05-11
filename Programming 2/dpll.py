import copy
import sys


# function for reading the clauses
def read_input():
    objects = []
    for line in sys.stdin:
        clause = line.strip().split()
        if clause[0] == "0":
            break
        clause = [int(i) for i in clause]
        objects.append(clause)
    return objects


# function for storing info of index2name
def read_names():
    objects = {}
    for line in sys.stdin:
        value, name = line.strip().split()
        objects[int(value)] = name
    return objects


# dpll algorithm
def dpll(CS, B):
    # solve the easy cases
    # the skeletons
    while True:
        flg, ind = easyCaseIn(CS, B, 1)
        if flg:
            # print('easy', CS[ind])
            CS, B = easyCase(CS, B, ind)
        else:
            break

    # set found pure literal as unbound atom so no need for while loop as in next iteration this step will be repeated
    if_choose = True
    flg, ind = easyCaseIn(CS, B, 2)
    if flg:
        P = ind
        if_choose = False
        # print("easy pure", ind)

    # check for failed cases
    if not CS:
        return B
    if [] in CS:
        return "Fail"

    # choose the unbound atom if no pure literal
    if if_choose:
        P = chooseUnboundAtom(B)
        # print('normal', P, CS)
    if P:
        # try P as True
        CSCopy = copy.deepcopy(CS)
        BCopy = copy.deepcopy(B)
        CSCopy, BCopy = propagate(CSCopy, BCopy, P, True)
        answer = dpll(CSCopy, BCopy)
        if answer != 'Fail':
            return answer

        # try P as False
        CSCopy = copy.deepcopy(CS)
        BCopy = copy.deepcopy(B)
        CSCopy, BCopy = propagate(CSCopy, BCopy, P, False)
        answer = dpll(CSCopy, BCopy)
        return answer


# function for detecting easy case
def easyCaseIn(CS, B, n):
    # skeleton
    if n == 1:
        for i in range(len(CS)):
            clause = CS[i]
            if len(clause) == 1:
                atom = abs(clause[0])
                if B[atom] is None:
                    return True, i

    # pure literal
    if n == 2:
        pure_literal = {}
        for i in range(len(CS)):
            clause = CS[i]
            for i in clause:
                ind = abs(i)
                pure_literal[ind] = pure_literal.get(
                    ind, ind == i) == (ind == i)

        for i in pure_literal.keys():
            if pure_literal[i] == True:
                # print(pure_literal, i)
                return True, i

    return False, -1


# function for solving easy case
def easyCase(CS, B, ind):
    clause = CS[ind][0]
    atom = abs(clause)
    truth_value = clause > 0
    B[atom] = truth_value
    CS.remove([clause])
    for c in CS.copy():
        if -clause in c:
            c.remove(-clause)

        if clause in c:
            CS.remove(c)
    return CS, B


# function to choose unbound atom
def chooseUnboundAtom(B):
    unbound_atoms = [atom for atom in B.keys() if B[atom] is None]
    if len(unbound_atoms) > 0:
        return unbound_atoms[0]
    else:
        return None


# function to set unbound atom to T or F
def propagate(CS, B, P, value):
    B[P] = value
    for clause in CS.copy():
        if P in clause:
            if value:
                CS.remove(clause)
            else:
                clause.remove(P)
        elif -P in clause:
            if value:
                clause.remove(-P)
            else:
                CS.remove(clause)
    return CS, B


if __name__ == '__main__':
    # prepare output file
    file = open("backend-input.txt", "w")
    # Example usage:
    # CS = [[1, 2, 3, 4], [-2, 3], [-3]]
    # CS = [[1, 2, 3], [1, -2, -3], [1, -4], [-2, -3, -4],
    #       [-1, -2, 3], [5, 6], [5, -6], [2, -5], [-3, -5]]
    # read inputs and prepare lists for storage
    CS = read_input()
    NL = read_names()
    B = {}
    for i in NL.keys():
        B[i] = None

    # run dpll
    result = dpll(CS, B)

    # write into output file
    if result is None or result == 'Fail':
        file.write("Failed\n0\n")
        print('failed')
    else:
        for atom in sorted(result):
            flg = 'F\n' if result[atom] == False else 'T\n'
            file.write(f"{atom} {flg}")
        file.write("0\n")

    for i in NL.keys():
        file.write(f"{i} {NL[i]}\n")

    file.close()

# python dpll.py < dpll-input.txt
