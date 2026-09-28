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
import glob
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

def main(sample: FourTerminal, keithley_x: KeithleySourceMeter, keithley_y: KeithleySourceMeter, pmt: HamamatsuH11890, qwp_rotstage: RotationMount,
         qwp_angles=(0,90),gate_time_ms=200, num_gates=10, laser_power=0,Ex_array=np.array([]),Ey_array=np.array([]),file_save='test.txt',close_fig_after=False):
    
    if len(np.unique(Ex_array)) == 1: sweep_axis = 'y'
    elif len(np.unique(Ey_array)) == 1: sweep_axis = 'x'
    else: sweep_axis = 'x'
    
    plt.ion()
    fig,axes,lines = init_main_plot(sweep_axis)
    file_path = make_data_file(sample,qwp_angles,laser_power,gate_time_ms,num_gates,file_save)
        
    pmt.set_hv(on=True)   
    set_keithleys(keithley_x,keithley_y)
    Ex_list, Ey_list, Ix_list, Iy_list, SHG_total_list, SHG_CD_list, SHG_CD_std_list, SHG_C_vals, SHG_C_stds, angle_ind = [],[],[],[],[],[],[],  [[],[]] , [[],[]], 0
    print(f"{'Ex':^8}" f"{'Ix':^7}" f"{'Ey':^6}" f"{'Iy':^10}" f"{'ang':^1}" f"{'counts':^12}")
    
    for (Ex,Ey) in zip(Ex_array,Ey_array):
        Vx,Vy,Vx_meas,Vy_meas,Ix_meas,Iy_meas = set_voltages(sample,keithley_x,keithley_y,Ex,Ey)
        time.sleep(.1)
        for i in range(2):
            if i==1: angle_ind = int(not angle_ind)
            update_rotation_stage(qwp_rotstage,qwp_angles[angle_ind]) 
            data = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
            SHG_C_vals[angle_ind].append(np.mean(data)), SHG_C_stds[angle_ind].append(np.mean(np.std(data)/np.sqrt(num_gates)))
            print(f"{Ex:^7.4f}" f"{Ix_meas:^8.3f}" f"{Ey:^7.2f}" f"{Iy_meas:^8.2f}" f"{angle_ind:^6}" f"{np.mean(data):^9.1f}")

        SHG_C1, SHG_C1_std, SHG_C2, SHG_C2_std, SHG_total, SHG_CD, SHG_CD_std = get_SHG_vals(SHG_C_vals,SHG_C_stds)
        SHG_total_list.append(SHG_total), SHG_CD_list.append(SHG_CD), SHG_CD_std_list.append(SHG_CD_std), Ex_list.append(Ex), Ey_list.append(Ey), Ix_list.append(Ix_meas),Iy_list.append(Iy_meas)
        update_plot(fig,axes,lines,Ex_list,Ey_list,SHG_total_list,SHG_CD_list,Ix_list,Iy_list,sweep_axis)
        update_saved_data(file_path,Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix_meas,Iy_meas,Vx_meas,Vy_meas)

    pmt.set_hv(on=False)
    time.sleep(.5)
    plt.ioff()
    plt.savefig(file_path.replace('.txt','plot.png'),dpi=500)
    plt.show()
    if close_fig_after:
        plt.close()
    
    return SHG_total_list,SHG_CD_list
    

def init_main_plot(sweep_axis):
    fig, axs = plt.subplots(2,2,figsize=(10,6),sharex=True,facecolor='whitesmoke')
    for ax in axs.ravel():
        ax.set_facecolor('whitesmoke')
    ax1,ax2,ax3,ax4, = axs[0,0],axs[1,0],axs[0,1],axs[1,1]
    
    ax2.set_xlabel(r'$E_{}$ (kV cm$^{-1}$)'.format(sweep_axis)), ax4.set_xlabel(r'$E_{}$ (kV cm$^{-1}$)'.format(sweep_axis))
    ax1.set_ylabel(r'SHG Intensity ($I_L+I_R$)'),ax2.set_ylabel(r'SHG-CD ($\%$)')
    ax3.set_ylabel(r'$I_x$  ($\mu$A)'),ax4.set_ylabel(r'$I_y$  ($\mu$A)')
    ms,lw,elw = 8,2.5,1
    
    if sweep_axis=='x': colord = 'r'
    elif sweep_axis== 'y': colord = 'b'
    
    SHG_ascend_line = Line2D([], [], color='black',marker='.',linewidth=lw,markersize=ms)
    SHG_descend_line = Line2D([], [], color=colord,marker='.',linewidth=lw,markersize=ms)
    CD_ascend_line = Line2D([], [], color='black',marker='.',linewidth=lw,markersize=ms)
    CD_descend_line = Line2D([], [], color=colord,marker='.',linewidth=lw,markersize=ms)
    Ix_ascend_line = Line2D([], [], color='black',marker='.',linewidth=lw,markersize=ms)
    Ix_descend_line = Line2D([], [], color=colord,marker='.',linewidth=lw,markersize=ms)
    Iy_ascend_line = Line2D([], [], color='black',marker='.',linewidth=lw,markersize=ms)
    Iy_descend_line = Line2D([], [], color=colord,marker='.',linewidth=lw,markersize=ms)
    
    ax1.add_line(SHG_ascend_line),ax1.add_line(SHG_descend_line),ax2.add_line(CD_ascend_line),ax2.add_line(CD_descend_line)
    ax3.add_line(Ix_ascend_line),ax3.add_line(Ix_descend_line),ax4.add_line(Iy_ascend_line),ax4.add_line(Iy_descend_line)
    
    axes = (ax1,ax2,ax3,ax4)
    lines= (SHG_ascend_line,SHG_descend_line,CD_ascend_line,CD_descend_line,Ix_ascend_line,Ix_descend_line,Iy_ascend_line,Iy_descend_line)

    try:
        fig.canvas.manager.window.move(1500, 60)
    except: None
    return fig,axes,lines

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
        f.write("# Vx (V) \t Vy (V) \t C1CountsMean \t C1CountsStd \t C2CountsMean \t C2CountsStd \t SHG_CD \t SHG_CD_std \t Ix (nA) \t Iy (nA) \t Vxmeas (V) \t Vymeas (V) \n")
    return file_path

