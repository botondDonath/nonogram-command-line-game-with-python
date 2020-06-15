#!/usr/bin/env python3

import os
from termcolor import colored
import generate_upgraded
import user


def main():

    clear()
    grid = []
    while 2 not in grid:
        grid_solved = generate_upgraded.get_grid_solved()
        clues = generate_upgraded.get_clues(grid_solved)
        grid = generate_upgraded.get_grid(grid_solved)

    head_start = []
    for i, cell in enumerate(grid):
        if cell == 1:
            grid[i] = 0
        elif cell == 2:
            head_start.append(i)
    previous_grids = []
    active_index = 0

    print_grid(grid, clues, active_index, head_start)

    solved = False
    while not solved:

        while True:
            user_input = user.get_input(grid, clues, active_index)
            if user.is_step(user_input):
                active_index = get_active_index(user_input, active_index)
                break
            elif user.is_mark(user_input):
                previous_grids.append(list(grid))
                grid = get_changed_grid(user_input, grid, active_index)
                break
            elif user.is_undo(user_input):
                if len(previous_grids):
                    grid = previous_grids.pop()
                break
            elif user.is_verification(user_input):
                solved = verify_solution(grid, grid_solved)
                if not solved:
                    input("\n Something's not quite right... Press Enter to continue.")
                break
            else:
                clear()
                print_grid(grid, clues, active_index, head_start)

        clear()
        print_grid(grid, clues, active_index, head_start)

    print(" Grid is complete indeed!")


def clear():
    os.system('clear')


def print_grid(grid, clues, active_index, head_start):
    max_row_clue_length = get_max_clue_length(clues, "rows")
    max_column_clue_length = get_max_clue_length(clues, "columns")

    CELL_WIDTH = 3
    FIELD_FOR_ROW_NUMBERS = 3
    left_indent_for_border_line = max_row_clue_length * FIELD_FOR_ROW_NUMBERS + 1
    left_indent_for_column_numbers = left_indent_for_border_line + 1
    border_line_dash_count = (10 * CELL_WIDTH + 11)

    print()
    for i in range(max_column_clue_length):
        row_to_print = " " * left_indent_for_column_numbers
        for clue in clues["columns"]:
            if len(clue) == max_column_clue_length:
                row_to_print += str(clue[i]).center(CELL_WIDTH) + " "
            else:
                clue_length_diff = max_column_clue_length - len(clue)
                if i >= clue_length_diff:
                    clue_number_index = i - clue_length_diff
                    row_to_print += str(clue[clue_number_index]).center(CELL_WIDTH) + " "
                else:
                    row_to_print += " " * (CELL_WIDTH + 1)
        print(row_to_print)

    rows = generate_upgraded.get_rows(grid)
    number_converter = {0: " ", 1: "O", 2: "-"}
    border_line = " " * left_indent_for_border_line + "-" * border_line_dash_count
    border_line_bold = " " * left_indent_for_border_line + "=" * border_line_dash_count

    print(border_line_bold)
    for i, row in enumerate(rows):
        clue_length_diff = max_row_clue_length - len(clues["rows"][i])
        indent_for_row_numbers = (FIELD_FOR_ROW_NUMBERS * clue_length_diff + 1)
        row_to_print = " " * indent_for_row_numbers
        for clue_number in clues["rows"][i]:
            row_to_print += str(clue_number).center(FIELD_FOR_ROW_NUMBERS)
        row_to_print += "|"
        for j, cell in enumerate(row):
            cell_index = i * 10 + j
            cell_printable = number_converter[cell]
            if cell_index in head_start:
                cell_printable = "X"
            if cell_index == active_index:
                cell_printable = colored(cell_printable, "green", attrs=["reverse"])
            if (j + 1) % 5:
                border_wall = ":"
            else:
                border_wall = "|"
            row_to_print += " " * (CELL_WIDTH // 2) + cell_printable + " " * (CELL_WIDTH // 2) + border_wall
        print(row_to_print)
        if (i + 1) % 5:
            print(border_line)
        else:
            print(border_line_bold)
    print()


def get_max_clue_length(clues, lines):
    maxlen = 0
    for line_clue in clues[lines]:
        if len(line_clue) > maxlen:
            maxlen = len(line_clue)
    return maxlen


def get_active_index(user_input, active_index):
    steps = {
        "w": (lambda index: index - 10), "ww": (lambda index: index - 20),
        "s": (lambda index: index + 10), "ss": (lambda index: index + 20),
        "a": (lambda index: index - 1), "aa": (lambda index: index - 2),
        "d": (lambda index: index + 1), "dd": (lambda index: index + 2)
    }
    if steps[user_input](active_index) in range(100):
        return steps[user_input](active_index)
    else:
        return active_index


def get_changed_grid(user_input, grid, active_index):
    marks = {"f": 1, "e": 2, "c": 0}
    grid[active_index] = marks[user_input]
    return grid


def verify_solution(grid, grid_solved):
    for cell_solved, cell in zip(grid_solved, grid):
        if cell_solved and cell_solved != cell:
            return False
    return True


main()
