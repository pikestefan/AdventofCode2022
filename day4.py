# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path

inputs_path = Path('inputs')

#%% First problem

assignment_pairs = []
with open(inputs_path / 'day4.txt', 'r') as file:
    for line in file.readlines():
        pair1, pair2 = line.strip().split(',')
        pair1 = list(map(int, pair1.split('-')))
        pair2 = list(map(int, pair2.split('-')))
        
        assignment_pairs.append([sorted(pair1), sorted(pair2)])
        
        
        
range_fully_contained = 0
for assignment_pair in assignment_pairs:
    pair1, pair2 = assignment_pair
     
    if pair2[0] > pair1[0]:
        if pair2[1] <= pair1[1]:
            range_fully_contained += 1
    elif pair1[0] > pair2[0]:
        if pair1[1] <= pair2[1]:
            range_fully_contained += 1
    else:
        range_fully_contained += 1
        
        
print("Fully contained assignments: ", range_fully_contained)


#%% Second problem 

range_dont_overlap = 0
for assignment_pair in assignment_pairs:
    pair1, pair2 = assignment_pair
    
    if pair1[0] <= pair2[0]:
        first_chunk = pair1
        second_chunk = pair2
    elif pair2[0] < pair1[0]:
        first_chunk = pair2
        second_chunk = pair1
    
    if (first_chunk[0] != second_chunk[0]) and (first_chunk[1] < second_chunk[0]):
        range_dont_overlap += 1
        
        
print("Overlapping assignments: ", len(assignment_pairs) - range_dont_overlap)