# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import numpy as np
from copy import deepcopy

inputs_path = Path('inputs')

with open(inputs_path / 'day12.txt', 'r') as file:
    start_coord, end_coord = 0, 0
    ref = ord('a')
    for ii, line in enumerate(file.readlines()):
        line = line.strip()
        if 'S' in line:
            start_idx = line.index('S')
            start_coord = [ii, start_idx]
            line = line.replace('S', 'a')
        if 'E' in line:
            end_idx = line.index('E')
            end_coord = [ii, line.index('E')]
            line = line.replace('E','z')
            
        height_line = [ord(char) - ref for char in line]
        if ii == 0:
            height_map = np.array(height_line)
        else:
            height_map = np.vstack((height_map, height_line))
            
def get_neighbours(curr_pos, matrix):
    row, col = curr_pos
    # L R U D
    coords, final = [], []
    for ncoord in [[0, -1], [0, +1], [-1, 0], [+1,0]]:
        nrow, ncol = ncoord
        nrow += row
        ncol += col
        if (0<=nrow<matrix.shape[0]) and (0<=ncol<matrix.shape[1]):
            coords.append(ncoord)
            final.append(matrix[nrow, ncol])
    return coords, final

def makepaths(path_lists, matrix):
    path_matrix = np.zeros((len(path_lists),) + matrix.shape)
    for ii, path in enumerate(path_lists):
        for jj, coord in enumerate(path):
            row, col = coord
            path_matrix[ii, row, col] = jj+1
    return path_matrix
#%% First problem

keep_going = True
max_iter = 1000001
iteration = 0

curr_row, curr_col = start_coord

branches_path = []
branch_points = []
curr_path = [[curr_row, curr_col]]

completed_paths = []

while keep_going:
    curr_row, curr_col = curr_path[-1]
    ncoords, neighbours = get_neighbours([curr_row, curr_col], height_map)
    
    available_steps = []
    for ncoord, neighbour in zip(ncoords, neighbours):
        if ((neighbour - height_map[curr_row, curr_col])<2 
            and (ncoord not in curr_path)):
            available_steps.append(ncoord)
    
    if len(available_steps) > 1:
        chosen_branch = available_steps.pop()
        branch_points.append(available_steps)
        branches_path.append(curr_path[:])
        curr_path.append(chosen_branch)
    elif len(available_steps) == 1:
        chosen_branch = available_steps[0]
    
        curr_path.append(chosen_branch)
        
    iteration += 1
    if [curr_row, curr_col] == end_coord or len(available_steps) == 0:
        if [curr_row, curr_col] == end_coord:
            completed_paths.append(curr_path[:])
        
        if len(branch_points[-1]) == 1:
            curr_path = branches_path.pop()
            new_point = branch_points[-1].pop()
            branch_points.pop()
        else:
            curr_path = branches_path[-1]
            new_point = branch_points[-1].pop()
            
        curr_path.append(new_point)
            
    if len(branch_points) == 0 or iteration == max_iter:
        keep_going = False
            
wow = makepaths([curr_path], height_map)
        
#%% Second problem 
