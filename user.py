#!/usr/bin/env python3


def get_input(grid, clues, active_index):
    JUST = len(" Mark active cell as filled-in or empty") + 1
    print(" Make a step".ljust(JUST), ": w/a/s/d")
    print(" Make 2 steps".ljust(JUST), ": ww/aa/ss/dd (example: 'ww' - 2 steps up)")
    print(" Mark active cell as filled-in or empty".ljust(JUST), ": f/e")
    print(" Clear active cell".ljust(JUST), ": c")
    print(" Undo previous step".ljust(JUST), ": u\n")
    print(" Verify current solution".ljust(JUST), ": v\n")
    return input(" Your input: ")


def is_step(user_input):
    step_keys = ["w", "a", "s", "d"]
    if user_input in step_keys or user_input in [x * 2 for x in step_keys]:
        return True
    else:
        return False


def is_mark(user_input):
    mark_keys = ["f", "e", "c"]
    if user_input in mark_keys:
        return True
    else:
        return False


def is_undo(user_input):
    if user_input == "u":
        return True
    else:
        return False


def is_verification(user_input):
    if user_input == "v":
        return True
    else:
        return False
