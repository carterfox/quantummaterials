#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 14:33:30 2025

@author: carterfox

APS Nano XRD data analysis

"""

# %% Making stress maps from Result.npz files

from matplotlib.colors import LogNorm
import matplotlib.cm as cm
from matplotlib_scalebar.scalebar import ScaleBar
import helper_function_library as hf
import numpy as np
import matplotlib.pylab as plt


path = directory+'p1degthick/r1m10/p1Thick_r1m10_tiltscan1_R5/'
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





