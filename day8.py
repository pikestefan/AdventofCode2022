# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import numpy as np

inputs_path = Path('inputs')

def check_neighbourhood(row_idx, col_idx, matrix):
    tot_rows, tot_cols = matrix.shape
    null_arr = None
    right = matrix[row_idx, (col_idx+1):] if (col_idx+1 < tot_cols) else null_arr
    left = matrix[row_idx,(col_idx-1)::-1] if (col_idx-1 >=0) else null_arr
    top = matrix[(row_idx-1)::-1, col_idx] if (row_idx-1 >=0) else null_arr
    bottom = matrix[(row_idx+1):, col_idx] if (row_idx+1 < tot_rows) else null_arr
    
    return [right, left, top, bottom]

def check_visibility(row_idx, col_idx, matrix):
    
    current = matrix[row_idx, col_idx]
    
    neighbourhood = check_neighbourhood(row_idx, col_idx, matrix)
    
    truth_vals = [np.all(loc_nei < current) for loc_nei in neighbourhood]
    
    return any(truth_vals)

def check_viewrange(row_idx, col_idx, matrix):
    
    current = matrix[row_idx, col_idx]
    
    neighbourhood = check_neighbourhood(row_idx, col_idx, matrix)
    
    scenic_score = 1
    for direction in neighbourhood:
        if direction is not None:
            first_equal = np.argwhere(direction>=current)
            scenic_score *= first_equal[0][0]+1 if first_equal.size else len(direction)
        else:
            scenic_score *= 0
    return scenic_score

#%% First problem
with open(inputs_path / 'day8.txt', 'r') as file:
    trees = []
    file_contents = file.readlines()
    for line in file_contents:
        line = line.strip()
        treeline = [int(tree) for tree in line]
        trees.append(treeline)

trees = np.array(trees, dtype=int)

visible_trees = 0
for jj in range(1, trees.shape[0]-1):
    for ii in range(1, trees.shape[1]-1):
        if check_visibility(jj, ii, trees):
            visible_trees += 1

visible_trees += ( trees.shape[1] + trees.shape[0] - 2)*2

print("Visible trees: ", visible_trees)

#%% Second problem 
view_ranges = np.zeros(trees.shape, dtype=int)
for jj in range(0, trees.shape[0]):
    for ii in range(0, trees.shape[1]):
        view_ranges[jj, ii] = check_viewrange(jj, ii, trees)
        
print("Max scenic score:", view_ranges.max())
