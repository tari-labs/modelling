#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:58:06 2019

@author: kevoulee
"""

import random
import numpy as np
import matplotlib.pyplot as plt

#this function packs a list of values into a string representation of the 
#specified type. The arguments must match the values required by the format exactly. 
#converts to bytes format


#the creation of a node 
class node:
    position_in_network = -1  #This represents then node ID
    malicious = False
    node_id = -1
        
def create_network(total_nodes, distribution_type):
    #Create basic nodes in the network
    network_nodes = [node() for i in range(total_nodes)]
    vec = [-1 for i in range(total_nodes)]
    exit_condition = np.int64(0)
    #Assign network position to the nodes
    for i in range(len(network_nodes)): 
        while vec[i] < 0 and exit_condition < len(network_nodes) * 1000:
            exit_condition += 1      
            index = get_random_index(distribution_type, 0, len(network_nodes)-1)
            if vec.count(index) == 0: #If not found
                network_nodes[i].position_in_network = index
                vec[i] = index
    #Assign node_id to the node
    vec = [-1 for i in range(total_nodes)]
    for i in range(len(network_nodes)): 
        while vec[i] < 0 and exit_condition < len(network_nodes) * 1000:
            exit_condition += 1      
            index = get_random_index(distribution_type, 1e6, 1e7)
            if vec.count(index) == 0: #If not found
                network_nodes[i].node_id = index
                vec[i] = index
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
    print ('repeat_factor: ', (exit_condition/len(network_nodes)))
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

total_nodes = int(input('What is the total amount of nodes?'))
bad_nodes = int(input('What is the amount of bad nodes?'))
bft_threshold = int(input('What is the BFT threshold?'))
n = int(input('How many nodes are to be drawn? '))
N = int(input('How many experiments? '))


# Run experiments
node_types = 'good', 'bad'
M = 0  # no of successes
max_value = 0
histogram_of_randomness = np.int64(np.zeros((3, total_nodes)))
#Create network
nodes = create_network(total_nodes, "uniform_ditribution")
#Assign bad nodes
nodes = assign_bad_nodes(nodes, bad_nodes, "uniform_ditribution")
print ('\nnodes = assign_bad_nodes(nodes, bad_nodes, "uniform_ditribution")\n')
for i in range(len(nodes)):
    print ('Node %s, node ID %s, position_in_network %s, malicouos %s' % (i, nodes[i].node_id, nodes[i].position_in_network, nodes[i].malicious))
print ('\n')
#Experiment
for e in range(N):
    #Create committe
    committee = assign_committee(nodes, n, "uniform_ditribution")
#    print ('\ncommittee = assign_committee(nodes, n, "uniform_ditribution")\n')
#    for i in range(len(committee)):
#        print ('Committee %s, node ID %s, position_in_network %s, malicouos %s' % (i, nodes[i].node_id, committee[i].position_in_network, committee[i].malicious))
#    print ('\n')
    #Create histogram to test random function 
    for i in range(len(committee)):
        if committee[i].malicious == True:
           histogram_of_randomness[0][i] += 1
        else:
            histogram_of_randomness[1][i] += 1
        if histogram_of_randomness[0][i] > max_value:
            max_value = histogram_of_randomness[0][i]
        if histogram_of_randomness[1][i] > max_value:
            max_value = histogram_of_randomness[1][i]   
        histogram_of_randomness[2][i] += 1
    #Count malicious nodes
    count = 0
    for i in range(len(committee)):
        if committee[i].malicious == True:
            count += 1
    #Test of committe has mpore malicious nodes than BFT threshold
    if count >= bft_threshold: 
        M += 1

#Probability of control
print ('Probability', float(M)/N)


print (histogram_of_randomness)

"""
## Standard graph settings 
fig, ax1 = plt.subplots(figsize=(12,9))   
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('Index', fontsize='18')
ax1.set_ylabel('histogram_of_randomness', fontsize='18')


A = histogram_of_randomness[1]
x = np.arange(0,len(histogram_of_randomness[0]))

plt.plot(x, A, 'b-')
plt.ylim((0, max_value))
plt.legend(loc='best')
plt.show()
"""