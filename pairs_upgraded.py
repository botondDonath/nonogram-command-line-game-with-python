#!/usr/bin/env python3

import random
import generate_upgraded
from itertools import combinations, product

SIZE = 10


def find_problematic_indices(lines, set_lines):
    grid = generate_upgraded.get_grid_from_rows(lines)
    problematic_indices = []
    for line_num_pair in combinations(range(SIZE), 2):
        (up, down) = line_num_pair
        for set_pair in product(set_lines[up], set_lines[down]):
            if not is_offset_one(set_pair):
                continue
            set_pair_in_grid = get_set_pair_in_grid(set_pair, line_num_pair)
            (pending_indices, opposite_indices) = get_relevant_indices(grid, set_pair_in_grid)
            if are_clues_the_same_after_swap(grid, pending_indices, opposite_indices):
                problematic_indices.append(random.choice(pending_indices))
    return problematic_indices


def is_offset_one(set_pair):
    for index_pair in zip(*set_pair):
        (index_up, index_down) = index_pair
        down_offset = index_down - index_up
        if down_offset not in [-1, 1]:
            break
    if down_offset in [-1, 1]:
        return True
    else:
        return False


def get_set_pair_in_grid(set_pair, line_num_pair):
    set_pair_in_grid = []
    for line_set, line_num in zip(set_pair, line_num_pair):
        set_pair_in_grid.append([line_num * SIZE + side for side in line_set])
    return set_pair_in_grid


def get_relevant_indices(grid, set_pair_in_grid):
    pending_indices = []
    opposite_indices = []
    for line_set, delta in zip(set_pair_in_grid, [SIZE, SIZE * -1]):
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
    clues = generate_upgraded.get_clues(grid)
    test_clues = generate_upgraded.get_clues(test_grid)
    if clues == test_clues:
        return True
    else:
        return False
