# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import numpy as np

inputs_path = Path('inputs')

#%% First problem

with open(inputs_path / 'day2.txt', 'r') as file:
    game = []
    for line in file.readlines():
        game.append(line.strip().replace(" ",""))

point_map = {"r": 1, "p": 2, "s": 3}

rockpapsis = ['r', 'p', 's']

pl1_map = dict(zip(['A','B','C'], rockpapsis))
pl2_map = dict(zip(['X','Y','Z'], rockpapsis))

victory_condition = ["rs", "pr", "sp"]


points = 0
for game_round in game:
    pl1, pl2 = game_round
    pl1_played, pl2_played = pl1_map[pl1], pl2_map[pl2]
    
    pl2points = point_map[pl2_played]
    if pl1_played == pl2_played:
        points +=  pl2points + 3   
    elif pl2_played+pl1_played in victory_condition:
        points += pl2points + 6
    else:
        points += pl2points
    
print("Player 2 points: ", points)

#%% Second problem 

lose_draw_win = {'r': ['s', 'r', 'p'],
                 'p': ['r', 'p', 's'],
                 's': ['p', 's', 'r']}

tot_points = 0
for game_round in game:
    pl1, instruction = game_round
    pl1_played = pl1_map[pl1]
    
    if instruction == 'X':
        index, points = 0, 0
    elif instruction =='Y':
        index, points = 1, 3
    else:
        index, points = 2, 6
        
    need_to_play = lose_draw_win[pl1_played][index]
    
    tot_points += points + point_map[need_to_play]

print("Actual points: ", tot_points)

