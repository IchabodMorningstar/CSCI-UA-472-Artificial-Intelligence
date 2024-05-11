import sys


# function for the first line of txt file
def read_input():
    target_value, budget, output_type = sys.stdin.readline().strip().split()
    target_value, budget = int(target_value), int(budget)
    return target_value, budget, output_type


# function for storing info of each item
def read_objects():
    objects = []
    for line in sys.stdin:
        name, value, cost = line.strip().split()
        objects.append((name, int(value), int(cost)))
    return objects


# defining dfs
def dfs(target_value, budget, depth, current_value, current_cost, path):
    # check budget
    if current_cost > budget:
        return [0, 0, 0]

    # check if need output
    if path and output_type == "V":
        print(f"{path}. Value = {current_value}. Cost = {current_cost}.")
    # return valid result
    if current_value >= target_value:
        return [current_value, current_cost, path]
    # terminate when reaching the depth
    if depth == len(path):
        return [0, 0, 0]

    # iterate through all the items
    for item in objects:
        if path:
            if item[0] <= path[-1]:
                continue

        best_value, best_cost, rsl_path = dfs(target_value, budget, depth, current_value +
                                              item[1], current_cost + item[2], path + [item[0]])

        # return a valid result
        if best_value:
            return [best_value, best_cost, rsl_path]

    return [0, 0, 0]


# IDS
def iterative_deepening(target_value, budget, objects, output_type):
    path = []

    # iterate through all depth possibilities
    for depth in range(1, len(objects)+1):
        if output_type == "V":
            print(f"\nDepth = {depth}.")
        best_value, best_cost, path = dfs(
            target_value, budget, depth, 0, 0, [])
        if best_value and best_cost and path:
            return best_value, best_cost, path

    return [0, 0, "No Solution"]


if __name__ == "__main__":
    # prepare data
    target_value, budget, output_type = read_input()
    objects = read_objects()
    # IDS
    best_value, best_cost, path = iterative_deepening(
        target_value, budget, objects, output_type)
    # result
    if path == "No Solution":
        print("\n", path)
    else:
        print(
            f"\nFound solution {path}. Value = {best_value}. Cost = {best_cost}.")
