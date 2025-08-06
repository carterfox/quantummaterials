#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 14:08:12 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import pandas as pd
def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/dual_gate_round2/RMCD/B_field_scans_at_diff_doping/'

zero = directory+'unstacked_region1_scan1_nodoping.txt1.7 K Sweep Oe .txt'
p4 = directory+'unstacked_region1_scan1_2Veach.txt1.7 K Sweep Oe .txt'
m4 = directory+'unstacked_region1_scan1_m2Veach.txt1.7 K Sweep Oe .txt'
p11 = directory+'unstacked_region1_scan1_5Veach.txt1.7 K Sweep Oe .txt'
m11 = directory+'unstacked_region1_scan1_m5Veach.txt1.7 K Sweep Oe .txt'


files_to_study = [m11,m4,zero,p4,p11]
doping_levels = [-11,-4.5,0,4.5,11]

sample = 'Unstacked - Doping' 
temp = '1.7K'

ylabel = r'RMCD $\% $        ' 
title = sample
factor = 100

fig, ax0 = plt.subplots(1,1,figsize=(5.5,6))
ax0.set_title(title)

for f,d in zip(files_to_study,doping_levels):
    
    
    data = np.loadtxt(fname=f,comments='#')
    b_field = data[:,0]/10000
    r = data[:,1]
    r_std = data[:,2]
    theta_r = data[:,3]
    theta_r_std = data[:,4]
    dr = data[:,5]
    dr_std = data[:,6]
    theta_dr = data[:,7]
    theta_dr_std = data[:,8]
    dr_over_r = -1*dr/r*factor 
    dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)*factor
    background=.6
    dr_over_r[np.where(theta_dr>=0)] = dr_over_r[np.where(theta_dr>=0)]*-1
    dr_over_r = dr_over_r+background
    
        
    ax0.errorbar(b_field,dr_over_r,yerr=dr_over_r_std,label=d)
    # ax1.errorbar(b_field,theta_dr,yerr=theta_dr_std)
    
    ax0.grid()

ax0.set_xlabel('$\mu_0$H (T)',fontsize=18)
ax0.set_ylabel(ylabel,rotation=90,fontsize=18)
plt.ticklabel_format(axis='both')
ax0.set_xlim(-.8,-.6)
# ax0.set_yticks(np.linspace(-10,10,21))
ax0.legend(title='(10^12 e/cm^2)',fontsize=12,loc='best')

plt.savefig(directory+'rmcd_scan_'+sample,bbox_inches='tight')

plt.show()




