# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 21:46:46 2022

@author: L
"""

import re
from copy import deepcopy

def mysum(c1,c2):
    return c1+c2

def myprod(c1, c2):
    return c1*c2

class monkeyclass:
    operation_dict = {"*": myprod,
                      "+": mysum}
    def __init__(self, items, operation, divtest, target_monkeys):
        self.items=items
        self.c1, self.op, self.c2 = operation
        if self.c1.isdigit():
            self.c1 = int(self.c1)
        else:
            self.c1 = None
        if self.c2.isdigit():
            self.c2 = int(self.c2)
        else:
            self.c2 = None
        self.op = self.operation_dict[self.op]
        self.divtest = divtest
        self.truetgt, self.falsetgt = target_monkeys
        self.inspection_counter = 0
        self.reduce_worry_lvl = True
        self.tot_divtests = 0
        
    def do_operation(self):
        item = self.items.pop(0)
        self.inspection_counter += 1
        if self.c1:
            c1 = self.c1
        else:
            c1 = item
        if self.c2:
            c2 = self.c2
        else:
            c2 = item
        return self.op(c1, c2)
    
    def take_divtest(self, item):
        if item % self.divtest == 0:
            tgt_monkey = self.truetgt
        else:
            tgt_monkey = self.falsetgt
        return tgt_monkey
    
    def turn(self):
        items_to_throw = []
        while len(self.items):
            item = self.do_operation()
            if self.reduce_worry_lvl:
                item //= 3
            if item % self.tot_divtests:
                item %= self.tot_divtests
            tgt_monkey = self.take_divtest(item)
            items_to_throw.append([tgt_monkey, item])
        return items_to_throw
    
    def get_item(self, item):
        self.items.append(item)
            

 
def monkey_round(monkey_list, narrate_round=False):
    for monkey in monkey_list:
        thrown_items = monkey.turn()
        for target, item in thrown_items:
            monkey_list[target].get_item(item)
        
    if narrate_round:
        for ii, monkey in enumerate(monkey_list):
            print(f"Monkey {ii} has: {monkey.items}\n")
            
        print("\n")
            
            

greedy_matcher = re.compile("Monkey \d+:"
                            "\s*Starting items: ((?:\d+, )*\d+)"
                            "\s*Operation: new = (\w+ [+*] \w+)"
                            "\s*Test: divisible by (\d+)"
                            "\s*If true: throw to monkey (\d+)"
                            "\s*If false: throw to monkey (\d+)")

start_monkeys = []
with open(r'inputs/day11.txt', 'r') as file:
    curr_monkey_info = ""
    
    keep_going = True
    
    tot_division_tests = 1
    while keep_going:
        line = file.readline()
        if line != "\n" and line !="":
            curr_monkey_info += line
        else:
            matched = greedy_matcher.match(curr_monkey_info)
            if matched:
                items, ops, divtest, truetgt, falsetgt = matched.groups()
                newmonkey = monkeyclass(list(map(int, items.split(","))),
                                        ops.split(" "),
                                        int(divtest),
                                        [int(truetgt), int(falsetgt)])
                start_monkeys.append(newmonkey)
                tot_division_tests *= int(divtest)
            curr_monkey_info = ""
        
        if line == "":
            keep_going = False
        
for monkey in start_monkeys:
    monkey.tot_divtests = tot_division_tests
        
# %% First problem
monkeys = deepcopy(start_monkeys)

turns = 20
for turn in range(turns):
    monkey_round(monkeys, narrate_round=False)

activities = sorted([monkey.inspection_counter for monkey in monkeys])
print("Top activity product:", activities[-2]*activities[-1])

# %% Second problem
monkeys = start_monkeys
for monkey in monkeys:
    monkey.reduce_worry_lvl = False
    
turns = 10000
for turn in range(turns):
    monkey_round(monkeys, narrate_round=False)

activities = sorted([monkey.inspection_counter for monkey in monkeys])
print("Top activity product:", activities[-2]*activities[-1])
