#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 11:49:52 2025

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
import astropy.constants as cont
import astropy.units as unit
import helper_function_library as hf
hf.init_plot_params()

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/'
path = path+'StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/SHG/CD-Efield/'

f1_c1 = hf.get_CD_data(path+'../CD/flake1_circ131..txt')
f1_c2 = hf.get_CD_data(path+'../CD/flake1_circ221.txt')
s_c1 = hf.get_CD_data(path+'../CD/stacked1_circ131..txt')
s_c2 = hf.get_CD_data(path+'../CD/stacked1_circ221..txt')
f1_CD, f1_CD_err = hf.CD(f1_c1[0],f1_c2[0],f1_c1[1],f1_c2[1])
s_CD, s_CD_err = hf.CD(s_c1[0],s_c2[0],s_c1[1],s_c2[1])

flake1_c1 = np.array([526.941,707.882, 796.4705])
flake1_c2 = np.array([579.1176,724.29,847.94117])
flake1_c1_std = np.array([24.3935,  31.948271,  30.85662])
flake1_c2_std = np.array([23.730, 25.87,39.5])
f1_quickscan_CD, f1_quickscan_CD_err = hf.CD(flake1_c1,flake1_c2,flake1_c1_std,flake1_c2_std)

# file = path+'stacked_scan7_EfieldSHG-CD_close_to_elec.txt'
# file = path+'stacked_scan8_EfieldSHG-CD_middle_of_elec.txt'
# file = path+'stacked_scan9_EfieldSHG-CD_3V_from_middle_of_elec.txt'
file = path+'stacked_scan10_EfieldSHG-CD_6V_from_middle_of_elec.txt'
# file = path+'stacked_scan11_EfieldSHG-CD_11V_from_middle_of_elec.txt'
scannum = 10
data = np.loadtxt(file,comments='#')

v = data[:,1]
cd_info, c1, c2, c1_std, c2_std = hf.CD(data[:,2],data[:,3],data[:,4],data[:,5]), data[:,2],data[:,3],data[:,4],data[:,5]
cd, cd_std = cd_info
cd = cd-cd[0]

I = data[:,-2]
title='NbOI2 3L+3L 90$^{\circ}$ twist'
channel = 10 #um

E = v/channel*10


# cd = np.delete(cd,56)
# cd_std = np.delete(cd_std,56)
# E = np.delete(E,56)
# # flake1_quickscan_E = np.array([-200,0,200])/channel*10

going_up = np.where(np.diff(E)>0)
going_down = np.where(np.diff(E)<=0)

E_up = E[going_up]
E_down = E[going_down]

cd_up, cd_up_std = cd[going_up], cd_std[going_up]
cd_up, cd_up_std = cd_up[np.argsort(E_up)], cd_up_std[np.argsort(E_up)]
c1_up, c1_up_std = c1[going_up], c1_std[going_up]
c1_up, c1_up_std = c1_up[np.argsort(E_up)], c1_up_std[np.argsort(E_up)]
c2_up, c2_up_std = c2[going_up], c2_std[going_up]
c2_up, c2_up_std = c2_up[np.argsort(E_up)], c2_up_std[np.argsort(E_up)]

E_up.sort()
cd_down, cd_down_std = cd[going_down], cd_std[going_down]
cd_down, cd_down_std = cd_down[np.argsort(E_down)], cd_down_std[np.argsort(E_down)]
c1_down, c1_down_std = c1[going_down], c1_std[going_down]
c1_down, c1_down_std = c1_down[np.argsort(E_down)], c1_down_std[np.argsort(E_down)]
c2_down, c2_down_std = c2[going_down], c2_std[going_down]
c2_down, c2_down_std = c2_down[np.argsort(E_down)], c2_down_std[np.argsort(E_down)]
E_down.sort()

fig, ax0 = plt.subplots(1,1,figsize=(6,6))
el=0
ax0.errorbar(E,cd,yerr=cd_std,elinewidth=el,c='black')
ax0.errorbar(E_up,cd_up,yerr=cd_up_std,elinewidth=el,label=r'$\rightarrow$ Twisted',c='r')
ax0.plot(E_up,cd_up,linestyle='-',label=r'$\rightarrow$',c='r')
ax0.plot(E_down,cd_down,marker='.',linestyle='-',label=r'$\leftarrow$',c='black')
ax0.fill_between(E_up,cd_up-cd_up_std,cd_up+cd_up_std,color='r', alpha=0.15)
ax0.fill_between(E_down,cd_down-cd_down_std,cd_down+cd_down_std,color='black', alpha=0.15)
ax0.set_xlabel(r'$E_{||}$ (kV/cm)')
ax0.set_ylabel('$\Delta$CD (%)')
# plt.ylabel('Current (nA)',fontsize=18)|
# ax0.legend(loc='upper left')
ax0.set_ylim(-15,29)
ax0.set_xlim(-210,210)
hf.plot_arrow_legend(ax0, x1=-100,y1=15,label='$E_{||}$')
plt.savefig(path+'Esweep_SHG-CD_normed_scan'+str(scannum)+'.png',bbox_inches='tight',dpi=500)
plt.show()

# ax0.plot(E_up,c1_up+c2_up,markersize=ms,marker='.',linestyle='-',label=r'$\rightarrow$',c='r')
# ax0.plot(E_down,c1_down+c2_down,markersize=ms,marker='.',linestyle='-',label=r'$\leftarrow$',c='b')
# ax0.fill_between(E_up,c1_up+c2_up-np.sqrt(c1_up_std**2 + c2_up_std**2),c1_up+c2_up+np.sqrt(c1_up_std**2 + c2_up_std**2),color='r', alpha=0.15)
# ax0.fill_between(E_down,c1_down+c2_down-np.sqrt(c1_down_std**2 + c2_down_std**2),c1_down+c2_down+np.sqrt(c1_down_std**2 + c2_down_std**2),color='b', alpha=0.15)

# ax0.set_xlabel(r'$E_{||}$ (kV/cm)',fontsize=16)
# ax0.set_ylabel('SHG Intensity',fontsize=16)
# # plt.ylabel('Current (nA)',fontsize=18)
# ax0.legend(loc='upper left',fontsize=14)
# # plt.ylim(-3,41)
# plt.xlim(-210,210)
# plt.savefig(path+'Esweep_SHG_intensity_scan'+str(scannum)+'.png',bbox_inches='tight',dpi=500)



# # plt.title('4mW    1s gate time')
# ax0.set_title(title)
# # plt.show()
