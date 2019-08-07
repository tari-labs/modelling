# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:03:01 2019

@author: pluto
"""

import sys, os

#Add ../utils to the Python system path
try:
    sys.path.index(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');
except ValueError:
    sys.path.append(os.getcwd().split(os.getcwd().split(os.sep)[-1])[0] + 'utils');

import rand_dist as r_d
import matplotlib.pyplot as plt
import numpy as np

def plotSettings(figure_size = (12,9), line_style_grid = '-.', line_style_axis = '-.', \
                 title = " ", x_label = '', y_label = '', title_font_size = '20',\
                 font_size = '18', fontweight="bold"):
    ## Standard graph settings 
    fig, ax1 = plt.subplots(figsize=figure_size)   
    ax1.grid(True, linestyle=line_style_grid)
    ax1.xaxis.grid(True, which='minor', linestyle=line_style_axis)
    ax1.set_title(title, fontsize=title_font_size, fontweight=fontweight)
    ax1.set_xlabel(x_label, fontsize=font_size)
    ax1.set_ylabel(y_label, fontsize=font_size)
   

lower_bound = 1
upper_bound = 1000
qty = 1000

no_of_type_in_set = np.round(qty/3)
sample_size = np.round(qty/7)

y1_u = r_d.get_random_distribution("uniform_ditribution", lower_bound, upper_bound, qty, False)
y1_n = r_d.get_random_distribution("normal", lower_bound, upper_bound, qty, False)
y1_p = r_d.get_random_distribution("poisson", lower_bound, upper_bound, qty, False)
y1_h = r_d.get_random_distribution("hypergeometric_distribution", lower_bound, upper_bound, qty, \
                                   False, no_of_type_in_set, sample_size)

y2_u = []
y2_n = []
y2_p = []
for i in range(qty):
    y2_u.append(r_d.get_random_index("uniform_ditribution", lower_bound, upper_bound, False))
    y2_n.append(r_d.get_random_index("normal", lower_bound, upper_bound, False))
    y2_p.append(r_d.get_random_index("poisson", lower_bound, upper_bound, False))


plotSettings(title= "uniform - get_random_distribution", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y1_u)), y1_u)
plt.show()

plotSettings(title= "uniform - get_random_index", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y2_u)), y2_u)
plt.show()

plotSettings(title= "normal - get_random_distribution", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y1_n)), y1_n)
plt.show()

plotSettings(title= "normal - get_random_index", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y2_n)), y2_n)
plt.show()

plotSettings(title= "poisson - get_random_distribution", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y1_p)), y1_p)
plt.show()

plotSettings(title= "poisson - get_random_index", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y2_p)), y2_p)
plt.show()

plotSettings(title= "hypergeometric - get_random_distribution", x_label= 'Index', y_label= 'Value')
plt.scatter(np.arange(0,len(y1_h)), y1_h)
plt.show()
