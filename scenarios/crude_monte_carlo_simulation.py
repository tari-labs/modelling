import sys, os

#Add ../utils to the Python system path
try:
    sys.path.index(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');
except ValueError:
    sys.path.append(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');

import network_setup as n_s

import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median, mode, stdev, StatisticsError
from scipy.stats import linregress

#-----------------------------------------------------------------------------
#Function definitions
#-----------------------------------------------------------------------------

# Run Experiment populating histogram of randomness 
def run_experiment(nodes, histogram, committe_size, bft_threshold, no_of_draws) -> np.float64:
    M = np.float64(0)
    for m in range(no_of_draws):
        # Create a new committee
        committee = n_s.assign_committee(nodes, committe_size, "hypergeometric-distribution")
        # Count number of times each node has been assigned to a committee
        for i in range(len(committee)):  
            j = committee[i].index
            if committee[i].malicious == True:  
                histogram[0][j] += 1
            else:
                histogram[1][j] += 1
            histogram[2][j] += 1
        # Test of committee has more malicious nodes than BFT threshold
        count = 0
        for i in range(len(committee)):
            if committee[i].malicious == True:
                count += 1
        if count >= bft_threshold: 
            M += 1
        probability = M/no_of_draws
    return probability, histogram

def run_distribution(distribution_type, total_nodes, no_of_bad_nodes, histogram, committe_size, bft_threshold, no_of_draws, no_of_experiments):
    nodes = n_s.create_network(total_nodes, [100,2500, 1], (100,2500), distribution_type, no_of_bad_nodes, committe_size)
    nodes = n_s.assign_bad_nodes(nodes, no_of_bad_nodes, distribution_type)
    #Run the experiments
    probabilities = []
    average_prob = 0;
    convergence = []
    for i in range(no_of_experiments):
        probability, histogram_of_randomness = run_experiment(nodes, histogram, \
                                                              committe_size, bft_threshold, no_of_draws)
        average_prob=((average_prob*i)+probability)/(i+1)
        probabilities.append(probability)
        convergence.append(average_prob)
    return convergence, probabilities, nodes

def plotSettings(figure_size = (12,9), line_style_grid = '-.', \
                 line_style_axis = '-.', title = " ", x_label = '', y_label = '',title_font_size = '20',font_size = '18', fontweight="bold"):
    ## Standard graph settings 
    fig, ax1 = plt.subplots(figsize=figure_size)   
    ax1.grid(True, linestyle=line_style_grid)
    ax1.xaxis.grid(True, which='minor', linestyle=line_style_axis)
    ax1.set_title(title, fontsize=title_font_size, fontweight=fontweight)
    ax1.set_xlabel(x_label, fontsize=font_size)
    ax1.set_ylabel(y_label, fontsize=font_size)
    
#-----------------------------------------------------------------------------
#Main program
#-----------------------------------------------------------------------------
debug = False

total_nodes = int(input('What is the total amount of nodes? '))
no_of_bad_nodes = int(input('What is the amount of bad nodes? '))
committe_size = int(input('How many nodes are to be drawn? '))
bft_threshold = int(input('What is the BFT threshold within the committee? '))
no_of_draws = int(input('What is the no of draws within an experiment? '))
no_of_experiments = int(input('How many experiments? ')) 
is_mean = input('Do you know theoratical mean? Y|N: ')
if is_mean == 'Y':
    theoretical_mean = float(input('What is the theoretical mean?'))
print("\n\n")

histogram_of_randomness = np.int64(np.zeros((3, total_nodes)))
"""nodes = n_s.create_network(total_nodes, [100,2500, 1], (100,2500), "hypergeometric_distribution", no_of_bad_nodes, committe_size)
nodes = n_s.assign_bad_nodes(nodes, no_of_bad_nodes, "hypergeometric_distribution")

#Run the experiments
probabilities = []
average_prob = 0;
convergence = []
for i in range(no_of_experiments):
    probability, histogram_of_randomness = run_experiment(nodes, histogram_of_randomness, \
                                                          committe_size, bft_threshold, no_of_draws)
    average_prob=((average_prob*i)+probability)/(i+1)
    probabilities.append(probability)
    convergence.append(average_prob)
"""
distributions = ['normal', 'uniform_ditribution', 'poisson', 'hypergeometric_distribution']
convergence_dict = {}
nodes_dict = {}
for distribution in distributions:
    convergence, probabilities, nodes = run_distribution(distribution, total_nodes, no_of_bad_nodes, histogram_of_randomness, committe_size, bft_threshold, no_of_draws, no_of_experiments)
    convergence_dict[distribution] = convergence
    nodes_dict[distribution] = nodes
# Plot individual probabilities  
    plotSettings(title= "Each Experiment's Individual Probability\n" + distribution ,x_label= 'Experiment No.', y_label= 'Probability')
    x = list(range(no_of_experiments))
    plt.plot(x, probabilities, marker=".")

# Fit line of best fit for all data
    if len(x) > 1:
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x, probabilities, 1))(np.unique(x)))

