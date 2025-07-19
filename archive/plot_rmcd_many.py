#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 14:52:52 2024

@author: carterfox
"""


import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

###  path to files
directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D1_BL/'

scan1 = directory+'gating_location1_2-22-medium_scan_before_gating1.7 K Sweep Oe .txt'
scan2 = directory+'500mV_location1_scan11.7 K Sweep Oe .txt'
scan3 = directory+'1000mV_location1_scan11.7 K Sweep Oe .txt'
scan4 = directory+'1000mV_location1_scan21.7 K Sweep Oe .txt'

files_to_study = [scan1,scan2,scan3,scan4]
flips = [0,0,1,1]
factor = 100

for file,flip in zip(files_to_study,flips):
    data = np.loadtxt(fname=file,comments='#')
    b_field = data[:,0]
    r = data[:,1]
    r_std = data[:,2]
    dr = data[:,5]
    dr_std = data[:,6]
    theta_dr = data[:,7]
    theta_dr_std = data[:,8]

    # r=np.average(r)
    dr_over_r = dr/r*factor
    dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)*factor
    mid = int(np.ceil(len(b_field)/2))
    b_field_low_to_high = b_field[0:mid]/10000
    b_field_high_to_low = b_field[mid:]/10000
    dr_over_r_low_to_high = dr_over_r[0:mid] 
    theta_dr_low_to_high = theta_dr[0:mid] 
    theta_dr_std_low_to_high = theta_dr_std[0:mid] 
    dr_over_r_high_to_low = dr_over_r[mid:] 
    theta_dr_high_to_low = theta_dr[mid:] 
    theta_dr_std_high_to_low = theta_dr_std[mid:] 
    dr_over_r_std_low_to_high = dr_over_r_std[0:mid]
    dr_over_r_std_high_to_low = dr_over_r_std[mid:]
    if flip == 1:
        dr_over_r[np.where(theta_dr<=0)] = dr_over_r[np.where(theta_dr<=0)]*-1
    else:
        dr_over_r[np.where(theta_dr>=0)] = dr_over_r[np.where(theta_dr>=0)]*-1

    plt.plot(b_field,dr_over_r,label=r'$\rightarrow$',linewidth=1)
