#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:42:37 2019

@author: kevoulee
"""

from IPython import get_ipython
get_ipython().magic('clear')
#get_ipython().magic('reset -sf')

import numpy as np
import math
import operator
from decimal import Decimal

def nCk(n,k): 
    if (n - k) < 0 or n < 0 or k < 0:
        return 0;
    return np.float64((Decimal(math.factorial(n)) / Decimal(math.factorial(n - k))) / Decimal(math.factorial(k)))

# An example problem using a deck of cards will be used to demonstrate definition of the terms
    # What is the probability of receiving 2 Kings from a deck of 52 playing cards (containing 4 Kings) 
    # when 6 cards are drawn from the deck 
## type_threshold is the number of a specific item from which the probability is calculated (e.g. 2 Kings)
## no_of_type_in_set is the number of the specific item found amongst the total number of items (e.g.4 Kings within the deck of 52 playing cards) 
## sample_size is the set of items that are drawn from the total (e.g. 6 cards drawn from the deck )
## set_size is the total number of the items in the set (e.g. the 52 cards in a deck of playing cards)

def probability(type_threshold, no_of_type_in_set, sample_size, set_size) -> np.float64:
    #Type checking - Python does not have built-in type checking   
    type_error = False
    ##type_threshold
    try:
        operator.index(type_threshold)
        T = np.int_(type_threshold)
    except TypeError:
        print('Error: \'type_threshold\' - expected int (or int variant), received %s' % (type(type_threshold)))
        type_error = True
    
    ##no_of_type_in_set
    try:
        operator.index(no_of_type_in_set)
        m = np.int_(no_of_type_in_set)
    except TypeError:
        print('Error: \'no_of_type_in_set\' - expected int (or int variant), received %s' % (type(no_of_type_in_set)))
        type_error = True
    
    ##sample_size
    try:
        operator.index(sample_size)
        n = np.int_(sample_size)
    except TypeError:
        print('Error: \'sample_size\' - expected int (or int variant), received %s' % (type(sample_size)))
        type_error = True
    
    ##set_size
    try:
        operator.index(set_size)
        N = np.int_(set_size)
    except TypeError:
        print('Error: \'set_size\' - expected int (or int variant), received %s' % (type(set_size)))
        type_error = True
    
    if type_error:
        return 0
    
    #Calculation
    P_tot = 0
    #Calculate probability
    for i in range(T, n + 1):
        P_tot = P_tot + nCk(m, i) * nCk(N - m, n - i) / nCk(N, n)
    return P_tot
