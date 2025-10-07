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
    fig, ax, lineup,linedown = init_main_plot()
    
    keithley_b.enable_source()
    keithley_b.apply_voltage()
    rmcd_list,rmcd_list_up,rmcd_list_down = [],[],[]
    d_b = sample.d_b
    # d_t = sample.d_t
    E_list,E_list_up,E_list_down = [],[],[]
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
        save_data(V_b,V_b_meas,I_b_meas,rmcd_data,saving_file)
        
        if len(E_list) != 0:
            if E >= E_list[-1]:
                E_list_up.append(E)
                rmcd_list_up.append(rmcd)
            if E <= E_list[-1]:
                E_list_down.append(E)
                rmcd_list_down.append(rmcd)
        else:
            if E <0:
                E_list_up.append(E)
                rmcd_list_up.append(rmcd)
            elif Vb>0:
                E_list_down.append(E)
                rmcd_list_down.append(rmcd)
        
        update_plot(fig,ax,lineup,linedown,E_list_up,E_list_down,rmcd_list_up,rmcd_list_down)
        
    plt.ioff()
    plt.show()
    
    return E_array,rmcd_list

def save_data(V_b,V_b_meas,I_b_meas,rmcd_data,saving_file):
    values = [round(V_b,3),round(V_b_meas,3), round(I_b_meas,4)]
    with open(saving_file, 'a') as file:
        file.write(' '.join(f"{v:.4f}" for v in values)+ ' ') 
        file.write(' '.join(f"{d:.9f}" for d in rmcd_data) + '\n') 
    values.append(round(rmcd_data[4]/rmcd_data[0]*100,3))
    print(" ".join(f"{v:.4f}" for v in values))
    
def update_plot(fig,ax,lineup,linedown,E_list_up,E_list_down,rmcd_list_up,rmcd_list_down):

    lineup.set_data(E_list_up,rmcd_list_up)
    linedown.set_data(E_list_down,rmcd_list_down)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

def init_main_plot():
    fig, ax = plt.subplots()
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('RMCD %')
    lineup = Line2D([], [], color='black',marker='.',label=r'$\rightarrow$')
    linedown = Line2D([], [], color='red',marker='.',label=r'$\leftarrow$')
    ax.add_line(lineup)
    ax.add_line(linedown)
    ax.legend()
    return fig,ax,lineup,linedown


def smooth(arr):
    """
    Smooths an array by averaging each element with its neighbors.
    Keeps the same length as the original array.
    
    Parameters:
    arr (array-like): Input array of values.
    
    Returns:
    np.ndarray: Smoothed array.
    
    """
    if False:
        arr = np.array(arr, dtype=float)
        smoothed = np.zeros_like(arr)
    
        for i in range(len(arr)):
            if i == 0:
                smoothed[i] = (arr[i] + arr[i+1]) / 2
            elif i == len(arr) - 1:
                smoothed[i] = (arr[i-1] + arr[i]) / 2
            else:
                smoothed[i] = (arr[i-1] + arr[i] + arr[i+1]) / 3
        return smoothed
    else:
        return arr


if __name__ == "__main__":
    # 
    tb.init_plot_params()
    # path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/'
    path_d3 = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/stacked/'
    # path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/'
    # path_d3 = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/'
    # sample = DualGate(sample_name='d4', d_b=18.45, d_t=5.67, data_path=path_d4)
    sample = DualGate(sample_name='d3', d_b=9.41, d_t=7.93, data_path=path_d3)
    sample.d_flake=0.7*4
    
    file = path_d3+'sweep8_8-18_2K_0T_after_m2T_m65deg.txt'
    # file = path_d3+'sweep5_8-18_2K_0T_after_m2T_m65deg.txt'
    # file = path_d3+'Esweep5_0T_stacked_p1_after_m2T_diffInput_faster.txt'
    # file = path_d3+'sweep6_8-18_2K_0T_after_m2T_m65deg.txt'
    data = np.loadtxt(file)
    Vb, R, dR, Ib, theta_dr = data[:,1], data[:,3], data[:,7], data[:,2], data[:,9]
    rmcd = dR/R*100
    rmcd[np.where(theta_dr>0)] *= -1
    E = tb.E_dualgate(Vb, 0, sample,no_middle_gr=True)
    
    fig,ax = plt.subplots()
    diffs = np.diff(E)
    change_indices = np.where(diffs < 0)[0]  # descending starts here
    if len(change_indices)==0:
        change_indices = np.array([len(E)-1])
    E_ascend = E[:change_indices[0] + 1]
    E_descend = E[change_indices[0] + 1:]
    rmcd_ascend = np.append(rmcd[change_indices[-1]:],rmcd[:change_indices[0] + 1])
    E_ascend = np.append(E[change_indices[-1]:],E[:change_indices[0] + 1])
    rmcd_descend = rmcd[change_indices[0] + 1:]
    
    center=rmcd_ascend[0]
    delta_rmcd_ascend = rmcd_ascend - center
    delta_rmcd_descend = rmcd_descend - center
    
    ax.plot(smooth(E_ascend), smooth(delta_rmcd_ascend), color='black', label=r'$\rightarrow$',marker='.',ms=5,zorder=1,lw=2)
    ax.plot(smooth(E_descend), smooth(delta_rmcd_descend), color='r', label=r'$\leftarrow$',marker='.',ms=5,zorder=0,lw=2)
    # ax.plot(E_ascend, rmcd_ascend-rmcd_descend[::-1], color='r', label=r'$\leftarrow$',marker='.')
    
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('$\DeltaRMCD %')
    ax.legend()
    # ax.set_ylim(.85,1.5)
    ax.set_xlim(-.45,.4)
    plt.savefig(file.replace('.txt','_plot.png'),dpi=500)
    plt.show()
    
    # keithleyb = KeithleySourceMeter('GPIB::1','2450')
    # keithleyb.compliance_current=.02

    # E_array = np.array([-.1,0,.1])
    # rmcd = main(sample, lockin,keithleyb,E_array,'testest.txt')
    # keithleyb.close()
    # lockin.close()
    
