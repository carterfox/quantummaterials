#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 15:48:27 2025

@author: carterfox
"""

import matplotlib.pylab as plt
import scipy
import numpy as np
import pandas as pd

directory = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/non-gated_devices/raman-pumpprobe-rmcd_sample_2-12-25/pump-probe/'

natural_c1 = directory+'CrI3nature_132_2.4mW_0.8mVprobe.txt'
natural_c2 = directory+'CrI3nature_42_2.4mW_0.8mVprobe.txt'
twisted_c1 = directory+'CrI3tw_132_2.4mW_0.715mVprobe.txt'
twisted_c1_2 = directory+'CrI3tw-132_5mW_1.38mVprobe.txt'
twisted_c1_3 = directory+'CrI3tw_132_2.4mW_mVprobe_long.txt'
twisted_c2 = directory+'CrI3tw_42_2.4mW_0.72mVprobe.txt'
twisted_c2_2 = directory+'CrI3tw_42_5mW_1.38mVprobe.txt'


file = twisted_c2_2
sample = 'natural c2_2 5mW'

data = np.loadtxt(file,skiprows=2)
time, dR, theta = data[:,0],data[:,1],data[:,2]
# print(time)
R = 0.00138
t0=988.5
time = -time/0.15 +t0
signal = dR/R

fft_ind = 45,270
signal_fft = signal[fft_ind[0]:fft_ind[1]]
time_fft = time[fft_ind[0]:fft_ind[1]]

sample_rate = 1/(time[1]-time[0])

fft_values = np.fft.rfft(signal_fft)
fft_frequencies = np.fft.rfftfreq(len(signal_fft), 1/sample_rate)


fig, (ax0,ax1) = plt.subplots(1,2,figsize=(8,4),gridspec_kw={'width_ratios': [1,2]})
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position("right")
plt.title(sample)
ax0.plot(time,signal)
ax0.plot(time_fft,signal_fft,label='FFT range')
ax1.plot(fft_frequencies, np.abs(fft_values))
ax0.legend()
# ax1.plot(freqs)
ax0.set_xlabel('Time (ps)',fontsize=14)
ax0.set_ylabel('dR/R',fontsize=14)
ax1.set_xlabel('Frequency (THz)',fontsize=14)
ax1.set_ylabel('FFT',fontsize=14)
# ax1.axvline(.46)
# ax0.set_xlim(-.5)
ax1.set_xlim(-.05,6)
ax0.set_ylim(.004)
ax1.set_ylim(-.001,.015)
# plt.ylim(.004)
# ax0.text(1,.0012,r'$t_0=$'+str(t0))
sample = sample.replace('.','p').replace(' ','_')
plt.savefig(directory+sample,bbox_inches='tight',dpi=500)
plt.show()
# plt.ylim(-0.0002,0.0003)



# twisted = path+'p3_book3.xls'
# natural = path+'p3_book1.xls'

# data_twisted = pd.read_excel(twisted,'Sheet1',names=['time','LCP_R','RCP_R','CD_R','LCP_dR_R','RCP_dR_R','CD_dR_R'])
# data_natural = pd.read_excel(natural,'Sheet1',names=['time','LCP_R','RCP_R','CD_R','LCP_dR_R','RCP_dR_R','CD_dR_R'])
# plt.figure()
# plt.plot(data_twisted['time'],data_twisted['LCP_dR_R'])
# plt.plot(data_twisted['time'],data_twisted['RCP_dR_R'])
# plt.plot(data_twisted['time'],data_twisted['CD_dR_R']*100,c='r',label='Twisted')
# plt.plot(data_natural['time'],data_natural['CD_dR_R']*100,c='b',label='Natural')
