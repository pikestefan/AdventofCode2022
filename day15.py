# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 00:16:33 2022

@author: L
"""

import numpy as np
import re
import matplotlib.pyplot as plt

pattern = re.compile(r".* x=([-]?\d+), y=([-]?\d+).*x=([-]?\d+), y=([-]?\d+)")

with open("inputs//day15.txt", "r") as file:
    beacons = []
    sensors = []
    manhattan_dists = []
    for line in file.readlines():
        line = line.strip("")
        coordinates = pattern.match(line).groups()
        coordinates = [int(num) for num in coordinates]
        
        sensor, beacon = coordinates[0:2], coordinates[2:]
        
        manhattan_dist = abs(beacon[1]-sensor[1]) + abs(beacon[0]-sensor[0])
        
        beacons.append(beacon)
        sensors.append(sensor)
        manhattan_dists.append(manhattan_dist)
        
        
def calc_range(sensor, manhattan_dist, target_row):
    scol, srow = sensor
    
    vert_manh = abs(srow-target_row)
    
    rem_manh = manhattan_dist - vert_manh
    
    hor_range = [scol-rem_manh, scol+rem_manh] if rem_manh >= 0 else []
    
    return hor_range

def merge_ranges(range1, range2):
    range1, range2 = sorted([range1, range2])
    new_range = []
    if range1[1] >= range2[0]-1:
        left = range1[0]
        right = max(range1[1], range2[1])
        new_range = [left, right]
    return new_range

def merge_range_list(range_list):
    range_list = sorted(range_list)
    ii = 0
    while ii < len(range_list)-1:
        new_range = merge_ranges(range_list[ii], range_list[ii+1])
        if new_range:
            range_list[ii] = new_range
            range_list.pop(ii+1)
        else:
            ii += 1
    return range_list

def calc_full_range(sensors, manh_dists, target_row):
    ranges_list = []
    
    for sensor, mdist in zip(sensors, manhattan_dists):
        hrange = calc_range(sensor, mdist, target_row)
        
        if hrange:
            ranges_list.append(hrange)
            
    return sorted(ranges_list)
  
    
# %% Part1
full_ranges = calc_full_range(sensors, manhattan_dist, 11)
target_row = 200000
full_ranges = calc_full_range(sensors, manhattan_dists, target_row)
full_ranges = merge_range_list(full_ranges)

full_sensor_range = 0
counted_beacons = []
for range_chunk in full_ranges:
    full_sensor_range += (range_chunk[1] - range_chunk[0] + 1)
    for beacon, sensor in zip(beacons, sensors):
        bcol, brow = beacon
        scol, srow = sensor
        if (range_chunk[0]<=bcol<=range_chunk[1]) and (brow == target_row) and (beacon not in counted_beacons):
            full_sensor_range -= 1
            counted_beacons.append(beacon)
        if (range_chunk[0]<=scol<=range_chunk[1]) and (srow == target_row):
            full_sensor_range -= 1
            
print(f"The beacon is not in {full_sensor_range} positions")


# %% Part 2
max_beacon_range = 4000000

row_idx = 0
while row_idx <= max_beacon_range:
    full_ranges = calc_full_range(sensors, manhattan_dists, row_idx)
    
    restricted_cols = []
    for range_chunk in full_ranges:
        if range_chunk[0] < 0:
            range_chunk[0] = 0
        if range_chunk[1] > max_beacon_range:
            range_chunk[1] = max_beacon_range
        restricted_cols.append(range_chunk)     
    merged_range = merge_range_list(restricted_cols)
    
    if len(merged_range) >= 2:
        print(f"Length is {len(merged_range)}. Estimated sensor at:"
              f" {row_idx, merged_range[0][1]+1}")
        output = max_beacon_range *(merged_range[0][1]+1) + row_idx
        break
    row_idx += 1
    
    
print(f"Final results: {output}")   
    
    
    


    
