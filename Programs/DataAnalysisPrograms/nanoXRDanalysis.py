#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 14:33:30 2025

@author: carterfox

APS Nano XRD data analysis

"""
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.cm as cm
import scipy
import hdf5plugin
import h5py  
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
from helper_function_library import get_stressmap_data, create_vector_map, get_scan_data,plot_xrd_roi, plot_XRD_scan
from readMDA import readMDA
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib_scalebar.scalebar import ScaleBar


directory = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/NbOI2/NanoXRD-NbOI2/stress_map_making/'


#%% Making stress maps from Result.npz files
path = directory+'p1degthick/r1m10/p1Thick_r1m10_tiltscan1_R5/bottomflake/'
file = path+'Result.npz'

I, d, tilt_lr, tilt_ud,data = get_stressmap_data(file)
X,Y,dX,dY = create_vector_map(d, tilt_lr, tilt_ud, binning=2)

fig, ax = plt.subplots(1,1)
ax.axis('off')
diff = 0.014
vm=3.7967
img=ax.imshow(d,vmin=vm,vmax=vm+diff,origin='lower',cmap=cm.coolwarm)
cb=fig.colorbar(img, ax=ax,pad=0.01)
cb.outline.set_linewidth(.5)
# ticks = np.array([3.79832,3.79834,3.79836,3.79838,3.79840,3.79842])
# cb.set_ticks(ticks)
# cb.set_ticklabels(ticks,fontsize=6)
ax.quiver(X,Y,dX,dY,scale=.06,width=.0035)
plt.savefig(path+'saved_plot.png',dpi=1000,bbox_inches='tight')
plt.show()

#%% Grabbing 2d scan data from h5 file and mda file 

path = directory+'p1degthin/r1m10/'

h5file = path+'scan_483_000481.h5'
mdafile = path+'26idbSOFT_0483.mda'

data, dim_x, dim_y, scale, scan_num = get_scan_data(h5file, mdafile)

#%% Summing over ROI
# roi='bottom'
roi=''
x_start,x_end = 781, 787
y_start,y_end = 553,560
# if roi == 'bottom':
#     x_start, x_end = 770, 893
#     y_start, y_end = 661, 721
# elif roi == 'top':
#     x_start, x_end = 926, 1044
#     y_start, y_end = 858, 923

img = plot_xrd_roi(data,dim_x,dim_y, y_start, y_end, x_start, x_end)

##%% plotting 2d scan
img = img/np.max(img)
sample = r"p1$^\circ$ Thin"
reflection = "(1,-1,0) "+roi

plot_XRD_scan(img, scale, sample, reflection,vmin=None,vmax=1)

# plt.savefig(path+'scan'+scan_num+'_'+roi+'flake_XRDmap',bbox_inches='tight',dpi=500)

#%% taking 2d fft of d spacing 

# path = directory+'180degthick/r1m12/180Thick_r1m12_tiltscan1_R7/top/'
# file = path+'Result.npz'

# I, d, tilt_lr, tilt_ud,data = get_stressmap_data(file)
d = img

fft_image = np.fft.fft2(d)

fft_image_centered = np.fft.fftshift(fft_image)

magnitude_spectrum = np.abs(fft_image_centered)

magnitude_spectrum_log = np.log(magnitude_spectrum + 1)

plt.figure()
plt.imshow(d)


plt.figure()
plt.imshow(magnitude_spectrum_log,vmax=5)
plt.colorbar()
scalebar = ScaleBar(30,"1/nm",box_alpha=0,color='white',location='lower right',length_fraction=1/7,dimension='si-length-reciprocal')
plt.gca().add_artist(scalebar)
# plt.xlabel('1/[nm]')
# plt.ylabel('1/[nm]')
plt.yticks([])
plt.xticks([])
# plt.xlim(30,60)
# plt.ylim(30,60)
# plt.savefig(path+'fft_dspacing.png',dpi=1000,bbox_inches='tight')

