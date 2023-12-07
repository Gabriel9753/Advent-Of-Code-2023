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

from enum import Enum

card_value = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "1": 1,
}

class Strength(Enum):
    FIVE = 999999999
    FOUR = 999999998
    FULL_HOUSE = 999999997
    THREE = 999999996
    TWO_PAIRS = 999999995
    # A23A4
    ONE_PAIR = 999999994
    # all distinct 23456
    HIGH_CARD = 999999993

def sort_hand(hand):
    # sort the hand based on the card value
    cards = [c for c in hand]
    cards = sorted(cards, key=lambda x: card_value[x], reverse=True)
    return "".join(cards)

def get_normal_hand_value(hand):
    _value = 0
    for i, c in zip(range(len(hand), 0, -1), hand):
        _value += card_value[c] * 10 ** i
    return _value

def rank_hand(hand):
    # return a rank based on the hand
    cards = [c for c in hand]
    cards = sorted(cards, key=lambda x: card_value[x], reverse=True)
    # check for FIVE
    if len(set(cards)) == 1:
        return Strength.FIVE.value
    # check for FOUR (4 of a kind in cards)
    if len(set(cards[:4])) == 1 or len(set(cards[1:])) == 1:
        return Strength.FOUR.value
    # check for FULL_HOUSE
    if len(set(cards[:3])) == 1 and len(set(cards[3:])) == 1:
        return Strength.FULL_HOUSE.value
    if len(set(cards[:2])) == 1 and len(set(cards[2:])) == 1:
        return Strength.FULL_HOUSE.value
    # check for THREE
    if len(set(cards[:3])) == 1 or len(set(cards[1:4])) == 1 or len(set(cards[2:])) == 1:
        return Strength.THREE.value
    # check for TWO_PAIRS
    if len(set(cards)) == 3:
        return Strength.TWO_PAIRS.value
    # check for ONE_PAIR
    if len(set(cards)) == 4:
        return Strength.ONE_PAIR.value
    if len(set(cards)) == 5:
        return Strength.HIGH_CARD.value
    return 0


@timer(return_time=True)
def task1(day_input):
    day_input = day_input.splitlines()
    hands = [line.split() for line in day_input]
    hands = [[sort_hand(hand[0]), int(hand[1]), rank_hand(hand[0])] for hand in hands]
    hands = sorted(hands, key=lambda x: x[2], reverse=True)
    # if the rank is the same, then compare the value of the hand with get_normal_hand_value function
    ranked_hands = defaultdict(list)
    for hand in hands:
        ranked_hands[hand[2]].append(hand)
    for key, value in ranked_hands.items():
        ranked_hands[key] = sorted(value, key=lambda x: get_normal_hand_value(x[0]), reverse=True)
    hands = []
    for key, value in ranked_hands.items():
        hands.extend(value)

    print(ranked_hands)
    result = 0
    for rank, hand in enumerate(hands[::-1], 1):
        # print(rank, hand)
        result += rank * hand[1]
    return result



@timer(return_time=True)
def task2(day_input):
    # Day-specific code for Task 2
    pass


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")


if __name__ == "__main__":
    main()
