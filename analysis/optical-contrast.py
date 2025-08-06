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

path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/contrast/'

data = np.loadtxt(path+'afm-image-linecut.txt',skiprows=2)
hieghts = data[:,1]*10**9*100 + 330
hieghts = np.flip(hieghts[10:60])
contrast_data = pd.read_csv('/Users/carterfox/Desktop/contrastdata.csv')
I=contrast_data['Gray_Value']*3+280
# xs = np.linspace(180,240,len(I))
xs = np.linspace(575,640,len(I))

img = image.imread(path+'f1 2.png')

plt.figure(edgecolor='white')
plt.imshow(img)
# plt.plot(xs,hieghts,markersize=0,zorder=0,c='white',linewidth=1)
plt.plot(xs,I,markersize=0,zorder=0,c='white',linewidth=1)
ax=plt.gca()
arrow = mpatches.FancyArrowPatch((560,572),(560,644),arrowstyle='<->',mutation_scale=15,color='white')# plt.xticks([]),plt.yticks([])
arrow2 = mpatches.FancyArrowPatch((570,540),(650,540),color='white')# plt.xticks([]),plt.yticks([])
ax.add_patch(arrow),
ax.add_patch(arrow2),
# plt.text(480,448,'1.4 nm',fontsize=10,color='white')
plt.text(470,600,r'$C=8.2 \%$',fontsize=10,color='white')
plt.xticks([]),plt.yticks([])
ax.set_frame_on(False)
plt.xlim(420,920),plt.ylim(280,780)
plt.savefig(path+'finalimage2.png',dpi=500)

plt.show()


# contrast_data = pd.read_csv('/Users/carterfox/Desktop/contrastdata.csv')
# dist=contrast_data['Distance_(pixels)']
# I=contrast_data['Gray_Value']
# plt.figure(figsize=(4,5))
# b=119.12
# um_per_pix=0.1

# C = (b-I)/(b+I)
# Cbin= []
# dist_bin = []
# binning=2

# plt.plot(dist*um_per_pix,C*100,markersize=8,c='C0')
# plt.xticks([0,2.5,5,7.5,10])
# plt.ylabel('Contrast')
# plt.xlabel(r'x ($\mu$m)')
# plt.xlim(0,10),plt.ylim(-1)
# ax=plt.gca()
# # ax.yaxis.tick_left()
# plt.savefig(path+'linecut.png')

# plt.show()

# from PIL import Image
# img = Image.open(path+'f1 2.png').convert('L')
# imgarray = np.array(img)
# # plt.text(770,620,'a')
# b=117
# imgarray = abs((b-imgarray)/(imgarray+b))*100
# imgarray[np.where(imgarray>50)]=0
# # img.save(.png')
# cx,cy=650,570
# plt.xlim(cx-200,cx+200)
# plt.ylim(cy+200,cy-200)
# plt.xticks([])
# plt.yticks([])
# plt.imshow(imgarray,vmin=0,vmax=30)
# cbar = plt.colorbar()
# cbar.set_label('Contrast (%)')

# scale = 1/10
# scalebar = ScaleBar(scale,"um",box_alpha=0,color='black',location='lower right')
# plt.gca().add_artist(scalebar)
# # plt.savefig(path+'contrast_f5')
# plt.show()


'''

layers = np.array([0,1,1,2,2, 2, 2, 2,3,3,3, 3,4,4,4,4,5,5,3,3,1,4,5,6,3,5])
contrasts = np.array([0,4.3,4.5,8,8.3,8.7,8.7,9, 11.9,11.2, 12.2,11.6,15.2,14.6,15.,15.1,17.,17.2,11.2,11.3,4.2,14.8,17.37,19.6,11.3,17.3])
# layers = np.array([0,1, 2,3,4])#,5,5])
# contrasts = np.array([0,4.3,8.6, 12,15])#,17.,17.2])
p,c = curve_fit(hf.line, layers, contrasts)

ax=hf.init_fig(figsize=(5,6))

ax.scatter(layers,contrasts,c='C0')
# ax.plot(layers,hf.line(layers,p[0],p[1]),marker='')
ax.set_xticks([0,1,2,3,4,5,6])
ax.set_xlabel('Number of Layers')
ax.set_ylabel('Optical Contrast (%)')

plt.savefig(path+'contrast_curve',bbox_inches='tight',dpi=500)
plt.show()
'''

