# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 23:05:29 2022

@author: L
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

sand_val = 2
rock_val = 1

sand_coord = [500, 0]

with open(r"inputs/day14.txt", 'r') as file:
    
    paths = []
    minrow, maxrow = np.inf, 0
    mincol, maxcol = np.inf, 0
    
    for line in file.readlines():
        curr_path = []
        line = line.strip().replace(" ","").split("->")
        for pair in line:
            pair = list(map(int, pair.split(",")))
            col_coord, row_coord = pair
            
            if row_coord > maxrow:
                maxrow = row_coord
            if row_coord < minrow:
                minrow = row_coord
            if col_coord > maxcol:
                maxcol = col_coord
            if col_coord < mincol:
                mincol = col_coord
            curr_path.append(pair)
                
        paths.append(curr_path)
        
        
minrow = sand_coord[1]

rowrange = np.arange(minrow, maxrow+1)
colrange = np.arange(mincol, maxcol+1)

sand_indices = [np.argwhere(rowrange==sand_coord[1])[0][0],
                np.argwhere(colrange==sand_coord[0])[0][0]]

rock_matrix = np.zeros(rowrange.shape+colrange.shape, dtype=int)

for path in paths:
    for ii in range(len(path)-1):
        start, stop = path[ii], path[ii+1]
        startrow, stoprow = start[1], stop[1]
        startcol, stopcol = start[0], stop[0]
        
        if startrow > stoprow:
            stoprow, startrow = startrow, stoprow
            
        if startcol > stopcol:
            stopcol, startcol = startcol, stopcol
            
        rowmask = np.logical_and(rowrange>=startrow, rowrange<=stoprow)
        colmask = np.logical_and(colrange>=startcol, colrange<=stopcol)
        rock_matrix[rowmask, colmask] = 1
        
    
def pour_sand(matrix, sandcoord):
    
    sandrow, sandcol = sandcoord
    matrix = np.copy(matrix)
    
    fallen_through = False
    stopped = False
    
    matrows, matcols = matrix.shape
    
    while not fallen_through and not stopped:
        if (sandrow+1) < matrows:
            if matrix[sandrow+1,sandcol] == 0:
                sandrow += 1
            elif (sandcol-1) >= 0 and matrix[sandrow+1, sandcol-1] == 0:
                sandrow += 1
                sandcol -= 1
            elif (sandcol-1) <= -1:
                fallen_through = True
            elif (sandcol+1) < matcols and matrix[sandrow+1, sandcol+1] == 0:
                sandrow += 1
                sandcol += 1
            elif (sandcol+1) >= matcols:
                fallen_through = True
            else:
                stopped = True
        else:
            fallen_through = True
            
        if stopped:
            matrix[sandrow, sandcol] = 2
            
    return matrix

def pour_sand_v2(matrix, sandcoord):
    
    sandrow, sandcol = sandcoord
    matrix = np.copy(matrix)
    
    stopped = False
    
    matrows, matcols = matrix.shape
    
    emptycol = np.zeros((matrows, 1))
    
    while not stopped:
        if (sandrow+1) < matrows:
            if matrix[sandrow+1,sandcol] == 0:
                sandrow += 1
            elif (sandcol-1) >= 0 and matrix[sandrow+1, sandcol-1] == 0:
                sandrow += 1
                sandcol -= 1
            elif (sandcol-1) <= -1:
                matrix = np.hstack((emptycol, matrix))
                sandcol = 0
                sandrow += 1
                sandcoord[1] += 1
            elif (sandcol+1) < matcols and matrix[sandrow+1, sandcol+1] == 0:
                sandrow += 1
                sandcol += 1
            elif (sandcol+1) >= matcols:
                matrix = np.hstack((matrix, emptycol))
                sandrow += 1
                sandcol += 1
            else:
                stopped = True
        else:
            stopped =True
            
        if stopped:
            matrix[sandrow, sandcol] = 2
            
    return matrix


# # %% problem 1
# plot = True
# maxit = 1000
# iternum = 0

# steadystate = False

# previous_matrix = rock_matrix

# while iternum < maxit and not steadystate:
#     next_matrix = pour_sand(previous_matrix, sand_indices)
    
#     if np.all(previous_matrix == next_matrix):
#         steadystate = True
        
#     if plot:
#         plt.imshow(next_matrix)
#         plt.show()
        
#     previous_matrix = next_matrix
#     iternum += 1
    
# print("Steady state at:", iternum-1)
    
# %% problem 2
plot = True
maxit = 100000000
iternum = 0
plot_divider = 100

filled_up = False

new_rock_matrix = np.vstack((rock_matrix, np.zeros((1, rock_matrix.shape[1]))))

previous_matrix = new_rock_matrix

while iternum < maxit and not filled_up:
    next_matrix = pour_sand_v2(previous_matrix, sand_indices)
    
    if next_matrix[sand_indices[0], sand_indices[1]] == 2:
        filled_up = True
        
    if plot and (iternum % plot_divider == 0):
        plt.imshow(next_matrix)
        plt.show()
        
    previous_matrix = next_matrix
    iternum += 1
    
print("Filled up at:", iternum)
