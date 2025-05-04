#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:34:00 2025

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
import sif
from sif_tools import sif2array
import helper_function_library as hf
hf.init_plot_params()

def rshift(lambda_exc,lambda_raman):
    return (10**7)*(1/lambda_exc - 1/lambda_raman)
    
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/non-gated_devices/raman-pumpprobe-rmcd_sample_2-12-25/raman_lowf/roomtemp/'

twisted = path+'GRT3_Exp120x6_CrI3_0324_300_0k_twisted_1_pol0.sif'
twisted2 = path+'GRT3_Exp240x15_CrI3_0324_300_0k_twisted_1_pol0.sif'
fourlayer = path+'GRT3_Exp120x6_CrI3_0324_300_0k_4L_1_pol0.sif'
thick = path+'GRT3_Exp120x6_CrI3_0324_300_0k_thick_1_pol0.sif'
bilayer = path+'GRT3_Exp120x6_CrI3_0324_300_0k_2L_1_pol0.sif'
# BN = path+''


# twisted = path+'GRT3_Exp120x6_CrI3_0324_2_0k_twisted_1_pol0.sif'
# fourlayer = path+'GRT3_Exp120x6_CrI3_0324_2_0k_4L_1_pol0.sif'
# thick = path+'GRT3_Exp120x3_CrI3_0324_2_0k_thickstack_1_pol0.sif'
# bilayer = path+'GRT3_Exp120x6_CrI3_0324_2_0k_2L_1_pol0.sif'
# # BN = path+'GRT3_Exp120x6_CrI3_0324_2_0k_below2L_1_pol0.sif'

data = sif2array(twisted)
data2 = sif2array(twisted2)
data4l = sif2array(fourlayer)
data2l = sif2array(bilayer)
# dataBN = sif2array(BN)
datathick = sif2array(thick)

wavelengths = rshift(632.8,data[:,0])
intensities = data[:,1]

wavelengths = rshift(632.8,data2[:,0])
intensities2 = data2[:,1]
wavelengths_4l = rshift(632.8,data4l[:,0])
intensities_4l = data4l[:,1]
wavelengths_thick = rshift(632.8,datathick[:,0])
intensities_thick = datathick[:,1]

wavelengths_2l = rshift(632.8,data2l[:,0])
intensities_2l = data2l[:,1] 

# wavelengths_bn = rshift(632.8,dataBN[:,0])
# intensities_bn = dataBN[:,1]*1#6


fig, ax0 = plt.subplots(1,1,figsize=(6,4))

# ax0.plot(wavelengths_thick,intensities_thick,label='thick')

if False:
    x=2
    wavelengths = wavelengths.reshape(-1, x).mean(axis=1)
    wavelengths_4l = wavelengths_4l.reshape(-1, x).mean(axis=1)
    wavelengths_2l = wavelengths_2l.reshape(-1, x).mean(axis=1)
    intensities = intensities.reshape(-1, x).mean(axis=1)
    intensities_4l = intensities_4l.reshape(-1, x).mean(axis=1)
    intensities_2l = intensities_2l.reshape(-1, x).mean(axis=1)

ax0.plot(wavelengths,intensities+200,label='Polar 2L+2L',c='b',marker='')
ax0.plot(wavelengths_4l,intensities_4l,label='Natural 4L',c='black',marker='',)
ax0.plot(wavelengths_2l,intensities_2l-200,label='Natural 2L',c='brown',marker='')
# ax0.plot(wavelengths,intensities2,label='2L+2L long')
# ax0.plot(wavelengths_bn,intensities_bn,label='BN',zorder=0)
# ax0.text(39.2,6650,r'$\uparrow$',fontsize=15)
# ax0.text(35.0,6100,r'$\uparrow$',fontsize=15)
# ax0.text(14.6,5400,r'$\uparrow$',fontsize=15)
# ax0.axvline(42,c='gray',zorder=0,ymax=.07)
# ax0.axvline(38.2,c='gray',zorder=0,ymax=.061)
# ax0.axvline(16.5,c='gray',zorder=0,ymax=.1)
# # plt.yscale('log')
ax0.set_ylim(5600)
ax0.set_xlim(60,140)
#ax0.set_title('293K - 0T',fontsize=ls)
# ax1.set_ylabel(r'Phase ($^{\circ}$)',fontsize=18)

ax0.set_xlabel(r'Raman Shift (cm$^{-1}$)')
ax0.set_ylabel('Intensity (a.u.)')
ax0.set_yticks([5750,6000,6250,6500,6750],[])
# ax0.ticklabel_format(axis='both')
ax0.legend(loc='upper left',framealpha=1)



plt.savefig(path+'Raman_plot_293K_0T.png')


plt.show()