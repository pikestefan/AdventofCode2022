# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path

inputs_path = Path('inputs')

#%% First problem

with open(inputs_path / 'day6.txt', 'r') as file:
    buffer = file.readline()
 
keep_searching = True 
index = 0
char_counter = 0
packet_len = 4
while index < (len(buffer)-packet_len-1) and keep_searching:
    char_counter += 1
    chunk = buffer[index:index+packet_len]
    
    uniques = len(set(chunk))
    
    if uniques == packet_len:
        keep_searching = False
    index += 1
    
print("First occurrence: ", char_counter + packet_len-1)
    
    

#%% Second problem 
keep_searching = True 
index = 0
char_counter = 0
packet_len = 14
while index < (len(buffer)-packet_len-1) and keep_searching:
    char_counter += 1
    chunk = buffer[index:index+packet_len]
    
    uniques = len(set(chunk))
    
    if uniques == packet_len:
        keep_searching = False
    index += 1
    
print("First occurrence: ", char_counter + packet_len-1)