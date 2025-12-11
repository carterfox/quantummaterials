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
import math

def main(sample: FourTerminal, keithley_x: KeithleySourceMeter, keithley_y: KeithleySourceMeter, pmt: HamamatsuH11890, qwp_rotstage: RotationMount,
         qwp_angles=(0,90),gate_time_ms=200, num_gates=10, laser_power=0,Ex_array=np.array([]),Ey_array=np.array([]),file_save='test.txt'):
    
    plt.ion()
    fig,ax1,line1,ax2,line2 = init_main_plot()
    file_path = make_data_file(sample,qwp_angles,laser_power,gate_time_ms,num_gates,file_save)
        
    #### turn on PMT, set keithleys, then initiate a bunch of litsts. angle_ind controls qwp setting (C1 vs C2)
    pmt.set_hv(on=True)   
    set_keithleys(keithley_x,keithley_y)
    Ex_list, Ey_list, SHG_total_list, SHG_CD_list, SHG_CD_std_list, SHG_C_vals, SHG_C_stds, angle_ind = [],[],[],[],[],  [[],[]] , [[],[]], 0
    print('Ex   Ix  Ey Iy  angind  counts')
    for (Ex,Ey) in zip(Ex_array,Ey_array):
        #### go to first qwp angle. set voltages in each keithley 
        qwp_real_angle = update_rotation_stage(qwp_rotstage,qwp_angles[angle_ind])     
        Vx,Vy,Vx_meas,Vy_meas,Ix_meas,Iy_meas = set_voltages(sample,keithley_x,keithley_y,Ex,Ey)
        time.sleep(.1)
        #### measure SHG data at both qwp angles
        for i in range(2):
            if i==1: angle_ind = int(not angle_ind)
            update_rotation_stage(qwp_rotstage,qwp_angles[angle_ind]) 
            data = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
            # data = np.random.randint(low=0,high=10,size=(num_gates))
            SHG_C_vals[angle_ind].append(np.mean(data)), SHG_C_stds[angle_ind].append(np.mean(np.std(data)/np.sqrt(num_gates)))
            print(round(Ex,2),round(Ix_meas,2),round(Ey,2),round(Iy_meas,2),angle_ind,round(np.mean(data),1))
        #### compute total SGH and SHG-CD. plot and save data    
        SHG_C1, SHG_C1_std, SHG_C2, SHG_C2_std, SHG_total, SHG_CD, SHG_CD_std = get_SHG_vals(SHG_C_vals,SHG_C_stds)
        SHG_total_list.append(SHG_total), SHG_CD_list.append(SHG_CD), SHG_CD_std_list.append(SHG_CD_std), Ex_list.append(Ex), Ey_list.append(Ey)
        update_plot(fig,ax1,ax2,line1,line2,Ex_list,Ey_list,SHG_total_list,SHG_CD_list,SHG_CD_std_list)
        update_saved_data(file_path,Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix_meas,Iy_meas)

    ### turn off PMT hv and interactive plotting
    pmt.set_hv(on=False)
    time.sleep(.5)
    plt.ioff()
    plt.savefig(file_path.replace('.txt','plot.png'),dpi=500)
    plt.show()
    
    return SHG_total_list,SHG_CD_list
    

def update_plot(fig,ax1,ax2,line1,line2,Ex_list,Ey_list,SHG_total_list,SHG_CD_list,SHG_CD_std_list):
    #currently just using Ex
    line1.set_data(np.array(Ey_list)*10,SHG_total_list)
    line2.set_data(np.array(Ey_list)*10,SHG_CD_list)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

def init_main_plot():
    # fig, (ax1,ax2) = plt.subplots(2,1,figsize=(4,8),gridspec_kw={'width_ratios': [1, 1]})
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(6,6),sharex=True)
    # ax1.set_xlabel(r'$E_x$ (kV/cm)')
    ax2.set_xlabel(r'$E_y$ (kV/cm)')
    ax1.set_ylabel(r'SHG Intensity ($I_L+I_R$)')
    ax2.set_ylabel(r'SHG-CD ($\%$)')
    line1 = Line2D([], [], color='C0',marker='.')
    line2 = Line2D([], [], color='C0',marker='.')
    ax1.add_line(line1)
    ax2.add_line(line2)
    try:
        fig.canvas.manager.window.move(1800, 60)
    except: None
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
        f.write("# Vx (V) \t Vy (V) \t C1CountsMean \t C1CountsStd \t C2CountsMean \t C2CountsStd \t SHG_CD \t SHG_CD_std \t Ix (nA) \t Iy (nA) \n")
    return file_path

def update_saved_data(file_path,Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,CD,CD_std,Ix,Iy):
    with open(file_path, 'a') as f:
        data_save = [Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,CD,CD_std,Ix,Iy]
        f.write(' '.join(f"{d:.3f}" for d in data_save) + '\n') 

def update_rotation_stage(qwp_rotstage: RotationMount,qwp_angle):
    qwp_home = qwp_rotstage.home
    qwp_angle = qwp_angle+qwp_home
    qwp_rotstage.move_to(qwp_angle)
    time.sleep(.5)
    return None

