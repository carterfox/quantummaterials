#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:10:39 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )


path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D2_BR/gate_sweeps_zero_field/'

data = np.loadtxt(path+'scan7_after_pos_pull_0T.txt',skiprows=1)
scan= '7'
v = data[:,1]
r = data[:,3]
r_std = data[:,7]
dr = data[:,4]
dr_std = data[:,8]
theta_r = data[:,5]
theta_dr = data[:,6]
dr[np.where(theta_dr<0)] = -1*dr[np.where(theta_dr<0)] 
current = data[:,11]*1000
current_std = data[:,12]*1000

dr_over_r = dr/r*100
dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)*100

fig, (ax0,ax1,ax2) = plt.subplots(3,1,figsize=(8,6),sharex=True,gridspec_kw={'height_ratios': [3,1,1]})

try:
    first_max = np.where(v==np.max(v))[0][1]
    first_min = np.where(v==np.min(v))[0][1]
    v_up = v[0:first_max]
    v_down = v[first_max:first_min]
    v_up2 = v[first_min:]
    dr_over_r_up = dr_over_r[0:first_max]
    dr_over_r_down = dr_over_r[first_max:first_min]
    dr_over_r_up2 = dr_over_r[first_min:]
    dr_over_r_std_up = dr_over_r_std[0:first_max]
    dr_over_r_std_down = dr_over_r_std[first_max:first_min]
    dr_over_r_std_up2 = dr_over_r_std[first_min:]
    theta_dr_up = theta_dr[0:first_max]
    theta_dr_down = theta_dr[first_max:first_min]
    theta_dr_up2 = theta_dr[first_min:]
    current_up = current[0:first_max]
    current_down = current[first_max:first_min]
    current_up2 = current[first_min:]
    current_std_up = current_std[0:first_max]
    current_std_down = current_std[first_max:first_min]
    current_std_up2 = current_std[first_min:]
    
    ax0.errorbar(v_up,dr_over_r_up,dr_over_r_std_up,label=r'$\rightarrow$',c='r')
    ax2.errorbar(v_up,theta_dr_up,c='r')
    ax1.errorbar(v_up,current_up,yerr=current_std_up,c='r')
    ax0.errorbar(v_down,dr_over_r_down,dr_over_r_std_down,label=r'$\leftarrow$',c='b')
    ax2.errorbar(v_down,theta_dr_down,c='b')
    ax1.errorbar(v_down,current_down,yerr=current_std_down,c='b')
    ax0.errorbar(v_up2,dr_over_r_up2,dr_over_r_std_up2,label=r'$\rightarrow$',c='g')
    ax2.errorbar(v_up2,theta_dr_up2,c='g')
    ax1.errorbar(v_up2,current_up2,yerr=current_std_up2,c='g')
    ax0.legend()

except:
    ax0.errorbar(v,dr_over_r,dr_over_r_std,c='r')
    ax2.errorbar(v,theta_dr,c='r')
    ax1.errorbar(v,current,yerr=current_std,c='r')
    
ax0.set_title('Scan '+scan)
# ax0.set_ylim(1.87,2.07)
ax2.set_xlim(-20,20)
ax2.set_xlabel('Voltage (V)',fontsize=18)
ax0.set_ylabel('RMCD %',fontsize=18)
ax1.set_ylabel('I (nA)',fontsize=18)
ax2.set_ylabel('Phase (  $\ocirc$)',fontsize=18)   
plt.savefig(path+'scan'+scan+'_0t_plot.png',bbox_inches='tight')


