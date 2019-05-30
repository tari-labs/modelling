#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:37:11 2019

What is the probability of selecting a majority of bad nodes from a total of 
8 nodes if the committee size is 3. There are 4 bad nodes and 4 good nodes. 

We perform N experiments, count how many times we get two or more bad nodes 
(M) and estimate the probability M/N.

Eash experment consists of making the total_nodes list, drawing a number of 
nodes and counting how many bad nodes were drawn.

@author: kevoulee
"""
import random
import numpy as np
import matplotlib.pyplot as plt

#node_type classifies a node as being good or bad

def draw_node(total_nodes):
#Draw a node using list index
    index = random.randint(0, len(total_nodes)-1)
    node_type = total_nodes.pop(index)
    return node_type, total_nodes

def new_nodes(total_nodes, bad_nodes, node_types):
    total_nodes_vec = []
    for i in range(total_nodes):
        total_nodes_vec.append(node_types[0])
    if bad_nodes > total_nodes: 
        return total_nodes_vec
    i = 0
    while i < bad_nodes:
        index = random.randint(0, total_nodes-1)
        if total_nodes_vec[index] != node_types[1]:
            total_nodes_vec[index] = node_types[1] 
            i += 1
    return total_nodes_vec


total_nodes = int(input('What is the total amount of nodes?'))
bad_nodes = int(input('What is the amount of bad nodes?'))
bft_threshold = int(input('What is the BFT threshold?'))
n = int(input('How many nodes are to be drawn? '))
N = int(input('How many experiments? '))


# Run experiments
node_types = 'good', 'bad'
M = 0  # no of successes
random_test = np.int64(np.zeros((2, total_nodes)))
for e in range(N):
    nodes = new_nodes(total_nodes, bad_nodes, node_types)
    for i in range(total_nodes):
        if nodes[i] == node_types[0]:
           random_test[0][i] += 1
        else:
            random_test[1][i] += 1
    print (nodes)
    for i in range(n):
        node_type, nodes = draw_node(nodes)
        print (nodes)
    if nodes.count('bad') >= bft_threshold: 
        M += 1
print ('Probability', float(M)/N)


print (random_test)

plt.hist(random_test, bins='auto')
plt.title("histogram with 'auto'bins")
plt.show()
