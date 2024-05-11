import sys


# function for the first line of txt file
def read_shape():
    places, empty = sys.stdin.readline().strip().split()
    places, empty = int(places), int(empty)
    return places, empty


# function for process info of every jumpable points
def read_peg():
    objects = []
    for line in sys.stdin:
        frs, sec, thr = line.strip().split()
        frs, sec, thr = int(frs), int(sec), int(thr)
        objects.append([frs, sec, thr])
        objects.append([thr, sec, frs])
    return objects


# function for generating precondition axioms
def precondition_axioms(places, objects):
    # loop over all possible jumpable combinations
    for combi in range(len(objects)):
        # loop over the maximun of time
        for time in range(places-2):
            # loop over the sencond part of A -> B V C V -D
            for elem in range(3):
                if elem < 2:
                    sign = ""
                else:
                    sign = "-"

                # mathematically find the index of the atoms
                file.write(
                    f"-{combi*(places-2)+1+time} {sign}{len(objects)*(places-2)+(objects[combi][elem]-1)*(places-1)+time+1}\n")


# funtion for generating causal axioms and similar to the above
def causal_axioms(places, objects):
    for combi in range(len(objects)):
        for time in range(places-2):
            for elem in range(3):
                if elem < 2:
                    sign = "-"
                else:
                    sign = ""

                file.write(
                    f"-{combi*(places-2)+1+time} {sign}{len(objects)*(places-2)+(objects[combi][elem]-1)*(places-1)+time+1+1}\n")


# function for generating frame axioms
def frame_axioms(places, objects):
    # condition A
    # loop over all possible places
    for peg in range(places):
        # loop over the maximun of time
        for time in range(places-2):
            file.write(
                f"-{len(objects)*(places-2)+peg*(places-1)+time+1} {len(objects)*(places-2)+peg*(places-1)+time+1+1} ")
            for combi in range(len(objects)):
                if objects[combi][0] == peg+1 or objects[combi][1] == peg+1:
                    file.write(f"{combi*(places-2)+1+time} ")
            file.write("\n")

    # condition B
    for peg in range(places):
        for time in range(places-2):
            file.write(
                f"{len(objects)*(places-2)+peg*(places-1)+time+1} -{len(objects)*(places-2)+peg*(places-1)+time+1+1} ")
            for combi in range(len(objects)):
                if objects[combi][2] == peg+1:
                    file.write(f"{combi*(places-2)+1+time} ")
            file.write('\n')


# function for one action
def one_action(places, objects):
    # loop over the maximun of time
    for time in range(places-2):
        # generate the combinations of all possible conflicting actions
        for i in range(len(objects)):
            for j in range(i+1, len(objects)):
                file.write(f"-{i*(places-2)+1+time} -{j*(places-2)+1+time}\n")


# function for start state
def start_state(places, empty, objects):
    for peg in range(places):
        # add the sign to the only empty peg
        if peg == empty-1:
            sign = "-"
        else:
            sign = ""

        file.write(
            f"{sign}{len(objects)*(places-2)+peg*(places-1)+1} ")
        file.write('\n')


# function for end state
def end_state(places, objects):
    rsl = []
    # to find all end state atoms
    for peg in range(places):
        ind = len(objects)*(places-2)+peg*(places-1)+places-1
        rsl.append(ind)
        file.write(
            f"{ind} ")
    file.write('\n')

    # generate the combinations of all possible conflicting places
    for i in range(len(rsl)):
        for j in range(i+1, len(rsl)):
            file.write(f"-{rsl[i]} -{rsl[j]}\n")


if __name__ == '__main__':
    # prepare output file
    file = open("dpll-input.txt", "w")
    # read the inputs
    places, empty = read_shape()
    jumps = read_peg()
    # generate all clauses
    precondition_axioms(places, jumps)
    causal_axioms(places, jumps)
    frame_axioms(places, jumps)
    one_action(places, jumps)
    start_state(places, empty, jumps)
    end_state(places, jumps)
    file.write("0\n")

    # write all index and atoms
    ind = 1
    # for jump()
    for combi in jumps:
        for time in range(places-2):
            file.write(
                f"{ind} Jump({combi[0]},{combi[1]},{combi[2]},{time+1})\n")
            ind += 1

    # for peg()
    for peg in range(places):
        for time in range(places-1):
            file.write(f"{ind} Peg({peg+1},{time+1})\n")
            ind += 1

    file.close()

# python frontend.py < front-input.txt
