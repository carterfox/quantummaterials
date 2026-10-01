#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:23:49 2024

@author: carterfox

Gr Sensor data analysis 
"""

# Rbox (Ohm) = 40000.000000
# Lockin wait time (ms) = 4000
# Freq (Hz) = 1000.000000
# Vb(V) = 0.000000
# Vref(V) Vbox(V) Ibox(A) Rdev(Ohm) theta(deg)

# Vb_set(mV) Vb_meas(mV) R_Gr(Ohm) Ib(uA) 


import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import glob 
import os 
from sklearn.linear_model import HuberRegressor
from sklearn.preprocessing import StandardScaler

def line(x,m,b):
    return m*x+b

initialR = np.array([1496, 1519, 1499, 1521, 1473, 1521, 1516, 1523, 1516, 1512, 1516,
       1503, 1521, 1494, 1503, 1517, 1516, 1511, 1535, 1506, 1509, 1539,
       1525, 1526, 1523, 1514, 1520, 1538])
initialV = np.array([0.0024 , 0.00237, 0.00234, 0.00231, 0.00228, 0.00225, 0.00222,
       0.00219, 0.00216, 0.00213, 0.0021 , 0.00207, 0.00204, 0.00201,
       0.00198, 0.00195, 0.00192, 0.00189, 0.00186, 0.00183, 0.0018 ,
       0.00177, 0.00174, 0.00171, 0.00168, 0.00165, 0.00162, 0.00159])

directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round6/12-5-dualgate-sensor/Gr_conductance/Vbsweep1_measGr/'
path = directory+''
os.chdir(path)

summary_file = path+'Vbsweep1_measGr.txt'

VI_data_files = [x for x in glob.glob('*.txt') if 'data' in x]
VI_data_files.sort(key=os.path.getmtime)

f = open(VI_data_files[0])
Rbox = float(f.readline().split('=')[1].strip()) #ohm

data = np.loadtxt(summary_file)

Vb_set, Vb_meas = data[:,0]/1000, data[:,1]/1000 #V
R_Gr = data[:,2] #Ohm
Ib = data[:,3] #uA

Vb_list = []

Rgr_list,Rgr_list_std = [],[]
plot_all = False
for file in VI_data_files:
    f = open(file)
    a = f.readlines()[3]
    Vb = int(1000*float(a.split(' = ')[1].strip()))
    VIdata = np.loadtxt(file)
    # Vb = int(file.split('mV')[0].split('Vb')[2])
    Vb_list.append(Vb)
    Vb_str = str(Vb) + 'mV'
    if 'return' in file:
        Vb_str = Vb_str + '_return'
    
    # Vref = VIdata[:,0][0:]*1000 #mV
    Vgr = VIdata[:,1][0:] #mV
    Igr = VIdata[:,2][0:] #uA
    Igr2 = Igr.reshape(len(Igr),1)
    # Rdev = VIdata[:,3][4:] #ohm
    # theta = VIdata[:,4][4:] #deg
    
    
    model = HuberRegressor()
    model.fit(Igr2,Vgr)
    
    pred = model.predict(Igr2)
    # plt.plot(Ibox,pred,label='huber')
    residuals = abs(pred-Vgr)
    # print(Vb_str,residuals)
    outliers = np.where(residuals>=1)
    if len(outliers[0]) !=0:
        rem = Vgr[outliers]
        # print(Vb_str,residuals)
        print('removing Vref = ',rem, '   in Vb = ',Vb_str)
    Igr_noout = Igr[np.where(residuals<1)]
    Vgr_noout = Vgr[np.where(residuals<1)]
    
    popt, pcov = curve_fit(line, Igr_noout, Vgr_noout)
    popt1, pcov1 = curve_fit(line, Igr, Vgr)
    Rgr = popt[0]*1000 #ohm
    Rgr_std = np.sqrt(np.diag(pcov)[0])*1000
    
    # R_std = round(np.sqrt(np.diag(pcov)[0])*1000,2)
    # Rgr = round(Rtotal - Rbox)
    # print(Rgr,R_std)
    Rgr_list.append(Rgr)
    Rgr_list_std.append(Rgr_std)
    if plot_all:
        fig = plt.figure(figsize=(7,5))
        plt.xlabel(r'I (nA)',fontsize=16), plt.ylabel(r'V$_{gr}$ ($\mu$V)',fontsize=16)
        plt.title(r"V$_b$ = "+Vb_str,fontsize=16)
        plt.scatter(Igr,Vgr,label='data')
        # plt.ylim(0,27)
        # plt.xlim(0,.7)
        plt.plot(Igr_noout,line(Igr_noout,popt[0],popt[1]),c='r',label='linear fit')
        # plt.text(.02,20,s=r'$R_{Gr}$ = '+str(Rgr)+' $\Omega$',fontsize=12)
        # plt.plot(Ibox,line(Ibox,popt1[0],popt1[1]),label='linear')
        plt.legend(fontsize=12)
        plt.savefig(path+'IV_fit_'+Vb_str,bbox_inches='tight')
Rgr_list = np.array(Rgr_list)/1000
Rgr_list_std = np.array(Rgr_list_std)/1000

    
plt.legend()
# Rgr_list = np.array(Rgr_list)
# Vb_set = np.array(Vb_set)
fig, ax0 = plt.subplots(1,1,figsize=(7,5))
d_b=6 #nm
E = np.array(Vb_list)/d_b/1000 #V/nm
going_down = np.where(np.diff(E)<.00001)
going_up = np.where(np.diff(E)>0)
E_up = E[going_up]
E_down = E[going_down]
Rgr_up = Rgr_list[going_up]
Rgr_down = Rgr_list[going_down]
Rgr_std_up = Rgr_list_std[going_up]
Rgr_std_down = Rgr_list_std[going_down]
Ggr_up = 1/Rgr_up
Ggr_down = 1/Rgr_down
Ggr_std_up = 0/Rgr_std_up
Ggr_std_down = 0/Rgr_std_down
# ax0.errorbar(E_up,Rgr_up,yerr=Rgr_std_up,label=r'$\rightarrow$',c='r',marker='.',markersize=7)
# ax0.errorbar(E_down,Rgr_down,yerr=Rgr_std_down,label=r'$\leftarrow$',c='b',marker='.',markersize=7)
# ax0.set_xlabel(r'$E_{\perp}$ (V/nm)',fontsize=16)
# ax0.set_ylabel(r'$R_{Gr}$ (k$\Omega$)',fontsize=16)
# ax0.legend()
# plt.title('CrI3 2L+2L')
# plt.savefig('Rgr_APS_plot.png',bbox_inches='tight')

ax0.errorbar(E_up,Ggr_up,yerr=Ggr_std_up,label=r'$\rightarrow$',c='r',marker='.',markersize=7)
ax0.errorbar(E_down,Ggr_down,yerr=Ggr_std_down,label=r'$\leftarrow$',c='b',marker='.',markersize=7)
ax0.set_xlabel(r'$E_{\perp}$ (V/nm)',fontsize=16)
ax0.set_ylabel(r'$G_{Gr}$ (mS)',fontsize=16)
ax0.legend()
plt.title('CrI3 2L+2L')
plt.savefig('Ggr_APS_plot.png',bbox_inches='tight')