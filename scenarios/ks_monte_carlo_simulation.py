#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:58:06 2019

@author: kevoulee
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median, mode, stdev 

#create class node 
class node:
    malicious = False
    node_id = -1
    index = -1
    def __init__(self, networkPosition = (0, 0)):
        self.NetworkPosition = networkPosition
        
def create_network(total_nodes, distribution_type):
    #Create basic nodes in the network
    _np = NetworkPosition(qty = total_nodes)
    randPoints = _np.generate_coordinates()
    network_nodes = [node(randPoints[i]) for i in range(total_nodes)]
    vec = [-1 for i in range(total_nodes)] #create an empty vector
    exit_condition = np.int64(0)
    #Assign node_id to the node
    vec = [-1 for i in range(total_nodes)] #create an empty vector
    for i in range(len(network_nodes)): 
        while vec[i] < 0 and exit_condition < len(network_nodes) * 1000:
            exit_condition += 1      
            node_id = get_random_index(distribution_type, 1e6, 1e7)
            if vec.count(node_id) == 0: #If the number has not been repeated 
                network_nodes[i].node_id = node_id
                vec[i] = node_id
    #Assign index to the node
    for i in range(len(network_nodes)): #iterate to the range of the network nodes length 
        network_nodes[i].index = i
    #return assigned vector of nodes
    return network_nodes

def get_random_index(distribution_type, lower_bound, upper_bound):
    index = np.int64(0)
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        index = random.randint(lower_bound, upper_bound)
    elif distribution_type == "normal":
        index = random.randint(lower_bound, upper_bound)  # ToDo: change to normal
    else:
        index = random.randint(lower_bound, upper_bound)  # ToDo: Add more options here
    return index

def assign_bad_nodes(network_nodes, bad_nodes, distribution_type):
    # If all nodes are bad
    if bad_nodes >= len(network_nodes) :
        for i in range(len(network_nodes)):
            network_nodes[i].malicious = True
        return network_nodes
    #If some nodes are bad
    exit_condition = np.int64(0)
    count = 0
    while count < bad_nodes and exit_condition < len(network_nodes) * 1000:
        exit_condition += 1
        index = get_random_index(distribution_type, 0, len(network_nodes)-1)
        if network_nodes[index].malicious != True:
            network_nodes[index].malicious = True
            count += 1
    #print ('\nrepeat_factor: ', (exit_condition/len(network_nodes)))
    return network_nodes

def assign_committee(network_nodes, committee_size, distribution_type):
    # If committee size = total nodes in network
    if committee_size >= len(network_nodes) :
        return network_nodes
    #If committee size < total nodes in network
    exit_condition = np.int64(0)
    count = 0
    committee = []
    while count < committee_size-1 and exit_condition < len(network_nodes) * 1000:
        exit_condition += 1
        #Draw node at random
        node_index = get_random_index(distribution_type, 0, len(network_nodes)-1)
        #Assign node if committee size = 0
        if len(committee) < 1:
            committee.append(network_nodes[node_index])
        #Assign node if not already assigned
        else:
            found = False
            #Test if node already assigned
            for i in range(len(committee)):
                if committee[i].node_id == network_nodes[node_index].node_id:
                    found = True
                    break
            #Assign node to committee if not assigned
            if found == False:
                committee.append(network_nodes[node_index])
                count += 1
    #Test if duplicates exist
    if len(committee) != len(set(committee)):
        committee = []
        print('Error! Duplicates nodes found in the proposed committee, committee not assigned.')
    return committee

#Create class NetworkPosition
class NetworkPosition:

#Create a function for the class 
	def __init__(self, radius = 1, maxRangeX = 2500, maxRangeY = 2500, qty = 100):
		self.radius = radius 
		self.rangeX = (0, maxRangeX) 
		self.rangeY = (0, maxRangeY) 
		self.qty = qty  
        
	def generate_coordinates(self):
		#Generate a set of all points within 1 of the origin
		deltas = set()
		for x in range(-self.radius, self.radius+1): 
			for y in range(-self.radius, self.radius+1): 
				if x*x + y*y <= self.radius*self.radius: 
					deltas.add((x,y))

		randPoints = []
		excluded = set()
		i = 0
		while i < self.qty:
			x = random.randrange(*self.rangeX)  
			y = random.randrange(*self.rangeY) 
			if (x,y) in excluded: continue 
			randPoints.append((x,y))
			i += 1
			excluded.update((x+dx, y+dy) for (dx,dy) in deltas)

		return randPoints

