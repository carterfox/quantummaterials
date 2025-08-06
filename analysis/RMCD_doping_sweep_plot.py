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

def n(V_b,V_t,d_b,d_t):
    V_b = V_b*unit.volt
    V_t = V_t*unit.volt
    d_t = d_t*unit.nm
    d_b = d_b*unit.nm
    n = (4*cont.eps0.si*(V_b/d_b + V_t/d_t )/cont.e.si).to(10**13/unit.cm**2)
    return n.value

# path = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round4/d3/RMCD/'
path = '/Users/carterfox/Google Drive/My Drive/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D1_BL/sweeping_gate_stacked/after_refocus/'

# stacked = path+'2-27_sweep4_start_3400G.txt'
stacked = path+'sweep_gate_start0_3000G_200mVsteps_to_2_then_400mVsteps_back.txt'
# unstacked = path+'sweep_gate_unstacked_start0_4975G_200mVsteps.txt'

file = stacked
data = np.loadtxt(file,skiprows=1)

sample = 'Stacked B=0.3T'
Vb = data[:,0]
Vt = data[:,0]*0
Vb_exp = data[:,0]
Vt_exp = data[:,0]*0
r = data[:,2]
r_std = data[:,6]
dr = data[:,3]
dr_std = data[:,7]
theta_r = data[:,4]
theta_dr = data[:,5]
# current_t = data[:,13]
# current_b = data[:,15]
# current_t_std = data[:,14]
# current_b_std = data[:,16]

background_rmcd=0.0
rmcd = dr/r*100 - background_rmcd
rmcd[np.where(theta_dr<-10)] = rmcd[np.where(theta_dr<-10)]*-1
dr_over_r_std = hf.A_over_B_error_prop(dr, r, dr_std, r_std)*100

d_b=15
d_t=20
n= n(Vb, Vb, 8, 10)
going_up = np.where(np.diff(n)>0.00000010)
going_down = np.where(np.diff(n)<0)
going_down = np.append(going_down,-1)
going_up = np.append(going_up,10)
# going_up = np.arange(0,11,1)
# going_down = np.arange(10,31,1)
n_up = n[going_up]
n_down = n[going_down]

data = rmcd
err = dr_over_r_std
data_up = data[going_up]
data_down = data[going_down]
err_up = err[going_up]
err_down = err[going_down]

data2= theta_dr
data2_up = data2[going_up]
data2_down = data2[going_down]

# fig, (ax0,ax1) = plt.subplots(2,1,figsize=(8,6),sharex=True,gridspec_kw={'height_ratios': [3,1]})
fig, ax0 = plt.subplots(1,1,figsize=(6,4))

ax0.errorbar(n_up,data_up,yerr=err_up,label=r'$\rightarrow$',c='black')
ax0.errorbar(n_down,data_down,yerr=err_down,label=r'$\leftarrow$',c='r')


plt.xlabel(r'$n$ (10$^{13}$ cm$^{-2}$)')
ax0.set_ylabel(r'RMCD $\%$')


ax0.set_yticks([-6,-3,0,3,6])
ax0.set_ylim(-6.5)
hf.plot_arrow_legend(ax0,r'$n$', x1=.25,y1= -2.6)

sample = sample.replace('.','p')
sample = sample.replace('-','m')
# ax0.set_ylim(-1.4,3.8)
# ax0.set_ylim(-.45,-.25)
# ax0.set_xlim(-.9,.9)
plt.savefig(path+'n_sweep_'+sample+'_.png')
# plt.figure()
# plt.plot(rmcd)
# plt.xlabel('Measurement Number')
# plt.ylabel('RMCD %')
plt.show()


