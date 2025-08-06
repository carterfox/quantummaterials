#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:07:32 2024

@author: carterfox
"""

import numpy as np
import matplotlib.pylab as plt
import os
import glob


os.chdir('/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/dual_gate_devices_round1/SHG/gate_sweep2/')
files=os.listdir('.')

files.sort(key=lambda x: os.path.getmtime(x))
# files = files[3:]
means,stds = [],[]
files = np.array(files)
files=np.delete(files,np.where(files=='info.txt'))
files=np.delete(files,np.where(files=='gatesweep2.png'))

for file in files:
    data=np.loadtxt(file,skiprows=4)
    counts = data[:,1]
    mean = np.mean(counts)
    std = np.std(counts)
    means.append(mean)
    stds.append(std)
    
plt.figure()
voltage1 = np.arange(0,19,1)
means1 = means[0:len(voltage1)]
stds1 = stds[0:len(voltage1)]
voltage2 = np.arange(17,-2,-2)
means2 = means[len(voltage1):(len(voltage1)+len(voltage2))]
stds2 = stds[len(voltage1):(len(voltage1)+len(voltage2))]
voltage3 = np.arange(-1,-19,-1)
means3 = means[(len(voltage1)+len(voltage2)):(len(voltage1)+len(voltage2)+len(voltage3))]
stds3 = stds[(len(voltage1)+len(voltage2)):(len(voltage1)+len(voltage2)+len(voltage3))]
voltage4 = np.arange(-17,9,2)
means4 = means[(len(voltage1)+len(voltage2)+len(voltage3)):]
stds4 = stds[(len(voltage1)+len(voltage2)+len(voltage3)):]

voltage23 = np.append(voltage2,voltage3)
means23 = np.append(means2,means3)
stds23 = np.append(stds2,stds3)
plt.errorbar(voltage4,means4,yerr=stds4,label=r'$\rightarrow$',marker='.',elinewidth=.5)
# plt.errorbar(voltage3,means3,yerr=stds3,label=r'$\leftarrow$',marker='.',elinewidth=.5)
plt.errorbar(voltage23,means23,yerr=stds23,label=r'$\leftarrow$',marker='.',elinewidth=.5)
plt.errorbar(voltage1,means1,yerr=stds1,label=r'$\rightarrow$',marker='.',elinewidth=.5)
plt.xlabel('Voltage (V)',fontsize=18)
plt.ylabel('Counts',fontsize=18)
plt.legend()
# plt.xlabel('Voltage (V)',fontsize=18)
# plt.ylabel('Counts',fontsize=18)
# plt.figure()
# plt.plot(means)

plt.savefig('gatesweep2.png',bbox_inches='tight')
