import random
import numpy as np

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
