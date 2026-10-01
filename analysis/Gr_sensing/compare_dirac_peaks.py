#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:19:58 2026

@author: carterfox
"""

import numpy as np
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from devices.dualgate import DualGate,DualGate_MLGsense
import toolbelt as tb
import os
from matplotlib.lines import Line2D
import math
import glob
from pathlib import Path
import logging

logging.getLogger('matplotlib').setLevel(logging.WARNING)
cur_dir = os.path.dirname(os.path.abspath(__file__))

tb.init_plot_params()
acolor='peru'
dcolor='steelblue'
fitascend_color='darkred'
fitdescend_color='mediumblue'

path="/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/"
path2=path+"other/option1_chip1/TM_S6/after_2ndclean/fourterm_RgrV1V2/"
# path=path+"option1_chip1/BM_S8/fourterm_Rgr_V1V2/"
path1 = path + "CrI3/round8/firstrun/c6_2L2L_3-1/GrSensorSingle/Vt_ground_twoterm/"
path3 = path + "CrI3/round8/c3_4L/GrSensorSingle/295K/"
path4 = path + "option4-chip1/twoterm_Rgr_V1V2/"
path5 = path + "option4-chip1/threeterm_Rgr_V23/"
path6 = path + "option4-chip1/threeterm_Rgr_V12/"
path7 = path + "option4-chip2/twoterm_Rgr_V1V3/"
path8 = path + "option4-chip2/fourterm_Rgr_V3V5/"
path9 = path + "option4-chip2/fourterm_Rgr_V1V3/"
# data_path = path + 'loop3.txt'
sample1 = DualGate_MLGsense('CrI3_2L+2L_MLG', d_b=11, d_m=2, d_t=11, d_flake=2.8, data_path=path)
sample2 = DualGate_MLGsense('option1test_TM', d_b=7, d_m=0, d_t=0, d_flake=0, data_path=path)
# sample = DualGate_MLGsense('option1test_BM', d_b=28, d_m=0, d_t=0, d_flake=0, data_path=path)
sample3 = DualGate_MLGsense('4L', d_b=8.7, d_m=3, d_t=0.01, d_flake=2.8, data_path=path)
sample4 = DualGate_MLGsense('option4_chip1', d_b=31, d_m=0, d_t=0, d_flake=0, data_path=path)
sample5 = sample4
sample6 = sample4
sample7 = DualGate_MLGsense('option4_chip2', d_b=21.5, d_m=0, d_t=0, d_flake=0, data_path=path)
sample8 = sample7
sample9 = sample7

file1 = path1+'loop2_300k_E1E5.txt'
file2 = path2+'scan3.txt'
file3 = path3+'loop7.txt'
file4 = path4+'loop2.txt'
file5 = path5+'loop1.txt'
file6 = path6+'loop1.txt'
file7 = path7+'loop1.txt'
file8 = path8+'loop3.txt'
file9 = path9+'loop1.txt'
Vsin,Rbox=0.1,1e6

samples = [sample4,sample5]
files = [file4,file5]


# %%

fig, ax = plt.subplots(1,1,figsize=(6,5))
for sample,file in zip(samples,files):

    db,dt,dm,dc = sample.d_b, sample.d_t, sample.d_m, sample.d_flake
    db = db+dm+dc
    d_gate = db

    data = np.loadtxt(file)
    Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5]

    diffs = np.diff(Vb)
    change_indices = np.where(diffs < 0)[0]  # descending starts here
    if len(change_indices)==0: change_indices = np.array([len(Vb)-1])
    Vb_ascend, Vb_descend = Vb[:change_indices[0] + 1], Vb[change_indices[0]:]
    E_ascend, E_descend = Vb_ascend/d_gate, Vb_descend/d_gate
    ascend,descend = R_Gr[:change_indices[0]+1], R_Gr[change_indices[0]:]
    std_ascend,std_descend = R_Gr_std[:change_indices[0]+1],R_Gr_std[change_indices[0]:]

    ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)') # , ax.set_xlabel('$E_{⟂}$ (Vnm$^{-1}$)')
    plot = 'R'
    ax.set_xlim(-.4,.4)
    # ax.set_ylim(.0,.65)

    if False: 
        plot = plot+'_zoom'
        center_a = np.argmax(ascend)
        center_d = np.argmax(descend)
        width =25
        x1,x2 = center_a-width,center_a+width
        x1d,x2d = center_d-width,center_d+width
        ymax = np.max(ascend[x1:x2]+.01)
        ymin = np.min(ascend[x1:x2]-.03)
        ax.set_ylim(ymin-.04,ymax)
        ax.set_xlim(E_ascend[center_a]-.013,E_ascend[center_a]+.013)
        order = 2
        xfine = np.linspace(E_ascend[x1],E_ascend[x2],100)
        coeffs_a = np.polyfit(E_ascend[x1:x2], ascend[x1:x2], order)   # linear fit
        y_fit_a = np.polyval(coeffs_a, xfine)
        dcoeffs_a = np.polyder(coeffs_a)
        critical_points_a = np.roots(dcoeffs_a)
        coeffs_d = np.polyfit(E_descend[x1d:x2d], descend[x1d:x2d], order)   # linear fit
        xfine_d = np.linspace(E_descend[x1d],E_descend[x2d],100)
        y_fit_d = np.polyval(coeffs_d, xfine_d)
        dcoeffs_d = np.polyder(coeffs_d)
        critical_points_d = np.roots(dcoeffs_d)
        a,d = -1,-1
        dV = round(np.abs(np.real(critical_points_d[d] - critical_points_a[a])*d_gate*1000),2)
        ax.plot(xfine,y_fit_a,ms=0,zorder=5,linewidth=2,c=fitascend_color)
        ax.plot(xfine_d,y_fit_d,ms=0,zorder=5,linewidth=2,c=fitdescend_color)
        ax.axvline(critical_points_a[a],ms=0,color=fitascend_color,linestyle='-',linewidth=.75)
        ax.axvline(critical_points_d[d],ms=0,color=fitdescend_color,linestyle='-',linewidth=.75)
        ax.text(E_ascend[center_a]+.001,(ymax+ymin)/2-.05,str(dV)+'mV',fontsize=16)
        ax.errorbar(E_ascend, ascend,yerr=std_ascend,color=acolor,marker='.',linestyle='',ms=3,label=r'$\rightarrow$',elinewidth=0)
        ax.errorbar(E_descend, descend,yerr=std_descend,color=dcolor,marker='.',linestyle='',ms=3,label=r'$\leftarrow$',elinewidth=0)
        ax.legend(loc='best')
        # ax.legend(title='n={}'.format(order),loc='best')
    else:
        if sample.d_b == 7:
            ascend = ascend
            E_ascend = E_ascend - 0.02
            acolor='r'
            label='singlecap Gr + cont. clean'
        elif sample.d_b==11:
            acolor='b'
            label='CrI3 dualcap Gr (-1.5k$\Omega$)'
            ascend = ascend - 1.5
        elif sample.d_b==31:
            if file == file4:
                acolor='purple'
                label='edge 2-term'
            elif file == file5:
                acolor='black'
                label='edge 3-term V$_{23}$'
        elif sample.d_b==21.5:
            if file == file7:
                acolor='b'
                label='edge 2-term'
                ascend = ascend
            elif file == file9:
                acolor='peru'
                label='edge 4-term'
                ascend = ascend
            # elif file == file6:
            #     acolor='grey'
            #     label='edge contacts three term V12'

        else:
            acolor='g'
            label='CrI3 singlecap Gr'
            ascend = ascend
            E_ascend = E_ascend-.003


            
        ax.errorbar(E_ascend, ascend,yerr=std_ascend,color=acolor,marker='.',linestyle='-',lw=1.5,ms=0,label=label,elinewidth=0)
        # ax.errorbar(E_descend, descend,yerr=std_descend,color=dcolor,marker='.',linestyle='-',lw=2,ms=0,label=r'$\leftarrow$',elinewidth=0)
        # ax.axvline(-.0045,zorder=0,ms=0,lw=1.5)
        # ax.axvline(.0075,zorder=0,ms=0,lw=1.5)
    ax.legend(loc='upper left',fontsize=10)
    # ax.axvline(.02,c='grey',linestyle='--',lw=1,ms=0)
    # ax.axvline(-.018,c='grey',linestyle='--',lw=1,ms=0)
    ax.set_xlim(-.21,.21)
    # ax.set_ylim(0,.8)
    ax.set_xlabel("$V_b/d_b$ (V nm$^{-1})$")
    plt.savefig(cur_dir+'/compare.png',dpi=500)

plt.show()


# %%

data = np.loadtxt(file1)
sample = sample1
Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5]
db,dt,dm,dc = sample.d_b, sample.d_t, sample.d_m, sample.d_flake
db = db+dm+dc
d_gate = db
diffs = np.diff(Vb)
change_indices = np.where(diffs < 0)[0]  # descending starts here
if len(change_indices)==0: change_indices = np.array([len(Vb)-1])
Vb_ascend, Vb_descend = Vb[:change_indices[0] + 1], Vb[change_indices[0]:]
E_ascend, E_descend = Vb_ascend/d_gate, Vb_descend/d_gate
ascend,descend = R_Gr[:change_indices[0]+1], R_Gr[change_indices[0]:]
std_ascend,std_descend = R_Gr_std[:change_indices[0]+1],R_Gr_std[change_indices[0]:]

fig, ax = plt.subplots(1,1,figsize=(6,5))
x1,x2=0,1200
ax.plot(E_ascend, ascend,color=acolor,marker='.',linestyle='-',lw=1.5,ms=3,label='4-term edge')
# ax.axvline(-.005,c='grey',linestyle='--',lw=1,ms=0)
# ax.axvline(.0075,c='grey',linestyle='--',lw=1,ms=0)
p,c = curve_fit(tb.lorentzian_abs_linear_bg, E_ascend[x1:x2], ascend[x1:x2], p0=[1,0,.01,0,0])
ax.plot(E_ascend[x1:x2],tb.lorentzian_abs_linear_bg(E_ascend[x1:x2], p[0],p[1],p[2],p[3],p[4]),lw=1,ms=0)
print(p)
ax.set_xlim(-.21,.21)
# ax.set_ylim(0.02,0.07)
# ax.set_xticks([-.05,0,.05])
ax.legend(loc='upper left',fontsize=10)
ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
ax.set_xlabel("$V_b/d_b$ (V nm$^{-1})$")
# plt.savefig(cur_dir+'/compare3.png',dpi=500)
plt.show()
