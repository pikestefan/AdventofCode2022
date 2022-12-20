# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

inputs_path = Path('inputs')

class rope_simulator:
    
    def __init__(self, head_start=[0,0], tail_start=[0,0], trackhead = True):
        self.head = head_start
        self.tail = tail_start
        self.tail_tracker = []
        self.headtrackable = trackhead
        if self.headtrackable:
            self.head_tracker = []
            self.track_head()
        self.track_tail()
        
    def move_head(self, direction, steps):
        idx, coeff = 1, 1
        
        if direction=="L":
            coeff = -1
        elif direction =="U":
            idx = 0
        elif direction == "D":
            idx = 0
            coeff = -1
        
        for step in range(steps):
            self.head[idx] += coeff
            if self.headtrackable:
                self.track_head()
            self.update_tail()
            
    def update_tail(self):
        delta_row, delta_col = [h-t for h,t in zip(self.head, self.tail)]
        
        if not( abs(delta_row)<=1 and abs(delta_col)<=1 ):
            rowstep = delta_row//abs(delta_row) if delta_row else 0
            colstep = delta_col//abs(delta_col) if delta_col else 0
            
            self.tail[0] += rowstep
            self.tail[1] += colstep
        
        self.track_tail()
        
    def track_tail(self):
        self.tail_tracker.append(deepcopy(self.tail))
    def track_head(self):
        self.head_tracker.append(self.head[:])
        
    def view_visited(self):
        visited = np.array(self.tail_tracker)
        
        minvis, maxvis = visited.min(), visited.max()
        rowrange = np.arange(minvis, maxvis+1)
        colrange = np.copy(rowrange)
        
        visited_matrix = np.zeros((len(rowrange), len(colrange)), dtype=int)
        
        for tailcoord in visited:
            trow, tcol = tailcoord
            visited_matrix[rowrange==trow, colrange==tcol] = 1
            
        return np.flipud(visited_matrix)
    
    def build_movie(self):
        head_coords = np.array(self.head_tracker)
        tail_coords = np.array(self.tail_tracker)
        
        minh, maxh = head_coords.min(), head_coords.max()
        mint, maxt = tail_coords.min(), tail_coords.max()
        
        rowrange = np.arange(min(minh, mint), max(maxh, maxt)+1)
        colrange = np.copy(rowrange)
        
        movie_matrix = np.zeros( ((len(head_coords),)
                                  + rowrange.shape 
                                  + colrange.shape) )
        
        for frame, hcoord, tcoord in zip(movie_matrix, head_coords, tail_coords):
            hrow, hcol = hcoord
            trow, tcol = tcoord
            
            frame[rowrange==trow, colrange==tcol] = 1
            frame[rowrange==hrow, colrange==hcol] = 2
            
        
        return movie_matrix
    
    
class long_rope_simulator(rope_simulator):
    def __init__(self, head_start=[0,0], tail_start=[0,0], trackhead = True):
        super().__init__(head_start, tail_start, trackhead)
        self.tail = [tail_start[:] for _ in range(9)]
        self.tail_tracker = []
        self.track_tail()
        
        
    def update_tail(self):
        previous = self.head[:]
        for ii, tail_segment in enumerate(self.tail):
            delta_row, delta_col = [h-t for h,t in zip(previous, tail_segment)]
            
            if not(abs(delta_row)<=1 and abs(delta_col)<=1):
                rowstep = delta_row//abs(delta_row) if delta_row else 0
                colstep = delta_col//abs(delta_col) if delta_col else 0
                
                tail_segment[0] += rowstep
                tail_segment[1] += colstep
                
                self.tail[ii] = tail_segment[:]
                
            previous = tail_segment[:]
        self.track_tail()
        
    def view_visited(self):
        visited = np.array(self.tail_tracker)
        visited = visited[:,-1,:]
        
        minvis, maxvis = visited.min(), visited.max()
        rowrange = np.arange(minvis, maxvis+1)
        colrange = np.copy(rowrange)
        
        visited_matrix = np.zeros((len(rowrange), len(colrange)), dtype=int)
        
        for tailcoord in visited:
            trow, tcol = tailcoord
            visited_matrix[rowrange==trow, colrange==tcol] = 1
            
        return visited_matrix
    
    def build_movie(self):
        head_coords = np.array(self.head_tracker)
        tail_coords = np.array(self.tail_tracker)
        
        minh, maxh = head_coords.min(), head_coords.max()
        mint, maxt = tail_coords.min(), tail_coords.max()
        
        rowrange = np.arange(min(minh, mint), max(maxh, maxt)+1)
        colrange = np.copy(rowrange)
        
        movie_matrix = np.zeros( ((len(head_coords),)
                                  + rowrange.shape 
                                  + colrange.shape) )
        
        for frame, hcoord, tcoord in zip(movie_matrix, head_coords, tail_coords):
            hrow, hcol = hcoord
            
            for ii, tsegment in enumerate(tcoord):
                trow, tcol = tsegment
                frame[rowrange==trow, colrange==tcol] = ii+1
            frame[rowrange==hrow, colrange==hcol] = 11
            
        
        return movie_matrix
    


with open(inputs_path / 'day9.txt', 'r') as file:
    instructions = []
    keep_going = True
    while keep_going:
        line = file.readline()
        if line:
            direc, steps = line.strip().split(' ')
            instructions.append([direc, int(steps)])
        else:
            keep_going = False
#%% First problem
rsim = rope_simulator()
for instruction in instructions:
    direc, steps = instruction
    rsim.move_head(direc, steps)

print(np.sum(rsim.view_visited()))
# movie = rsim.build_movie()

# for frame in movie:
#     plt.figure(figsize=(10,10))
#     plt.imshow(frame, aspect='equal',origin='lower')
#     plt.show()
    
#%% Second problem 

lrsim = long_rope_simulator()
for instruction in instructions:
    direc, steps = instruction
    lrsim.move_head(direc, steps)
    
tail_visited = lrsim.view_visited()
movie = lrsim.build_movie()
for frame in movie:
    plt.figure(figsize=(10,10))
    plt.imshow(frame, aspect='equal',origin='lower')
    plt.show()

plt.figure(figsize=(10,10))
plt.imshow(tail_visited, aspect='equal',origin='lower')
plt.show()

print("Long tail visits:", np.sum(tail_visited))