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


# Set number of nodes to 500 with T = 50%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500_50 = []

committee_size_500_50_start = 10  
 # Reduce max size of committee to 400
committee_size_500_50_max = 400

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500_50 = np.arange(committee_size_500_50_start, committee_size_500_50_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.50

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_500_50 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500_50 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500_50)):
    P_tot_500_50.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500_50[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500_50[j], bft_threshold[j], j, P_tot_500_50[j]))
    

# Set number of nodes to 500 with T = 55%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500_55 = []

committee_size_500_55_start = 10  
 # Reduce max size of committee to 400
committee_size_500_55_max = 400

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500_55 = np.arange(committee_size_500_55_start, committee_size_500_55_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.55

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_500_55 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500_55 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500_55)):
    P_tot_500_55.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500_55[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500_55[j], bft_threshold[j], j, P_tot_500_55[j]))
    
# Set number of nodes to 500 with T = 60%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500_60 = []

committee_size_500_60_start = 10  
 # Reduce max size of committee to 400
committee_size_500_60_max = 400

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500_60 = np.arange(committee_size_500_60_start, committee_size_500_60_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.60

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_500_60 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500_60 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500_55)):
    P_tot_500_60.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500_60[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500_60[j], bft_threshold[j], j, P_tot_500_60[j]))

# Set number of nodes to 500 with T = 65%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500_65 = []

committee_size_500_65_start = 10  
# Reduce max size of committee to 400 
committee_size_500_65_max = 400 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500_65 = np.arange(committee_size_500_65_start, committee_size_500_65_max + 1, incr)

# Create and Initialize scenario variables 

## Percentage of Bad actors 

bad_actors_percentage = 0.6


## BFT threshold percentage 

bft_threshold = []
bft_threshold_percentage = 0.65

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))

## Calculate the BFT threshold (product of committee size (n) and BFT threshold percentage, round up)

bft_threshold = np.int_(np.ceil(committee_size_500_65 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500_65 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500_65)):
    P_tot_500_65.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500_65[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500_65[j], bft_threshold[j], j, P_tot_500_65[j]))
    
# Set number of nodes to 500 with T = 67%

no_of_nodes = 500

# Declare and initialize variables for commitee size 

committee_size_500_67 = []

committee_size_500_67_start = 10  
# Reduce max size of committee to 400 
committee_size_500_67_max = 400 

## Node increment 

incr = 10                 

## Create nodes array 

committee_size_500_67 = np.arange(committee_size_500_67_start, committee_size_500_67_max + 1, incr)

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

bft_threshold = np.int_(np.ceil(committee_size_500_67 * bft_threshold_percentage))

# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_500_67 = []
print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(committee_size_500_67)):
    P_tot_500_67.append(hdp.probability(bft_threshold[j], no_of_bad_actors, committee_size_500_67[j], no_of_nodes))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
        (no_of_nodes, no_of_bad_actors, committee_size_500_67[j], bft_threshold[j], j, P_tot_500_67[j]))

#Plots

import matplotlib.pyplot as plt

## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('Committee Size', fontsize='18')
ax1.set_ylabel('Probability of bad actors controlling the network', fontsize='18')


plt.plot(committee_size_500_50, P_tot_500_50, 'c-', label='T = 50')
plt.plot(committee_size_500_55, P_tot_500_55, 'm-', label='T = 55')
plt.plot(committee_size_500_60, P_tot_500_60, 'k-', label='T = 60')
plt.plot(committee_size_500_65, P_tot_500_65, 'r-', label='T = 65')
plt.plot(committee_size_500_67, P_tot_500_67, 'y-', label='T = 67')
plt.legend(loc='best')
plt.show()