#!/usr/bin/env python3

import generate
from termcolor import colored


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

    rows = generate.get_rows(grid)
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
