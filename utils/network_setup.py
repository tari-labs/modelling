import sys, os

#Add ../utils to the Python system path
try:
    sys.path.index(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');
except ValueError:
    sys.path.append(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');

import rand_dist as r_d

import numpy as np

class Network:
    def __init__(self, rangeX, rangeY, qty, radius = 1):
        #Runtime type checking
        type_error = True
        if type(rangeX) is list:
            if len(rangeX) == 2:
                if rangeX[0] < rangeX[1]:
                    type_error = False
        if type_error == False:
            print("\nError! class Network: rangeX must be of type \'list\' size 2")
            rangeX = [0, qty*10]
            print("       Resetted \'rangeX\' to: %s\n" % (rangeX))
        type_error = True
        if type(rangeY) is list:
            if len(rangeY) == 2:
                if rangeY[0] < rangeY[1]:
                    type_error = False
        if type_error == False:
            print("\nError! class Network: rangeY must be of type \'list\' size 2")
            rangeY = [0, qty*10]
            print("       Resetted \'rangeY\' to: %s\n" % (rangeY))
        #Init
        self.radius = radius 
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.qty = qty
        self.network_nodes = []
        for i in range(self.qty):
            self.network_nodes.append(node())
        
    # Generate a set of all points within `radius` of the origin
    def generate_coordinates(self, distribution_type):
        deltas = set()
        for x in range(-self.radius, self.radius+1): 
            for y in range(-self.radius, self.radius+1): 
                if x*x + y*y <= self.radius*self.radius: 
                    deltas.add((x,y))
        randPoints = []
        excluded = set()
        i = 0
        while i < self.qty:
            x = r_d.get_random_index(distribution_type, self.rangeX[0], self.rangeX[1])
            y = r_d.get_random_index(distribution_type, self.rangeY[0], self.rangeY[1])
            if (x,y) in excluded: continue 
            randPoints.append((x,y))
            i += 1
            excluded.update((x+dx, y+dy) for (dx,dy) in deltas)
        return randPoints

    #Assign node characteristics
    def assign_characteristics(self, distribution_type):
        #Assign coordinates
        randPoints = self.generate_coordinates(distribution_type)
        i = 0
        for _node in self.network_nodes:
            _node.updatePosition(randPoints[i])
            i += 1
        #Assign node_id to the node
        self.vec = [-1 for i in range(self.qty)] #create an empty vector
        exit_condition = np.int64(0)
        for i in range(len(self.network_nodes)): 
            while self.vec[i] < 0 and exit_condition < len(self.network_nodes) * 1000:
                exit_condition += 1      
                node_id = r_d.get_random_index(distribution_type, 1e6, 1e7)
                if self.vec.count(node_id) == 0: #If the number has not been repeated 
                    self.network_nodes[i].node_id = node_id
                    self.vec[i] = node_id
        #Assign index to the node
        for i in range(len(self.network_nodes)): #iterate to the range of the network nodes length 
            self.network_nodes[i].index = i
            
    def getNetworkNodes(self):
        return self.network_nodes
    
# Create class node 
class node:
    malicious = False
    node_id = -1
    index = -1
    def __init__(self, networkPosition = (0, 0)):
        self.NetworkPosition = networkPosition
    
    def updatePosition(self, nodePosition):
        self.NetworkPosition = nodePosition

# Create the network 
def create_network(total_nodes, rangeX, rangeY, distribution_type):
    # Initialize basic network of nodes
    _np = Network(rangeX, rangeY, qty = total_nodes)
    #Assign node characteristics
    _np.assign_characteristics(distribution_type)
    return _np.getNetworkNodes()

# Assign random nodes as being bad 
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
        index = r_d.get_random_index(distribution_type, 0, len(network_nodes)-1)
        if network_nodes[index].malicious != True:
            network_nodes[index].malicious = True
            count += 1
    #print ('\nrepeat_factor: ', (exit_condition/len(network_nodes)))
    return network_nodes

# Draw a committee 
def assign_committee(network_nodes, committee_size, distribution_type):
    # If committee size = total nodes in network
    if committee_size >= len(network_nodes) :
        return network_nodes
    # If committee size < total nodes in network
    exit_condition = np.int64(0)
    count = 0
    committee = []
    while count < committee_size-1 and exit_condition < len(network_nodes) * 1000:
        exit_condition += 1
        # Draw node at random
        node_index = r_d.get_random_index(distribution_type, 0, len(network_nodes)-1)
        # Assign node if committee size = 0
        if len(committee) < 1:
            committee.append(network_nodes[node_index])
        # Assign node if not already assigned
        else:
            found = False
            # Test if node already assigned
            for i in range(len(committee)):
                if committee[i].node_id == network_nodes[node_index].node_id:
                    found = True
                    break
            # Assign node to committee if not assigned
            if found == False:
                committee.append(network_nodes[node_index])
                count += 1
    # Test if duplicates exist
    if len(committee) != len(set(committee)):
        committee = []
        print('Error! Duplicates nodes found in the proposed committee, committee not assigned.')
    return committee
