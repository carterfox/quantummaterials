#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 18:46:49 2023

@author: carterfox
plotting for signal mapping
"""
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib import transforms
from matplotlib_scalebar.scalebar import ScaleBar
import helper_function_library as hf
from scipy import interpolate
hf.init_plot_params()

plt.rcParams["figure.constrained_layout.use"] = False


# path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/HQGraphene Crystals/10-11/chip4/T-S_TL/MOKE_RMCD/december2023/'
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round3/device2/RMCD/no-gating/mapping/'
temp = '1.7K'
# file_path = path+'mapping_0T_after_m2T.txt'
# file_path = path+'mapping_m2p1T.txt'
# file_path = path+'mapping_0T_after_m2p1T_v2.txt'
# file_path = path+'mapping_m2p1T.txt'
# file_path = path+'mapping_m2p1T_finescan.txt'
# file_path = path+'mapping_0T_after_m2p1T.txt'
# file_path = path+'mapping_fine_0T_after_m2T.txt'
file_path = path+'mapping_0T_after_m2T.txt'
# file_path = path+'mapping_m2p1T.txt'
# file_path = path+'mapping -1p2T.txt'

field = '0T after -2T'

# plt.figure(figsize=(7,5))

sample = r'CrI3 2L+2L'

cbarmax=1.0

data = np.loadtxt(file_path,skiprows=5)
xvoltages = data[:,1]
yvoltages = data[:,0]
num_x_points = int(np.sqrt(len(xvoltages)))
num_y_points = num_x_points
R = data[:,2]
dR = data[:,4]
theta_r = data[:,3]
theta_dr = data[:,5]
detector_gain_comp = 180 #accounts for difference between RF output and monitor gains, as well as balanced detection and waveplate giving factors of 2
dR_over_R = -100*dR/R
# dR_over_R = 1000*(dR/R)/detector_gain_comp #end up in mrad
background = 0
# dR_over_R = dR_over_R - .5
nrows, ncols = num_x_points, num_y_points
plt.ylabel(r'Axis 2 ($\mu$m )',fontsize=14)
plt.xlabel(r'Axis 1 ($\mu$m)',fontsize=14)
um_per_volt = 0.2
ticks=5
scale = um_per_volt*yvoltages[1]-yvoltages[0]
xyticks = np.linspace(np.min(yvoltages)-0.5,np.max(yvoltages)-0.5,num_y_points)
# plt.yticks(np.linspace(-0.5,num_y_points-0.5,8),np.round(np.linspace(np.max(yvoltages),np.min(yvoltages),8)*um_per_volt,2))
# plt.xticks(np.linspace(-0.5,num_x_points-0.5,8),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),8)*um_per_volt,2))
plt.xticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(yvoltages),np.max(yvoltages),ticks)*um_per_volt,2))
plt.yticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),ticks)*um_per_volt,2))

dR_over_R[np.where(theta_dr<=-70)] = dR_over_R[np.where(theta_dr<=-70)]*-1
dR = dR*1000000
R = R*1000

# dR_over_R = np.abs(dR_over_R)
# plot_type = dR
# plot_type = R
plot_type = dR_over_R
# plot_type = theta_dr


if any(plot_type == R):
    plot_typelabel = 'R'
    clabel = r'R (mV)'  
    # plt.clim(2.5,5)  

if any(plot_type == dR):
    plot_typelabel = 'dR'
    clabel = r'dR ($\mu$V)'  
    # plt.clim(330,1020)  

if any(plot_type == dR_over_R):
    plot_typelabel = 'dR_over_R'
    clabel = r'RMCD %'  
    # plt.clim(3,5)  

if any(plot_type == theta_dr):
    plot_typelabel = 'theta_dR'
    clabel = r'theta_dR'  
    # plt.clim(-180,180)  
    clabel = r'$\theta_{dR}$'   
    
try:
    plt.figure(figsize=(7,5))
    # plt.ylabel(r'Axis 2 ($\mu$m)',fontsize=14),plt.xlabel(r'Axis 1 ($\mu$m)',fontsize=14)
    # plt.ylabel(r'$\mu$m'),plt.xlabel(r'$\mu$m')
    plt.xticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(yvoltages),np.max(yvoltages),ticks)*um_per_volt,2))
    plt.yticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),ticks)*um_per_volt,2))
    grid = plot_type.reshape((nrows, ncols))
    grid = np.rot90(grid)
    grid = np.rot90(grid)
    im=plt.imshow(grid, cmap=cm.viridis)
    # plt.title(sample+'     '+temp)
    cbar=plt.colorbar(im)
    #6, 11.2, 16
    #2.5, 6.2, 11
    # x = 18.3
    # y =23.7
    # plt.axvline(y,c='r',label='axis1:' +str(round(y*np.max(yvoltages)/(num_y_points-1),2))+' V')
    # plt.axhline(x,c='b',label='axis2:' +str(round(x*np.max(xvoltages)/(num_x_points-1),2))+' V')
    
except:
    plt.figure(figsize=(6,5))
    plt.scatter(yvoltages,-xvoltages,s=50,marker='s',c=plot_type,cmap=cm.viridis)
    cbar=plt.colorbar()
    # plt.clim(0,4)
    # plt.xlim(0,30),plt.ylim(-30,0)  
    plt.ylabel(r'Axis 2 ($\mu$m)',fontsize=14),plt.xlabel(r'Axis 1 ($\mu$m)',fontsize=14)


    
cbar.set_label(clabel,fontsize=18)
# plt.legend(loc='lower left')
# plt.clim(.2,3)
# plt.xlim(2,24),plt.ylim(27,1)
# plt.scatter(13,0,c='r')# (13,39) #axis2, max_axis1-axis1

# cbarmax = str(cbarmax).replace('.','p')
# plt.title(sample+'     '+temp+'     '+field)
temp = temp.replace('.','p')
field = field.replace(' ','')
field = field.replace('.','p')
sample = sample.replace(' ','_')
sample = sample.replace('.','p')
plt.xticks([]),plt.yticks([])
scalebar = ScaleBar(scale,"um",box_alpha=0,color='white',location='lower left' )
plt.gca().add_artist(scalebar)

plt.savefig(path+'map1')
plt.show()


