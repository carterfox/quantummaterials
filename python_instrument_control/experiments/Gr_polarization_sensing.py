#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 09:42:58 2025

@author: carterfox
"""


import numpy as np
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from devices.dualgate import DualGate
import toolbelt as tb
import os
from matplotlib.lines import Line2D
from sklearn.linear_model import HuberRegressor
from sklearn.preprocessing import StandardScaler
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import numpy as np
import sys

def update_plot(line: Line2D, x_data, y_data, ax: plt.Axes, fig: plt.Figure, pause_time: float = 0.05):
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)

def init_plot():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,8))
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_xlabel(r'V$_{b}$ (V)')
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    line1 = Line2D([], [], color='blue',marker='.')
    ax1.add_line(line1)
    ax2.set_xlabel(r'I$_{Gr}$ (nA)')
    ax2.set_ylabel(r'V$_{Gr}$ ($\mu$V)')
    line2 = Line2D([], [], color='red',marker='.',linewidth=0)
    ax2.add_line(line2)
    line3 = Line2D([], [], color='red',marker='')
    ax2.add_line(line3)
    return fig,ax1,ax2,line1,line2,line3

def main(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter,Vb_array,Vsin_array,file_save):
    
    lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin_array[0])
    Rbox = sample.Rbox
    d_b = sample.d_b
    
    if not os.path.exists(sample.data_path+"/GrSensor"):
        os.makedirs(sample.data_path+"/GrSensor")
    if not os.path.exists(sample.data_path+"/GrSensor/"+file_save.split('.txt')[0]):
        os.makedirs(sample.data_path+"/GrSensor/"+file_save.split('.txt')[0]+'_VI_data')
    gen_path = sample.data_path+'/GrSensor/'+file_save
    save_file_Vb_gen = sample.data_path+'/GrSensor/'+file_save.split('.txt')[0]+'_VI_data/'
    saving_file = tb.make_Gr_resistance_saving_file(gen_path,Rbox,lockin.delay,lockin.sine_out_freq,0,file='full')

    plt.ion()
    fig,ax1,ax2,line1,line2,line3 = init_plot()
    
    keithley_b.enable_source()
    keithley_b.apply_voltage()
    
    Vb_list, R_Gr_list, R_Gr_std_list = [],[],[]

    for Vb in Vb_array: # sweep Vb 

        keithley_b.source_voltage = Vb
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)
        print(Vb,V_b_meas,I_b_meas)
    
        file_Vb = tb.make_Gr_resistance_saving_file(save_file_Vb_gen,Rbox,lockin.delay,lockin.sine_out_freq,Vb,file='Vb') # make file for this Vb
        
        time.sleep(0.3)
        I_Gr_list, V_Gr_list = [],[]
        line3.set_data([],[])
        for Vsin in Vsin_array: # sweep Vsin and measure Vgr,Igr to determine Rgr at that Vb
            
            lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin)
            time.sleep(lockin.delay)
            mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
            V_Gr, theta = mean_R_chan[0], mean_R_chan[1]
            V_Gr = V_Gr*10**6   #uV 
            Vbox = Vsin*10**6 - V_Gr  #uV
            I_Gr = Vbox/Rbox *10**3 #nA  . Rbox should be in ohm
                        
            I_Gr_list.append(I_Gr) #nA
            V_Gr_list.append(V_Gr) #uV
            data = [Vsin,V_Gr,I_Gr,theta]

            # Update plot of V_Gr vs I_Gr and save new data to file
            line2.set_data(I_Gr_list,V_Gr_list)
            update_plot(line2,I_Gr_list,V_Gr_list,ax2,fig)

            with open(file_Vb, 'a') as file:
                file.write(' '.join(f"{d:.9f}" for d in data) + '\n') 
                
        lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin_array[0])
        time.sleep(3)

        R_Gr,  R_Gr_std, p = fit_resistance(I_Gr_list,V_Gr_list,Vb)
        
        fit = tb.line(np.array(I_Gr_list),p[0],p[1])
        update_plot(line3,I_Gr_list,fit,ax2,fig)
        
        Vb_list.append(Vb)
        R_Gr_list.append(R_Gr) #kOhm
        R_Gr_std_list.append(R_Gr_std) #kOhm
        data_save = [Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std]
        with open(saving_file, 'a') as file:
            file.write(' '.join(f"{d:.9f}" for d in data_save) + '\n') 
        
        # Update plot of R_Gr vs Vb and save new data to file 
        update_plot(line1,Vb_list,R_Gr_list,ax1,fig)

    plt.ioff()
    plt.show()
    
    return V_Gr_list,I_Gr_list,R_Gr_list,R_Gr_std_list
    
    
def fit_resistance(I_Gr_list,V_Gr_list,Vb):
    model = HuberRegressor()
    I_Gr_list2 = np.array(I_Gr_list).reshape(len(I_Gr_list),1)
    model.fit(I_Gr_list2,V_Gr_list)
    pred = model.predict(I_Gr_list2)
    residuals = abs(pred-V_Gr_list)
    outliers = np.where(residuals>=.8)
    if len(outliers[0]) !=0:
        rem = np.array(V_Gr_list)[outliers]
        print('removing Vref = ',rem, '   in Vb = ',str(Vb))
    Igr_noout = np.array(I_Gr_list)[np.where(residuals<1)]
    Vgr_noout = np.array(V_Gr_list)[np.where(residuals<1)]
    
    p, c = curve_fit(tb.line, Igr_noout, Vgr_noout)
    R_Gr,  R_Gr_std = p[0], np.sqrt(np.diag(c))[0]
    return R_Gr, R_Gr_std, p

