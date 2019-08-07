import numpy as np

# Create a random distribution
def get_random_distribution(distribution_type, lower_bound, upper_bound, set_size, \
                            round = True, no_of_type_in_set = None, sample_size = None):
    if distribution_type == "uniform_ditribution":  #use global constant/enum for this?
        randomNums = np.random.uniform(low= lower_bound, high= upper_bound, size=set_size)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "normal":
        # Generate normal Distribution:
        randomNums = np.random.normal((int((lower_bound + upper_bound)/2)), size=set_size)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "poisson":
        randomNums = np.random.poisson((int((lower_bound + upper_bound)/2)), size=set_size)
        if round == True:
            randomNums = np.round(randomNums)
    elif distribution_type == "hypergeometric_distribution":
        remainder_in_set = set_size - no_of_type_in_set
        randomNums = np.random.hypergeometric(remainder_in_set, no_of_type_in_set, sample_size, size=set_size)
        if round == True:
            randomNums = np.round(randomNums) + lower_bound
    else:
        print('Error! Undefined `distribution_type`: %s' % (distribution_type))
    #print(randomNums)
    return randomNums

# Create a random index
def get_random_index(distribution_type, lower_bound, upper_bound, round = True):
    if distribution_type == "uniform_ditribution" or distribution_type == "hypergeometric_distribution":
        randomNums = np.random.uniform(lower_bound, upper_bound, size=1)
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
    else:
        print('Error! Undefined `distribution_type`: %s' % (distribution_type))
    return randomNums
