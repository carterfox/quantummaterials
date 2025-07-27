#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 14:33:30 2025

@author: carterfox

APS Nano XRD data analysis

"""
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.cm as cm
import scipy
import hdf5plugin
import h5py  
from readMDA import readMDA
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
from helper_function_library import get_stressmap_data, create_vector_map, get_scan_data,plot_xrd_roi, plot_XRD_scan
from readMDA import readMDA
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib_scalebar.scalebar import ScaleBar

#path to folder with h5 and and mda files
directory = '/Users/carterfox/My Drive (cdfox@wisc.edu)/'
path = directory+'XiaoWang_Group_data_2024on/ChenS/scandata_0628/'

#%% Grabbing 2d scan data from h5 file and mda file 

# path = directory+'p1degthin/r1m10/p1Thin_r1m10_tiltscan1/'


h5file = path+'scan_60_000060.h5'
mdafile = path+'26idbSOFT_0060.mda'

data, dim_x, dim_y, scale, scan_num = get_scan_data(h5file, mdafile)

#%% Summing over ROI
# roi='bottom'
roi=''

x_start,x_end = 601, 625
y_start,y_end = 757,796

img = plot_xrd_roi(data,dim_x,dim_y, y_start, y_end, x_start, x_end)

##%% plotting 2d scan
plt.figure()
img = img/np.max(img)
sample = r"Chen"
reflection = "(1,-1,0) "+roi
plot_XRD_scan(img, scale, sample, reflection,vmin=None,vmax=.6)

# plt.savefig(path+'scan'+scan_num+'_'+roi+'flake_XRDmap',bbox_inches='tight',dpi=500)
plt.show()