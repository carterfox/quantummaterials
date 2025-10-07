#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 21:08:59 2023

@author: carterfox

Raman measurement data analysis template
"""


import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import toolbelt as tb
def lin(x,m,b):
    return m*x + b

tb.init_plot_params()
lab_data_folder = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/TEM-samples/Rice_measurement_run2/'
# BN_file = data_subfolder+'BN.txt'
# file5 = lab_data_folder + 'thickish.txt'
s1_p1 = lab_data_folder+'sample5_60deg_2L2L/2l-60deg-stacked-raman.txt'
s2_p1 = lab_data_folder+'sample4_90deg_3L3L/3l-90deg-stacked-raman.txt'
# s1_p2 = lab_data_folder+'sample2-p2.txt'
# r5 = lab_data_folder+'r5.txt'

# FGT_file1 = data_subfolder + 'raman_19.txt'
# FGT_file2 = data_subfolder + 'raman_20.txt'
# FGT_file3 = data_subfolder + 'raman_21.txt'


sample = r'NbOI2'
laser = '532nm'
power = '1'

file1_data = pd.read_table(s1_p1,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
file2_data = pd.read_table(s2_p1,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
# file2_data = pd.read_table(s1_p2,comment='#',names=['Raman Shift','Counts'])
# file5_data = pd.read_table(r5,comment='#',names=['Raman Shift','Counts'])

# file3_data = pd.read_table(pos3low,comment='#',names=['Raman Shift','Counts'])
# file11_data = pd.read_table(pos2high,comment='#',names=['Raman Shift','Counts'])
# file22_data = pd.read_table(pos1high,comment='#',names=['Raman Shift','Counts'])
# file33_data = pd.read_table(pos3high,comment='#',names=['Raman Shift','Counts'])
# file4_data = pd.read_table(file4,comment='#',names=['Raman Shift','Counts'])
# file5_data = pd.read_table(file5,comment='#',names=['Raman Shift','Counts'])
# CrI3_2_data = pd.read_table(CrI3_file2,comment='#',names=['Raman Shift','Counts'])
# CrI3_3_data = pd.read_table(CrI3_file3,comment='#',names=['Raman Shift','Counts'])

# FGT1_data = pd.read_table(FGT_file1,comment='#',names=['Raman Shift','Counts'])
# FGT2_data = pd.read_table(FGT_file2,comment='#',names=['Raman Shift','Counts'])
# FGT3_data = pd.read_table(FGT_file3,comment='#',names=['Raman Shift','Counts'])

plt.figure(figsize=(6,4))
# x=300
# y=119
z=1.5
plt.plot(file1_data['Raman Shift'],file1_data['Counts'],linewidth=z,c='b',label='sample5',ms=0)
plt.plot(file2_data['Raman Shift'],file2_data['Counts'],linewidth=z,c='r',label='sample4',ms=0)
# plt.plot(file2_data['Raman Shift'],file2_data['Counts'],linewidth=z,c='b',label='s2-p2')
# plt.plot(file3_data['Raman Shift'],file3_data['Counts'],linewidth=z,c='g',label='HQ-1',linestyle='dotted')
# plt.plot(file4_data['Raman Shift'],1.3*file4_data['Counts'],linewidth=z,c='g',label='HQ-2',linestyle='dotted')
# plt.plot(file11_data['Raman Shift'][y:],file11_data['Counts'][y:]/100+17.00,linewidth=z,c='g')
# plt.plot(file22_data['Raman Shift'][y:],file22_data['Counts'][y:]/100+7.00,linewidth=z,c='r')
# plt.plot(file33_data['Raman Shift'][y:],file33_data['Counts'][y:]/100,linewidth=z,c='b',)
# plt.plot(file4_data['Raman Shift'],file4_data['Counts'],label=r'top',linewidth=1.5)
# plt.yscale('log')
# plt.yticks([400,600,800,1000,1200],['','','','',''])
plt.ylabel('Intensity (a.u.)',fontsize=14)
plt.xlim(80,300)
# plt.yscale('log')
plt.xlabel('Raman Shift (cm$^{-1}$)',fontsize=14)
plt.ylim(1000,2000)
# plt.xlim(94,110)
plt.legend(loc='upper right',fontsize=10)
# plt.title(sample+' - '+laser+' - '+power+'%')

# plt.savefig(lab_data_folder+power+'_'+sample+'.png',bbox_inches='tight',dpi=300)
plt.savefig(lab_data_folder+'sample5-raman.png',bbox_inches='tight',dpi=500)

plt.show()

