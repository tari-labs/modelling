#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:37:11 2019

What is the probability of selecting a majority of bad nodes from a total of 
5 nodes if the committee size is 3. There are 3 bad nodes and 2 good nodes 

@author: kevoulee
"""
import random

def total_nodes(): #make total_nodes with 5 nodes 
    total_nodes = []
    for node_type in 'bad' 'good':
 #       for i in the range(total_nodes):
            total.append(node_type)
    return total 

def committee_size(total):
    index = random.randint(0, len(total_nodes))
    node_type = total_nodes[index];  del total_nodes[index]
    return node_type

# run experiments:
n = input('How many nodes in the committee_size? ')
N = input('How many experiments? ')
M = 0  # no of successes

for e in range(N):
    nodes = []         # the n nodes we draw
    for i in range(n):
        node_type, total_nodes = commitee_size(total_nodes)
        nodes.append(node_type)
    if nodes.count('bad') >= 2:  # two bad nodes or more
        M += 1
print 'Probability:', float(M)/N