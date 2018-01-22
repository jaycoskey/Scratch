#!/usr/bin/env python
# Derived from the code at http://code.activestate.com/recipes/577777-backtracking-template-method/ 

from collections import Counter
from enum import Enum


class Direction(Enum):
    Fwd = 1
    Back = -1


def backtracking_search(is_valid, slots, choices):
    """
    Returns a stream of key-value pairs of the form s:c, where each key is a slot, and each value is a choice 
    :param Func is_valid: A function that returns whether a choice is valid for a given slot, given previous choices.
               def is_valid(slot, choice, solution):
          solution is a dict that holds the previous assignments of choices to slots.
              dict = {s0:c0, s1:c1, ...}, where each si is a slot and each ci is a choice.
              For this dict: type(key) == type(slot) and type(value) == type(choice).
    :param List[int] slots: Each slot is a holder for a choice.
    :param List[int] choices: Each choice is held in a slot.
    """
    soln = {}  # Keys are slots and and values are choices.

    num_slots = len(slots)
    num_choices = len(choices)
    last_slot = num_slots - 1
    last_choice = num_choices - 1

    choice = 0
    dirn = Direction.Fwd
    is_done = False
    slot = 0

    while not is_done:
        ####################
        # Search forward
        ####################
        # print('INFO: Forward section: Slot={}; direction={}'.format(slot, dirn))
        while dirn == Direction.Fwd:
            if is_valid(soln, slot, choice):
                soln[slot] = choice
                if slot == last_slot:
                    yield {slots[k]:choices[v] for k,v in soln.items()}
                    del soln[slot]             # Next soln
                    if choice != last_choice:
                        choice += 1            # Next choice
                    else:
                        dirn = Direction.Back  # Backtrack to earlier slots
                else:
                    slot += 1                  # Next slot
                    choice = 0
            elif choice != last_choice:
                choice += 1                    # Next candidate
            else:
                dirn = Direction.Back          # Last choice is invalid => backtracking mode

        ####################
        # Backtrack
        ####################
        is_done = (slot == 0)
        # print('INFO: Backtracking section: Slot={}; direction={}'.format(slot, dirn))
        while dirn == Direction.Back and not is_done:
            slot -= 1
            choice = soln.pop(slot)
            if choice != last_choice:
                choice += 1
                dirn = Direction.Fwd
            elif slot == 0:
                is_done = True


def problem_eight_queens():
    rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def is_valid_8queens(soln, row, col) -> bool:
        for r, c in soln.items():
            if c == col:
                return False
            elif r - c == row - col:
                return False
            elif r + c == row + col:
                return False
        return True 
    
    for soln in backtracking_search(is_valid_8queens, rows, cols):
        print(soln)


def problem_four_color():
    neighbors = [set(), set(),set(),set(),set()]
    borders = [ (0, 1), (0, 2)
              , (1, 0), (1, 2), (1, 3)
              , (2, 0), (2, 1), (2, 4)
              , (3, 1), (3, 4)
              , (4, 2), (4,3)
              ]
    for b in borders:
        neighbors[b[0]].add(b[1])

    nations = ['Italy','Spain','France','Germany','England']
    colors = ['Red','Green','Blue','Black']
 
    def is_valid_4colors(soln, nation, color) -> bool:
        """
        A color is valid for a given nation if no neighboring country shares the same color.
        """
        same_color = set([n for n, c in soln.items() if c == color])
        return neighbors[nation].isdisjoint(same_color)
 
    for soln in backtracking_search(is_valid_4colors, nations, colors):
        print(soln)


# TODO: Modify to account for each day's schedule requiring multiple choices
#       from the list of pairs, instead of just one.
# 
# def problem_schedule_pairs():
#     def is_valid_schedule(soln, day, pairs) -> bool:
#         '''Require two things for a solution to be valid:
#              (a) for each date, no name is double-booked;
#              (b) no pair is added to a schedule for an (n+1)st time
#                  until all pairs have been added n times.
#         '''
#         scheduled_pairs = set()
#         test_soln = soln.copy()
#         test_soln[day] = pairs
#         for d in test_soln.keys():
#             print('===>>> test_soln[{}]={}'.format(d, test_soln[d]))
#             is_duplication = max(Counter(test_soln[d])) > 1
#             if is_duplication:
#                 return False
#             scheduled_pairs.extend(test_soln[d])
#             if len(scheduled_pairs) == len(pairs):
#                 scheduled_pairs.clear()
#         return True 
#     
#     dates = ['1','2','3','4','5','6','7','8','9','10','11','12']
#     names = ['A', 'B', 'C', 'D', 'E', 'F']
#     pairs = [(names[k1], names[k0])
#                 for k0 in range(len(names))
#                 for k1 in range(k0)
#             ]
# 
#     for soln in backtracking_search(is_valid_schedule, dates, pairs):
#         print(soln)


if __name__=='__main__':
    problem_eight_queens()
    problem_four_color()

