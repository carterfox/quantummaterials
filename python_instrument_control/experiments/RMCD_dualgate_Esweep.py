#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:09:25 2024

@author: carterfox

RMCD experiment 
"""
from typing import Union
import numpy as np
import logging
import time
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from homemade_servers.QDopticool import Opticool
from devices.dualgate import DualGate
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb
from tqdm import tqdm
import numpy as np

def main(sample: DualGate, lockin: LockInOE1022D,
         keithley_b: KeithleySourceMeter,
         E_array,file_save):
    
    """
    Perform a pure out-of-plane electric field sweep using a dual-gated sample
    and record RMCD data at each field point.

    Parameters
    ----------
    sample : DualGate
        Sample object containing geometry and file path info, including gate thicknesses.
    lockin : LockInOE1022D
        Lock-in amplifier used to collect RMCD signals.
    keithley_b : KeithleySourceMeter
        Source meter connected to the bottom gate.
    keithley_t : KeithleySourceMeter
        Source meter connected to the top gate.
    E_array : array-like
        List or array of electric field values (in V/nm) to apply.
    file_save : str
        Filename for saving the sweep data.

    Returns
    -------
    None
    """
    if not os.path.exists(sample.data_path+"/RMCD/Esweep"):
        os.makedirs(sample.data_path+"/RMCD/Esweep")

    gen_path = sample.data_path+'/RMCD/Esweep/'+file_save
    saving_file = tb.make_rmcd_saving_file(gen_path,'Esweep-Vb')
    
    plt.ion()
    fig, ax, line = init_main_plot()
    
    keithley_b.enable_source()
    keithley_b.apply_voltage()
    rmcd_list = []
    d_b = sample.d_b
    # d_t = sample.d_t
    
    for E in E_array:
        V_b = E*d_b*2
        # V_t = -V_b*d_t/d_b
        
        keithley_b.source_voltage = V_b
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)

        lockin.reset_buffer()
        time.sleep(lockin.delay)
        rmcd_data = tb.read_lockin_rmcd_data(lockin)#tb.read_lockin_rmcd_data(lockin)
        rmcd = rmcd_data[4]/rmcd_data[0]*100
        rmcd_list.append(rmcd)
        save_data(E,V_b,V_b_meas,I_b_meas,rmcd_data,saving_file)
        update_plot(fig,ax,line,E_array[0:len(rmcd_list)],rmcd_list)
        
    plt.ioff()
    plt.show()
    
    return E_array,rmcd_list

def save_data(V_b,V_b_meas,I_b_meas,rmcd_data,saving_file):
    values = [E, V_b, V_b_meas, I_b_meas, rmcd]
    print(" ".join(f"{v:.4f}" for v in values))
    with open(saving_file, 'a') as file:
        file.write('{} {} {} '.format(round(V_b,3),round(V_b_meas,3), round(I_b_meas,4)) )
        file.write(' '.join(f"{d:.9f}" for d in rmcd_data) + '\n') 

def update_plot(fig,ax,line,xdata,ydata):
    line.set_data(xdata,ydata)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

def init_main_plot():
    fig, ax = plt.subplots()
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('RMCD %')
    line = Line2D([], [], color='blue',marker='.')
    ax.add_line(line)
    return fig,ax,line

if __name__ == "__main__":
    # 
    tb.init_plot_params()
    path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/'
    # sample = DualGate(sample_name='d4', d_b=18.45, d_t=5.67, data_path=path_d4)
    sample = DualGate(sample_name='d3', d_b=9.41, d_t=7.93, data_path=path_d3)
    
    file = path_d3+'Esweep2_0T_stacked_p6_after_m2T.txt'
    data = np.loadtxt(file)
    Vb, R, dR, Ib, theta_dr = data[:,1], data[:,3], data[:,7], data[:,2], data[:,9]
    rmcd = dR/R*100
    E = tb.E_dualgate(Vb, 0, sample.d_b, sample.d_t)
    
    fig,ax = plt.subplots()
    diffs = np.diff(E)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    
    except: transition_index=len(E)
        
    E_ascend = E[0:transition_index]
    E_descend = E[transition_index:]
    rmcd_ascend = rmcd[0:transition_index]
    rmcd_descend = rmcd[transition_index:]
    
    ax.plot(E_ascend, rmcd_ascend, color='black', label=r'$\rightarrow$',marker='.')
    ax.plot(E_descend, rmcd_descend, color='r', label=r'$\leftarrow$',marker='.')
    # ax.plot(E_ascend, rmcd_ascend-rmcd_descend[::-1], color='r', label=r'$\leftarrow$',marker='.')
    
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('RMCD %')
    ax.legend()
    # ax.set_ylim(.5,.8)
    plt.savefig(file.replace('.txt','_plot.png'),dpi=500)
    plt.show()
    
    # keithleyb = KeithleySourceMeter('GPIB::1','2450')
    # keithleyb.compliance_current=.02

    # E_array = np.array([-.1,0,.1])
    # rmcd = main(sample, lockin,keithleyb,E_array,'testest.txt')
    # keithleyb.close()
    # lockin.close()
    
