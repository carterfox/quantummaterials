#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:08:59 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import astropy.constants as cont
import astropy.units as unit

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )
def Eperp(V_b,V_t,d_b,d_t):
    return (V_b/d_b - V_t/d_t )/2

def n(V_b,V_t,d_b,d_t):
    V_b = V_b*unit.volt
    V_t = V_t*unit.volt
    d_t = d_t*unit.nm
    d_b = d_b*unit.nm
    n = (-4*cont.eps0.si*(V_b/d_b + V_t/d_t )/2/cont.e.si).to(10**12/unit.cm**2)
    return n.value

# path = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round4/d3/RMCD/'
# path = '/Users/carterfox/Google Drive/My Drive/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round4/d4/RMCD/'
path = '/Users/carterfox/Google Drive/My Drive/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D2_BR/gate_sweeping_stacked/'
# zeroBfield_after_m2T_path = path+'Esweeps_0T_after_m2T/'
# zeroBfield_after_2T_path = path+'Esweeps_0T_after_2T/'

# after_m2T_path = path + 'Esweep_0T_after_m2T/'
# Bfield_after_m2T_path = path + 'Esweep_bfield_after_m2T/'

# zeroBfield_after_m2T = zeroBfield_after_m2T_path+'stacked_location4_0T_scan3.txt'
# zeroBfield_after_2T = zeroBfield_after_2T_path+'stacked_location1_0T_scan1.txt'
# Bfield_after_m2T = Bfield_after_m2T_path+'stacked_location1_p1T_scan1.txt'
# Bfield_after_2T = Bfield_after_2T_path+'stacked_location1_mp1T_scan1.txt'

file = path+'2-27_sweep4_start_3400G.txt'
data = np.loadtxt(file,skiprows=1)
path = file.split('stacked')[0]
sample = 'Stacked L3 Scan1 0T'
# sample = 'Stacked L1 '+file.split('_')[-1].split('.txt')[0]+' '+file.split('_')[-2].replace('p','.').replace('m','-')
# sample = 'Neutral region1 scan1'
# sample = 'Unstacked region2 scan2'
# Vb = data[:,1]
# Vt = data[:,3]
Vb_exp = data[:,0]
# Vt_exp = data[:,2]
r = data[:,2]
r_std = data[:,6]
dr = data[:,3]
dr_std = data[:,7]
# theta_r = data[:,7]
theta_dr = data[:,5]
# current_t = data[:,13]
# current_b = data[:,15]
# current_t_std = data[:,14]
# current_b_std = data[:,16]
# dr[np.where(theta_dr<0)] = -1*dr[np.where(theta_dr<0)] 

background_rmcd=0.0
rmcd = dr/r*100 - background_rmcd
rmcd[np.where(theta_dr>0)] = rmcd[np.where(theta_dr>0)]*-1
dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)*100
problemzone = np.where(dr_over_r_std>.1)
Vb_exp = Vb_exp[np.where(dr_over_r_std<.1)]
rmcd = rmcd[np.where(dr_over_r_std<.1)]
dr_over_r_std = dr_over_r_std[np.where(dr_over_r_std<.1)]
# current = data[:,11]*1000
# current_std = data[:,12]*1000
d_b=15
d_t=20
# E= Eperp(Vb, Vt, d_b, d_t)
# E= n(Vb, Vt, d_b, d_t)
# E= (Vt_exp)#/40/4
E= Vb_exp/(d_b+d_t)
going_up = np.where(np.diff(E)>0)
going_down = np.where(np.diff(E)<0)
E_up = E[going_up]
E_down = E[going_down]


data = rmcd
err = dr_over_r_std
data_up = data[going_up]
data_down = data[going_down]
err_up = err[going_up]
err_down = err[going_down]
plt.figure(figsize=(7,5))

# plt.scatter(E_up,data_up,label=r'$\rightarrow$',c='r')
# plt.plot(E,data)
# plt.scatter(E_down,data_down,label=r'$\leftarrow$',c='b')
plt.errorbar(E_up,data_up,yerr=err_up,label=r'$\rightarrow$',c='r',marker='.',markersize=7)
plt.errorbar(E_down,data_down,yerr=err_down,label=r'$\leftarrow$',c='b',marker='.',markersize=7)

plt.grid()# plt.axvline(-8)
# plt.axvline(8)# plt.legend(fontsize=9)
# plt.annotate("", xy=(1.6, 1.85), xytext=(0, 0),arrowprops=dict(arrowstyle="->"),c='b')
# plt.xlabel(r'$n (cm^{-2}$)',fontsize=16)
plt.xlabel(r'$E_\perp$ (V/nm)',fontsize=16)
plt.title(sample)
plt.ylabel(r'RMCD $\%$',fontsize=16)
# plt.xlabel('V',fontsize=16)
plt.legend()
sample = sample.replace('.','p')
sample = sample.replace('-','m')
# plt.ylim(-2.21,-1.8)
# plt.ylim(-2.75,-2.6)
# plt.xticks([-.25,-.2,-.15,-.1,-.05,0,.05,.1,.15,.2,.25])
plt.xlim(-.3,.3)
plt.savefig(path+'Esweep_'+sample,bbox_inches='tight')
# plt.figure()
# plt.plot(rmcd)
# plt.xlabel('Measurement Number')
# plt.ylabel('RMCD %')



