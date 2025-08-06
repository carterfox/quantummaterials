#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:59:10 2023

@author: carterfox

data analysis of SHG measurements""
"""

import numpy as np
import matplotlib.pylab as plt
import helper_function_library as hf
hf.init_plot_params()
plt.rcParams["font.size"] = 12
plt.rcParams["xtick.direction"] = 'out'
plt.rcParams["ytick.direction"] = 'out'
#     x = theta+phi
#     return ( A*np.sin(3*x) + B*np.sin(x) + C*np.cos(3*x) + D*np.cos(x) )**2 + h

labdata = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/'
path = labdata+'StackingTransitions/CrI3/non-gated_devices/10-11-23/shg/80K/NIR_obj/10-18/'

temp = '80K'
sample = r'CrI3 2L+2L'

file_path1 = path+'stacked_0T_good.txt'
file_path2 = path+'unstacked_0T_good.txt'
file_path3 = path+'BN_0T_good.txt'

files = np.array([file_path1,file_path2,file_path3])
labels = ['Polar stacking','Natural stacking', 'Substrate']
title = '80K SHG Intensity'

fig,ax,angles_list,means_list,stds_list = hf.plotseveralSHG(title,files,labels,factor=[1,.8,1],ms=8,append=True,normalize=True,legend=False,el=.4,subtract_substrate=False)


plt.savefig(path+'SHG_plot_nolegend_scaled_natural_0p8_'+sample.replace('+','p')+'.png',)

plt.show()