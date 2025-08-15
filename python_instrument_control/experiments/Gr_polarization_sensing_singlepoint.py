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


def main(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter,Vb_array,Vsin,file_save):
  
    
    lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin)
    Rbox = sample.Rbox
    d_b = sample.d_b
    saving_file = make_files(sample,lockin,file_save)

    plt.ion()
    fig,ax1,line1 = init_plot()
    
    keithley_b.enable_source()
    keithley_b.apply_voltage(compliance_current=keithley_b.compliance_current)
    
    Vb_list, R_Gr_list = [],[]
    
    for Vb in Vb_array: # sweep Vb 

        keithley_b.source_voltage = Vb
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)
        print(Vb,V_b_meas,I_b_meas)
        
        time.sleep(lockin.delay)
        
        mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
        V_Gr, V_Gr_std = mean_R_chan[0], std_R_chan[0]
        V_Gr = V_Gr*10**6   #uV 
        Vbox = Vsin*10**6 - V_Gr  #uV
        I_Gr = Vbox/Rbox *10**3 #nA  . Rbox should be in ohm
        R_Gr = V_Gr/I_Gr
        
        Vb_list.append(Vb)
        R_Gr_list.append(R_Gr) #kOhm
        
        save_data([Vb,V_b_meas,I_b_meas,R_Gr,V_Gr,I_Gr,V_Gr_std,Vbox],saving_file)
        update_plot(line1,Vb_list,R_Gr_list,ax1,fig)

    plt.ioff()
    plt.show()
    
    return Vb_list, R_Gr_list
    
    

def save_data(data_save,saving_file):
    with open(saving_file, 'a') as file:
        file.write(' '.join(f"{d:.9f}" for d in data_save) + '\n') 
        
def update_plot(line: Line2D, x_data, y_data, ax: plt.Axes, fig: plt.Figure, pause_time: float = 0.05):
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)

def init_plot():
    fig, ax1 = plt.subplots()
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_xlabel(r'V$_{b}$ (V)')
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    line1 = Line2D([], [], color='blue',marker='.')
    ax1.add_line(line1)
    return fig,ax1,line1

def make_files(sample,lockin,file_save):
    if not os.path.exists(sample.data_path+"/GrSensor"):
        os.makedirs(sample.data_path+"/GrSensor")
    gen_path = sample.data_path+'/GrSensor/'+file_save
    saving_file = make_Gr_resistance_saving_file(gen_path,sample.Rbox,lockin.delay,lockin.sine_out_freq,0,file='full')
    return saving_file


def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,file='Vb'):
    if file == 'full':
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        header = '#Vb_set(V) Vb_meas(V) Ib_meas(nA) R_Gr(kOhm) V_Gr(uV) I_Gr(nA) V_Gr_std(uV) Vbox(uV)'
        with open(filename, 'a') as file:
            file.write(header + '\n') 
    return filename


if __name__ == "__main__":

    path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/GrSensor/'    
    file = path+'sweep10_2K_0T.txt'
    
    data = np.loadtxt(file)
    Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4]
    
    diffs = np.diff(Vb)
    try:
        transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+1
    except:
        transition_index=int(len(Vb)/2)
        
        
    # G_Gr = 1000/R_Gr
    # G_Gr_std = 1000/R_Gr_std
    
    Vb_ascend = Vb[0:transition_index]
    Vb_descend = Vb[transition_index:]
    R_Gr_ascend = R_Gr[0:transition_index]
    R_Gr_descend = R_Gr[transition_index:]
    R_Gr_std_ascend = R_Gr_std[0:transition_index]
    R_Gr_std_descend = R_Gr_std[transition_index:]
    
    
    tb.init_plot_params()
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    ax.errorbar(Vb_descend, R_Gr_descend,color='black',marker='.',ms=5,label=r'$\rightarrow$',elinewidth=0)
    ax.errorbar(Vb_ascend, R_Gr_ascend,color='r',marker='.',ms=5,label=r'$\leftarrow$',elinewidth=0)
    # ax.errorbar(Vb_ascend, G_Gr_ascend,color='black',marker='.',ms=5,label=r'$\rightarrow$',elinewidth=0)
    # ax.errorbar(Vb_descend, G_Gr_descend,color='r',marker='.',ms=5,label=r'$\leftarrow$',elinewidth=0)
    ax.legend()
    ax.set_xlabel('V$_{b}$ (V)'), ax.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    ax.set_ylim(1.7,2.4)
    ax.set_xlim(-.5,7.5)
    # ax.set_ylim(350,700)
    # plt.savefig(file.replace('.txt','_G_plot.png'),dpi=500)
    plt.show()
    