def update_saved_data(file_path,Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,CD,CD_std,Ix,Iy,Vxmeas,Vymeas):
    for attempt in range(10): 
        try: 
            with open(file_path, 'a') as f:
                data_save = [Vx,Vy,C1_mean,C1_std,C2_mean,C2_std,CD,CD_std,Ix,Iy,Vxmeas,Vymeas]
                f.write(' '.join(f"{d:.4f}" for d in data_save) + '\n') 
            break 
        except FileNotFoundError: time.sleep(0.2)

def update_rotation_stage(qwp_rotstage: RotationMount,qwp_angle):
    qwp_home = qwp_rotstage.home
    qwp_angle = qwp_angle+qwp_home
    qwp_rotstage.move_to(qwp_angle)
    # time.sleep(.5)
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


def update_plot(fig,axes,lines,Ex_list,Ey_list,SHG_total,SHG_CD,Ix,Iy,sweep_axis,absolute=False):
    ax1,ax2,ax3,ax4, = axes
    SHG_ascend_line,SHG_descend_line,CD_ascend_line,CD_descend_line,Ix_ascend_line,Ix_descend_line,Iy_ascend_line,Iy_descend_line = lines
    if sweep_axis == 'x': E_list = Ex_list
    elif sweep_axis == 'y': E_list = Ey_list
    E_list = np.array(E_list)*10
    
    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    
    Ix,Iy = np.asarray(Ix)/1000, np.asarray(Iy)/1000
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    SHG_CD_ascend,SHG_CD_descend,SHG_total_ascend,SHG_total_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:],SHG_total[0:transition_index],SHG_total[transition_index:]    
    Ix_ascend,Ix_descend,Iy_ascend,Iy_descend = Ix[0:transition_index],Ix[transition_index:],Iy[0:transition_index],Iy[transition_index:]
    if absolute: SHG_CD_ascend,SHG_CD_descend = np.abs(SHG_CD_ascend),np.abs(SHG_CD_descend)

    SHG_ascend_line.set_data(E_list_ascend,SHG_total_ascend)
    SHG_descend_line.set_data(E_list_descend,SHG_total_descend)
    CD_ascend_line.set_data(E_list_ascend,SHG_CD_ascend)
    CD_descend_line.set_data(E_list_descend,SHG_CD_descend)
    Ix_ascend_line.set_data(E_list_ascend,Ix_ascend)
    Ix_descend_line.set_data(E_list_descend,Ix_descend)
    Iy_ascend_line.set_data(E_list_ascend,Iy_ascend)
    Iy_descend_line.set_data(E_list_descend,Iy_descend)
    ax1.relim(),ax2.relim(),ax3.relim(),ax4.relim()
    ax1.autoscale_view(),ax2.autoscale_view(),ax3.autoscale_view(),ax4.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

