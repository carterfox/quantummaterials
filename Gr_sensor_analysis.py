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

directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round6/12-5-dualgate-sensor/Gr_conductance/VCrI3_sweep1/'
# directory = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round6/12-5-dualgate-sensor/Gr_conductance/Vbsweep4/'
path = directory+''
os.chdir(path)

sweep1_file_list = ['Vb_sweep1_VI_data_Vb1500mV_.txt',
 'Vb_sweep1_VI_data_Vb1200mV_.txt',
 'Vb_sweep1_VI_data_Vb900mV_.txt',
 'Vb_sweep1_VI_data_Vb600mV_.txt',
 'Vb_sweep1_VI_data_Vb300mV_.txt',
 'Vb_sweep1_VI_data_Vb0mV_.txt',
 'Vb_sweep1_VI_data_Vb-300mV_.txt',
 'Vb_sweep1_VI_data_Vb-600mV_.txt',
 'Vb_sweep1_VI_data_Vb-900mV_.txt',
 'Vb_sweep1_VI_data_Vb-1200mV_.txt',
 'Vb_sweep1_VI_data_Vb-1500mV_.txt',
 'Vb_sweep1_VI_data_Vb-1800mV_.txt',
 'Vb_sweep1_VI_data_Vb-2100mV_.txt',
 'Vb_sweep1_VI_data_Vb-2400mV_.txt',
 'Vb_sweep1_VI_data_Vb-2400mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-2100mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-1800mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-1500mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-1200mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-900mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-600mV_return_.txt',
 'Vb_sweep1_VI_data_Vb-300mV_return_.txt',
 'Vb_sweep1_VI_data_Vb0mV_return_.txt',
 'Vb_sweep1_VI_data_Vb300mV_return_.txt',
 'Vb_sweep1_VI_data_Vb600mV_return_.txt',
 'Vb_sweep1_VI_data_Vb900mV_return_.txt',
 'Vb_sweep1_VI_data_Vb1200mV_return_.txt',
 'Vb_sweep1_VI_data_Vb1500mV_return_.txt']

sweep2_file_list = [ 
 'Vb_sweep2_VI_data_Vb1800mV_.txt',
 'Vb_sweep2_VI_data_Vb1400mV_.txt',
 'Vb_sweep2_VI_data_Vb1000mV_.txt',
 'Vb_sweep2_VI_data_Vb600mV_.txt',
 'Vb_sweep2_VI_data_Vb200mV_.txt',
 'Vb_sweep2_VI_data_Vb-200mV_.txt', 
 'Vb_sweep2_VI_data_Vb-600mV_.txt',
 'Vb_sweep2_VI_data_Vb-1000mV_.txt',
 'Vb_sweep2_VI_data_Vb-1400mV_.txt',
 'Vb_sweep2_VI_data_Vb-1800mV_.txt',
 'Vb_sweep2_VI_data_Vb-2200mV_.txt',
 'Vb_sweep2_VI_data_Vb-2600mV_.txt',
 'Vb_sweep2_VI_data_Vb-3000mV_.txt',
 'Vb_sweep2_VI_data_Vb-3000mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-2600mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-2200mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-1800mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-1400mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-1000mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-600mV_return_.txt',
 'Vb_sweep2_VI_data_Vb-200mV_return_.txt',
 'Vb_sweep2_VI_data_Vb200mV_return_.txt',
 'Vb_sweep2_VI_data_Vb600mV_return_.txt',
 'Vb_sweep2_VI_data_Vb1000mV_return_.txt',
 'Vb_sweep2_VI_data_Vb1400mV_return_.txt',
 'Vb_sweep2_VI_data_Vb1800mV_return_.txt']


sweep3_file_list = ['Vb_sweep3_VI_data_Vb3000mV_.txt',
 'Vb_sweep3_VI_data_Vb2700mV_.txt',
 'Vb_sweep3_VI_data_Vb2400mV_.txt',
 'Vb_sweep3_VI_data_Vb2100mV_.txt',
 'Vb_sweep3_VI_data_Vb1800mV_.txt',
 'Vb_sweep3_VI_data_Vb1500mV_.txt',
 'Vb_sweep3_VI_data_Vb1200mV_.txt',
 'Vb_sweep3_VI_data_Vb900mV_.txt',
 'Vb_sweep3_VI_data_Vb600mV_.txt',
 'Vb_sweep3_VI_data_Vb300mV_.txt',
 'Vb_sweep3_VI_data_Vb0mV_.txt',
 'Vb_sweep3_VI_data_Vb-300mV_.txt',
 'Vb_sweep3_VI_data_Vb-600mV_.txt',
 'Vb_sweep3_VI_data_Vb-900mV_.txt',
 'Vb_sweep3_VI_data_Vb-1200mV_.txt',
 'Vb_sweep3_VI_data_Vb-1500mV_.txt',
 'Vb_sweep3_VI_data_Vb-1800mV_.txt',
 'Vb_sweep3_VI_data_Vb-2100mV_.txt',
 'Vb_sweep3_VI_data_Vb-2400mV_.txt',
 'Vb_sweep3_VI_data_Vb-2700mV_.txt',
 'Vb_sweep3_VI_data_Vb-3000mV_.txt',    
 'Vb_sweep3_VI_data_Vb-3000mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-2700mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-2400mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-2100mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-1800mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-1500mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-1200mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-900mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-600mV_return_.txt',
 'Vb_sweep3_VI_data_Vb-300mV_return_.txt',
 'Vb_sweep3_VI_data_Vb0mV_return_.txt',
 'Vb_sweep3_VI_data_Vb300mV_return_.txt',
 'Vb_sweep3_VI_data_Vb600mV_return_.txt',
 'Vb_sweep3_VI_data_Vb900mV_return_.txt',
 'Vb_sweep3_VI_data_Vb1200mV_return_.txt',
 'Vb_sweep3_VI_data_Vb1500mV_return_.txt',
 'Vb_sweep3_VI_data_Vb1800mV_return_.txt',
 'Vb_sweep3_VI_data_Vb2100mV_return_.txt',
 'Vb_sweep3_VI_data_Vb2400mV_return_.txt',
 'Vb_sweep3_VI_data_Vb2700mV_return_.txt',
 'Vb_sweep3_VI_data_Vb3000mV_return_.txt']
