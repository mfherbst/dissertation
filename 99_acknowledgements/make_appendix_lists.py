#!/usr/bin/env python3

import random


SCIENCE_DEBATES = [
    "Prof.~Eric~Cancès",
    "Prof.~Reinhold~Schneider",
    "Dr.~Denis~Davydov",
    "Dr.~Katharina~Kormann",
    #
    "Adrian Dempwolff",
    "Dr.~Tim~Stauch",
    "Manuel~Hodecker",
    "Maximilian~Scheurer",
    "Dr.~Tobias~Setzer",
    #
    "Dr.~Klaus~Birkelund",
    "Dr.~Mads~Kristensen",
    #
    "Henrik~Larsson",
    "Dr.~Jenny~Wagner",
    "Lucas~Fabian~Hackl",
    "Jan~Janßen",
    "Jan~Christoph~Peters",
    "Fabian~Klein",
]

CHAOS_PEOPLE = [
    "cherti",
    "hauro",
    "janx2",
    "kungi",
    "rami",
    "supaake",
]

PROOF_READERS = [
    "Henrik~Larsson",
    "Fabian~Faulstich",
    "Maximilian~Scheurer",
    "Dr.~Jenny~Wagner",
    "Adrian~Dempwolff",
    "Manuel~Hodecker",
    "Marvin~Hoffmann",
    "Dr.~James~Avery",
    # "Reena~Sen"
    # "Mikael~Scott"
    # "Dr.~Jim~Dengler"
    # "Carine~Dengler"
]


def random_store(names, path, add_and=True):
    random.shuffle(names)
    last = names[-1]
    names = names[:-1]

    last_but_one = " and\n"
    if not add_and:
        last_but_one = ",\n"

    with open(path, "w") as f:
        f.write(",\n".join(names))
        f.write(last_but_one)
        f.write(last)


def main():
    random_store(SCIENCE_DEBATES, "list_science_debates.tex", add_and=False)
    random_store(CHAOS_PEOPLE, "list_chaos.tex", add_and=False)
    random_store(PROOF_READERS, "list_proof.tex")


if __name__ == "__main__":
    main()
