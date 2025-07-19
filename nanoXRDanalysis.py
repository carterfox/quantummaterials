#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 14:33:30 2025

@author: carterfox

APS Nano XRD data analysis

"""

#%% only need to run this cell once, unless you want to change scan and/or roi
import numpy as np
import matplotlib.pylab as plt
from helper_function_library import XRD_ScanAnalyzer

#sample and path information. the path directory must have 'h5' and 'mda' subfolders with the data files
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/'+ \
    '.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/'+ \
    'XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/NanoXRD-NbOI2/stress_map_making/'
    
sample = r'$0.1^\circ$ Thin'
reflection = '(1,-1,0)'
scannum = 474  
scan = XRD_ScanAnalyzer(path,sample,reflection,scannum)

#ROI information
x_start,x_end = 757, 827
y_start,y_end = 529,599
scan.set_roi(x_start, x_end, y_start, y_end)

#%%

scan.image_roi_sum()
scan.image_roi_com(axis='x',vmin=784,vmax=794)
scan.image_roi_com(axis='y',vmin=558,vmax=567)



# scan.image_roi_shift(axis='x',save=True)
# scan.plot_scan_image(scan.shift_img,'SHIFTx',vmin=-3,vmax=3)
# imgx,namex,scale,data = hf.plot_xrd_roi_com(h5file, mdafile, sample, reflection, x_start, x_end, y_start, y_end, axis='x')
# plt.savefig(path+namex,bbox_inches='tight',dpi=500)
# plt.show()

# imgy,namey,scale,data = hf.plot_xrd_roi_com(h5file, mdafile, sample, reflection, x_start, x_end, y_start, y_end, axis='y')
# plt.savefig(path+namey,bbox_inches='tight',dpi=500)
# plt.show()

# imgsx,imgsx_std,namesx,scale,data,normed_prof = hf.plot_xrd_roi_shift(h5file, mdafile, sample, reflection, x_start, x_end, y_start, y_end, axis='x',normed_prof=normed_prof)
# plt.show()


#%% Making stress maps from Result.npz files

from matplotlib.colors import LogNorm
import matplotlib.cm as cm
from matplotlib_scalebar.scalebar import ScaleBar
import helper_function_library as hf
# path = directory+'p1degthick/r1m10/p1Thick_r1m10_tiltscan1_R5/'
file = path+'Result.npz'

I, d, tilt_lr, tilt_ud,data = hf.get_stressmap_data(file)
X,Y,dX,dY = hf.create_vector_map(d, tilt_lr, tilt_ud, binning=2)
scale = 3000/(np.shape(d)[0])

fig, ax = plt.subplots(1,1)
ax.axis('off')
diff = 0.025
vm=3.79
img=ax.imshow(d,vmin=vm,vmax=vm+diff,origin='lower',cmap=cm.coolwarm)
cb=fig.colorbar(img, ax=ax,pad=0.01)
cb.outline.set_linewidth(.5)
cb.set_label('d-spacing')
ticks = np.array([3.793,3.798,3.803,3.808,3.813])
cb.set_ticks(ticks)
cb.set_ticklabels(ticks,fontsize=7)
ax.quiver(X,Y,dX,dY,scale=.06,width=.003,color='black')
scalebar = ScaleBar(scale,"nm",box_alpha=0,color='black',location='lower left',font_properties={"size": 0})
ax.add_artist(scalebar)
plt.savefig(path+'saved_plot.png',dpi=1000,bbox_inches='tight')
plt.show()


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