summary_file = path+'VCrI3_sweep1.txt'
# summary_file = path+'VCrI3_sweep1.txt'
# VI_data_files = sweep1_file_list#[x for x in glob.glob('*.txt') if 'data' in x]
# VI_data_files = sweep2_file_list#[x for x in glob.glob('*.txt') if 'data' in x]
# VI_data_files = sweep3_file_list#[x for x in glob.glob('*.txt') if 'data' in x]
VI_data_files = [x for x in glob.glob('*.txt') if 'data' in x]
VI_data_files.sort(key=os.path.getmtime)

f = open(VI_data_files[0])
Rbox = float(f.readline().split('=')[1].strip()) #ohm

data = np.loadtxt(summary_file)

Vb_set, Vb_meas = data[:,0]/1000, data[:,1]/1000 #V
R_Gr = data[:,2] #Ohm
Ib = data[:,3] #uA

Vb_list = []

Rgr_list = []
plot_all = True
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
    
    Vref = VIdata[:,0][0:]*1000 #mV
    Vbox = VIdata[:,1][0:] #mV
    Ibox = VIdata[:,2][0:] #uA
    Ibox2 = Ibox.reshape(len(Ibox),1)
    # Rdev = VIdata[:,3][4:] #ohm
    # theta = VIdata[:,4][4:] #deg
    
    
    model = HuberRegressor()
    model.fit(Ibox2,Vref)
    
    pred = model.predict(Ibox2)
    # plt.plot(Ibox,pred,label='huber')
    residuals = abs(pred-Vref)
    # print(Vb_str,residuals)
    outliers = np.where(residuals>=1)
    if len(outliers[0]) !=0:
        rem = Vref[outliers]
        # print(Vb_str,residuals)
        print('removing Vref = ',rem, '   in Vb = ',Vb_str)
    Ibox_noout = Ibox[np.where(residuals<1)]
    Vref_noout = Vref[np.where(residuals<1)]
    
    popt, pcov = curve_fit(line, Ibox_noout, Vref_noout)
    popt1, pcov1 = curve_fit(line, Ibox, Vref)
    Rtotal = popt[0]*10**3 #ohm
    
    R_std = round(np.sqrt(np.diag(pcov)[0])*1000,2)
    Rgr = round(Rtotal - Rbox)
    # print(Rgr,R_std)
    Rgr_list.append(Rgr)
    if plot_all:
        fig = plt.figure(figsize=(7,5))
        plt.xlabel(r'I (uA)',fontsize=16), plt.ylabel(r'V$_{ref}$ (mV)',fontsize=16)
        plt.title(r"V$_b$ = "+Vb_str,fontsize=16)
        plt.scatter(Ibox,Vref,label='data')
        plt.ylim(0,27)
        plt.xlim(0,.7)
        plt.plot(Ibox_noout,line(Ibox_noout,popt[0],popt[1]),c='r',label='linear fit')
        plt.text(.02,20,s=r'$R_{Gr}$ = '+str(Rgr)+' $\Omega$',fontsize=12)
        # plt.plot(Ibox,line(Ibox,popt1[0],popt1[1]),label='linear')
        plt.legend(fontsize=12)
        plt.savefig(path+'IV_fit_'+Vb_str,bbox_inches='tight')

    
plt.legend()
# Rgr_list = np.array(Rgr_list)
# Vb_set = np.array(Vb_set)
plt.figure(figsize=(7,5))
plt.plot(Vb_list,Rgr_list,marker='.',markersize=10)
# plt.plot(1000*np.append(initialV,Vb_set),np.append(initialR,Rgr_list),marker='.',markersize=10)
plt.xlabel(r'$V_{CrI3}$ ($mV$)',fontsize=16)
plt.ylabel(r'$R_{Gr}$ ($\Omega$)',fontsize=16)
plt.savefig('Rgr_plot_sweep4',bbox_inches='tight')
plt.figure(figsize=(7,5))
plt.plot(Vb_list,1000/np.array(Rgr_list),marker='.',markersize=10)
# plt.plot(1000*np.append(Vb_list,Vb_set),1000/np.append(initialR,Rgr_list),marker='.',markersize=10)
plt.xlabel(r'$V_{CrI3}$ (mV)',fontsize=16)
plt.ylabel(r'$G_{Gr}$ (mS)',fontsize=16)
plt.savefig('Ggr_plot_sweep4',bbox_inches='tight')
    
    
    