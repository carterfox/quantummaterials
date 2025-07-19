#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:22:02 2023

@author: carterfox
"""

import numpy as np
import scipy
from astropy import constants as cont
from astropy import units as uu
import matplotlib.pylab as plt
import pandas as pd

file = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1riZacJd_1_jmKfGgrjDuP7KcecvMS3i2/Xiao research group/Lab Data (Xiao and Wang groups)/StackingTransitions/WTe2/test copy.txt'
a,b,c = 3.51860,  6.30234, 15.00578
unitcell_area = (a*b*uu.angstrom**2).to(uu.m**2)

atom = np.loadtxt(file,skiprows=2,usecols=0,dtype=str)
xcoord = np.loadtxt(file,skiprows=2,usecols=1)*a
ycoord = np.loadtxt(file,skiprows=2,usecols=2)*b
zcoord = np.loadtxt(file,skiprows=2,usecols=3)*c
# xcoord[np.where(zcoord>3)] = a - xcoord[np.where(zcoord>3)]
weight = np.loadtxt(file,skiprows=2,usecols=4)
charges = np.ones(len(atom))
charges = weight
charges[np.where(atom =='W')]=charges[np.where(atom =='W')]*4
charges[np.where(atom =='Te')]=charges[np.where(atom =='Te')]*(-2)
# charges[np.where(atom =='S')]=charges[np.where(atom =='S')]*(-2)

origin = 0*np.array([a,b,c])/2
dipolex = np.sum(charges*(xcoord-origin[0]))
dipoley = np.sum(charges*(ycoord-origin[1]))
dipolez = np.sum(charges*(zcoord-origin[2]))
dipole = ((dipolex,dipoley,dipolez)*(cont.e.si)*uu.angstrom).to(uu.C*uu.m)
dipole = dipole / unitcell_area
dipole = dipole*10**(12)
print(dipole)

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(xcoord[np.where(atom =='W')], ycoord[np.where(atom =='W')], zcoord[np.where(atom =='W')], color = "blue",s=50)
ax.scatter3D(xcoord[np.where(atom =='Te')], ycoord[np.where(atom =='Te')], zcoord[np.where(atom =='Te')], color = "red",s=50)
# ax.scatter3D(xcoord[np.where(atom =='S')], ycoord[np.where(atom =='S')], zcoord[np.where(atom =='S')], color = "orange",s=50)
plt.title("simple 3D scatter plot")
ax.set_xlabel('a-axis', fontweight ='bold')
ax.set_ylabel('b-axis', fontweight ='bold')
ax.set_zlabel('c-axis', fontweight ='bold')
 
# show plot
ax.view_init(0,0,'z')
plt.show()
