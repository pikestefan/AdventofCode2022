# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import re
import numpy as np

inputs_path = Path('inputs')

#%% First problem


with open(inputs_path / 'day5.txt', 'r') as file:
    
    file_contents = file.readlines()
    
    watershed_idx = file_contents.index('\n')
    
    stack = file_contents[:watershed_idx-1]
    stack_addresses = file_contents[watershed_idx-1]
    instructions_strings = file_contents[watershed_idx+1:]
    
stack_addresses = stack_addresses.strip()
stack_addresses = list(map(int, re.split("\s+", stack_addresses)))
    
    
original_stack_matrix = []
for line in stack:
    clean_string = line.replace("\n","").replace("[", "").replace("]", "")
    clean_string = re.sub("\s{4}", ",", clean_string)
    clean_string = clean_string.replace(" ", "," )
    clean_string = clean_string.split(',')
    original_stack_matrix.append(clean_string)
    
original_stack_matrix = np.array(original_stack_matrix)
    
instructions_pattern = "move (\d+) from (\d+) to (\d+)"

instructions = []
for instruction in instructions_strings:
    matched = re.match(instructions_pattern, instruction)
    translated = [int(element) for element in matched.groups()]
    instructions.append(translated)
    

stack_matrix = np.copy(original_stack_matrix)
for instruction in instructions:
    amount, origin, destination = instruction
    origin -= 1
    destination -= 1
    origin_column =stack_matrix[:, origin]
    origin_column = origin_column[origin_column!='']
    
    new_origin_column = origin_column[amount:]
    boxes =  np.flip(origin_column[:amount])
    
    destination_column = stack_matrix[:, destination]
    destination_column = destination_column[destination_column != '']
    
    destination_column = np.hstack((boxes, destination_column))
    
    if len(destination_column) > len(stack_matrix):
        new_rows = len(destination_column) - len(stack_matrix)
        
        empty_lines = np.full(shape=(new_rows,
                                     len(stack_addresses)), 
                              fill_value = '')
        
        stack_matrix = np.vstack( (empty_lines, stack_matrix) )
        
    stack_matrix[:, destination] = ''
    stack_matrix[:, origin] = ''
    stack_matrix[-len(destination_column):, destination] = destination_column
    if new_origin_column.size:
        stack_matrix[-len(new_origin_column):, origin] = new_origin_column
        
crates_on_top = ""
for column in stack_matrix.T:
    column = column[column != '']
    if column.size:
        crates_on_top += column[0]

print("Crates on top: ", crates_on_top)
#%% Second problem 

#Copy paste all, only difference is that boxes is not flipped

stack_matrix = np.copy(original_stack_matrix)
for instruction in instructions:
    amount, origin, destination = instruction
    origin -= 1
    destination -= 1
    origin_column =stack_matrix[:, origin]
    origin_column = origin_column[origin_column!='']
    
    new_origin_column = origin_column[amount:]
    boxes =  origin_column[:amount]
    
    destination_column = stack_matrix[:, destination]
    destination_column = destination_column[destination_column != '']
    
    destination_column = np.hstack((boxes, destination_column))
    
    if len(destination_column) > len(stack_matrix):
        new_rows = len(destination_column) - len(stack_matrix)
        
        empty_lines = np.full(shape=(new_rows,
                                     len(stack_addresses)), 
                              fill_value = '')
        
        stack_matrix = np.vstack( (empty_lines, stack_matrix) )
        
    stack_matrix[:, destination] = ''
    stack_matrix[:, origin] = ''
    stack_matrix[-len(destination_column):, destination] = destination_column
    if new_origin_column.size:
        stack_matrix[-len(new_origin_column):, origin] = new_origin_column
        
crates_on_top = ""
for column in stack_matrix.T:
    column = column[column != '']
    if column.size:
        crates_on_top += column[0]

print("Crates on top: ", crates_on_top)