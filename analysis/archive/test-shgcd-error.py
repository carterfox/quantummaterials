#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 11:28:02 2025

@author: carterfox
"""

import matplotlib.pylab as plt
import numpy as np
import scipy
from scipy.integrate import quad
from functools import partial
from scipy import integrate

directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/SHG/'
twisted = directory+'stacked_region1_noanalyzer.txt'
data = np.loadtxt(twisted,skiprows=7)
means = data[:,1]/np.max(data[:,1])
angles = data[:,0]*2*np.pi/180+np.pi/4


def ellipse(angle,a):
    b = 1/(a)
    # print(b)
    return a*b/np.sqrt(a**2*np.sin(angle)**2 + b**2*np.cos(angle)**2)



fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# ax.set_theta_zero_location("N")


meanshigh = means*ellipse(angles,1.05**2)
meanslow = means*ellipse(angles,0.95**2)

fhigh = integrate.simps(meanshigh,angles)
flow = integrate.simps(meanslow,angles)

print(fhigh)
print(flow)
print(abs(fhigh-flow)/(fhigh+flow))

ax.plot(angles,meanshigh,label='meanshigh')
ax.plot(angles,meanslow,label='meanslow')
ax.plot(angles,means,label='means')
ax.legend()

plt.show()