def replot(Ex_list,Ey_list,SHG_total,SHG_total_std,SHG_CD,SHG_CD_std,Ix,Iy,E='x',absolute=True,xy=None):
    fig, axs = plt.subplots(2,2,figsize=(7,4),sharex=True)
    plt.subplots_adjust(wspace=.35)
    ax1,ax2,ax3,ax4, = axs[0,0],axs[1,0],axs[0,1],axs[1,1]
    Ix,Iy = Ix/1000, Iy/1000
    
    if E=='x': E_list,colord = Ex_list,'r'
    elif E == 'y': E_list,colord = Ey_list,'b'
    
    fs=8
    ax2.set_xlabel(r'$E_{}$  (V nm$^{-1}$)'.format(E),fontsize=fs)
    ax1.set_ylabel(r'SHG Intensity ($I_L+I_R$)',fontsize=fs),ax2.set_ylabel(r'SHG-CD ($\%$)',fontsize=fs)
    # ax4.set_xlabel(r'$E_{}$  (kV cm$^{-1}$)'.format(E))
    ax4.set_xlabel(r'$E_{}$  (V nm$^{-1}$)'.format(E),fontsize=fs)
    ax4.set_xlabel(r'$E_{\perp}$  (V nm$^{-1}$)',fontsize=fs)
    ax2.set_xlabel(r'$E_{\perp}$  (V nm$^{-1}$)',fontsize=fs)
    # ax3.set_ylabel(r'$I_x$  ($\mu$A)',fontsize=fs),ax4.set_ylabel(r'$I_y$  ($\mu$A)',fontsize=fs)
    ax3.set_ylabel(r'$I_b$  ($\mu$A)',fontsize=fs),ax4.set_ylabel(r'$I_b$  ($\mu$A)',fontsize=fs)
    ax1.tick_params(axis="both", labelsize=fs) 
    ax2.tick_params(axis="both", labelsize=fs) 
    ax3.tick_params(axis="both", labelsize=fs) 
    ax4.tick_params(axis="both", labelsize=fs) 

    
    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_total_ascend,SHG_total_descend = SHG_total[0:transition_index],SHG_total[transition_index:]    
    SHG_total_std_ascend,SHG_total_std_descend = SHG_total_std[0:transition_index],SHG_total_std[transition_index:]    
    Ix_ascend,Ix_descend,Iy_ascend,Iy_descend = Ix[0:transition_index],Ix[transition_index:],Iy[0:transition_index],Iy[transition_index:]
    
    if absolute: SHG_CD_ascend,SHG_CD_descend = np.abs(SHG_CD_ascend),np.abs(SHG_CD_descend)
    
    ms,lw,elw,ec = 3,1.2,.75,'gray'
    ax1.errorbar(E_list_ascend, SHG_total_ascend, yerr=SHG_total_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax1.errorbar(E_list_descend, SHG_total_descend, yerr=SHG_total_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax2.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax2.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)

    ax3.errorbar(E_list_ascend, Ix_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax3.errorbar(E_list_descend, Ix_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax4.errorbar(E_list_ascend, Iy_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)
    ax4.errorbar(E_list_descend, Iy_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms,lw=lw,ecolor=ec)

    # tb.plot_arrow_legend(ax1,r'$E_{}$'.format(E),x1=110,y1=1068,ls=10,yratio=.058,xratio=.12,wratio=.0872,colord=colord)
    # tb.plot_arrow_legend(ax1,,x1=146,y1=600,ls=12,yratio=.058,xratio=.12,wratio=.0872,colord=colord)
    # ax2.text(40,4,r'$E_y$={}kV cm$^{-1}$$\rightarrow$'.format(x),fontsize=12)
    
def plot_for_proposal(Ex_list,Ey_list,SHG,SHG_std,SHG_CD,SHG_CD_std,Esweep='x',Efixval=0):
    plt.rcParams["font.size"] = 14
        
    if Esweep=='x': E_list,colord = Ex_list,'r'
    elif Esweep == 'y': E_list,colord = Ey_list,'b'
    
    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
          
    fig, (ax1,ax0) = plt.subplots(2,1,figsize=(3.5,4.5),sharex=True)
    Estr = r'$E_{}$'.format(Esweep)
    ax0.set_xlabel(Estr+r' (kV cm$^{-1}$)'),ax0.set_ylabel(r'SHG-CD ($\%$)'),ax1.set_ylabel(r'SHG Intensity')
    ms,lw,elw = 6,2,1
    ax0.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax0.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    
    ax1.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    
    # ax0.fill_between(E_list_ascend,SHG_CD_ascend+SHG_CD_std_ascend,SHG_CD_ascend-SHG_CD_std_ascend,color='black',alpha=.15)
    # ax0.fill_between(E_list_descend,SHG_CD_descend+SHG_CD_std_descend,SHG_CD_descend-SHG_CD_std_descend,color='r',alpha=.15)
    
    # ax0.set_ylim(-23,23)
    ax0.set_yticks([-20,-10,0,10,20])
    ax0.set_xticks([-150,-75,0,75,150])
    
    # tb.plot_arrow(ax0, 60,-17.5,-40,0,w=2.5)
    # tb.plot_arrow(ax0, 10,17, 40,0,w=2.5,c='black')
    ax1.set_title('$E_y$ = {} kV cm$^{-1}$'.format(Efixval),fontsize=10)
    # ax1.text(35,2000,'$E_y$=10 kV cm$^{-1}$',fontsize=10)

def analyze_files_2dmap(folder_path,fast_axis='x',slow_direction='a'):
    if fast_axis=='x': slow_axis = 'y'
    elif fast_axis=='y': slow_axis = 'x'
    files = [Path(p) for p in glob.glob(str(Path(folder_path) / "*.txt"))]
    ascend_files, descend_files = [f for f in files if "ascend" in f.name.lower()], [f for f in files if "descend" in f.name.lower()]
    ascend_yvals, descend_yvals = [],[]
    
    for f in ascend_files: ascend_yvals.append(float(f.name.lower().split('_')[3].replace('m','-').replace('p','.')))
    for f in descend_files: descend_yvals.append(float(f.name.lower().split('_')[3].replace('m','-').replace('p','.')))
        
    ascend_files = np.array(ascend_files)[np.argsort(ascend_yvals)]
    descend_files = np.array(descend_files)[np.argsort(descend_yvals)]
    xs,ys,SHG_CD_ascend_vals,SHG_CD_descend_vals,SHG_ascend_vals,SHG_descend_vals,SHG_hysteresis_vals,SHG_CD_hysteresis_vals = np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
    
    # for file in ascend_files:
    if slow_direction == 'a': files = ascend_files
    elif slow_direction == 'd': files = descend_files
    
    for file in files:
        data=np.loadtxt(file)
        if fast_axis=='x': ascend_ind = np.where(np.diff(data[:,0])==0)[0][0]
        elif fast_axis=='y': ascend_ind = np.where(np.diff(data[:,1])==0)[0][0]
        
        data_ascend,data_descend = data[0:ascend_ind+1],data[ascend_ind+1:]
        
        counts_C1_ascend,counts_C2_ascend,Ix_ascend,Iy_ascend,Vx_ascend,Vy_ascend = data_ascend[:,2],data_ascend[:,4],data_ascend[:,8],data_ascend[:,9],data_ascend[:,0],data_ascend[:,1]
        counts_C1_descend,counts_C2_descend,Ix_descend,Iy_descend,Vx_descend,Vy_descend = np.flip(data_descend[:,2]),np.flip(data_descend[:,4]),np.flip(data_descend[:,8]),np.flip(data_descend[:,9]),np.flip(data_descend[:,0]),np.flip(data_descend[:,1])
        SHG_ascend = counts_C1_ascend+counts_C2_ascend
        SHG_descend = counts_C1_descend+counts_C2_descend
        SHG_CD_ascend = (counts_C1_ascend-counts_C2_ascend)/(counts_C1_ascend+counts_C2_ascend)*100
        SHG_CD_descend = (counts_C1_descend-counts_C2_descend)/(counts_C1_descend+counts_C2_descend)*100
        SHG_CD_hysteresis = SHG_CD_descend - SHG_CD_ascend
        SHG_hysteresis = SHG_descend - SHG_ascend
            
        xs,ys = np.append(xs,Vx_ascend), np.append(ys,Vy_ascend)
        SHG_CD_ascend_vals = np.append(SHG_CD_ascend_vals,SHG_CD_ascend)
        SHG_CD_descend_vals = np.append(SHG_CD_descend_vals,SHG_CD_descend)
        SHG_ascend_vals = np.append(SHG_ascend_vals,SHG_ascend)
        SHG_descend_vals = np.append(SHG_descend_vals,SHG_descend)
        SHG_CD_hysteresis_vals = np.append(SHG_CD_hysteresis_vals,SHG_CD_hysteresis)
        SHG_hysteresis_vals = np.append(SHG_hysteresis_vals,SHG_hysteresis)
        
    xs,ys = xs/5*10, ys/5*10
    x_unique, y_unique = np.unique(xs), np.unique(ys)
    image_cda = np.zeros((len(x_unique), len(y_unique)))
    image_cdd = np.zeros((len(x_unique), len(y_unique)))
    image_cdh = np.zeros((len(x_unique), len(y_unique)))
    image_ta = np.zeros((len(x_unique), len(y_unique)))
    image_td = np.zeros((len(x_unique), len(y_unique)))
    image_th = np.zeros((len(x_unique), len(y_unique)))
    
    for x, y, cda, cdd, cdh, ta, td, th in zip(xs, ys, SHG_CD_ascend_vals,SHG_CD_descend_vals, SHG_CD_hysteresis_vals,SHG_ascend_vals,SHG_descend_vals,SHG_hysteresis_vals):
        xi,yi = np.where(x_unique == x)[0][0],np.where(y_unique == y)[0][0]
        image_cda[xi, yi] = cda
        image_cdd[xi, yi] = cdd
        image_cdh[xi, yi] = cdh
        image_ta[xi, yi] = ta
        image_td[xi, yi] = td
        image_th[xi, yi] = th
    image_cda=np.transpose(image_cda)
    image_cdd=np.transpose(image_cdd)
    image_cdh=np.transpose(image_cdh)
    image_ta=np.transpose(image_ta)
    image_td=np.transpose(image_td)
    image_th=np.transpose(image_th)
        
    # plot_map(image, x_unique, y_unique, cbarlabel)
    
    # plt.savefig(path_map+'plot_2dmap_{}_{}_{}_{}_{}.png'.format(slow_axis,slow_direction,fast_axis,fast_direction,value),dpi=500)
    # plt.show()
    return x_unique,y_unique,image_cda,image_cdd,image_cdh,image_ta,image_td,image_th

def plot_map(image,x_unique,y_unique,value='CD',vmin=None,vmax=None):
    if value == 'CD': cbarlabel = "SHG-CD (%)"
    elif value == 'CDhyst': cbarlabel = "SHG-CD (%)\nhysteresis"
    if value == 'total': cbarlabel = "SHG Intensity"
    elif value == 'totalhyst': cbarlabel = "SHG Intensity\nhysteresis"
    fig=plt.figure(figsize=(1.5,1.5))
    plt.imshow(image,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=vmin,vmax=vmax,cmap='coolwarm')
    cbar=plt.colorbar(shrink=0.4) 
    fs=5
    cbar.set_label(cbarlabel, ha='center',fontsize=fs)
    cbar.set_ticks([-10,-0,10])
    cbar.ax.tick_params(labelsize=fs)
    plt.xlabel("$E_x$ (kV cm$^{-1}$)",fontsize=fs)
    plt.ylabel("$E_y$ (kV cm$^{-1}$)",fontsize=fs)  
    plt.xticks([-140,-70,0,70,140],fontsize=fs)
    plt.yticks([-140,-70,0,70,140],fontsize=fs)
    plt.tick_params(axis='both',color='white')
    # plt.title("2D Map") 
    # plt.show()
    return fig

def plot_dualmap(image_ta,image_td,image_cda, image_cdd, x_unique,y_unique):
    
    maxval = np.max([np.max(image_ta),np.max(image_td)])
    image_ta,image_td = image_ta/maxval,image_td/maxval
        
    # fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(4, 3), constrained_layout=True)
    fig1,ax1 = tb.create_axes_with_exact_size(1.35, 1.2)
    fig2,ax2 = tb.create_axes_with_exact_size(1.35, 1.2)
    fig3,ax3 = tb.create_axes_with_exact_size(1.35, 1.2)
    fig4,ax4 = tb.create_axes_with_exact_size(1.35, 1.2)


    im1 = ax1.imshow(image_ta,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=.1,vmax=.9,cmap='Reds') 
    im2 = ax2.imshow(image_td,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=.1,vmax=.9,cmap='Reds') 
   
    im3 = ax3.imshow(image_cda,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=-17,vmax=17,cmap='coolwarm') 
    im4 = ax4.imshow(image_cdd,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=-17,vmax=17,cmap='coolwarm') 
   
    fs=8
    lp=.75
    xlabel = "$E_x$ (kV cm$^{-1}$)"
    ylabel = "$E_y$ (kV cm$^{-1}$)"
    
    ax1.set_xlabel(xlabel, fontsize=fs,labelpad=lp) 
    ax1.set_ylabel(ylabel, fontsize=fs,labelpad=-4) 
    ax1.tick_params(axis="both", labelsize=fs) 
    ax2.set_xlabel(xlabel, fontsize=fs,labelpad=lp) 
    # ax2.set_ylabel("$E_y$ (kV cm$^{-1}$)", fontsize=fs) 
    ax2.set_yticks([-140,-70,0,70,140],[])
    ax1.set_xticks([-140,-70,0,70,140])
    ax2.set_xticks([-140,-70,0,70,140])
    ax1.set_yticks([-140,-70,0,70,140])
    ax1.tick_params(axis="both", labelsize=fs,length=2) 
    ax2.tick_params(axis="both", labelsize=fs,length=2) 
    ax3.set_xlabel(xlabel, fontsize=fs,labelpad=lp) 
    ax3.set_ylabel(ylabel, fontsize=fs,labelpad=-4) 
    ax3.tick_params(axis="both", labelsize=fs) 
    ax4.set_xlabel(xlabel, fontsize=fs,labelpad=lp) 
    # ax4.set_ylabel("$E_y$ (kV cm$^{-1}$)", fontsize=fs) 
    ax4.set_yticks([-140,-70,0,70,140],[])
    ax3.set_xticks([-140,-70,0,70,140])
    ax4.set_xticks([-140,-70,0,70,140])
    ax3.set_yticks([-140,-70,0,70,140])
    ax3.tick_params(axis="both", labelsize=fs,length=2) 
    ax4.tick_params(axis="both", labelsize=fs,length=2) 
    
    # cbar = fig1.colorbar(im1, ax=ax1, location="right", fraction=0.05) 
    cbar2 = fig2.colorbar(im2, ax=ax2, location="right", fraction=0.05,pad=0.03) 
    cbar4 = fig4.colorbar(im4, ax=ax4, location="right", fraction=0.05,pad=0.03)  
    cbar2.set_ticks([0.2,0.4,0.6,0.8])
    cbar2.ax.tick_params(labelsize=fs,length=1.85)
    cbar4.set_ticks([-16,-8,0,8,16])
    cbar4.ax.tick_params(labelsize=fs,length=1.85)
    cbar2.set_label('SHG Intensity (a.u.)' ,fontsize=fs,labelpad=3)
    cbar4.set_label('SHG-CD (%)',fontsize=fs,labelpad=-2)
    
    ax2.annotate( "", xy=(-120, 138), xytext=(-115, 138), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="-", color='white', linewidth=0.1) )    
    ax2.annotate( "", xy=(-124, 138), xytext=(140, 138), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='white', linewidth=1) )    
    ax1.annotate( "", xy=(140, 138), xytext=(-124, 138), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='white', linewidth=1) )    
    ax1.annotate( "", xy=(137, 138), xytext=(132, 138), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='white', linewidth=0.1) )    
    ax1.annotate( "", xy=(-132.5, 140), xytext=(-132.5, -140), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='white', linewidth=0.1) )    
    ax2.annotate( "", xy=(-132.5, 140), xytext=(-132.5, -140), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='white', linewidth=0.1) )    

    # ax4.annotate( "", xy=(-120, 138), xytext=(-115, 138), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="-", color='k', linewidth=0.1) )    
    # ax4.annotate( "", xy=(-124, 138), xytext=(140, 138), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='k', linewidth=1) )    
    # ax3.annotate( "", xy=(140, 138), xytext=(-124, 138), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='k', linewidth=1) )    
    # ax3.annotate( "", xy=(137, 138), xytext=(132, 138), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='k', linewidth=0.1) )    
    # ax3.annotate( "", xy=(-132.5, 140), xytext=(-132.5, -140), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='k', linewidth=0.1) )    
    # ax4.annotate( "", xy=(-132.5, 140), xytext=(-132.5, -140), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.04",linestyle="--", color='k', linewidth=0.1) )    

    bw=0.5
    for spine in ax1.spines.values(): spine.set_linewidth(bw) 
    for spine in ax2.spines.values(): spine.set_linewidth(bw) 
    for spine in ax3.spines.values(): spine.set_linewidth(bw) 
    for spine in ax4.spines.values(): spine.set_linewidth(bw) 
    cbar2.outline.set_linewidth(bw)
    cbar4.outline.set_linewidth(bw)
    
    return fig1,fig2,fig3,fig4
    
