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
from matplotlib import transforms
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
axes_rotation=45

# path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/HQGraphene Crystals/10-11/chip4/T-S_TL/MOKE_RMCD/december2023/'
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_round3/device1/RMCD/no-gating/'

temp = '1.7K'
# file_path = path+'mapping_0T_after_m2T.txt'
# file_path = path+'mapping_m2p1T.txt'
# file_path = path+'mapping_0T_after_m2p1T_v2.txt'
file_path = path+'mapping_m2p1T.txt'
# file_path = path+'mapping_0T_after_m2p1T.txt'

field = '-2.1T'

fig=plt.figure(figsize=(6,6))

sample = r'Device1'

cbarmax=1.0

data = np.loadtxt(file_path,skiprows=1)
xvoltages = data[:,1]
yvoltages = data[:,0]
num_x_points = int(np.sqrt(len(xvoltages)))
num_y_points = num_x_points
R = data[:,2]
dR = data[:,4]
theta_r = data[:,3]
theta_dr = data[:,5]
detector_gain_comp = 180 #accounts for difference between RF output and monitor gains, as well as balanced detection and waveplate giving factors of 2
dR_over_R = 100*dR/R
#dR_over_R = 1000*(dR/R)/detector_gain_comp #end up in mrad
background = 0
# dR_over_R = dR_over_R - .5
nrows, ncols = num_x_points, num_y_points

scales = (0, 29.5, 0, 29.5)

t = Affine2D().rotate_deg(axes_rotation)
h = floating_axes.GridHelperCurveLinear(t, scales)
ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=h)
ax.set_ylabel(r'Axis 1 ($\mu$m )',fontsize=14)
ax.set_xlabel(r'Axis 2 ($\mu$m)',fontsize=14)
um_per_volt = .2
xyticks = np.linspace(np.min(yvoltages)-0.5,np.max(yvoltages)-0.5,num_y_points)
ax.set_yticks(np.linspace(-0.5,num_y_points-0.5,8),np.round(np.linspace(np.max(yvoltages),np.min(yvoltages),8)*um_per_volt,2))
ax.set_xticks(np.linspace(-0.5,num_y_points-0.5,8),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),8)*um_per_volt,2))

# dR_over_R[np.where(theta_dr<=70)] = dR_over_R[np.where(theta_dr<=70)]*-1
dR = dR*1000000
R = R*1000

# plot_type = R
plot_type = dR
# plot_type = dR_over_R
# plot_type = theta_dr

grid = plot_type.reshape((nrows, ncols))

grid=np.rot90(grid)
grid=grid.T
max_val = round(np.max(grid),3)


tr = transforms.Affine2D().rotate_deg(axes_rotation)
im=ax.imshow(grid, transform=tr + ax.transData,cmap=cm.jet)
ax.set_yticks(np.linspace(-0.5,num_y_points-0.5,8),np.round(np.linspace(np.max(yvoltages),np.min(yvoltages),8)*um_per_volt,2))
ax.set_xticks(np.linspace(-0.5,num_y_points-0.5,8),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),8)*um_per_volt,2))

fig.add_subplot(ax)

plt.title(sample+'     '+temp+'     '+field)
cbar=fig.colorbar(im,orientation='horizontal',fraction=.03)

if any(plot_type == R):
    plot_typelabel = 'R'
    clabel = r'R (mV)'  
    # fig.clim(0,1)
    # plt.clim(6.4,15)  
    # cbar.clim(0,1)

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
    # clabel = r'theta_dR'  
    # plt.clim(-180,180)  
    clabel = r'$\theta_{dR}$'   
    
cbar.set_label(clabel,fontsize=18)
# plt.scatter(13,0,c='r')# (13,39) #axis2, max_axis1-axis1
plt.tight_layout()
# cbarmax = str(cbarmax).replace('.','p')
temp = temp.replace('.','p')
field = field.replace(' ','')
field = field.replace('.','p')
sample = sample.replace(' ','_')



# plt.savefig(path+'rmcd_plot_'+sample+'_'+plot_typelabel+'_'+field,bbox_inches='tight')
plt.show()


