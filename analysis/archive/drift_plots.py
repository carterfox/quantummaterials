#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:54:40 2023

@author: carterfox
for plotting drift
"""


import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import matplotlib.cm as cm

um_per_pix = 3.45/20



x1 = np.array([619,619,619,619,619,620,620,619,618,618,618,618,618])
y1 = np.array([415,415,415,415,415,416,416,416,415.5,415.5,415,415,414])
fields1 = np.array([0,.5,1,1.5,2,2.5,3,2.5,2,1.5,1,.5,0])

x2 = np.array([616,616,616.5,617,616])
y2=np.array([414,414,415,415,414])
fields2 = np.array([0,1,2,3,0])

x3 = np.array([617,617,617,618,617,617,617])
y3 = np.array([414,414,415,415,415,414.5,414])
fields3 = np.array([0,-1,-2,-3,-2,-1,0])

def plot_drifts(x,y,fields):
    x = (x-x[0])*um_per_pix
    y = (y-y[0])*um_per_pix
    distance = np.sqrt(x**2 + y**2)
    # x =x[0:7]
    # y = y[0:7]
    # fields = fields[0:7]
    # print(x,y)

    # plt.plot(x,y,c='grey')
    # plt.scatter(x,y,c=fields,zorder=5,cmap=cm.rainbow)
    # cbar=plt.colorbar()
    # cbar.set_cmap(cm.rainbow)
    # cbar.set_label('B-field (T)')
    # plt.xlabel('X (um)')
    # plt.ylabel('Y (um)')
    # plt.figure()
    plt.scatter(fields,distance)
    plt.plot(fields,distance)
    plt.xlabel('B-Field (T)')
    plt.ylabel('Drift (um)')

plot_drifts(x3,y3,fields3)
plot_drifts(x2,y2,fields2)
# plot_drifts(x1[7:],y1[7:],fields1[7:])
# plt.xlim(-.2,.2)
# plt.ylim(-.2,.2)
# plot_drifts(x3[0:4],y3[0:4],fields3[0:4])
# plot_drifts(x3[4:],y3[4:],fields3[4:])