def plot_linecut(Ex_list,Ey_list,SHG,SHG_std,SHG_CD,SHG_CD_std,Esweep='x',Efixval=0,value='CD'):
    plt.rcParams["font.size"] = 10
        
    if Esweep=='x': E_list,colord = Ex_list,'r'
    elif Esweep == 'y': E_list,colord = Ey_list,'b'
    
    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    maxval = 2743.3# np.max([np.max(SHG_ascend),np.max(SHG_descend)])
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    
    # fig, ax0 = plt.subplots(1,1,figsize=(1.7,1.5),sharex=True)
    
    fig_t,ax0 = tb.create_axes_with_exact_size(1.35, 1.2)
    fig_CD,ax1 = tb.create_axes_with_exact_size(1.35, 1.2)
    
    ax0.yaxis.tick_right(), ax1.yaxis.tick_right() 
    ax0.yaxis.set_label_position("right"), ax1.yaxis.set_label_position("right")

    # ax1.yaxis.tick_right() 
    # ax1.yaxis.set_label_position("right")
    Estr = r'$E_{}$'.format(Esweep)
    ms,lw,elw,fs = 5,1.5,1,8
    lp = .75
    
    ax0.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax0.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax0.set_ylabel(r'SHG-CD ($\%$)', fontsize=fs,labelpad=3)
    ax0.set_yticks([-20,-10,0,10,20])
    ax0.set_ylim(-24,24)
    ax0.text(-155,-20.5,'$E_y$ = 10 kV cm$^{-1}$',fontsize=fs*.82)
    ax0.annotate( "", xy=(65, 6), xytext=(0, 6), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='k', linewidth=0.15) )    
    ax0.annotate( "", xy=(40, -16.5), xytext=(105, -16.5), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='r', linewidth=0.15) )    
        
    ax1.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.set_ylabel(r'SHG Intensity', fontsize=fs,labelpad=3) 
    # ax1.set_yticks([.3,.6,.9])
    ax1.text(-8,.74,'$E_y$ = 10 kV cm$^{-1}$',fontsize=fs*.82)
    ax1.annotate( "", xy=(40, .57), xytext=(-25, .57), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='k', linewidth=0.15) )    
    ax1.annotate( "", xy=(-20, .38), xytext=(45, .38), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='r', linewidth=0.15) )    
        
    ax0.set_xlabel(Estr+r' (kV cm$^{-1}$)', fontsize=fs,labelpad=lp), ax1.set_xlabel(Estr+r' (kV cm$^{-1}$)', fontsize=fs,labelpad=lp)
    ax0.set_xticks([-140,-70,0,70,140]), ax1.set_xticks([-140,-70,0,70,140])
    ax0.tick_params(axis="both", labelsize=fs,length=2), ax1.tick_params(axis="both", labelsize=fs,length=2) 
    
    bw=0.5
    for spine in ax0.spines.values(): spine.set_linewidth(bw) 
    for spine in ax1.spines.values(): spine.set_linewidth(bw) 
    # ax1.tick_params(axis="both", labelsize=fs,length=2) 
    return fig_t,fig_CD
    
