import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import numpy as np
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day


@timer(return_time=True)
def task1(instructions, nodes):
    total_steps = 0
    cur, target = "AAA", "ZZZ"
    while cur != target:
        for instr in instructions:
            total_steps += 1
            cur = nodes[cur][instr]
    return total_steps


@timer(return_time=True)
def task2(instructions, nodes):
    total_steps = 0
    curs = set([s for s in nodes if s.endswith("A")])
    targets = set(t for t in nodes if t.endswith("Z"))
    solutions = []

    while targets and curs:
        for instr in instructions:
            total_steps += 1
            curs = {nodes[c][instr] for c in curs}
            for c in curs.intersection(targets):
                solutions.append(total_steps)
                curs.remove(c)
                targets.remove(c)
    return reduce(math.lcm, solutions)


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt")).splitlines()
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt")).splitlines()

    instructions = day_input[0].replace("R", "1").replace("L", "0")
    instructions = [int(i) for i in instructions]

    nodes = [l.replace("(", "").replace(")", "") for l in day_input[2:]]
    nodes = {
        node.split(" = ")[0]: [tn for tn in node.split(" = ")[1].split(", ")]
        for node in nodes
    }

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(instructions, nodes)
    result_task2, time_task2 = task2(instructions, nodes)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # Day 8
    # ------------------

    # Answers:
    # Task 1: 20513
    # Task 2: 15995167053923

    # Times:
    # Task 1: 0.000499 seconds
    # Task 2: 0.013520 seconds


if __name__ == "__main__":
    main()
