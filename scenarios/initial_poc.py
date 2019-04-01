#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:46:27 2019

@author: kevoulee
"""

#!/usr/bin/python

import sys, os

#Add ../utils to the Python system path
try:
    sys.path.index(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');
except ValueError:
    sys.path.append(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');

import hyper_dist_prob as hdp

import numpy as np
from IPython import get_ipython
get_ipython().magic('clear')


# Declare and initialize variables 

no_of_nodes = []

no_of_nodes_start = 1  
no_of_nodes_max = 100 

## Node increment 

incr = 1                 

## Create nodes array 

no_of_nodes = np.arange(no_of_nodes_start, no_of_nodes_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

no_of_bad_actors = []
bad_actors_percentage = 0.6

## Percentage of Committee size

committee_size = []
committee_size_percentage = 0.6

## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.5

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the committee size (product of Total nodes (N) and Committee size percentage, round up)

committee_size = np.int_(np.ceil(no_of_nodes * committee_size_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot = []
for j in range(0, len(no_of_nodes)):
    P_tot.append(hdp.probability(bft_threshold[j], no_of_bad_actors[j], committee_size[j], no_of_nodes[j]))
    print(' %3s  %3s  %3s  %3s    j=%3s     P_tot= %-20s' % \
        (no_of_nodes[j], no_of_bad_actors[j], committee_size[j], bft_threshold[j], j, P_tot[j]))

import matplotlib.pyplot as plt

#Plots

fig, ax1 = plt.subplots(figsize=(12,9))   
ax2 = ax1.twinx()

ax1.set_xlabel('Total of Network Nodes', fontsize='18')
ax1.set_ylabel('Probability of bad actors controlling the network', fontsize='18')
ax2.set_ylabel('Number of nodes', fontsize='18')
ax1.tick_params(axis='both', labelsize='14')
ax2.tick_params(axis='both', labelsize='14')
 
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

x = no_of_nodes
y1 = P_tot
y2 = no_of_bad_actors
y3 = committee_size
y4 = bft_threshold

ax1.plot(x, y1, 'g-', label='Probability')
ax2.plot(x, y2, 'b-', label='No of bad actors')
ax2.plot(x, y3, 'r-', label='Committee size')
ax2.plot(x, y4, 'y-', label='BFT threshold')
ax1.legend(fontsize='16', loc=3)
ax2.legend(fontsize='16', loc=4)
