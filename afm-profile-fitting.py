#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 08:46:36 2025


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
plt.rcParams["font.size"] = 16
plt.rcParams["legend.fontsize"] = 0.7 * 16    
plt.rcParams["lines.markersize"] = 5


path = '/Users/carterfox/Google Drive/My Drive/StackingTransitions/CrI3/round7/afm/2L2L/'

#.txt file should be from gwyddion profile. if you save multiple profiles in one file, the excess rows will be dashes. You need to replace those with 0's first. 


#d1

'''
#bottom
#prof1
f1 = path+'bottom-bn-2L2L-profiles.txt'
x11, h11 = hf.get_afm_profile(f1, 1,0,23)
x12, h12 = hf.get_afm_profile(f1, 1,16,-1)
h12 = h12-2
xsim = np.arange(0,2.6,.01)
p11,c11 = curve_fit(hf.sum_of_line_and_tanh, x11, h11,p0=[4,-3,.7,13,10])
p11 = np.round(p11,2)
p12,c12 = curve_fit(hf.sum_of_line_and_tanh, x12, h12,p0=[4,-3,1.7,13,-10])
p12 = np.round(p12,2)
#prof2-3
f1 = path+'bottom-bn-2L2L-profiles.txt'
x2, h2 = hf.get_afm_profile(f1, 2)
x3, h3 = hf.get_afm_profile(f1, 3)
xsim = np.arange(0,1.6,.01)
p2,c2 = curve_fit(hf.sum_of_line_and_tanh, x2, h2,p0=[4,-3,.7,13,10])
p2 = np.round(p2,2)
p3,c3 = curve_fit(hf.sum_of_line_and_tanh, x3, h3,p0=[4,-3,.7,13,10])
p3 = np.round(p3,2)
#prof4-5
f1 = path+'bottom-bn-2L2L-profiles.txt'
x4, h4 = hf.get_afm_profile(f1, 4,0,-3)
x5, h5 = hf.get_afm_profile(f1, 5)
xsim = np.arange(0,1.5,.01)
p4,c4 = curve_fit(hf.sum_of_line_and_tanh, x4, h4,p0=[4,-3,.7,13,-10])
p4 = np.round(p4,2)
p5,c5 = curve_fit(hf.sum_of_line_and_tanh, x5, h5,p0=[4,-3,.7,13,10])
p5 = np.round(p5,2)
'''

#top


f1 = path+'top-bn-2L2L-profiles.txt'
x1, h1 = hf.get_afm_profile(f1, 1)
x2, h2 = hf.get_afm_profile(f1, 2)
x3, h3 = hf.get_afm_profile(f1, 3)
x4, h4 = hf.get_afm_profile(f1, 4)
xsim = np.arange(0,1.6,.01)
p1,c1 = curve_fit(hf.sum_of_line_and_tanh, x1, h1,p0=[4,-3,.7,13,10])
p1 = np.round(p1,2)
p2,c2 = curve_fit(hf.sum_of_line_and_tanh, x2, h2,p0=[4,-3,.7,13,10])
p2 = np.round(p2,2)
p3,c3 = curve_fit(hf.sum_of_line_and_tanh, x3, h3,p0=[4,-3,.7,13,10])
p3 = np.round(p3,2)
p4,c4 = curve_fit(hf.sum_of_line_and_tanh, x4, h4,p0=[4,-3,.7,13,-10])
p4 = np.round(p4,2)


plt.figure()
plt.plot(x1,h1,c='C2')
plt.plot(x2,h2,c='C0')
plt.plot(x3,h3,c='C1')
plt.plot(x4,h4,c='C3')

plt.plot(xsim,hf.sum_of_line_and_tanh(xsim, *p1),marker='',c='g',label='p1='+str(p1[3])+' nm')
plt.plot(xsim,hf.sum_of_line_and_tanh(xsim, *p2),marker='',c='b',label='p2='+str(p2[3])+' nm')
plt.plot(xsim,hf.sum_of_line_and_tanh(xsim, *p3),marker='',c='r',label='p3='+str(p3[3])+' nm')
plt.plot(xsim,hf.sum_of_line_and_tanh(xsim, *p4),marker='',c='purple',label='p4='+str(p4[3])+' nm')

plt.legend()
plt.xlabel(r'x ($\mu $m)')
plt.ylabel(r'height (nm)')

plt.savefig(path+'2L2L_top_plot1.png',bbox_inches='tight',dpi=500)

plt.show()

