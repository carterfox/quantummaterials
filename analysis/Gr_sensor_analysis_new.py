#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 16:24:20 2025

@author: carterfox
"""


import numpy as np
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from devices.dualgate import DualGate
import toolbelt as tb
import os
from matplotlib.lines import Line2D
from sklearn.linear_model import HuberRegressor
import glob


path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/GrSensor/'    
folder = path+'sweep10_2K_0T_VI_data/*'

filelist = glob.glob(folder)
filelist.sort(key=os.path.getmtime)

Vb_list = []
Vgr_list, Igr_list = [],[]
Rgr_list=[]
index = -5

for file in filelist:
    # print(file)
    Vb = float(file.split('Vb')[1].split('mV')[0])/1000
    data = np.loadtxt(file)
    Vgr = data[:,1]
    Igr = data[:,2]
    Vgr_list.append(Vgr[index])
    Igr_list.append(Igr[index])
    Rgr_list.append(Vgr[index]/Igr[index])
    Vb_list.append(Vb)
    
    
tb.init_plot_params()
fig, ax = plt.subplots(1,1,figsize=(6,5))
ax.plot(Vb_list, Rgr_list,color='red',marker='.',ms=5,label=r'$\rightarrow$')
ax.set_xlabel('V$_{b}$ (V)'), ax.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
ax.set_ylim(1.7,2.4)
ax.set_xlim(-.5,7.5)
ax.legend()
plt.show()