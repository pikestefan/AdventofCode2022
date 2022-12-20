# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

inputs_path = Path('inputs')

class cpu:
    def __init__(self, commands):
        self.commands = deepcopy(commands)
        self.X = 1
        self.clk = 0
        
        self.clktrace = []
        self.Xtrace = []
        
    def run_program(self):
        while self.commands:
            command = self.commands.pop(0)
            if command == 'noop':
                self.command_noop()
            elif command[:4] == 'addx':
                _, amt = command.split(' ')
                amt = int(amt)
                self.command_add(amt)
                
    def command_noop(self):
        self.clk += 1
        self.update_traces()
        
    def command_add(self, amt):
        self.clk += 1
        self.update_traces()
        self.X += amt
        self.clk+=1
        self.update_traces()
        
    def update_clk(self):
        self.clktrace.append(self.clk)
    
    def update_X(self):
        self.Xtrace.append(self.X)
        
    def update_traces(self):
        self.update_clk()
        self.update_X()

class gpu(cpu):
    def __init__(self, commands):
        super().__init__(commands)
        
        self.crt_w, self.crt_h = 40, 6
        
        self.image = np.zeros((self.crt_h, self.crt_w))
        
    def command_add(self, amt):
        self.clk+=1
        self.draw()
        self.update_traces()
        self.clk+=1
        self.draw()
        self.X += amt
        self.update_traces()
        
    def command_noop(self):
        super().command_noop()
        self.draw()
        
    def draw(self):
        current_col = (self.clk-1) % self.crt_w
        current_row = (self.clk-1) // self.crt_w
        print(self.clk, current_col, self.X)
        
        if (self.X-1 <= current_col <= self.X+1):
            self.image[current_row, current_col] = 1
            print("paint")
        else:
            print("no paint")

with open(inputs_path / 'day10.txt', 'r') as file:
    commands = []
    for line in file.readlines():
        commands.append(line.strip())
#%% First problem

program = cpu(commands)
program.run_program()

desired_cycles = [20 + ii*40 for ii in range(6)]

selected_cycles = []
for ii, cycle in enumerate(program.clktrace):
    if cycle in desired_cycles:
        selected_cycles.append([cycle, program.Xtrace[ii-1]])

sig_strength = sum([cycle*Xval for cycle, Xval in selected_cycles]) 

print("Signal strength:", sig_strength)

#%% Second problem 
image_program = gpu(commands)
image_program.run_program()

plt.figure(figsize = (10,10))
plt.imshow(image_program.image, aspect = 'equal')
