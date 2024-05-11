import copy
import pdb


def propagate(CS, B, A, V):
    # print(f"Propagate called with A={A}, V={V}, B={B}")
    B[abs(A)] = V
    new_CS = []
    for clause in CS:
        if V > 0:
            if A in clause:
                continue
            if -A in clause:
                new_clause = []
                for atom in clause:
                    if atom != -A:
                        new_clause.append(atom)
                new_CS.append(new_clause)
            else:
                new_CS.append(clause)
        else:
            if -A in clause:
                continue
            if A in clause:
                new_clause = []
                for atom in clause:
                    if atom != A:
                        new_clause.append(atom)
                new_CS.append(new_clause)
            else:
                new_CS.append(clause)
    return new_CS, B


def easy_cases_helper(CS, B):
    # print("Checking for easy cases...")

    helper_dict = {}  # structure: {atom: [positive_count, negative_count]}
    for clause in CS:
        # if there is a singleton clause
        if len(clause) == 1:
            # print(f"Singleton clause {clause} found")
            if clause[0] > 0:
                return True, propagate(CS, B, abs(clause[0]), 1)
            else:
                return True, propagate(CS, B, abs(clause[0]), -1)

        # check for pure literals
        for atom in clause:
            if abs(atom) in helper_dict:
                if atom > 0:
                    helper_dict[abs(atom)][0] += 1
                else:
                    helper_dict[abs(atom)][1] += 1
            else:
                if atom > 0:
                    helper_dict[abs(atom)] = [1, 0]
                else:
                    helper_dict[abs(atom)] = [0, 1]
    # pdb.set_trace()
    for atom in helper_dict:
        if helper_dict[atom][0] == 0 or helper_dict[atom][1] == 0:
            # print(f"Pure literal {atom} found")
            if helper_dict[atom][0] > 0:
                return True, propagate(CS, B, abs(atom), 1)
            else:
                return True, propagate(CS, B, abs(atom), -1)
    # print("No easy cases found")
    return False, [CS, B]


def choose_atom(CS, B):
    for clause in CS:
        for atom in clause:
            if B.get(abs(atom)) == None:
                return abs(atom)
    return None


def dpll(CS, B):

    while True:
        # print(f"CS: {CS}\n B: {B}")
        # pdb.set_trace()
        if len(CS) == 0:
            # print("Empty set found")
            return B
        if [] in CS:
            # print("Found an empty clause. Failing...")
            return False

        # deal with easy cases
        is_easy, CS_B_list = easy_cases_helper(CS, B)
        CS, B = CS_B_list[0], CS_B_list[1]
        if not is_easy:
            break

    # print(f"CS: {CS}\n B: {B}")
    # pdb.set_trace()

    # deep copy CS and B
    CS_copy = copy.deepcopy(CS)
    B_copy = copy.deepcopy(B)

    # choose a literal
    # literal = choose_atom(CS, B)
    literal = CS[0][0]
    if literal == None:
        # print("No unbound atoms found")
        return B
    # print("=====================================")
    # print(f"Choosing atom {literal}")

    CS_copy, B_copy = propagate(CS_copy, B_copy, abs(literal), 1)
    # print(f"Propagating {abs(literal)} to True")
    # print("=====================================")

    result = dpll(CS_copy, B_copy)
    # print(f"Result for True branch of literal {literal}: {result}")

    if result != False:
        return result
    else:
        # deep copy CS and B
        CS_copy = copy.deepcopy(CS)
        B_copy = copy.deepcopy(B)

        # print("=====================================")
        # print(f"Trying literal {abs(literal)} for the other branch")

        CS_copy, B_copy = propagate(CS_copy, B_copy, abs(literal), -1)
        # print(f"Propagating {abs(literal)} to False")
        # print("=====================================")
        # print(f"Result for False branch of literal {literal}: {result}")
        return dpll(CS_copy, B_copy)


if __name__ == "__main__":
    clause_list = []
    bindings = {}

    # parse the output from the front end
    with open("dpll-input.txt", "r") as f:
        lines = f.readlines()
        for index in range(len(lines)):
            line = lines[index].strip()
            if line == "0":
                info = lines[index+1:]
                break
            clause_list.append(line.split())

    # convert the clause list to integers
    for clause in clause_list:
        for index in range(len(clause)):
            clause[index] = int(clause[index])
    # print(f"Clause list: {clause_list}")

    output_file = open("dpll_output.txt", "w")

    number_of_atoms = len(info)
    # print(f"Number of atoms: {number_of_atoms}")

    # apply dpll
    result = dpll(clause_list, bindings)
    if result:
        for atom in range(1, number_of_atoms+1):
            if atom in result:
                if result[atom] > 0:
                    output_file.write(f"{atom} T\n")
                else:
                    output_file.write(f"{atom} F\n")
            else:
                # if the atom can be either true or false, we choose true
                output_file.write(f"{atom} T\n")
    else:
        output_file.write("No solution\n")

    output_file.write("0\n")
    for line in info:
        output_file.write(line)
    output_file.close()

    # check the output
    with open("dpll-input.txt", "r") as f:
        lines = f.readlines()
        for index in range(len(lines)):
            line = lines[index].strip()
            if line == "0":
                info = lines[index+1:]
                break
            clause_list.append(line.split())

    # convert the clause list to integers
    for clause in clause_list:
        for index in range(len(clause)):
            clause[index] = int(clause[index])

    # check the output
    for clause in clause_list:
        # calculate the truth value of the clause
        clause_value = False
        for atom in clause:
            # only need one to be true
            if result:
                if atom * result[abs(atom)] > 0:
                    clause_value = True
                    break
        if not clause_value:
            print(f"The clause {clause} is not satisfied")
    print("Check complete")
    for atom in result:
        if result[atom] > 0:
            print(f"Atom: {atom}, T")
        else:
            print(f"Atom: {atom}, F")
