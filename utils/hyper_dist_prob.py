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
from decimal import Decimal

def nCk(n,k): 
    if (n - k) < 0 or n < 0 or k < 0:
        return 0;
    return np.float64((Decimal(math.factorial(n)) / Decimal(math.factorial(n - k))) / Decimal(math.factorial(k)))

def probability(type_threshold, no_of_type_in_set, sample_size, set_size) -> np.float64:
    #Type checking - Python does not have built-in type checking 
    
    ##type_threshold
    if (type(type_threshold) == 'np.int64' or type(type_threshold) == 'int'):
        T = np.int_(type_threshold)
    else:
        print('Error: \'type_threshold\' - expected int/np.int64, received %s' % (type(type_threshold)))
        return 0
    
    ##no_of_type_in_set
    if (type(no_of_type_in_set) == 'np.int64' or type(no_of_type_in_set) == 'int'):
        T = np.int_(no_of_type_in_set)
    else:
        print('Error: \'no_of_type_in_set\' - expected int/np.int64, received %s' % (type(no_of_type_in_set)))
        return 0
    
    ##sample_size
    if (type(sample_size) == 'np.int64' or type(sample_size) == 'int'):
        T = np.int_(sample_size)
    else:
        print('Error: \'sample_size\' - expected int/np.int64, received %s' % (type(sample_size)))
        return 0
    
    ##set_size
    if (type(set_size) == 'np.int64' or type(set_size) == 'int'):
        T = np.int_(set_size)
    else:
        print('Error: \'set_size\' - expected int/np.int64, received %s' % (type(set_size)))
        return 0
    
    
    m = no_of_type_in_set
    N = set_size
    n = sample_size
    P_tot = 0
    #Calculate probability
    for i in range(T, n + 1):
        P_tot = P_tot + nCk(m, i) * nCk(N - m, n - i) / nCk(N, n)
    return P_tot
