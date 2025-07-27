#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:13:19 2023

@author: carterfox

Image interpolation
"""


import numpy as np
import matplotlib.pylab as plt
import scipy
from scipy.interpolate import RegularGridInterpolator, interp2d
import matplotlib.cm as cm

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1riZacJd_1_jmKfGgrjDuP7KcecvMS3i2/Xiao research group/Lab Data (Xiao and Wang groups)/UCLA_Duan_Intercalated_Samples_Collab/CoMoS2/RMCD/field_sweep_mapping/sweep_down/'
file= '1p7k_rmcd_map_-1.00T_d'
file_path = path+file+'.txt'
sample = 'CoMoS$_2$'
field = file[-8:-2]
temp = '1.7K'

data = np.loadtxt(file_path,skiprows=1)
xvoltages_full = data[:,0]
yvoltages_full = data[:,1]
yvoltages = np.unique(yvoltages_full)
xvoltages = np.unique(xvoltages_full)
num_x_points = len(yvoltages)
num_y_points = len(xvoltages)
R = data[:,2]
dR = data[:,3]
theta_r = data[:,4]
theta_dr = data[:,5]
dR_over_R = dR/R*100


grid_original = dR_over_R.reshape((num_x_points, num_y_points))

interp = interp2d(xvoltages,yvoltages,grid_original,kind='cubic')
    
scale = 1
coords_new_x = np.linspace(xvoltages.min(),xvoltages.max(),num_x_points*scale)
coords_new_y = np.linspace(yvoltages.min(),yvoltages.max(),num_y_points*scale)

grid_interpolated=interp(coords_new_x,coords_new_y)
max_val = round(np.max(grid_original),3)

plt.imshow(grid_interpolated, extent=(xvoltages.min(), xvoltages.max(), yvoltages.max(), yvoltages.min()), cmap=cm.magma,vmin=0,vmax=0.85)

# plt.ylim(21.5,5.5)
# plt.xlim(1.5,17.5)

cbar=plt.colorbar()
cbar.set_label(label=r'$\Delta R/R $ %',fontsize=14)
plt.xlabel('X (V)',fontsize=14)
plt.ylabel('Y (V)',fontsize=14)
plt.title('RMCD Map of '+sample+':  T = '+temp+'   B = '+field+'\n max value = '+str(max_val)+'%',fontsize=14)

field=field.replace('.','p')
temp=temp.replace('.','p')

# plt.savefig(path+'smoothed/RMCD_map_CoMoS2_'+temp+'_'+field,bbox_inches='tight')

plt.show()