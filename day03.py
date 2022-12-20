# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path

inputs_path = Path('inputs')

#%% First problem

rucksacks = []
with open(inputs_path / 'day3.txt', 'r') as file:
    input_info = file.readlines()
    for line in input_info:
        line = line.strip()
        linelen = len(line)
        rucksacks.append([line[:linelen//2], line[linelen//2:]])

offset_val = ord('a') - 1

priorities = []
for rucksack in rucksacks:
    c1, c2 = rucksack
    
    keep_going = True
    ii = 0
    while keep_going:
        if c1[ii] in c2:
            found_item = c1[ii]
            if found_item.isupper():
                priority = ord(found_item.lower()) - offset_val + 26
            else:
                priority = ord(found_item) - offset_val
            priorities.append(priority)
            keep_going = False
        else:
            ii+=1
        
print("Total priority: ", sum(priorities))
#%% Second problem 

common_item_vals = []
for index in range(0, len(input_info), 3):
    g1, g2, g3 = input_info[index], input_info[index+1], input_info[index+2]
    
    keep_going = True
    ii = 0
    while keep_going:
        if (g1[ii] in g2) and (g1[ii] in g3):
            common_item = g1[ii]
            if common_item.isupper():
                common_val = ord(common_item.lower()) - offset_val + 26
            else:
                common_val = ord(common_item) - offset_val
            common_item_vals.append(common_val)
            keep_going = False
        else:
            ii+=1
            
print("Common item values: ", sum(common_item_vals))
