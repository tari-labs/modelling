#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:46:27 2019

This scenario sees the analysis of bad attackers with variations in the total number of nodes (300, 400, 500, 1000)
There is a fixed BFT threshold (67%), and variation in committee size is dependent on the total number of nodes. 

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


# Set number of nodes to 300 with T = 67%

no_of_nodes = 300

# Declare and initialize variables for commitee size 

committee_size_300 = []

committee_size_300_start = 10   
committee_size_300_max = 300 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_300 = np.arange(committee_size_300_start, committee_size_300_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_300 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_300 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_300)):
    P_tot_300.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_300[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_300[j], bft_threshold[j], j, P_tot_300[j]))

# Set number of nodes to 400 with T = 67%

no_of_nodes = 400

# Declare and initialize variables for commitee size 

committee_size_400 = []

committee_size_400_start = 10   
committee_size_400_max = 400 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_400 = np.arange(committee_size_400_start, committee_size_400_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_400 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_400 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_400)):
    P_tot_400.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_400[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_400[j], bft_threshold[j], j, P_tot_400[j]))

# Set number of nodes to 500 with T = 67%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500 = []

committee_size_500_start = 10  
# Reduce max size of committee to 400 
committee_size_500_max = 400 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500 = np.arange(committee_size_500_start, committee_size_500_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_500 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500)):
    P_tot_500.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500[j], bft_threshold[j], j, P_tot_500[j]))

# Set number of nodes to 1000 with T = 67%

no_of_nodes = 1000

# Declare and initialize variables for commitee size 

committee_size = []

committee_size_1000_start = 10   
# Reduce max size of committee to 400
committee_size_1000_max = 400 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_1000 = np.arange(committee_size_1000_start, committee_size_1000_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_1000 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_1000 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_1000)):
    P_tot_1000.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_1000[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_1000[j], bft_threshold[j], j, P_tot_1000[j]))

#Plots

import matplotlib.pyplot as plt

## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('Committee Size', fontsize='18')
ax1.set_ylabel('Probability of bad actors controlling the network', fontsize='18')

plt.plot(committee_size_300, P_tot_300, 'b-', label='N = 300')
plt.plot(committee_size_400, P_tot_400, 'r-', label='N = 400')
plt.plot(committee_size_500, P_tot_500, 'y-', label='N = 500')
plt.plot(committee_size_1000, P_tot_1000, 'g-', label='N = 1000')
plt.legend(loc='best')
plt.show()