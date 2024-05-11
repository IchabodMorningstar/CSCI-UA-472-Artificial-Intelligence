import sys


# function for reading truth value
def read_input():
    objects = {}
    for line in sys.stdin:
        if line.strip() == "Failed":
            return "Failed"
        data = line.strip().split()
        if data[0] == "0":
            break
        objects[int(data[0])] = data[1]
    return objects


# function to read index2name
def read_names():
    objects = {}
    for line in sys.stdin:
        value, name = line.strip().split()
        if name.startswith('Peg'):
            break
        objects[int(value)] = name
    return objects


if __name__ == '__main__':
    # prepare output file
    file = open("result.txt", "w")
    # read input file
    truth = read_input()
    if truth == "Failed":
        print("No solution")
        sys.exit()
    names = read_names()
    # print(truth, names)

    # convert truth value to human understandable form
    objects = {}
    for i in names.keys():
        if truth[i] == "T":
            if names[i][-3] == ",":
                objects[int(names[i][-2])] = names[i]
            else:
                objects[int(names[i][-3:-1])] = names[i]

    # write into output file
    for j in range(1, len(objects.keys())+1):
        print(objects[j])
        file.write(f"{objects[j]}\n")

    file.close()

# python backend.py < backend-input.txt
