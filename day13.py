# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:05:23 2022

@author: L
"""

from pathlib import Path
import ast
inputs_path = Path('inputs')

def compare(pair1, pair2):
    keep_going = True
    right_order = None
    ii = 0
    #print("Compare",pair1,"vs",pair2)
    
    while keep_going:
        if (ii == len(pair1) and ii < len(pair2)):
            right_order = True
        elif (ii == len(pair2) and ii < len(pair1)):
            right_order = False
        elif (ii == len(pair2) and ii == len(pair1)):
            keep_going = False
        else:
            elm1, elm2 = pair1[ii], pair2[ii]
            #print(" -Compare",elm1,"vs",elm2)
            if not isinstance(elm1, list) and not isinstance(elm2, list):
                if elm1 < elm2:
                    right_order = True
                elif elm1 > elm2:
                    right_order = False
            else:
                if not isinstance(elm1, list):
                    elm1 = [elm1]
                
                if not isinstance(elm2, list):
                    elm2 = [elm2]
                    
                right_order = compare(elm1, elm2)
        
        if right_order is not None:
            keep_going = False
        ii += 1
        
    return right_order

with open(inputs_path / 'day13.txt', 'r') as file:
    lines = file.readlines()
    
    pair_list = []
    full_pairs = []
    for jj in range(0,len(lines), 3):
        pair = lines[jj:jj+2]
        translated_pairs = list(map(ast.literal_eval, pair)) 
        pair_list.append( translated_pairs )
        
        full_pairs += translated_pairs
    
#%% First problem
right_orders = []
for pair in pair_list:
    left, right = pair
    output_comparison = compare(left, right)
    # print("In order:",output_comparison)
    right_orders.append(output_comparison)
    
    
right_order_sum = 0
for ii, truth_val in zip(range(len(right_orders)), right_orders):
    if truth_val:
        right_order_sum += ii+1
    
print("Sum indices: ", right_order_sum)


#%% Second problem 
divider_packets = [[[2]], [[6]]]
full_pairs += divider_packets
iternum = 0
iters = 1000
keep_going = True

while iternum < iters and keep_going:
    all_ordered = True
    
    for ii in range(0, len(full_pairs)-1, 1):
        left, right = full_pairs[ii:ii+2]
        
        ordered = compare(left, right)
        all_ordered = all_ordered and ordered
        
        if not ordered:
            full_pairs[ii] = right[:]
            full_pairs[ii+1] =  left[:]
    iternum+=1
    if all_ordered:
        keep_going = False
        
packet_idx = []   
for ii, ordered_item in enumerate(full_pairs):
    if ordered_item in divider_packets:
        packet_idx.append(ii+1)

print("Packet product:", packet_idx[0]*packet_idx[1])
        
    
