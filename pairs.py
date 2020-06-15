#!/usr/bin/env python3

import random
import generate


def find_problematic_indices(rows, set_rows):
    problematic_indices = []
    for i in range(10 - 1):
        for j in range(i, 10):
            problematic_indices += check_set_row_pair(rows, set_rows, i, j)
    return problematic_indices


def check_set_row_pair(rows, set_rows, row_up_index, row_down_index):
    problematic_indices2 = []
    for set_up in set_rows[row_up_index]:
        for set_down in set_rows[row_down_index]:
            problematic_indices2 += check_set_pair(rows, row_up_index, row_down_index, set_up, set_down)
    return problematic_indices2


def check_set_pair(rows, row_up_index, row_down_index, set_up, set_down):
    problematic_indices3 = []
    down_offset = find_down_offset(set_up, set_down)
    if not down_offset:
        return problematic_indices3
    pending_indices = get_pending_indices(row_up_index, row_down_index, set_up, set_down, down_offset)
    opposite_indices = get_opposite_indices(row_up_index, row_down_index, set_up, set_down, down_offset)
    if check_clues(rows, pending_indices, opposite_indices):
        problematic_indices3.append(random.choice(pending_indices))
    return problematic_indices3


def find_down_offset(set_up, set_down):
    if any(any_set[0] == any_set[1] for any_set in [set_up, set_down]):
        return 0
    if set_up[0] > 0:
        if all(set_up[i] - 1 == set_down[i] for i in range(2)):
            return -1
    if set_up[1] < 9:
        if all(set_up[i] + 1 == set_down[i] for i in range(2)):
            return 1
    return 0


def get_pending_indices(row_up_index, row_down_index, set_up, set_down, down_offset):
    if down_offset == -1:
        pending_index_up = row_up_index * 10 + set_up[0] - 1
        pending_index_down = row_down_index * 10 + set_down[1] + 1
    if down_offset == 1:
        pending_index_up = row_up_index * 10 + set_up[1] + 1
        pending_index_down = row_down_index * 10 + set_down[0] - 1
    return [pending_index_up, pending_index_down]


def get_opposite_indices(row_up_index, row_down_index, set_up, set_down, down_offset):
    if down_offset == -1:
        opposite_index_up = row_up_index * 10 + set_up[1]
        opposite_index_down = row_down_index * 10 + set_down[0]
    if down_offset == 1:
        opposite_index_up = row_up_index * 10 + set_up[0]
        opposite_index_down = row_down_index * 10 + set_down[1]
    return [opposite_index_up, opposite_index_down]


def check_clues(rows, pending_indices, opposite_indices):
    grid = generate.get_grid_from_rows(rows)
    clues = generate.get_clues(grid)
    test_grid = list(grid)
    for pending, opposite in zip(pending_indices, opposite_indices):
        pending_cell = test_grid[pending]
        test_grid[pending] = test_grid[opposite]
        test_grid[opposite] = pending_cell
    test_clues = generate.get_clues(test_grid)
    if test_clues == clues:
        return True
    else:
        return False
