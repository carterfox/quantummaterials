#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:31:49 2023

@author: carterfox

Moke and RMCD data analysis
"""


import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

def get_data(file):
    data = np.loadtxt(fname=file,comments='#')
    b_field = data[:,0]/10000
    r = data[:,1]
    r_std = data[:,2]
    theta_r = data[:,3]
    theta_r_std = data[:,4]
    dr = data[:,5]
    dr_std = data[:,6]
    theta_dr = data[:,7]
    theta_dr_std = data[:,8]
    
    return b_field, r, dr, theta_r, theta_dr, r_std, dr_std, theta_r_std, theta_dr_std

factor = 1000/180 #gain difference and going to mrad

def process_data(b_field, r, dr, theta_r, theta_dr, r_std, dr_std, theta_r_std, theta_dr_std):
    # dr[np.where(theta_dr<0)]= dr[np.where(theta_dr<0)]*-1
    dr_over_r = dr/r
    dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)
    mid = int(np.ceil(len(b_field)/2))
    b_field_low_to_high = b_field[0:mid]
    b_field_high_to_low = b_field[mid:]
    dr_over_r_low_to_high = dr_over_r[0:mid] *factor
    theta_dr_low_to_high = theta_dr[0:mid] 
    theta_dr_std_low_to_high = theta_dr_std[0:mid] 
    dr_over_r_high_to_low = dr_over_r[mid:] *factor
    theta_dr_high_to_low = theta_dr[mid:] 
    theta_dr_std_high_to_low = theta_dr_std[mid:] 
    dr_over_r_std_low_to_high = dr_over_r_std[0:mid]*factor
    dr_over_r_std_high_to_low = dr_over_r_std[mid:]*factor
    return b_field_low_to_high, b_field_high_to_low, dr_over_r_low_to_high, dr_over_r_high_to_low, theta_dr_low_to_high,theta_dr_high_to_low, dr_over_r_std_low_to_high, dr_over_r_std_high_to_low, theta_dr_std_low_to_high, theta_dr_std_high_to_low

###  path to files
# directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1riZacJd_1_jmKfGgrjDuP7KcecvMS3i2/Xiao research group/Lab Data (Xiao and Wang groups)/StackingTransitions/CrI3/HQGraphene Crystals/10-11/chip4/T-S_TL/MOKE_RMCD/'
directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/lab_troubleshooting/MOKE_troubleshoot/1-6-24/'
directory2 = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/Fan Fei/MOKE/1-8 MOKE troubleshoot/'
# CrI31_device3_natural = directory+'10-11/chip4/T-S_TL/MOKE/'+'10_26_natural2.0 K Sweep Oe .txt'
# CrI31_device3_stacked2 = directory+'10-11/chip4/T-S_TL/MOKE/'+'10_26_stackedV2_2.0 K Sweep Oe .txt'
# CrI31_device3_stacked3 = directory+'10-11/chip4/T-S_TL/MOKE/'+'10_26_stackedV32.0 K Sweep Oe .txt'
# substrate_device3 = directory+'10-11/chip4/T-S_TL/MOKE/'+'10_27_substrate_widerscan_2.0 K Sweep Oe .txt'
# substrate_device3 = directory+'10-11/chip4/T-S_TL/MOKE/'+'10_26_substrate2.0 K Sweep Oe .txt'
# CrI31_device2_stacked = directory+'10-6/chip6/BMR_t-s/MOKE/CrI3_device2_stacked2.0 K Sweep Oe .txt'
# substrate_device2 = directory+'10-6/chip6/BMR_t-s/MOKE/CrI3_device2_substrate2.0 K Sweep Oe .txt'
# substrate1 = directory+'10_27_substrate_widerscan_2.0 K Sweep Oe .txt'
# test = directory+'Si_MOKE_test11.6 K Sweep Oe .txt'
Si_1 = directory2+ 'MOKE_Si_midpower1.6 K Sweep Oe .txt'
Si_2 = directory2+ 'MOKE_Si_highpower1.6 K Sweep Oe .txt'
Si_3 = directory2+ 'MOKE_Si_highpower21.6 K Sweep Oe .txt'

file_to_study = Si_3
substrate = None
subdir = file_to_study[:-len(file_to_study.split('/')[-1])]

    
sample = 'test'
temp = '2K'

ylabel = r'$\theta_k (mrad)$         ' 
# ylabel = r'$\theta_k/\theta_{k,2T}$         ' 
title = 'MOKE - '+sample+' - '+temp

### collect data from file
b_field, r, dr, theta_r, theta_dr, r_std, dr_std, theta_r_std, theta_dr_std = get_data(file_to_study)
# r = np.average(r[np.where(b_field==0)])*1
pack = process_data(b_field, r, dr, theta_r, theta_dr, r_std, dr_std, theta_r_std, theta_dr_std)
b_field_low_to_high, b_field_high_to_low, dr_over_r_low_to_high, dr_over_r_high_to_low, theta_dr_low_to_high,theta_dr_high_to_low, dr_over_r_std_low_to_high, dr_over_r_std_high_to_low, theta_dr_std_low_to_high, theta_dr_std_high_to_low = pack
fig, (ax0,ax1) = plt.subplots(2,1,figsize=(8,6),sharex=False,gridspec_kw={'height_ratios': [3,1]})
ax0.set_title(title)

process=True
if process:
#     s_b_field, s_r, s_dr, s_theta_r, s_theta_dr, s_r_std, s_dr_std, s_theta_r_std, s_theta_dr_std = get_data(substrate)
#     s_pack = process_data(s_b_field, s_r, s_dr, s_theta_r, s_theta_dr, s_r_std, s_dr_std, s_theta_r_std, s_theta_dr_std)
#     s_b_field_low_to_high, s_b_field_high_to_low, s_dr_over_r_low_to_high, s_dr_over_r_high_to_low, s_theta_dr_low_to_high, s_theta_dr_high_to_low, s_dr_over_r_std_low_to_high, s_dr_over_r_std_high_to_low, s_theta_dr_std_low_to_high, s_theta_dr_std_high_to_low = s_pack
#     s_mid = int(np.ceil(len(s_b_field)/2))
    
    # s_r = np.average(s_r[np.where(s_b_field==0)])
    
    # s_dr_over_r = factor*s_dr/s_r
#     s_dr_over_r[0:50] = s_dr_over_r[0:50]*-1
#     s_dr_over_r[151:] = s_dr_over_r[151:]*-1
#     s_dr_over_r_low_to_high = s_dr_over_r[0:s_mid]
#     s_dr_over_r_high_to_low = s_dr_over_r[s_mid:]
# #    popt,pcov = curve_fit(line, s_b_field, s_dr_over_r)
    # dr_over_r_low_to_high[0:20] = dr_over_r_low_to_high[0:20]*-1
    # dr_over_r_high_to_low[20:] = dr_over_r_high_to_low[20:]*-1

    
    dr_over_r_low_to_high[0:2] = dr_over_r_low_to_high[0:2]*-1
    dr_over_r_high_to_low[2:] = dr_over_r_high_to_low[2:]*-1
    
    z_lth=np.polyfit(b_field_low_to_high,dr_over_r_low_to_high,1)
    p_lth = np.poly1d(z_lth)
    z_htl=np.polyfit(b_field_high_to_low,dr_over_r_high_to_low,1)
    p_htl = np.poly1d(z_htl)
    # dr_over_r_ = np.append(dr_over_r_low_to_high,dr_over_r_high_to_low)
    # z_=np.polyfit(b_field,dr_over_r_,2)
    # p_ = np.poly1d(z_)
   
    # dr_over_r_low_to_high = 1*(dr_over_r_low_to_high - 1*p_lth(b_field_low_to_high))
    # dr_over_r_high_to_low = 1*(dr_over_r_high_to_low - 1*p_htl(b_field_high_to_low))

    # dr_over_r_low_to_high,dr_over_r_high_to_low=dr_over_r_low_to_high/max(dr_over_r_low_to_high),dr_over_r_high_to_low/max(dr_over_r_low_to_high)
    # dr_over_r_low_to_high[0:69] = -1.8-dr_over_r_low_to_high[0:69]
    # dr_over_r_high_to_low[29:] = -1.8-dr_over_r_high_to_low[29:]
    # dr_over_r_low_to_high[0:26] = -5.56-dr_over_r_low_to_high[0:26]
    # dr_over_r_high_to_low[70:] = -5.56-dr_over_r_high_to_low[70:]
    # dr_over_r_high_to_low = dr_over_r_high_to_low+1.9
    # dr_over_r_low_to_high = dr_over_r_low_to_high+1.9
    # dr_over_r_high_to_low = dr_over_r_high_to_low/max(dr_over_r_low_to_high)
    # dr_over_r_low_to_high = dr_over_r_low_to_high/max(dr_over_r_low_to_high)

errbars = True
if errbars:
    x=1
else:
    x=0
    
ax0.errorbar(b_field_low_to_high,dr_over_r_low_to_high,yerr=x*dr_over_r_std_low_to_high,c='r',label=r'$\rightarrow$')
ax0.errorbar(b_field_high_to_low,dr_over_r_high_to_low,yerr=x*dr_over_r_std_high_to_low,c='b',label=r'$\leftarrow$')
ax1.errorbar(b_field_low_to_high,theta_dr_low_to_high,yerr=x*theta_dr_std_low_to_high,c='r',label=r'$\rightarrow$')
ax1.errorbar(b_field_high_to_low,theta_dr_high_to_low,yerr=x*theta_dr_std_high_to_low,c='b',label=r'$\leftarrow$')
# ax0.axvline(-.72)
# ax0.axvline(.72)


ax1.set_xlabel('$\mu_0$H (T)',fontsize=18)
# ax0.set_xticks([-2,-1,0,1,2])
ax0.set_ylabel(ylabel,rotation=90,fontsize=18)
# ax1.set_ylabel('Phase ($^\circ}$)',fontsize=18)
plt.ticklabel_format(axis='both')
ax0.legend(fontsize=14,loc='best')
# ax0.set_xlim(-.5,.5)

# ax0.set_xlim(-.01,.01)
ax0.set_ylim(-.025,.04)
try:
    len(r)
    name = subdir+'moke_polyfit_v2'+sample
except:
    name = subdir+'moke_polyfit_avg_r_v2_faked'+sample


# plt.savefig(name,bbox_inches='tight')

plt.show()


