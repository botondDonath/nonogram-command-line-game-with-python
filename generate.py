#!/usr/bin/env python3

import random


def get_grid_solved():
    grid_solved = [0] * 100
    fill_factor = random.randrange(50, 70)
    for i in range(fill_factor):
        while True:
            cell_index = random.randrange(0, 100)
            if not grid_solved[cell_index]:
                grid_solved[cell_index] = 1
                break
    return grid_solved


def get_clues(grid_solved):
    clues = {"rows": [], "columns": []}
    rows = get_rows(grid_solved)
    columns = get_columns(grid_solved)
    for lines in [rows, columns]:
        if lines == rows:
            name = "rows"
        else:
            name = "columns"
        for i, line in enumerate(lines):
            clues[name].append([])
            empty_previous = True
            for j, cell in enumerate(line):
                if cell and empty_previous:
                    empty_previous = False
                    set_length = 1
                    if j == len(line) - 1:
                        clues[name][i].append(set_length)
                elif cell:
                    set_length += 1
                    if j == len(line) - 1:
                        clues[name][i].append(set_length)
                elif not empty_previous:
                    empty_previous = True
                    clues[name][i].append(set_length)
                    set_length = 0
    return clues


def get_grid(grid):
    rows = get_rows(grid)
    rows = amend_rows(rows)
    rowsT = rotate_rows(rows, "left")
    rowsT = amend_rows(rowsT)
    rows = rotate_rows(rowsT, "right")
    return get_grid_from_rows(rows)


def rotate_rows(rows, direction):
    if direction == "left":
        return [list(reversed(column)) for column in zip(*rows)]
    elif direction == "right":
        return [list(column) for column in reversed(list(zip(*rows)))]


def get_grid_from_rows(rows):
    return [cell for row in rows for cell in row]


def get_rows(grid):
    return [[grid[j] for j in range(i, i + 10)] for i in range(0, 100, 10)]


def get_columns(grid):
    return [[grid[j] for j in range(i, i + 91, 10)] for i in range(10)]


def get_set_rows(rows):
    set_rows = []
    for row in rows:
        set_rows.append(get_set_row(row))
    return set_rows


def get_set_row(row):
    set_row = []
    empty_previous = True
    for i, cell in enumerate(row):
        if cell and empty_previous:
            start = i
            empty_previous = False
            if i == len(row) - 1:
                set_row.append([i, i])
        elif cell and not empty_previous and i == len(row) - 1:
            end = i
            set_row.append([start, end])
        elif not cell and not empty_previous:
            end = i - 1
            set_row.append([start, end])
            empty_previous = True
    return set_row


def amend_rows(rows):
    import pairs
    set_rows = get_set_rows(rows)
    problematic_indices = pairs.find_problematic_indices(rows, set_rows)
    grid = get_grid_from_rows(rows)
    for index in problematic_indices:
        grid[index] = 2
    return get_rows(grid)
