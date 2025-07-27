#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:36:59 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import astropy.constants as cont
import astropy.units as unit

def Eperp(V_b,V_t,d_b,d_t):
    return (V_b/d_b - V_t/d_t )/2

def n(V_b,V_t,d_b,d_t):
    V_b = V_b*unit.volt
    V_t = V_t*unit.volt
    d_t = d_t*unit.nm
    d_b = d_b*unit.nm
    n = (-4*cont.eps0.si*(V_b/d_b + V_t/d_t )/2/cont.e.si).to(10**12/unit.cm**2)
    return n

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/'
path = path+'StackingTransitions/CrI3/dual_gate_round4/d5/SHG/'


file = path+'Esweep_stacked_region1_80k_wp107deg_scan2.txt'

title='CrI3 2L+2L'
# meas_time = 1.5

data = np.loadtxt(file,comments='#')
d_t = 16 #nm
d_b = 23 #nm
voltage_b = data[:,0]
voltage_t = voltage_b*(-1*d_t/d_b)


E= Eperp(voltage_b,voltage_t,d_b,d_t)

going_up = np.where(np.diff(E)>0.00000010)
going_down = np.where(np.diff(E)<0)
going_up=np.append(going_up,41)
going_down=np.append(going_down,20)

E_up = E[going_up]
E_down = E[going_down]

counts = data[:,2]
counts_up = counts[going_up]
counts_down = counts[going_down]
stds = data[:,3]
stds_up = stds[going_up]
stds_down = stds[going_down]
current = data[:,4]*10**3
current2 = data[:,6]*10**9
# try:
#     first_max = np.where(voltage_real==np.max(voltage_real))[0][1]
#     first_min = np.where(voltage_real==np.min(voltage_real))[0][1]
#     voltage_real_up = voltage_real[0:first_max]
#     voltage_real_down = voltage_real[first_max:first_min]
#     voltage_real_up2 = voltage_real[first_min:]
#     counts_up = counts[0:first_max]
#     counts_down = counts[first_max:first_min]
#     counts_up2 = counts[first_min:]
#     stds_up = stds[0:first_max]
#     stds_down = stds[first_max:first_min]
#     stds_up2 = stds[first_min:]

#     plt.figure()
#     plt.errorbar(voltage_real_up,counts_up,yerr=stds_up,c='r',marker='.',elinewidth=.5,label=r'$\rightarrow$')
#     plt.errorbar(voltage_real_down,counts_down,yerr=stds_down,c='b',marker='.',elinewidth=.5,label=r'$\leftarrow$')
#     plt.errorbar(voltage_real_up2,counts_up2,yerr=stds_up2,c='g',marker='.',elinewidth=.5,label=r'$\rightarrow$')
    
# except:
# plt.plot(E,counts)
# plt.plot(E_up,counts_up,label=r'$\rightarrow$',marker='.',c='r')
# plt.plot(E_down,counts_down,label=r'$\leftarrow$',marker='.',c='b')
ms=6
el=.5
fig, ax0 = plt.subplots(1,1,figsize=(7,5))

ax0.errorbar(E_up,counts_up,yerr=stds_up,marker='.',markersize=ms,elinewidth=el,label=r'$\rightarrow$',c='r')
ax0.errorbar(E_down,counts_down,yerr=stds_down,marker='.',markersize=ms,elinewidth=el,label=r'$\leftarrow$',c='b')


# plt.xlabel('Voltage (V)',fontsize=18)
ax0.set_xlabel(r'$E_\perp$ (V/nm)',fontsize=16)
ax0.set_ylabel('SHG Counts',fontsize=16)
# plt.ylabel('Current (nA)',fontsize=18)
ax0.legend(loc='upper left')
# plt.ylim(630,680)

# plt.title('4mW    1s gate time')
ax0.set_title(title)
plt.savefig(path+'Esweep_APS_plot_'+title+'.png',bbox_inches='tight')
