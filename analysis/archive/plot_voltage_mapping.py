#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:33:51 2024

@author: carterfox
"""
import os
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm
import astropy.units as unit
import astropy.constants as cont

def Eperp(V_b,V_t,d_b,d_t):
    return (V_b/d_b - V_t/d_t )/2


def n(V_b,V_t,d_b,d_t):
    V_b = V_b*unit.volt
    V_t = V_t*unit.volt
    d_t = d_t*unit.nm
    d_b = d_b*unit.nm
    n = (-4*cont.eps0.si*(V_b/d_b + V_t/d_t )/2/cont.e.si).to(10**12/unit.cm**2)
    return n.value

os.chdir('/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/TaIrTe4/dualgate/11-18/RMCD/2dmapping/')
data = np.loadtxt('voltage_2d_mapping_scan8.txt')
vt= data[:,2]
vb = data[:,0]
r = data[:,5]
r_theta = data[:,6]
rstd = data[:,7]
r_thetastd = data[:,8]
dr = data[:,9]
dr_theta = data[:,10]
drstd = data[:,11]
dr_thetastd = data[:,12]
currentb = data[:,13]
currentbstd = data[:,14]
currentt = data[:,15]
currenttstd = data[:,16]

rmcd = dr/r*100

plt.figure(figsize=(7.5,6))
plt.ylim(-7,7)
plt.xlim(-3.8,3.8)
I = currentt
plt.xlabel(r'$V_t$ (V)',fontsize=16)
plt.ylabel(r'$V_b$ (V)',fontsize=16)
plt.scatter(vt,vb,c=I,marker='s',s=250,cmap=cm.plasma)
# plt.scatter(vt,vb,c=rmcd,marker='s',s=250,cmap=cm.plasma)
# plt.scatter(vt,vb,c=rmcd,marker='s',s=48,cmap=cm.plasma)
cbar = plt.colorbar(label='RMCD %')
cbar.ax.yaxis.label.set_size(15)
# plt.clim(.319,.355)
vb_line = np.linspace(-11,11,10)
vt_line = np.linspace(6,-6,10)

# plt.plot(vt_line,vb_line,linestyle='dashed',linewidth=.75,c='black',label=r'$n$=0')
plt.legend(fontsize=12,loc='lower left')
# plt.scatter(vt,vb,c=currentb,marker='s',s=230)
# plt.savefig('voltage_mapping_plot_scan8',bbox_inches='tight')
plt.show()

