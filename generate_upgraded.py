#!/usr/bin/env python3

import random
from itertools import groupby, combinations, product

SIZE = 10
AREA = SIZE ** 2


def get_grid_solved():
    grid_solved = [0] * AREA
    fill_factor = random.randrange(50, 70)
    for i in range(fill_factor):
        while True:
            cell_index = random.randrange(0, AREA)
            if not grid_solved[cell_index]:
                grid_solved[cell_index] = 1
                break
    return grid_solved


def get_clues(grid_solved):
    clues = {"rows": [], "columns": []}
    rows = get_rows(grid_solved)
    columns = get_columns(grid_solved)
    set_rows = get_set_lines(rows)
    set_columns = get_set_lines(columns)
    for key, set_lines in {"rows": set_rows, "columns": set_columns}.items():
        for set_line in set_lines:
            clues[key].append([s[1] - s[0] + 1 for s in set_line])
    return clues


def get_grid(grid):
    rows = get_rows(grid)
    rows = amend_lines(rows)
    rowsT = rotate_rows(rows, "left")
    rowsT = amend_lines(rowsT)
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


def get_set_lines(lines):
    set_lines = []
    indices = list(range(len(lines)))
    for line in lines:
        set_line = []
        for filled, unbroken in groupby(indices, lambda x: line[x]):
            if not filled:
                continue
            u = list(unbroken)
            set_line.append((u[0], u[-1]))
        set_lines.append(set_line)
    return set_lines


def amend_lines(lines):
    set_lines = get_set_lines(lines)
    problematic_indices = find_problematic_indices(lines, set_lines)
    grid = get_grid_from_rows(lines)
    for index in problematic_indices:
        grid[index] = 2
    return get_rows(grid)


def find_problematic_indices(lines, set_lines):
    grid = get_grid_from_rows(lines)
    problematic_indices = []
    for line_num_pair in combinations(range(SIZE), 2):
        (up, down) = line_num_pair
        for set_pair in product(set_lines[up], set_lines[down]):
            if not is_offset_one(set_pair):
                continue
            set_pair_in_grid = get_set_pair_in_grid(set_pair, line_num_pair)
            (pending_indices, opposite_indices) = get_relevant_indices(grid, set_pair_in_grid, line_num_pair)
            if are_clues_the_same_after_swap(grid, pending_indices, opposite_indices):
                problematic_indices.append(random.choice(pending_indices))
    return problematic_indices


def is_offset_one(set_pair):
    if any(s[0] == s[1] for s in set_pair):
        return False
    down_offsets = []
    for index_pair in zip(*set_pair):
        (index_up, index_down) = index_pair
        down_offset = index_down - index_up
        down_offsets.append(down_offset)
    (left, right) = down_offsets
    if left in [-1, 1] and left == right:
        return True
    else:
        return False


def get_set_pair_in_grid(set_pair, line_num_pair):
    set_pair_in_grid = []
    for line_set, line_num in zip(set_pair, line_num_pair):
        set_pair_in_grid.append([line_num * SIZE + side for side in line_set])
    return set_pair_in_grid


def get_relevant_indices(grid, set_pair_in_grid, line_num_pair):
    (up, down) = line_num_pair
    line_diff = down - up
    pending_indices = []
    opposite_indices = []
    for line_set, delta in zip(set_pair_in_grid, [SIZE * line_diff, SIZE * line_diff * -1]):
        for side in line_set:
            if not grid[side + delta]:
                pending_indices.append(side + delta)
                opposite_indices.append(side)
    return (pending_indices, opposite_indices)


def are_clues_the_same_after_swap(grid, pending_indices, opposite_indices):
    test_grid = list(grid)
    for pending, opposite in zip(pending_indices, opposite_indices):
        test_grid[pending] = 1
        test_grid[opposite] = 0
    clues = get_clues(grid)
    test_clues = get_clues(test_grid)
    if clues == test_clues:
        return True
    else:
        return False
