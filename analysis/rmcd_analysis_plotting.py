#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:31:49 2023

@author: carterfox

Moke and RMCD data analysis
"""


import numpy as n
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import helper_function_library as hf
hf.init_plot_params()

STpath = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/'

directory = STpath+'CrI3/dual_gate_round3/device2/RMCD/no-gating/'

# scan = directory+'4layer_2.txt2.0 K Sweep Oe .txt'
# scan1 = directory+'twisted.txt2.0 K Sweep Oe .txt'
# scan2 = directory+'twisted_fine.txt2.0 K Sweep Oe .txt'
scan3 = directory+'stacked_region3_scan11.7 K Sweep Oe .txt'

sample = 'twisted'
temp = '1.7K'
    

p = hf.get_rmcd_data(scan3,10,'<=',0)
b_low_to_high, b_high_to_low, rmcd_low_to_high, rmcd_high_to_low  = p


ax0=hf.init_fig('RMCD')

ax0.plot(b_low_to_high,rmcd_low_to_high,c='black',label='$\rightarrow$')
ax0.plot(b_high_to_low,rmcd_high_to_low,c='r',label='$\leftarrow$')

ax0.set_xlim(-2.1,2.1)
ax0.set_ylim(-12.5,12.5)

ax0=hf.plot_arrow_legend(ax0, r'$B$')#,xratio=.16,yratio=.04,wratio=.065)

plt.savefig(directory+'rmcd_'+sample.replace('.','p'))


plt.show()