def set_voltages(sample,keithley_x,keithley_y,Ex,Ey):
    Vx, Vy = Ex*sample.channel_width, Ey*sample.channel_width
    if keithley_x != None:
        keithley_x.source_voltage = Vx
        Vx_meas = keithley_x.measure_voltage_avg(10)
        Ix_meas = 10**9 * keithley_x.measure_current_avg(10)
    else: Vx_meas, Ix_meas = 0,0
    if keithley_y != None:
        keithley_y.source_voltage = Vy
        Vy_meas = keithley_y.measure_voltage_avg(10)
        Iy_meas = 10**9 * keithley_y.measure_current_avg(10)
    else: Vy_meas, Iy_meas = 0,0
    return Vx, Vy, Vx_meas,Vy_meas,Ix_meas,Iy_meas

def get_SHG_vals(SHG_C_vals,SHG_C_stds):
    SHG_C1, SHG_C2 = SHG_C_vals[0][-1], SHG_C_vals[1][-1]
    SHG_C1_std, SHG_C2_std = SHG_C_stds[0][-1], SHG_C_stds[1][-1]
    SHG_total = SHG_C1 + SHG_C2
    SHG_diff = SHG_C1 - SHG_C2
    SHG_CD = SHG_diff/SHG_total*100
    SHG_CD_std = get_SGH_CD_std(SHG_C1, SHG_C2, SHG_C1_std, SHG_C2_std)
    return SHG_C1, SHG_C1_std, SHG_C2, SHG_C2_std, SHG_total, SHG_CD, SHG_CD_std

def set_keithleys(keithley_x,keithley_y):
    if keithley_x != None:
        keithley_x.enable_source()
        keithley_x.apply_voltage(compliance_current=keithley_x.compliance_current)
    if keithley_y != None:
        keithley_y.enable_source()
        keithley_y.apply_voltage(compliance_current=keithley_y.compliance_current)

def get_SGH_CD_std(x, y, sigma_x, sigma_y):
    numerator = np.sqrt((y**2) * (sigma_x**2) + (x**2) * (sigma_y**2))
    denominator = (x + y)**2
    return 100 * 2 * numerator / denominator

def replot(Ex_list,Ey_list,SHG_total,SHG_total_std,SHG_CD,SHG_CD_std,E='x',absolute=True,x=None):
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(6,6),sharex=True)
    
    if E=='x': 
        E_list = Ex_list
        colord = 'r'
    elif E == 'y':
        E_list = Ey_list
        colord = 'b'
    ax2.set_xlabel(r'$E_{}$  (kV/cm)'.format(E))
    ax1.set_ylabel(r'SHG Intensity ($I_L+I_R$)')
    ax2.set_ylabel(r'SHG-CD ($\%$)')
    

    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_total_ascend,SHG_total_descend = SHG_total[0:transition_index],SHG_total[transition_index:]    
    SHG_total_std_ascend,SHG_total_std_descend = SHG_total_std[0:transition_index],SHG_total_std[transition_index:]    
    
    # E_list_ascend,E_list_descend =  np.append(E_list[62:] , E_list[0:21]) , E_list[21:62]
    # SHG_CD_ascend,SHG_CD_descend = np.append(SHG_CD[62:] , SHG_CD[0:21]) , SHG_CD[21:62]
    # SHG_CD_std_ascend,SHG_CD_std_descend = np.append(SHG_CD_std[62:] , SHG_CD_std[0:21]) , SHG_CD_std[21:62]
    # SHG_total_ascend,SHG_total_descend = np.append(SHG_total[62:] , SHG_total[0:21]) , SHG_total[21:62] 
    # SHG_total_std_ascend,SHG_total_std_descend = np.append(SHG_total_std[62:] , SHG_total_std[0:21]) , SHG_total_std[21:62] 

    if absolute: SHG_CD_ascend,SHG_CD_descend = np.abs(SHG_CD_ascend),np.abs(SHG_CD_descend)
    
    ms=8
    lw=2.5
    elw=1.
    ax1.errorbar(E_list_ascend, SHG_total_ascend, yerr=SHG_total_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.errorbar(E_list_descend, SHG_total_descend, yerr=SHG_total_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
   
    ax2.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax2.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)

    tb.plot_arrow_legend(ax1,r'$E_{}$'.format(E),x1=127,y1=700,ls=10,yratio=.058,xratio=.12,wratio=.0872,colord=colord)
    # tb.plot_arrow_legend(ax1,,x1=146,y1=600,ls=12,yratio=.058,xratio=.12,wratio=.0872,colord=colord)
    # ax2.text(74,14,r'$E_x$={}$\rightarrow$'.format(x),fontsize=12)
    # ax2.set_ylim(-8,17)
    # ax1.set_ylim(450,2550)
    

if __name__ == "__main__":

    tb.init_plot_params()
    # path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/RMCD/Esweep/'
    path_d1 = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/90deg_3L3L_4term_S2/SHG-CD-Efield/'
    sample = FourTerminal('NbOI290deg4termS1', 5, path_d1)
    w = sample.channel_width
    
    file_path = path_d1+'fullscany4_floatx1.txt'
    # file_old = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/90deg_3L3L/SHG/CD-Efield/stacked_scan7_EfieldSHG-CD_close_to_elec.txt'
    
    data = np.loadtxt(file_path,comments='#')
    # Vx = data[:,0]
    # Vy=0
    # SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std,SHG_CD = np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,8])
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total = SHG_C1 + SHG_C2
    SHG_total_std = np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    replot(Ex_list,Ey_list,SHG_total,SHG_total_std,SHG_CD,SHG_CD_std,E='y',absolute=False,x=None)
    plt.savefig(file_path.replace('.txt','plot.png'),dpi=500)
    plt.show()
    
    
    
    

