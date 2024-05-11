import sys
import random


# function for the first line of txt file
def read_input():
    target_value, budget, output_type, restarts = sys.stdin.readline().strip().split()
    target_value, budget, restarts = int(
        target_value), int(budget), int(restarts)
    return target_value, budget, output_type, restarts


# function for storing info of each item
def read_objects():
    objects = []
    for line in sys.stdin:
        name, value, cost = line.strip().split()
        objects.append((name, int(value), int(cost)))
    return objects


# defining hill climbing
def hill_climbing(target_value, budget, restarts, objects, output_type):
    # create a random state for start
    def random_start():
        state = []
        for item in objects:
            if random.random() >= 0.5:
                state.append(item[0])
        return state

    # calculate value cost and error
    def evaluate(state):
        value = sum(objects[i][1] for i in range(
            len(objects)) if objects[i][0] in state)
        cost = sum(objects[i][2]
                   for i in range(len(objects)) if objects[i][0] in state)
        error = max(target_value - value, 0) + max(cost - budget, 0)
        return value, cost, error

    # do the hill climbing
    def hill_climb(state):
        current_value, current_cost, current_error = evaluate(state)
        best_error, best_state = current_error, state[:]
        # loop over all the neighbors
        for item in objects:
            cur_state = state[:]
            # delete if exists or add if not in the state
            if item[0] in cur_state:
                cur_state.remove(item[0])
            else:
                cur_state.append(item[0])
            neighbor_value, neighbor_cost, neighbor_error = evaluate(cur_state)

            # check output type
            if output_type == "V":
                cur_state.sort()
                print(
                    f"{cur_state}. Value = {neighbor_value}. Cost = {neighbor_cost}. Error = {neighbor_error}.")

            # move to better state
            if neighbor_error < current_error:
                current_error, best_state = neighbor_error, cur_state[:]

        # do hill climbing on new state if needed
        if current_error < best_error:
            value, cost, error = evaluate(best_state)
            if output_type == "V":
                best_state.sort()
                print(
                    f"\nMove to {best_state}.  Value = {value}. Cost = {cost}. Error = {error}.\nNeignbors:")
            best_state = hill_climb(best_state)

        return best_state

    # states = [['V'], ['U', 'V', 'W', 'X', 'Y']]
    # do random start n times as specified
    for i in range(restarts):
        state = random_start()
        # state = states[i]
        value, cost, error = evaluate(state)
        if output_type == "V":
            state.sort()
            print(
                f"Randomly chosen starting state:\n{state}. Value = {value}. Cost = {cost}. Error = {error}.\nNeignbors:")
        solution = hill_climb(state)
        # check if this time has solution
        if solution:
            value, cost, error = evaluate(solution)
            if value >= target_value and cost <= budget:
                break
            if output_type == "V":
                print("Search failed\n")

    if solution:
        value, cost, error = evaluate(solution)
        if value >= target_value and cost <= budget:
            return solution, value, cost
        else:
            return ["No Solution", 0, 0]
    else:
        return ["No Solution", 0, 0]


if __name__ == "__main__":
    target_value, budget, output_type, restarts = read_input()
    objects = read_objects()
    solution, value, cost = hill_climbing(target_value, budget,
                                          restarts, objects, output_type)
    if solution == "No Solution":
        print(solution)
    else:
        solution.sort()
        print(
            f"\nFound solution:\n{solution}. Value = {value}. Cost = {cost}. ")
