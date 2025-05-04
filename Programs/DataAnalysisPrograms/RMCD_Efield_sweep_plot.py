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
import helper_function_library as hf
hf.init_plot_params()

def Eperp(V_b,V_t,d_b,d_t):
    return (V_b/d_b - V_t/d_t )/2

def n(V_b,V_t,d_b,d_t):
    V_b = V_b*unit.volt
    V_t = V_t*unit.volt
    d_t = d_t*unit.nm
    d_b = d_b*unit.nm
    n = (-4*cont.eps0.si*(V_b/d_b + V_t/d_t )/2/cont.e.si).to(10**12/unit.cm**2)
    return n.value

path = '/Users/carterfox/Google Drive/My Drive/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round2/RMCD/Efield_sweeps/'

stacked = path+'stacked_region3_scan6.txt'
unstacked = path+'unstacked_region2_scan1.txt'

file = stacked
data = np.loadtxt(file,skiprows=1)

sample = 'CrI3 2L+2L'

Vb = data[:,0]
Vt = data[:,2]
Vb_exp = data[:,0]
Vt_exp = data[:,2]
r = data[:,5]
r_std = data[:,9]
dr = data[:,6]
dr_std = data[:,10]
theta_r = data[:,7]
theta_dr = data[:,8]
current_t = data[:,13]
current_b = data[:,15]
current_t_std = data[:,14]
current_b_std = data[:,16]

background_rmcd=0.0
rmcd = dr/r*100 - background_rmcd
# rmcd[np.where(theta_dr>10)] = rmcd[np.where(theta_dr>10)]*-1
dr_over_r_std = hf.A_over_B_error_prop(dr, r, dr_std, r_std)*100

d_b=23
d_t=23
E= Eperp(Vb, Vt, d_b, d_t)
going_up = np.where(np.diff(E)>0.00000010)
going_down = np.where(np.diff(E)<0)

E_up = E[going_up]
E_down = E[going_down]

data = rmcd
err = dr_over_r_std
data_up = data[going_up]
data_down = data[going_down]
err_up = err[going_up]
err_down = err[going_down]

data2= theta_dr
data2_up = data2[going_up]
data2_down = data2[going_down]

fig, ax0 = plt.subplots(1,1,figsize=(5,6.5))

ax0.errorbar(E_up,data_up,yerr=err_up,label=r'$\rightarrow$',c='black')
ax0.errorbar(E_down,data_down,yerr=err_down,label=r'$\leftarrow$',c='r')

# plt.plot(E,dr*80000)
ax0.set_xlabel(r'$E$ (V nm$^{-1}$)')
# ax0.set_title(sample)
ax0.set_ylabel(r'RMCD $\%$')
ax0.set_yticks([1.475,1.525,1.575,1.625,1.675])

sample = sample.replace('.','p')
sample = sample.replace('-','m')

ax0.set_xlim(-.9,.9)
hf.plot_arrow_legend(ax0, r'$E$',x1=-.32, y1=1.655,xratio=.16,yratio=.04,wratio=.065)


plt.savefig(path+'Esweep_plot_'+sample+'_.png',bbox_inches='tight')
plt.show()



