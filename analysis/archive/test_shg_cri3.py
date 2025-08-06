#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 16:44:32 2025

@author: carterfox
"""

import scipy
import numpy as np
import matplotlib.pylab as plt


def Ipar(phi,chi_xxx,chi_xyy,chi_yxy):
    
    return ( chi_xxx*np.cos(phi)**3 + (chi_xyy + 2*chi_yxy)*np.cos(phi)*np.sin(phi)**2 )**2

def Iperp(phi,chi_xxx,chi_xyy,chi_yxy):
    
    return ( chi_xyy*np.sin(phi)**3 + (chi_xxx - 2*chi_yxy)*np.sin(phi)*np.cos(phi)**2 )**2


def Ifull(phi,chi_xxx,chi_xyy,chi_yxy):
    
    I = Ipar(phi,chi_xxx,chi_xyy,chi_yxy) + Iperp(phi,chi_xxx,chi_xyy,chi_yxy)
    
    return I


phis = np.arange(0,2*np.pi+.1,.1)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
# ax.set_title(title, va='top')

chi_xxx = -.8
chi_xyy = .5
chi_yxy = .8
off=-1
Ipp = Iperp(phis+off,chi_xxx,chi_xyy,chi_yxy)
Ip = Ipar(phis+off,chi_xxx,chi_xyy,chi_yxy)
If = Ifull(phis+off,chi_xxx,chi_xyy,chi_yxy)

ax.plot(phis,Ip,c='black')
ax.plot(phis,Ipp,c='red')
ax.plot(phis,If,c='blue')