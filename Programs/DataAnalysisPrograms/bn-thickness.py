#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  6 08:46:36 2025

@author: carterfox
"""

import matplotlib.pylab as plt
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib_scalebar.scalebar import ScaleBar
import helper_function_library as hf
import numpy as np
from matplotlib import image
from skimage import color
import pandas as pd
from skimage import io
from matplotlib_scalebar.scalebar import ScaleBar
from scipy.optimize import curve_fit
import matplotlib.patches as mpatches

hf.init_plot_params()
plt.rcParams["image.cmap"] = "terrain_r"

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/other/Carter_Fox_rhodeslab_copy/CrI3_dualgate1/CrI3_devices/'


#d1
data = np.loadtxt(path+'d1_both-bn_v2.txt',skiprows=4)
heights1 =np.flip(data[:,1]*10.5*10**9) + 975
heights2 = data[:,3]*10.5*10**9 + 660
xs1 = np.linspace(1285,1455,len(heights1))
xs2 = np.linspace(80,230,len(heights2))

img = image.imread(path+'D1-supplement-image.png')

plt.figure(edgecolor='white')
plt.imshow(img)
plt.plot(xs1,heights1,markersize=0,zorder=0,c='white',linewidth=1)
plt.plot(xs2,heights2,markersize=0,zorder=0,c='white',linewidth=1)
ax=plt.gca()
arrow = mpatches.FancyArrowPatch((1230,882),(1230,1032),arrowstyle='<->',mutation_scale=15,color='white')# plt.xticks([]),plt.yticks([])
arrow2 = mpatches.FancyArrowPatch((300,540),(300,680),arrowstyle='<->',mutation_scale=15,color='white')# plt.xticks([]),plt.yticks([])
ax.add_patch(arrow),
ax.add_patch(arrow2),
plt.text(1000,968,'10 nm',fontsize=10,color='white')
plt.text(350,638,'8 nm',fontsize=10,color='white')
plt.xticks([]),plt.yticks([])
ax.set_frame_on(False)
plt.savefig(path+'device1_finalimage.png',dpi=500)

plt.show()

#d2
'''
data = np.loadtxt(path+'d2_both-bn_v2.txt',skiprows=4)
heights = data[:,1]*8*10**9 + 1450
xs = np.linspace(630,975,len(heights))

img = image.imread(path+'D2-supplement-image.png')

plt.figure(edgecolor='white')
plt.imshow(img)
plt.plot(xs,heights,markersize=0,zorder=0,c='white',linewidth=1)
ax=plt.gca()
arrow = mpatches.FancyArrowPatch((1000,632),(1000,802),arrowstyle='<->',mutation_scale=15,color='white')# plt.xticks([]),plt.yticks([])
arrow2 = mpatches.FancyArrowPatch((580,740),(580,910),arrowstyle='<->',mutation_scale=15,color='white')# plt.xticks([]),plt.yticks([])
ax.add_patch(arrow),
ax.add_patch(arrow2),
plt.text(1040,748,'16 nm',fontsize=10,color='white')
plt.text(350,848,'16 nm',fontsize=10,color='white')
plt.xticks([]),plt.yticks([])
ax.set_frame_on(False)
plt.savefig(path+'device2_finalimage.png',dpi=500)

plt.show()
'''
