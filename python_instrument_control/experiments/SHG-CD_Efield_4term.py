#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 13:49:03 2025

@author: carterfox
"""

import numpy as np
import logging
import time
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import toolbelt as tb
from homemade_servers.H11890PMT import HamamatsuH11890
from homemade_servers.ThorlabsKCube import RotationMount
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from devices.transport import FourTerminal

def main(sample: FourTerminal, keithley_x: KeithleySourceMeter, keithley_y: KeithleySourceMeter, pmt: HamamatsuH11890, qwp_rotstage: RotationMount,
         qwp_angles=(0,90),gate_time_ms=200, num_gates=10, laser_power=0,Ex_array=np.array([]),Ey_array=np.array([]),file_save='test.txt'):
    
    plt.ion()
    fig,ax1,line1,ax2,line2 = init_main_plot()
    fig.canvas.manager.window.move(1920, 60)
    file_path = make_data_file(sample,qwp_angles,laser_power,gate_time_ms,num_gates,file_save)
    qwp_real_angle = update_rotation_stage(qwp_rotstage,qwp_angles[0])      
        
    keithley_x.enable_source()
    keithley_x.apply_voltage()
    keithley_y.enable_source()
    keithley_y.apply_voltage()
    
    ### turn on PMT then initiate a bunch of litsts
    pmt.set_hv(on=True)   
    Ex_list, Ey_list, SHG_C1_means, SHG_C1_stds, SHG_C2_means, SHG_C2_stds, SHG_total_list, SHG_CD_list = [],[],[],[],[],[],[],[]
    
    for (Ex,Ey) in zip(Ex_array,Ey_array):
        
        #### go to first qwp angle
        qwp_real_angle = update_rotation_stage(qwp_rotstage,qwp_angles[0])     
        
        #### set voltages in each keithley 
        Vx = Ex/sample.channel_width
        Vy = Ey/sample.channel_width
        keithley_x.source_voltage = Vx
        Vx_meas = keithley_x.measure_voltage_avg(10)
        Ix_meas = 10**9 * keithley_x.measure_current_avg(20)
        keithley_y.source_voltage = Vy
        Vy_meas = keithley_y.measure_voltage_avg(10)
        Iy_meas = 10**9 * keithley_y.measure_current_avg(20)
        
        #### measure SHG data at first qwp angle
        data_C1 = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
        SHG_C1_means.append(np.mean(data_C1))
        SHG_C1_stds.append(np.std(data_C1)/np.sqrt(num_gates))

        #### move to second qwp angle and measure SHG data at the second qwp angle
        qwp_real_angle = update_rotation_stage(qwp_rotstage,qwp_angles[1])    
        data_C2 = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
        SHG_C2_means.append(np.mean(data_C2))
        SHG_C2_stds.append(np.std(data_C1)/np.sqrt(num_gates))
        
        #### compute total SGH and SHG-CD
        SHG_total = SHG_C1_means[-1] + SHG_C2_means[-1]
        SHG_CD = (SHG_C1_means[-1] - SHG_C2_means[-1])/SHG_total*100
        SHG_total_list.append(SHG_total)
        SHG_CD_list.append(SHG_CD)
        
        Ex_list.append(Ex)
        Ey_list.append(Ey)
        
        #### plot data and return to first qwp angle 
        update_plot(fig,ax1,ax2,line1,line2,Ex_list,Ey_list,SHG_total_list,SHG_CD_list)
        update_saved_data(file_path,Vx,Vy,SHG_C1_means[-1],SHG_C1_stds[-1],SHG_C2_means[-1],SHG_C2_stds[-1],Ix_meas,Iy_meas)
        qwp_real_angle = update_rotation_stage(qwp_rotstage,qwp_angles[0])   
        
    ### turn off PMT hv and interactive plotting
    pmt.set_hv(on=False)
    time.sleep(.5)
    plt.ioff()
    plt.savefig(file_path.replace('.txt','plot.png'),dpi=500)
    plt.show()
    return SHG_total_list,SHG_CD_list
    

def update_plot(fig,ax1,ax2,line1,line2,Ex_list,Ey_list,SHG_total_list,SHG_CD_list):
    #currently just using Ex
    line1.set_data(Ex_list,SHG_total_list)
    line2.set_data(Ex_list,SHG_CD_list)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

def init_main_plot():
    fig, (ax1,ax2) = plt.subplots(1,2)
    ax1.set_xlabel(r'E_x (V/nm)')
    ax2.set_xlabel(r'E_x (V/nm)')
    ax1.set_ylabel('SHG Intensity (I_L+I_R)')
    ax2.set_ylabel(r'SHG-CD ($\%$)')
    line1 = Line2D([], [], color='C0',marker='.')
    line2 = Line2D([], [], color='C2',marker='.')
    ax1.add_line(line1)
    ax2.add_line(line2)
    return fig,ax1,line1,ax2,line2

def make_data_file(sample,qwp_angles,laser_power,gate_time_ms,num_gates,file_save):
    if not os.path.exists(sample.data_path+"/SHG-CD-Efield"):
        os.makedirs(sample.data_path+"/SHG-CD-Efield")
    file_path = sample.data_path+'/SHG-CD-Efield/'+file_save
    
    while os.path.exists(file_path):  
        print('file already exists. making a new one with add on to name')
        file_path = file_path.replace(".txt", "_new.txt")
    
    with open(file_path, "a") as f:
        f.write(f"# Sample Name: {sample.sample_name}\n")
        f.write(f"# Channel Width: {sample.channel_width}\n")
        f.write(f"# QWP Angles (C1,C2): {qwp_angles}\n")
        f.write(f"# Laser Power: {laser_power} mW\n")
        f.write(f"# Gate Time: {gate_time_ms} ms\n")
        f.write(f"# Num Gates: {num_gates}\n")
        f.write("# Vx (V) \t Vy (V) \t C1CountsMean \t C1CountsStd \t C2CountsMean \t C2CountsStd \t Ix (nA) \t Iy (nA) \n")
    return file_path

def update_saved_data(file_path,Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,Ix,Iy):
    with open(file_path, 'a') as f:
        data_save = [Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,Ix,Iy]
        f.write(' '.join(f"{d:.3f}" for d in data_save) + '\n') 

def update_rotation_stage(qwp_rotstage: RotationMount,qwp_angle):
    qwp_home = qwp_rotstage.home
    qwp_angle = qwp_angle+qwp_home
    qwp_rotstage.move_to(qwp_angle)
    time.sleep(.5)
    return qwp_angle