total_nodes = int(input('What is the total amount of nodes? '))
bad_nodes = int(input('What is the amount of bad nodes? '))
bft_threshold = int(input('What is the BFT threshold? '))
n = int(input('How many nodes are to be drawn? '))
start = int(input('How many experiments start? '))  
end = int(input('How many experiments end? '))  


_np = NetworkPosition()
randPoints = _np.generate_coordinates()
print(randPoints)

#Run experiments

def run_experiment(total_nodes, bad_nodes, bft_threshold, n, N):
    # Run experiments
    #node_types = 'good', 'bad'
    M = 0  # no of successes
    #max_value = 0
    histogram_of_randomness = np.int64(np.zeros((3, total_nodes)))
    # Create network
    nodes = create_network(total_nodes, "uniform_ditribution")
    # Assign bad nodes
    nodes = assign_bad_nodes(nodes, bad_nodes, "uniform_ditribution")
#    print('\nnodes = assign_bad_nodes(nodes, bad_nodes, "uniform_ditribution")\n')
#    for i in range(len(nodes)):
#        print('Node %s, node ID %s, position_in_network %s, malicious %s' % (
#            nodes[i].index, nodes[i].node_id, nodes[i].position_in_network, nodes[i].malicious))
#    print('\n')
    #Experiment
    for k in range(N):
        # Create committe
        committee = assign_committee(nodes, n, "uniform_ditribution")
        #    print ('\ncommittee = assign_committee(nodes, n, "uniform_ditribution")\n')
        #    for i in range(len(committee)):
        #        print ('Committee %s, node ID %s, position_in_network %s, malicious %s' % (i, nodes[i].node_id, committee[i].position_in_network, committee[i].malicious))
        #    print ('\n')
        # Create histogram to test random function
        for i in range(len(committee)):  
            j = committee[i].index
            if committee[i].malicious == True:  
                histogram_of_randomness[0][j] += 1
            else:
                histogram_of_randomness[1][j] += 1
            histogram_of_randomness[2][j] += 1
        # Count malicious nodes
        count = 0
        for i in range(len(committee)):
            if committee[i].malicious == True:
                count += 1
        # Test of committe has more malicious nodes than BFT threshold
        if count >= bft_threshold:
            M += 1

    #Probability of control
    print('\nProbability %s\n' % (float(M) / N))
    return float(M)/ N, histogram_of_randomness, nodes

#Graph of no of experiments vs probability to see convergence (law of large numbers)

x = list(range(start, end))
y = []
for i in range(start, end):
    probability, histogram_of_randomness, nodes = run_experiment(total_nodes, bad_nodes, bft_threshold, n, i)
    y.append(probability)
#print(x)
#print(y)

## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('No. of Experiments', fontsize='18')
ax1.set_ylabel('Probabilities', fontsize='18')
plt.plot(x,y)

# Fit line of best fit for all data
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))

# Analysis of best fit line
#print('intercept: ', )
# Histogram of randomness  

print (histogram_of_randomness)

## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('Index', fontsize='18')
ax1.set_ylabel('histogram_of_randomness', fontsize='18')

x = np.arange(0,len(histogram_of_randomness[2]))
y = histogram_of_randomness[2]

plt.plot(x, y)
plt.ylim((-1, max(histogram_of_randomness[2])))
plt.legend(loc='best')
plt.show()

# Statistics for histogram of randomness 
## Mean 
stat_mean = mean(histogram_of_randomness[2])
print('Mean:', stat_mean)

## Median 
stat_median = median(histogram_of_randomness[2])
print('Median:', stat_median)

## Mode 
stat_mode = mode(histogram_of_randomness[2])
print('Mode', stat_mode)

## Standard_deviation
stat_stdev = stdev(histogram_of_randomness[2])
print('Standard deviation', stat_stdev)

# Get distribution_of_bad_nodes
## Distribution_of_bad_nodes = [-1 for i in range(len(nodes))]
distribution_of_bad_nodes = []
distribution_of_good_nodes = []
for i in range(len(nodes)):
    if nodes[i].malicious:
	    distribution_of_bad_nodes.append(nodes[i].NetworkPosition)
    else:
        distribution_of_good_nodes.append(nodes[i].NetworkPosition)
print (distribution_of_bad_nodes)

# Distribution of Bad Nodes 
## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('X coordinate', fontsize='18')
ax1.set_ylabel('Y coordinate', fontsize='18')

#x = np.arange(0,len(distribution_of_bad_nodes))
#y = distribution_of_bad_nodes

# Scatter Plot 
plt.scatter(*zip(*distribution_of_good_nodes), color = 'blue', label = 'good')
plt.scatter(*zip(*distribution_of_bad_nodes), color = 'red', label = 'bad')
plt.legend(loc='best')
plt.show()