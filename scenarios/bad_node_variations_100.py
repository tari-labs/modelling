## Create nodes array 

no_of_nodes = np.arange(no_of_nodes_start, no_of_nodes_max + 1, incr)

# Quantify Committee size

committee_size_80 = 100

# Create and Initialize scenario variables 

## Percentage of Bad actors 

no_of_bad_actors = []
bad_actors_percentage = 0.8

## Quantify BFT threshold

bft_threshold = 67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))


# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_80 = []
#print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(no_of_nodes)):
    P_tot_80.append(hdp.probability(bft_threshold, no_of_bad_actors[j], committee_size_80, no_of_nodes[j]))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
       (no_of_nodes[j], no_of_bad_actors[j], committee_size_80, bft_threshold, j, P_tot_80[j]))

# Set environment with m = 90%
# Declare and initialize variables 

no_of_nodes = []

no_of_nodes_start =100
no_of_nodes_max = 20000

## Node increment 

incr = 1000

## Create nodes array 

no_of_nodes = np.arange(no_of_nodes_start, no_of_nodes_max + 1, incr)

# Quantify Committee size

committee_size_90 = 100

# Create and Initialize scenario variables 

## Percentage of Bad actors 

no_of_bad_actors = []
bad_actors_percentage = 0.9

## Quantify BFT threshold

bft_threshold = 67

# Populate input arrays 

## Calculate the number of Bad actors (product of total nodes (N) and Bad actors percentage, round down)

no_of_bad_actors = np.int_(np.floor(no_of_nodes * bad_actors_percentage))


# Calculate the total probability of bad actors controlling the committee, starting from the BFT threshold 
# up to the committee size 

P_tot_90 = []
#print('Tot_nodes Bad_nodes Committee Threshold  index   Probability to control')
for j in range(0, len(no_of_nodes)):
    P_tot_90.append(hdp.probability(bft_threshold, no_of_bad_actors[j], committee_size_90, no_of_nodes[j]))
    print('    %3s      %3s        %3s     %3s      j=%3s   P_tot= %-20s' % \
       (no_of_nodes[j], no_of_bad_actors[j], committee_size_90, bft_threshold, j, P_tot_90[j]))

#Plots

import matplotlib.pyplot as plt

## Standard graph settings

fig, ax1 = plt.subplots(figsize=(12,9))
ax1.grid(True, linestyle='-.')
ax1.xaxis.grid(True, which='minor', linestyle='-.')

ax1.set_xlabel('Total Nodes', fontsize='18')
ax1.set_ylabel('Probability of bad actors controlling the network', fontsize='18')
ax1.set_title('Bad actor variation when committee size = 100')

plt.plot(no_of_nodes, P_tot_10, 'c-', label='m = 10%')
plt.plot(no_of_nodes, P_tot_20, 'c-', label='m = 20%')
plt.plot(no_of_nodes, P_tot_30, 'm-', label='m = 30%')
plt.plot(no_of_nodes, P_tot_40, 'k-', label='m = 40%')
plt.plot(no_of_nodes, P_tot_50, 'r-', label='m = 50%')
plt.plot(no_of_nodes, P_tot_60, 'y-', label='m = 60%')
plt.plot(no_of_nodes, P_tot_70, 'y-', label='m = 70%')
plt.plot(no_of_nodes, P_tot_80, 'y-', label='m = 80%')
plt.plot(no_of_nodes, P_tot_90, 'y-', label='m = 90%')
plt.xlim(0,20000)
plt.ylim(3e-53,1)
plt.legend(loc=3)
plt.show()