# Analysis of line of best fit 
        slope, intercept, r_value, p_value, std_err = linregress([x], probabilities)
        print("\n\n")
        print('Slope:', slope)
        print('Intercept:', intercept)
        print('Standard Deviation:', stdev(np.float64(probabilities))) #a quantity expressing by how much the members of a group differ from the mean value for the group.
    #plt.show()
#Debug info
if debug == True:
    print(histogram_of_randomness)
    
# Plot histogram of randomness  
plotSettings(title= "Histogram of Randomness", x_label= 'Node Index', y_label= 'Frequency of Node being Drawn')
plt.plot(np.arange(0,len(histogram_of_randomness[2])), histogram_of_randomness[2])
#plt.ylim((-1, max(histogram_of_randomness[2])))
plt.legend(loc='best')
plt.show()

# Statistics for histogram of randomness 
## Mean 
stat_mean = mean(np.float64(histogram_of_randomness[2]))
print('Mean:', stat_mean)
## Median 
stat_median = median(np.float64(histogram_of_randomness[2]))
print('Median:', stat_median)
## Mode 
try:
    stat_mode = mode(np.float64(histogram_of_randomness[2]))
    print('Mode', stat_mode)
except StatisticsError:
    print("There is no mode!")
## Standard_deviation
stat_stdev = stdev(np.float64(histogram_of_randomness[2]))
print('Standard deviation', stat_stdev)
print("\n\n")

# Plot convergence  
plotSettings(title= "Convergence Proving LLN", x_label= 'Experiment No.', y_label= 'Average Probability')
for distribution in distributions:
    plt.plot(np.arange(0,len(convergence_dict[distribution])), convergence_dict[distribution], linestyle='-', label = distribution)
if is_mean == 'Y':
    plt.axhline(y=theoretical_mean, color='b', linewidth=3, linestyle='-', label='Theoretical Mean')
plt.legend(loc='best')
plt.show()


for distribution in distributions:
# Get distribution_of_bad_nodes
    distribution_of_bad_nodes = []
    distribution_of_good_nodes = []
    for i in range(len(nodes_dict[distribution])):
        if nodes_dict[distribution][i].malicious:
	        distribution_of_bad_nodes.append(nodes_dict[distribution][i].NetworkPosition)
        else:
            distribution_of_good_nodes.append(nodes_dict[distribution][i].NetworkPosition)

#Debug info
    if debug == True:
        print (distribution_of_bad_nodes)
        print("\n\n")

# Plot position of nodes within network
    plotSettings(title= "Position of Nodes within Network\n" + distribution, x_label= 'X coordinate', y_label= 'Y coordinate')
    plt.scatter(*zip(*distribution_of_good_nodes), color = 'blue', label = 'good')
    plt.scatter(*zip(*distribution_of_bad_nodes), color = 'red', label = 'bad')
    plt.legend(loc='best')
    plt.show()