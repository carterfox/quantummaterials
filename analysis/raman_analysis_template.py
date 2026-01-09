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
from brokenaxes import brokenaxes
import toolbelt as tb
def lin(x,m,b):
    return m*x + b

# tb.init_plot_params()
lab_data_folder = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/Gr_for_devices/contrast-calibration/raman/633/'
scana = lab_data_folder + '1ML_a_.txt'
scanb = lab_data_folder + '1ML_b_.txt'
scanc = lab_data_folder + '1ML_c_.txt'
scand = lab_data_folder + '1ML_d_.txt'
# scane = lab_data_folder + '1ML_e_.txt'
# scan5 = lab_data_folder + '5p_scan5.txt'

# FGT_file1 = data_subfolder + 'raman_19.txt'
# FGT_file2 = data_subfolder + 'raman_20.txt'
# FGT_file3 = data_subfolder + 'raman_21.txt'


sample = r'Graphene'
laser = '633nm'
power = '5'

file_a_data = pd.read_table(scana,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
file_b_data = pd.read_table(scanb,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
file_c_data = pd.read_table(scanc,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
file_d_data = pd.read_table(scand,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
# file_e_data = pd.read_table(scane,comment='#',names=['Raman Shift','Counts'],encoding='latin1')

maxval = np.max(file_a_data['Counts'][600:1000])
file_a_data['Counts'] = file_a_data['Counts']/maxval
file_b_data['Counts'] = file_b_data['Counts']/maxval
file_c_data['Counts'] = file_c_data['Counts']/maxval
# file5_data = pd.read_table(scan5,comment='#',names=['Raman Shift','Counts'],encoding='latin1')
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

# plt.figure(figsize=(6,4))
# x=300
# y=119
z=1.5
fig = plt.figure(figsize=(7,5))
bax = brokenaxes(xlims=((1500, 1650), (2580, 2790)))
bax.plot(file_a_data['Raman Shift'],file_a_data['Counts'],linewidth=z,label='1L',ms=0)
bax.plot(file_b_data['Raman Shift'],file_b_data['Counts'],linewidth=z,label='2L',ms=0)
bax.plot(file_c_data['Raman Shift'],file_c_data['Counts'],linewidth=z,label='3L',ms=0)
# plt.plot(file_d_data['Raman Shift'],file_d_data['Counts'],linewidth=z,label='d',ms=0)
# plt.plot(file_e_data['Raman Shift'],file_e_data['Counts'],linewidth=z,label='e',ms=0)
# plt.plot(file5_data['Raman Shift'],file5_data['Counts'],linewidth=z,c='g',label='Scan5',ms=0)
# plt.plot(file2_data['Raman Shift'],file2_data['Counts'],linewidth=z,c='b',label='s2-p2')
# plt.plot(file3_data['Raman Shift'],file3_data['Counts'],linewidth=z,c='g',label='HQ-1',linestyle='dotted')
# plt.plot(file4_data['Raman Shift'],1.3*file4_data['Counts'],linewidth=z,c='g',label='HQ-2',linestyle='dotted')
# plt.plot(file11_data['Raman Shift'][y:],file11_data['Counts'][y:]/100+17.00,linewidth=z,c='g')
# plt.plot(file22_data['Raman Shift'][y:],file22_data['Counts'][y:]/100+7.00,linewidth=z,c='r')
# plt.plot(file33_data['Raman Shift'][y:],file33_data['Counts'][y:]/100,linewidth=z,c='b',)
# plt.plot(file4_data['Raman Shift'],file4_data['Counts'],label=r'top',linewidth=1.5)
# plt.yscale('log')
# plt.yticks([400,600,800,1000,1200],['','','','',''])
# bax.axvline(1587.94,c='C0')
# bax.axvline(1584.16,c='C1')
bax.set_ylabel('Intensity (a.u.)',fontsize=15,labelpad=30)
# plt.xlim(1470,1700)
# plt.xlim(2570,2800)
# plt.yscale('log')
bax.set_xlabel('Raman Shift (cm$^{-1}$)',fontsize=15,labelpad=20)
# plt.ylim(1000,2000)
# plt.ylim(0,14000)
# bax.set_yticks([])
bax.legend(loc='center')
# plt.title(sample+' - '+laser+' - '+power+'%')

# plt.savefig(lab_data_folder+'comparison.png',bbox_inches='tight',dpi=500)
# plt.savefig(lab_data_folder+'power5-plot.png',bbox_inches='tight',dpi=500)

plt.show()

