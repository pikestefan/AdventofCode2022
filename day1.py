# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path

inputs_path = Path('inputs')

#%% First problem

input_file= inputs_path / 'day1.txt'

with open(input_file, 'r') as file:
    calorie_list = []
    elf_calories = []
    
    for line in file.readlines():
        if line == '\n':
            calorie_list.append(elf_calories)
            elf_calories = []
        else:
            elf_calories.append(int(line))
            
tot_elf_calories = list(map(sum, calorie_list))

print("Max calories: ", max(tot_elf_calories))

#%% Second problem 

sorted_total = sorted(tot_elf_calories)

print("Top three max calories: ", sum(sorted_total[-3:]))