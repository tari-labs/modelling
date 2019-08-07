import numpy as np

# Create a random distribution
def get_random_distribution(distribution_type, lower_bound, upper_bound, qty, round = True, bad = None, committe_size = None):
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        randomNums = np.random.uniform(low= lower_bound, high= upper_bound, size=qty)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "normal":
        # Generate normal Distribution:
        randomNums = np.random.normal((int((lower_bound + upper_bound)/2)), size=qty)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "poisson":
        randomNums = np.random.poisson((int((lower_bound + upper_bound)/2)), size=qty)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "hypergeometric_distribution":
        good_nodes = qty - bad
        randomNums = np.random.hypergeometric(good_nodes, bad, committe_size, size=qty)
        if round == True:
            randomNums = np.round(randomNums) + lower_bound
    return randomNums

# Create a random index
def get_random_index(distribution_type, lower_bound, upper_bound, round = True):
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        randomNums = np.random.uniform(low= lower_bound, high= upper_bound, size=1)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "normal":
        randomNums = np.random.normal((int((lower_bound + upper_bound)/2)), size=1)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "poisson":
        randomNums = np.random.poisson((int((lower_bound + upper_bound)/2)), size=1)
        if round == True:
            randomNums = np.round(randomNums)
    return randomNums
