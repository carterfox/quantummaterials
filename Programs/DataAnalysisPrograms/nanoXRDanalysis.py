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
from helper_function_library import XRD_ScanAnalyzer, init_plot_params
init_plot_params()
#sample and path information. the path directory must have 'h5' and 'mda' subfolders with the data files
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/'+ \
    '.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/'+ \
    'XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/NanoXRD-NbOI2/stress_map_making/'

scannum = 357
reflection = '(1,-1,0)'

# sample = r'$180^\circ$ Thick Bottom'
# x_start,x_end = 760, 815
# y_start,y_end = 570,610 

sample = r'$180^\circ$ Thick Top'
x_start, x_end = 840, 880
y_start, y_end = 680 ,725 

scan = XRD_ScanAnalyzer(path,sample,reflection,scannum)
scan.set_roi(x_start, x_end, y_start, y_end)


# %%
scan.image_roi_sum(vmin=0)
# scan.image_roi_com(axis='x')#,vmin=810,vmax=850)
# scan.image_roi_com(axis='y')#,vmin=695,vmax=705)
# scan.image_roi_shift(axis='x')
# scan.image_roi_shift(axis='y')

# scan.plot_scan_image(scan.shift_img_x,cbarlabel='SHIFTx',vmin=-3,vmax=4,threshold=1000)
# scan.plot_scan_image(scan.shift_img_y,cbarlabel='SHIFTy',vmin=-3.5,vmax=3.5,threshold=1000)


# sumimage = scan.sum_images()
# scan.plot_sum_images(vmin=0,vmax=150,zoom_roi=False,save=True)
plt.show()



