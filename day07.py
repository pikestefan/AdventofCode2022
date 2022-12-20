# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import re

inputs_path = Path('inputs')

class folder:
    def __init__(self, name = None, parent = None):
        self.name = name
        self.parent = parent
        self.folders = dict()
        self.files = dict()
    
    def add_folder(self, folder):
        self.folders[folder.name] = folder
        
    def add_file(self, file):
        self.files[file.name] = file
        
    def size(self):
        tot_size = 0
        stack_size = []
        for file in self.files.values():
            tot_size += file.size()
        for subfolder in self.folders.values():
            previous_tot, prev = subfolder.size()
            tot_size += previous_tot
            stack_size += prev
        stack_size.append(tot_size)
        return tot_size, stack_size
        
class fileclass:
    def __init__(self, name, size):
        self.name = name
        self._size = size
        
    def size(self):
        return self._size

#%% First problem

with open(inputs_path / 'day7.txt', 'r') as file:
    shell_io = [line.strip() for line in file.readlines()]
    
directories = dict()
command_pattern = r"(\$ cd (.*)|\$ ls)"
directory_lst = "$ ls"


match = re.match(command_pattern, shell_io[0])
folder_name = match.group(2)
parent_folder = folder(folder_name)

current_folder = parent_folder
index = 1
while index < len(shell_io):
    line = shell_io[index]
    match = re.match(command_pattern, line)
    if match and match.group(0) != r"$ ls":
        request = match.group(2)
        if request != "..":
            current_folder = current_folder.folders[request]
        else:
            current_folder = current_folder.parent
        #print(directory_tracker)
    elif match and match.group(1) == r"$ ls":
        index += 1
        keep_going = True
        while (index < len(shell_io)) and keep_going:
            line = shell_io[index]
            
            if line[:3] == 'dir':
                new_folder = folder(line[4:], parent=current_folder)
                current_folder.add_folder(new_folder)
            else:
                filesize, filename = line.split(' ')
                new_file = fileclass(filename, int(filesize))
                current_folder.add_file(new_file)
            if (index+1 < len(shell_io)) and shell_io[index+1][0] == "$":
                keep_going = False
            else:
                index += 1
            
    index+=1
    
total_size, stack_size = parent_folder.size()

below_100000 = [element for element in stack_size if element <= 100000]
print("Total sum below 100000: ", sum(below_100000))



#%% Second problem 
tot_disk_space = 70000000
required_space = 30000000

sorted_stack = sorted(stack_size)

unused_space = tot_disk_space - sorted_stack[-1]

deletable = [memory for memory in sorted_stack if (unused_space + memory)>=required_space]

print("Memory freed up by smallest: ", deletable[0])
