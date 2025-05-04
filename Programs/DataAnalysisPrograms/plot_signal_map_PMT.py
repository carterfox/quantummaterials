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
import matplotlib

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/samples/22p5deg/SHG/mapping_positions/'
# path = 'D:/LabData\XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/samples/22p5deg/SHG/mapping_positions/'
temp = '293K'
file_path = path+'mapping5_wp0.txt'

sample = 'NbOI2 22.5deg flake2 pos1'

data = np.loadtxt(file_path,skiprows=1)
xvoltages = data[:,1] # scanner 2
yvoltages = data[:,0] # scanner 1
num_x_points = int(np.sqrt(len(xvoltages)))
num_y_points = num_x_points
means = data[:,2]
stds = data[:,3]
nrows, ncols = num_x_points, num_y_points
um_per_volt = 1
ticks = 10
xyticks = np.linspace(np.min(yvoltages)-0.5,np.max(yvoltages)-0.5,num_y_points)

try:
    plt.figure(figsize=(7,5))
    plt.ylabel(r'Axis 2 (V)',fontsize=14),plt.xlabel(r'Axis 1 (V)',fontsize=14)
    plt.xticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(yvoltages),np.max(yvoltages),ticks)*um_per_volt,2))
    plt.yticks(np.linspace(0,num_y_points-1,ticks),np.round(np.linspace(np.min(xvoltages),np.max(xvoltages),ticks)*um_per_volt,2))
    grid = means.reshape((nrows, ncols))
    
    im=plt.imshow(grid, cmap=cm.magma,vmax=900)
    plt.title(sample+'     '+temp)
    cbar=plt.colorbar(im)
    #6, 11.2, 16
    #2.5, 6.2, 11
    x = 11.2
    y =6.2
    plt.axvline(y,c='r',label='axis1:' +str(round(y*np.max(yvoltages)/(num_y_points-1),2))+' V')
    plt.axhline(x,c='b',label='axis2:' +str(round(x*np.max(xvoltages)/(num_x_points-1),2))+' V')
except:
    plt.figure(figsize=(6,5))
    plt.scatter(yvoltages,-xvoltages,s=250,marker='s',c=means,cmap=cm.magma)
    plt.colorbar(),plt.clim(0,200)
    plt.xlim(0,12),plt.ylim(-12,0)
    


plt.legend(loc='lower left')
plt.tight_layout()
temp = temp.replace('.','p')
sample = sample.replace(' ','_')
sample = sample.replace('.','p')

# plt.savefig(path+''+sample+'_',bbox_inches='tight')
plt.show()


