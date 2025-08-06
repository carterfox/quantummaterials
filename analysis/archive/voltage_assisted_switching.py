#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 18:51:58 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import astropy.constants as cont
import astropy.units as uu

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

def ndop(Vb,db,Vt,dt):
    eps = 4*cont.eps0
    return (eps*(Vb*uu.V/(db*uu.nm)+Vt*uu.V/(dt*uu.nm))).to(uu.C/uu.cm**2)*6.25*10**18

directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D1_BL/sweeping_gate_stacked/'
directory2 = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D1_BL/sweeping_gate_unstacked/'
directory3 = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/RMCD/D2_BR/gate_sweeping_stacked/'

scan1 = directory+'after_refocus/sweep_gate_start0_3000G_200mVsteps_to_2_then_400mVsteps_back.txt' #pure doping
# scan2 = directory+'before_refocus/sweep_gate_2800G_start0_100mVsteps.txt'
# scan3 = directory+'before_refocus/sweep_gate_2800G_start0_m100mVsteps.txt'
# scan4 = directory+'before_refocus/sweep_gate_2950G_start0_400mVsteps.txt'
# scan5 = directory+'before_refocus/sweep_gate_2970G_start0_200mVsteps.txt'
# scan6 = directory2+'sweep_gate_unstacked_start0_4975G_200mVsteps.txt'

# scan1 = directory3+'stacked1_start0_200mV_steps.txt'
# scan2 = directory3+'stacked2_1800G_start0_200mV_steps.txt'
# scan3 = directory3+'stacked2_3400G_start0_200mV_steps_updated.txt'
# scan4 = directory3+'stacked2_3400G_start0_m500mV_steps.txt'
# scan5 = directory3 + '2-27_sweep1_start_3300G.txt'
scan6 = directory3 + '2-27_sweep4_start_3400G.txt' #pure E field 
# scan7 = directory3 + '2-27_sweep5_start_2900G.txt'

file_to_study = scan1

data = np.loadtxt(fname=file_to_study,comments='#',skiprows=1)
if file_to_study.split('/')[-1] == '2-27_sweep4_start_3400G.txt':
    data = np.delete(data,(25,26),axis=0)
factor = 100
voltage= data[:,0]
R = data[:,2]
dR = data[:,3]
dR_over_R = dR/R*factor
theta_dR = data[:,5]
R_std = data[:,6]
dR_std = data[:,7]
dR_over_R_std = A_over_B_error_prop(dR, R, dR_std, R_std)*factor

# dR_over_R[np.where(theta_dR>=0)] = -1*dR_over_R[np.where(theta_dR>=0)] 
dR_over_R[np.where(theta_dR<=0)] = -1*dR_over_R[np.where(theta_dR<=0)] 
fig, (ax0,ax1) = plt.subplots(2,1,figsize=(6,5),sharex=False,gridspec_kw={'height_ratios': [3,1]})
# ax0.set_title('Stacked    B=0.340')
x=1
t=37
E= -(voltage)/t/2
doping = ndop(voltage,10,voltage,8)/10**(12)

# ax0.errorbar(E[0:44],dR_over_R[0:44],yerr=dR_over_R_std[0:44]*x,marker='.',c='b',label=r'$\leftarrow$')
# ax0.errorbar(E[44:],dR_over_R[44:],yerr=dR_over_R_std[44:]*x,marker='.',c='r',label=r'$\rightarrow$',zorder=0)
# ax1.plot(E[0:44],theta_dR[0:44],c='b')
# ax1.plot(E[44:],theta_dR[44:],c='r',zorder=0)

ax0.errorbar(doping[0:11],dR_over_R[0:11],yerr=dR_over_R_std[0:11]*x,marker='.',c='r',label=r'$\rightarrow$')
ax0.errorbar(doping[11:],dR_over_R[11:],yerr=dR_over_R_std[11:]*x,marker='.',c='b',label=r'$\leftarrow$')
ax1.plot(doping[0:11],theta_dR[0:11],c='r')
ax1.plot(doping[11:],theta_dR[11:],c='b',zorder=0)

# plt.xlabel(r'$E_\perp$ (V/nm)',fontsize=18)
plt.xlabel(r'$n_e$ $(10^{12}$cm$^{-2})$',fontsize=18)
ax0.set_ylabel('RMCD %',fontsize=18)
ax1.set_ylabel('phase',fontsize=18)
ax0.legend(fontsize=16,loc='lower right')
# ax0.set_ylim(-5,-4)
# ax0.set_xlim(-8,8)
# plt.savedif(directory2+'unstacked_gate_sweep.png')
# plt.savefig(directory3+'Efield_figure_poster.png',bbox_inches='tight')
plt.savefig(directory3+'doping_figure_poster.png',bbox_inches='tight')

plt.show()
