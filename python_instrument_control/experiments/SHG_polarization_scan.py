#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 13:55:45 2025
SHG polarization scanning
@author: carterfox

experiment file for measuring SHG while rotating HWPs in the incident and/or detection path

"""

from typing import Union
import numpy as np
import logging
import time
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import toolbelt as tb
from tqdm import tqdm
from homemade_servers.H11890PMT import HamamatsuH11890
from homemade_servers.ThorlabsKCube import RotationMount
from devices.optical import Optical

def main(sample: Optical, pmt: HamamatsuH11890, 
         exc_stage_hwp: RotationMount=None, det_stage_pol: RotationMount=None, 
         exc_stage_angles=None, det_stage_angles=None, rotating='exc', 
         gate_time_ms=200, num_gates=10, laser_power=0, file_save='shgdata.txt',home_after=True):   
    '''
    Run a second harmonic generation (SHG) experiment with optional rotation stages and live polar plotting.

    Parameters
    ----------
    sample : Optical
        The sample under test.
    pmt : HamamatsuH11890
        The photomultiplier tube (PMT) used for signal detection.
    exc_stage_hwp : RotationMount, optional
        Rotation stage for the excitation half wave plate (default is None).
    det_stage_pol : RotationMount, optional
        Rotation stage for the detection polarizer (default is None).
    exc_stage_angles : list or array-like
        List of angles for the excitation half wave plate stage. Give the raw values given to the stage. Must match length of `det_stage_angles`.
    det_stage_angles : list or array-like
        List of angles for the detection polarizer stage. Give the raw values given to the stage. Must match length of `exc_stage_angles`.
    rotating : str, optional
        Indicates which stage is rotating ('exc' or 'det'). Used for plotting (default is 'exc').
    gate_time_ms : int, optional
        Integration time per gate in milliseconds (default is 200).
    num_gates : int, optional
        Number of gates to average per measurement (default is 10).
    laser_power : float, optional
        Laser power in mW used during the experiment (default is 0).
    file_save : str, optional
        Filename for saving the SHG data (default is 'shgdata.txt').

    Returns
    -------
    means : list of float
        List of mean PMT signals collected at each angle step.

    Notes
    -----
    Assumes rotation stage in the excitation path rotates a half wave plate.
    Assumes rotation stage in the detection path rotates a polarizer
    '''


    ### initiate plot, file, and move stages to start positions
    plt.ion()
    fig,ax,line = make_polar_plot()
    fig.canvas.manager.window.move(1920, 60)
    file_path = make_data_file(sample,exc_stage_hwp,det_stage_pol,laser_power,gate_time_ms,num_gates,file_save)
    exc_real_angle, det_real_angle = update_rotation_stages(exc_stage_hwp,det_stage_pol,exc_stage_angles[0],det_stage_angles[0])      
        
    
    ### turn on PMT high voltage
    pmt.set_hv(on=True)    
    means, std_errs, angs_exc, angs_det, = [], [], [], []
    
    ### loop through angles. update plot and file    
    for exc_stage_ang,det_stage_ang in zip(exc_stage_angles,det_stage_angles):
        
        exc_real_angle, det_real_angle = update_rotation_stages(exc_stage_hwp,det_stage_pol,exc_stage_ang,det_stage_ang)
        
        data = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
        means.append(np.mean(data))
        std_errs.append(np.std(data)/np.sqrt(num_gates))
        angs_exc.append(exc_stage_ang)
        angs_det.append(det_stage_ang)
        print(exc_stage_ang,det_stage_ang,means[-1])
        update_saved_data(file_path,exc_stage_ang,det_stage_ang,means[-1],std_errs[-1])
        update_polar_plot(fig,ax,line,angs_exc,angs_det,means,rotating)
    
    ### turn off PMT hv and interactive plotting
    pmt.set_hv(on=False)
    time.sleep(.5)
    plt.ioff()
    plt.savefig(file_path.replace('.txt','plot.png'),dpi=500)
    plt.show()
    
    if home_after:
        exc_real_angle, det_real_angle = update_rotation_stages(exc_stage_hwp, det_stage_pol,0,0)
        print('returning to {}\u00b0, {}\u00b0'.format(exc_real_angle, det_real_angle))
        
    return means



def make_data_file(sample,waveplate,polarizer,laser_power,gate_time_ms,num_gates,file_save):
    if not os.path.exists(sample.data_path+"/SHG"):
        os.makedirs(sample.data_path+"/SHG")
    file_path = sample.data_path+'/SHG/'+file_save
    
    while os.path.exists(file_path):  
        print('file already exists. making a new one with add on to name')
        file_path = file_path.replace(".txt", "_new.txt")
    
    with open(file_path, "a") as f:
        f.write(f"# Sample Name: {sample.sample_name}\n")
        # f.write(f"# Waveplate Home: {waveplate.home}\n")
        # f.write(f"# Polarizer Home: {polarizer.home}\n")
        f.write(f"# Laser Power: {laser_power} mW\n")
        f.write(f"# Gate Time: {gate_time_ms} ms\n")
        f.write(f"# Num Gates: {num_gates}\n")
        f.write("# PolarizerHWPStageAngle\tAnalyzerStageAngle\tCountsMean\tCountsStd\n")
    return file_path

def update_saved_data(file_path,exc_stage_ang,det_stage_ang,means,std_errs):
    with open(file_path, 'a') as f:
        data_save = [exc_stage_ang,det_stage_ang,means,std_errs]
        f.write(' '.join(f"{d:.2f}" for d in data_save) + '\n') 
    
    
def update_rotation_stages(exc_hwp: RotationMount, det_hwp: RotationMount,exc_angle,det_angle):
    exc_home,det_home =None,None
    if exc_hwp != None:
        exc_home = exc_hwp.home
        exc_angle = exc_angle+exc_home
        exc_hwp.move_to(exc_angle)
    if det_hwp != None:
        det_home = det_hwp.home
        det_angle = det_angle+det_home
        det_hwp.move_to(det_angle)
    time.sleep(.5)
    return exc_angle,det_angle
    
def make_polar_plot():
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_rlabel_position(-10)
    ax.set_xticks(np.arange(0, np.radians(360),np.radians(30)))
    line = Line2D([], [], color='b',marker='.')
    ax.add_line(line)
    return fig,ax,line

def update_polar_plot(fig,ax,line,angles_exc_list,angles_det_list, counts_mean_list,rotating='exc'):
    
    '''
    angles are doubled if plotting the angles given to excitation path stage rotating have wave plate
    '''
    
    if rotating=='exc':
        angles = np.array(angles_exc_list)*2
    if rotating=='both':
        angles = np.array(angles_exc_list)*2
    elif rotating=='det':
        angles = np.array(angles_det_list)
    # print(angles,np.array(counts_mean_list))
    angles = angles*np.pi/180
    line.set_data(angles, np.array(counts_mean_list))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.1)
    
    return None
        

if __name__ == "__main__":
    # 
    tb.init_plot_params()
    path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/XiaoWang_Group_data_2024on/ChenS/sample_argonne_10/devices/SHG/'
    file = path+'d3-thick.txt'
    
    data = np.loadtxt(file,comments='#')
    hwp,pol,means,stds = data[:,0]*np.pi/180,data[:,1]*np.pi/180,data[:,2],data[:,3]
    
    fig, ax = plt.subplots(figsize=(5,5),subplot_kw={'projection': 'polar'})
    # ax.set_rlabel_position(-10)
    ax.set_xticks(np.arange(0, np.radians(360),np.radians(60)))
    ax.set_yticklabels([])
    
    ax.plot(pol      ,means,color='C0',ms=12)
    ax.plot(pol+np.pi,means,color='C0',ms=12)
    x=47
    y=x+60
    z=y+60
    ax.axvline(x*np.pi/180,c='C1'),ax.axvline((x+180)*np.pi/180,c='C1')
    ax.axvline(y*np.pi/180,c='C1'),ax.axvline((y+180)*np.pi/180,c='C1')
    ax.axvline(z*np.pi/180,c='C1'),ax.axvline((z+180)*np.pi/180,c='C1')
    
    ax.set_title('SHG Intensity ($I_{||}$) \n')
    
    plt.show()
    
    




    
    