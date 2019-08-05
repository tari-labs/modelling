import random
import numpy as np

# Create a random distribution
def get_random_distribution(distribution_type, lower_bound, upper_bound, qty, bad = None, committe_size = None):
    index = np.int64(0)
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        randomNums = np.random.uniform(low= lower_bound, high= upper_bound, size=qty)
        randomInts = np.round(randomNums)
    elif distribution_type == "normal":
        # Generate normal Distribution:
        randomNums = np.random.normal((int((lower_bound + upper_bound)/2)), size=qty)
        randomInts = np.round(randomNums)
    elif distribution_type == "poisson":
        randomNums = np.random.poisson((int((lower_bound + upper_bound)/2)), size=qty)
        randomInts = np.round(randomNums)
    elif distribution_type == "hypergeometric_distribution":
        good_nodes = qty - bad
        randomNums = np.random.hypergeometric(good_nodes, bad, committe_size, size=qty)
        randomInts = np.round(randomNums) + lower_bound
    return randomInts

# Create a random index
def get_random_index(distribution_type, lower_bound, upper_bound):
    index = np.int64(0)
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        index = random.randint(lower_bound, upper_bound)
    elif distribution_type == "normal":
        index = random.randint(lower_bound, upper_bound)  # ToDo: change to normal
    else:
        index = random.randint(lower_bound, upper_bound)  # ToDo: Add more options here
    return index
