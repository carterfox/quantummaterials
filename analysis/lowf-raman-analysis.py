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
from sif_tools import SIFconvert
import toolbelt as tb
import helper_function_library as hf
tb.init_plot_params()

def rshift(lambda_exc,lambda_raman):
    return (10**7)*(1/lambda_exc - 1/lambda_raman)
    
def get_raman_data(file,norm=False):
    data = SIFconvert(file)
    lams = rshift(632.8,data[:,0])
    Is = data[:,1]
    if norm:
        Is = Is/np.max(Is)
    return lams,Is


path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/raman/'
path = path+'2K/'
stacked_long = path+'GRT3_Exp60x10_stacked_0822_2_0k_Vb0_longexposure.sif'
natural_long = path+'GRT3_Exp60x10_natural_0822_2_0k_Vb0_longexposure.sif'
Si = path+'GRT3_Exp120x3_sio2_0822_2_0k_Vb_float.sif'
BN = path+'GRT3_Exp120x3_BN_0822_2_0k_Vb_float.sif'
# natural = path+'GRT3_Exp120x6_CrI3_0324_300_0k_2L_1_pol0.sif'
# BN = path+''

stacked_long_lam, stacked_long_I = get_raman_data(stacked_long)
natural_long_lam, natural_long_I = get_raman_data(natural_long)
Si_lam, Si_I = get_raman_data(Si,norm=True)
# BN_lam, BN_I = get_raman_data(BN,norm=False)

maxval = np.max([stacked_long_I,natural_long_I])
stacked_long_I = stacked_long_I/maxval
natural_long_I = natural_long_I/maxval

fig,ax0 = plt.subplots(1,1,figsize=(7,5))
ax0.tick_params(axis='both', length=2)  

ax0.plot(stacked_long_lam,stacked_long_I,label='2L+2L Polar',c='blue',marker='',)
ax0.plot(natural_long_lam,natural_long_I-.002,label='2L Natural',c='brown',marker='',)
ax0.plot(Si_lam,Si_I+.135,label='Substrate',c='black',marker='',)
# ax0.plot(BN_lam,BN_I,label='BN',c='purple',marker='',)
# ax0.text(14.6,5400,r'$\uparrow$',fontsize=15)
# ax0.axvline(11.7,c='gray',linestyle='-',marker='',zorder=0,lw=1,label=r'11.7 cm$^{-1}$')
# ax0.set_ylim(5600)
ax0.text(12.7,.178,r'11.7 cm$^{-1}$',ha='center',fontsize=11)
ax0.set_xlim(8,60)
ax0.set_ylim(0.15,.19)
#ax0.set_title('293K - 0T',fontsize=ls)
ax0.set_xlabel(r'Raman Shift (cm$^{-1}$)')
ax0.set_ylabel('Intensity (a.u.)')
# ax0.ticklabel_format(axis='both')
# ax0.set_yscale('log')
ax0.legend()



# plt.savefig(path+'Raman_plot_long_lowf.png')


plt.show()