def plot_supp_linecut_Ey(path_d1,indices=[0,1,2,3,4]):
    x_unique,y_unique,image_cda,image_cdd,image_cdh,image_ta,image_td,image_th = analyze_files_2dmap(path_d1)
    
    # image_t = image_ta/np.max(image_ta)
    image_t = image_td/np.max(image_td)
    
    plt.rcParams["font.size"] = 10
    plt.rcParams["figure.constrained_layout.use"] = False
    ms,lw,elw,fs,bw = 5,1.5,1,8,.5
    fig, axs = plt.subplots(1,5,figsize=(6.4,1.2), dpi=500,sharex=True,gridspec_kw={'hspace':0,'wspace':.05})
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # ax1,ax0,ax3,ax2,ax5,ax4,ax7,ax6,ax9,ax8 = axs[0,0],axs[1,0],axs[0,1],axs[1,1],axs[0,2],axs[1,2],axs[0,3],axs[1,3],axs[0,4],axs[1,4]
    ax1,ax3,ax5,ax7,ax9 = axs[0],axs[1],axs[2],axs[3],axs[4]
    ax1.set_xlabel(r'$E_y$ (kV cm$^{-1}$)', fontsize=fs)
    ax3.set_xlabel(r'$E_y$ (kV cm$^{-1}$)', fontsize=fs)
    ax5.set_xlabel(r'$E_y$ (kV cm$^{-1}$)', fontsize=fs)
    ax7.set_xlabel(r'$E_y$ (kV cm$^{-1}$)', fontsize=fs)
    ax9.set_xlabel(r'$E_y$ (kV cm$^{-1}$)', fontsize=fs)
    # ax0.set_ylabel(r'SHG-CD ($\%$)', fontsize=fs)
    ax1.set_ylabel(r'SHG Intensity', fontsize=fs)
    ax1.set_title(r'$E_y$ = '+str(y_unique[indices[0]])+' kV cm$^{-1}$',fontsize=fs)
    ax3.set_title(r'$E_y$ = '+str(y_unique[indices[1]])+' kV cm$^{-1}$',fontsize=fs)
    ax5.set_title(r'$E_y$ = '+str(y_unique[indices[2]])+' kV cm$^{-1}$',fontsize=fs)
    ax7.set_title(r'$E_y$ = '+str(y_unique[indices[3]])+' kV cm$^{-1}$',fontsize=fs)
    ax9.set_title(r'$E_y$ = '+str(y_unique[indices[4]])+' kV cm$^{-1}$',fontsize=fs)

    xticks=[-140,-70,0,70,140]
    ax1.set_xlim(-170,170)
    yticksCD, yticksT = [-30,-20,-10,0,10,20], [0,.2,.4,.6,.8,1,1.2]
    ymin_CD,ymax_CD = -30,21
    ymin_T,ymax_T = .05,1.25
    ax1.set_xticks(xticks),ax3.set_xticks(xticks),ax5.set_xticks(xticks),ax7.set_xticks(xticks),ax9.set_xticks(xticks)
    # ax0.set_yticks(yticksCD)
    ax1.set_yticks(yticksT)
    # ax2.set_yticks(yticksCD,[]),ax4.set_yticks(yticksCD,[]),ax6.set_yticks(yticksCD,[]),ax8.set_yticks(yticksCD,[])
    ax3.set_yticks(yticksT,[]),ax5.set_yticks(yticksT,[]),ax7.set_yticks(yticksT,[]),ax9.set_yticks(yticksT,[])
    # ax0.set_ylim(ymin_CD,ymax_CD),ax2.set_ylim(ymin_CD,ymax_CD),ax4.set_ylim(ymin_CD,ymax_CD),ax6.set_ylim(ymin_CD,ymax_CD),ax8.set_ylim(ymin_CD,ymax_CD)
    ax1.set_ylim(ymin_T,ymax_T),ax3.set_ylim(ymin_T,ymax_T),ax5.set_ylim(ymin_T,ymax_T),ax7.set_ylim(ymin_T,ymax_T),ax9.set_ylim(ymin_T,ymax_T)
    
    # ax0.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs),ax2.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs)
    # ax4.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs),ax6.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs), ax8.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs)

    for ax in axs:
        ax.tick_params(axis="both", labelsize=fs,length=2) 
        for spine in ax.spines.values(): spine.set_linewidth(bw) 
            
    ax1.errorbar(y_unique, image_t[:,indices[0]], color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    # ax0.errorbar(y_u1nique, image_cda[:,indices[0]],color='black', label=r'$\rightarrow$',marker='.',ms=ms)

    ax3.errorbar(y_unique, image_t[:,indices[1]], color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    # ax2.errorbar(y_1unique, image_cda[:,indices[1]],color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    
    ax5.errorbar(y_unique, image_t[:,indices[2]], color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    # ax4.errorbar(y_unique, image_cda[:,indices[2]],color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    
    ax7.errorbar(y_unique, image_t[:,indices[3]], color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    # ax6.errorbar(y_unique, image_cda[:,indices[3]],color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    
    ax9.errorbar(y_unique, image_t[:,indices[4]], color='black', label=r'$\rightarrow$',marker='.',ms=ms)
    # ax8.errorbar(y_unique, image_cda[:,indices[4]],color='black', label=r'$\rightarrow$',marker='.',ms=ms)

    return fig,str(y_unique[indices])

    
def plot_supp_linecut(Ex_list,
                      SHG_total_m14,SHG_total_std_m14,SHG_CD_m14,SHG_CD_std_m14,
                      SHG_total_m10,SHG_total_std_m10,SHG_CD_m10,SHG_CD_std_m10,
                      SHG_total_m3,SHG_total_std_m3,SHG_CD_m3,SHG_CD_std_m3,
                      SHG_total_1,SHG_total_std_1,SHG_CD_1,SHG_CD_std_1,
                      SHG_total_10,SHG_total_std_10,SHG_CD_10,SHG_CD_std_10,
                      Esweep='x',Efixval=0,value='CD'):
    plt.rcParams["font.size"] = 10
    plt.rcParams["figure.constrained_layout.use"] = False
    ms,lw,elw,fs,bw = 5,1.5,1,8,.5
    
    fig, axs = plt.subplots(2,5,figsize=(6.35,2.4), dpi=500,sharex=True,gridspec_kw={'hspace':0,'wspace':.05})
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax1,ax0,ax3,ax2,ax5,ax4,ax7,ax6,ax9,ax8 = axs[0,0],axs[1,0],axs[0,1],axs[1,1],axs[0,2],axs[1,2],axs[0,3],axs[1,3],axs[0,4],axs[1,4]
    xticks=[-140,-70,0,70,140]
    ax1.set_xlim(-170,170)
    yticksCD, yticksT = [-20,-10,0,10,20], [.2,.4,.6,.8,1]
    ax1.set_xticks(xticks),ax3.set_xticks(xticks),ax5.set_xticks(xticks),ax7.set_xticks(xticks),ax9.set_xticks(xticks)
    ax0.set_yticks(yticksCD),ax1.set_yticks(yticksT)
    ax2.set_yticks(yticksCD,[]),ax4.set_yticks(yticksCD,[]),ax6.set_yticks(yticksCD,[]),ax8.set_yticks(yticksCD,[])
    ax3.set_yticks(yticksT,[]),ax5.set_yticks(yticksT,[]),ax7.set_yticks(yticksT,[]),ax9.set_yticks(yticksT,[])
    ymin_CD,ymax_CD = -28,23
    ymin_T,ymax_T = .1,1.05
    ax0.set_ylim(ymin_CD,ymax_CD),ax2.set_ylim(ymin_CD,ymax_CD),ax4.set_ylim(ymin_CD,ymax_CD),ax6.set_ylim(ymin_CD,ymax_CD),ax8.set_ylim(ymin_CD,ymax_CD)
    ax1.set_ylim(ymin_T,ymax_T),ax3.set_ylim(ymin_T,ymax_T),ax5.set_ylim(ymin_T,ymax_T),ax7.set_ylim(ymin_T,ymax_T),ax9.set_ylim(ymin_T,ymax_T)
    
    ax1.set_ylabel(r'SHG Intensity', fontsize=fs), ax0.set_ylabel(r'SHG-CD ($\%$)', fontsize=fs)
    ax0.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs),ax2.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs)
    ax4.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs),ax6.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs), ax8.set_xlabel(r'$E_x$ (kV cm$^{-1}$)', fontsize=fs)

    for ax in axs:
        for axx in ax:
            axx.tick_params(axis="both", labelsize=fs,length=2) 
            for spine in axx.spines.values(): spine.set_linewidth(bw) 
        
    E_list,colord = Ex_list,'r'
    diffs = np.diff(E_list)
    try: transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+2
    except: transition_index=len(E_list)
    E_list_ascend,E_list_descend = E_list[0:transition_index],E_list[transition_index:]
    maxval = 2743.3 

    SHG,SHG_std,SHG_CD,SHG_CD_std = SHG_total_m14,SHG_total_std_m14,SHG_CD_m14,SHG_CD_std_m14
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    ax0.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax0.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)            
    ax1.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax1.set_title('$E_y$ = -140 kV cm$^{-1}$',fontsize=fs)
    ax1.annotate( "", xy=(65, .8), xytext=(0, .85), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='k', linewidth=0.15) )    
    ax1.annotate( "", xy=(0, .41), xytext=(65, .37), arrowprops=dict(arrowstyle="simple,head_length=0.3,head_width=0.2,tail_width=0.07",linestyle="-", color='r', linewidth=0.15) )    
        
    SHG,SHG_std,SHG_CD,SHG_CD_std = SHG_total_m10,SHG_total_std_m10,SHG_CD_m10,SHG_CD_std_m10
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    ax2.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax2.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)            
    ax3.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax3.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax3.set_title('$E_y$ = -100 kV cm$^{-1}$',fontsize=fs)

    SHG,SHG_std,SHG_CD,SHG_CD_std = SHG_total_m3,SHG_total_std_m3,SHG_CD_m3,SHG_CD_std_m3
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    ax4.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax4.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)            
    ax5.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax5.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax5.set_title('$E_y$ = -30 kV cm$^{-1}$',fontsize=fs)

    SHG,SHG_std,SHG_CD,SHG_CD_std = SHG_total_1,SHG_total_std_1,SHG_CD_1,SHG_CD_std_1
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    ax6.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax6.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)            
    ax7.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax7.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax7.set_title('$E_y$ = 10 kV cm$^{-1}$',fontsize=fs)

    SHG,SHG_std,SHG_CD,SHG_CD_std = SHG_total_10,SHG_total_std_10,SHG_CD_10,SHG_CD_std_10
    SHG_CD_ascend,SHG_CD_descend = SHG_CD[0:transition_index],SHG_CD[transition_index:]
    SHG_CD_std_ascend,SHG_CD_std_descend = SHG_CD_std[0:transition_index],SHG_CD_std[transition_index:]
    SHG_ascend,SHG_descend = SHG[0:transition_index],SHG[transition_index:]
    SHG_std_ascend,SHG_std_descend = SHG_std[0:transition_index],SHG_std[transition_index:]
    SHG_ascend,SHG_descend,SHG_std_ascend,SHG_std_descend = SHG_ascend/maxval,SHG_descend/maxval,SHG_std_ascend/maxval,SHG_std_descend/maxval
    ax8.errorbar(E_list_ascend, SHG_CD_ascend, yerr=SHG_CD_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax8.errorbar(E_list_descend, SHG_CD_descend, yerr=SHG_CD_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)            
    ax9.errorbar(E_list_ascend, SHG_ascend, yerr=SHG_std_ascend,color='black',  label=r'$\rightarrow$',marker='.',elinewidth=elw,ms=ms)
    ax9.errorbar(E_list_descend, SHG_descend, yerr=SHG_std_descend,color=colord,  label=r'$\leftarrow$',marker='.',elinewidth=elw,ms=ms)
    ax9.set_title('$E_y$ = 100 kV cm$^{-1}$',fontsize=fs)

    return fig

if __name__ == "__main__":
    tb.init_plot_params()
    path_d1 = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/90deg_3L3L_4term_S3/SHG-CD-Efield/1-16-2dmap/'
    # txtfiles=glob.glob(path_d1+'*txt')
    # txtfiles_sorted = sorted(txtfiles, key=os.path.getmtime)
    sample = FourTerminal('NbOI290deg4termS3', 5, path_d1)
    w = sample.channel_width
    # file_path = path_d1+'loop1.txt'
    # data = np.loadtxt(file_path,comments='#')
    # Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    # Ex_list, Ey_list = Vx/w, Vy/w
    # SHG_total,SHG_total_std = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    # SHG_CD_std = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    # replot(Ex_list, Ey_list, SHG_total, SHG_total_std, SHG_CD, SHG_CD_std, Ix, Iy)
    # plt.savefig(file_path.replace('.txt','plot.png'), dpi=500)

    x_unique,y_unique,image_cda,image_cdd,image_cdh,image_ta,image_td,image_th = analyze_files_2dmap(path_d1)
    fig_ta,fig_td,fig_cda,fig_cdd=plot_dualmap(image_ta,image_td, image_cda, image_cdd, x_unique, y_unique)    # plt.show()
    # fig_ta.savefig(path_d1+'plot_fig4_c.svg',dpi=500)
    # fig_td.savefig(path_d1+'plot_fig4_d.svg',dpi=500)
    # fig_cda.savefig(path_d1+'plot_fig4_f.svg',dpi=500)
    # fig_cdd.savefig(path_d1+'plot_fig4_g.svg',dpi=500)
    # fig,ystr=plot_supp_linecut_Ey(path_d1, [2,7,13,25,29])
    # filesave = path_d1+'Eylinecuts_v2/Ey_linceuts_intensity_Exdescend.svg'
    # fig.savefig(filesave, dpi=500)
    plt.show()    
    
    '''
    file_path = path_d1+'mapping_fix_y_1p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total,SHG_total_std = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    
    
    fig_t,fig_CD=plot_linecut(Ex_list,Ey_list,SHG_total,SHG_total_std,SHG_CD,SHG_CD_std,Esweep='x',Efixval=10,value='CD')
    fig_t.savefig(path_d1+'plot_supp_linecut1_total.svg',dpi=500)
    fig_CD.savefig(path_d1+'plot_supp_linecut1_CD.svg',dpi=500)
    plt.show()
    '''
    
    '''
    file_path = path_d1+'mapping_fix_y_m14p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total_m14,SHG_total_std_m14 = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std_m14 = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    SHG_CD_m14 = SHG_CD
    
    file_path = path_d1+'mapping_fix_y_m10p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total_m10,SHG_total_std_m10 = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std_m10 = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    SHG_CD_m10 = SHG_CD
    
    file_path = path_d1+'mapping_fix_y_m3p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total_m3,SHG_total_std_m3 = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std_m3 = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    SHG_CD_m3 = SHG_CD
    
    file_path = path_d1+'mapping_fix_y_1p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total_1,SHG_total_std_1 = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std_1 = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    SHG_CD_1 = SHG_CD
    
    file_path = path_d1+'mapping_fix_y_10p0_ascend.txt'
    data = np.loadtxt(file_path,comments='#')
    Vx,Vy,SHG_C1,SHG_C1_std,SHG_C2,SHG_C2_std,SHG_CD,SHG_CD_std,Ix,Iy = data[:,0],data[:,1],np.array(data[:,2]),np.array(data[:,3]),np.array(data[:,4]),np.array(data[:,5]),np.array(data[:,6]),np.array(data[:,7]),data[:,8],data[:,9]
    Ex_list, Ey_list = Vx/w*10, Vy/w*10
    SHG_total_10,SHG_total_std_10 = SHG_C1 + SHG_C2, np.sqrt(SHG_C1_std**2 + SHG_C2_std**2)
    SHG_CD_std_10 = get_SGH_CD_std(SHG_C1,SHG_C2,SHG_C1_std,SHG_C2_std)
    SHG_CD_10 = SHG_CD
    
    
    fig=plot_supp_linecut(Ex_list,
                          SHG_total_m14,SHG_total_std_m14,SHG_CD_m14,SHG_CD_std_m14,
                          SHG_total_m10,SHG_total_std_m10,SHG_CD_m10,SHG_CD_std_m10,
                          SHG_total_m3,SHG_total_std_m3,SHG_CD_m3,SHG_CD_std_m3,
                          SHG_total_1,SHG_total_std_1,SHG_CD_1,SHG_CD_std_1,
                          SHG_total_10,SHG_total_std_10,SHG_CD_10,SHG_CD_std_10,
                          Esweep='x',Efixval=10,value='CD')
    fig.savefig(path_d1+'plot_supp_linecuts.svg',dpi=500)
    plt.show()
    # '''
    '''

    # path_map = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/90deg_3L3L_4term_S3/SHG-CD-Efield/1-16-2dmap/'
    # x_unique,y_unique,image_cda,image_cdd,image_cdh,image_ta,image_td,image_th = analyze_files_2dmap(path_map,fast_axis='x',slow_direction='a')
    # x_unique_d,y_unique_d,image_cda_d,image_cdd_d,image_cdh_d,image_ta_d,image_td_d,image_th_d = analyze_files_2dmap(path_map,fast_axis='x',slow_direction='a')
    # plot_map(image_cdd, x_unique, y_unique,vmin=-18,vmax=18)
    # fig_ta,fig_td,fig_cda,fig_cdd=plot_dualmap(image_ta,image_td, image_cda, image_cdd, x_unique, y_unique)
    # fig_ta.savefig(path_d1+'plot_fig4_c.svg',dpi=500)
    # fig_td.savefig(path_d1+'plot_fig4_d.svg',dpi=500)
    # fig_cda.savefig(path_d1+'plot_fig4_f.svg',dpi=500)
    # fig_cdd.savefig(path_d1+'plot_fig4_g.svg',dpi=500)
    # plt.figure()
    # for x in range(0,31):
    #     fig,(ax0,ax1) = plt.subplots(2,1,figsize=(4.5,5),sharex=True)
    #     ax0.plot(y_unique,image_td[:,x]/2743.3 ,color='k')
    #     ax1.plot(y_unique,image_cdd[:,x],color='k')
        
    #     ax0.plot(y_unique_d,image_td_d[:,x]/2743.3 ,color='r')
    #     ax1.plot(y_unique_d,image_cdd_d[:,x],color='r')
    #     y = str(y_unique[x]) 
    #     ystr = str(y_unique[x]).replace('-','m')
    #     ax1.set_xlabel('$E_y$ (kV cm$^{-1}$)')
    #     ax1.set_ylabel('SHG-CD (%)')
    #     ax0.set_ylabel('SHG Intensity')
    #     ax1.set_xticks([-140,-70,0,70,140])
    #     plt.suptitle('$E_x$ = {} kV cm$^{-1}$'.format(y))
        # plt.savefig(path_d1+'Eylinceuts/linecut_Ex_{}_ascend.png'.format(ystr),dpi=500)
        # plt.close()
    plt.show()   
    # '''
