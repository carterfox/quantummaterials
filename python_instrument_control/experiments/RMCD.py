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

def RMCD_bfield_scan(sample, lockin: LockInOE1022D,opticool: Opticool,bfield_array,file_save):
    
    """
    Perform a magnetic field scan to collect RMCD data and update a live plot.

    Parameters
    ----------
    sample : object
        Sample object containing metadata and file path information.
    lockin : LockInOE1022D
        Lock-in amplifier used to collect RMCD signals.
    opticool : Opticool
        Magnet controller used to set and stabilize magnetic fields.
    bfield_array : array-like
        List or array of magnetic field values (in Gauss) to scan.
    file_save : str
        Filename for saving the RMCD scan data.

    Returns
    -------
    None
    """

    gen_path = sample.data_path+'/RMCD/bfield_scan/'+file_save
    saving_file = tb.make_rmcd_saving_file(gen_path,'bscan')
    
    plt.ion()
    fig,ax,line_up,line_down = init_rmcd_bfield_scan_plot(bfield_array)
    
    b_list, rmcd_list,b_list_ascend, b_list_descend, rmcd_list_ascend,rmcd_list_descend = [],[],[],[],[],[]
    for b in tqdm(bfield_array):
        field_T = b/10000
        lockin.reset_buffer()
        opticool.set_field(b, 110, opticool.field.approach_mode.linear)
        opticool.wait_for(lockin.delay, 0, opticool.field.waitfor) 

        data = tb.read_lockin_rmcd_data(lockin) #THIS FUNCTION IS UNFINISHED. NEEDS TETSING
        theta_dr = data[6]
        rmcd = data[4]/data[0]*100
        if theta_dr>0:
            rmcd = -1*rmcd
        
        with open(saving_file, 'a') as file:
            file.write(str(field_T)+' ') 
            file.write(' '.join(f"{d:.9f}" for d in data) + '\n') 
        
        try:
            if field_T>=b_list[-1]:
                b_list_ascend.append(field_T)
                rmcd_list_ascend.append(rmcd)
            if field_T<=b_list[-1]:
                b_list_descend.append(field_T)
                rmcd_list_descend.append(rmcd)
        except:
            b_list_ascend.append(field_T)
            rmcd_list_ascend.append(rmcd)
            
        b_list.append(field_T)
        update_rmcd_bfield_scan_plot(fig,ax,line_up,line_down,
                                     b_list_ascend,rmcd_list_ascend,b_list_descend,rmcd_list_descend)
    
    plt.ioff()
    plt.show()
    
    return None

def update_rmcd_bfield_scan_plot(fig,ax,line_up,line_down,b_list_ascend,rmcd_list_ascend,
                                 b_list_descend,rmcd_list_descend):
    line_up.set_data(b_list_ascend, rmcd_list_ascend)
    line_down.set_data(b_list_descend, rmcd_list_descend)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.05)
    return None

def init_rmcd_bfield_scan_plot(bfield_array):
    fig, ax = plt.subplots()
    ax.set_xlabel('B (T)'), ax.set_ylabel('RMCD %')
    ax.set_xlim(min(bfield_array)/10000,max(bfield_array)/10000)
    line_up = Line2D([], [], color='black', label=r'$\rightarrow$',marker='.')
    line_down = Line2D([], [], color='r', label=r'$\leftarrow$',marker='.')
    # tb.plot_arrow_legend(ax,r'$B_{\perp}$',x1=1.3,y1=-8,ls=18,yratio=.058,xratio=.12,wratio=.0872)
    ax.add_line(line_up)
    ax.add_line(line_down)
    ax.legend()
    return fig,ax,line_up,line_down
    
def RMCD_mapping(sample, lockin: LockInOE1022D, ANC: ANC300, x_start, x_end, y_start=None, y_end=None, points=5, returnsteps=30,file_save='test.txt'):
    
    """
    Performs a raster scan over a 2D grid to collect RMCD (Reflective Magnetic Circular Dichroism) data
    using a lock-in amplifier and motion controller, and saves the results to a file.

    The scan proceeds line-by-line in the X direction for each Y level, collecting data at each point.
    After each forward scan line, the instrument performs a stepwise return movement in X (without recording data)
    to prepare for the next Y level. The collected RMCD values are stored in a 2D NumPy array and saved
    to a file with corresponding X and Y coordinates.

    Parameters:
    ----------
    lockin : object
        Lock-in amplifier interface used to collect RMCD data.
    anc300 : object
        Motion controller interface (not directly used in this function but assumed to control movement).
    x_start : float
        Starting X position of the scan.
    x_end : float
        Ending X position of the scan.
    y_start : float
        Starting Y position of the scan.
    y_end : float
        Ending Y position of the scan.
    points : int
        Number of scan points along each axis (X and Y).
    returnsteps : int
        Number of steps used to return to the starting X position after each scan line.
        These movements are not recorded in the output array.
    file_save : str
        Path to the file where scan data will be saved.

    Returns:
    -------
    scan_array : np.ndarray
        A 2D array of shape (points, points) containing RMCD values at each scanned (X, Y) position.
        Each value is computed as `data[4] / data[0]` from the lock-in amplifier output.
    """
    
    if y_start == None:
        y_start,y_end = x_start, x_end
    
    scannerx = ANC.submodules['axis1']
    scannery = ANC.submodules['axis2']
    
    gen_path = sample.data_path+'/RMCD/mapping/'+file_save    
    saving_file = tb.make_rmcd_saving_file(gen_path,'mapping')
    
    y_points = points
    x_points = points
   
    stepx = (x_end-x_start)/(x_points-1)
    stepy = (y_end-y_start)/(y_points-1)

    scan_array = np.zeros((y_points, x_points))
    return_step_size = -(x_end - x_start) / returnsteps
    
    plt.ion()
    fig,ax,im = plot_rmcd_map(scan_array,stepx,stepy,'RMCD')

    for j in tqdm(range(y_points)):
        y = round(y_start + j * stepy,2)
        scannery.offset(y)
        
        for i in range(x_points):
            lockin.reset_buffer()
            x = round(x_start + i * stepx,2)
            scannerx.offset(x)
            time.sleep(lockin.delay)
            data = tb.read_lockin_rmcd_data(lockin)
            
            with open(saving_file, 'a') as file:
                file.write(str(x)+' '+str(y)+' ') 
                file.write(' '.join(f"{d:.9f}" for d in data) + '\n') 
            rmcd_value = data[4]/data[0]
            scan_array[j, x_points-1-i] = rmcd_value
        
        im.set_data(scan_array)
        im.set_clim(vmin=np.min(scan_array), vmax=np.max(scan_array))
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Return path (no data stored)
        for r in range(returnsteps):
            x_back = x_end + (r+1) * return_step_size
            scannerx.offset(x_back)
            time.sleep(0.1)
    
    for r in range(returnsteps):
        y_back = y_end + (r+1) * return_step_size
        scannery.offset(y_back)
        time.sleep(0.15)
            
    plt.ioff()
    plt.show()

    return scan_array


def RMCD_dualgate_pure_Efield_sweep(sample: DualGate, lockin: LockInOE1022D,
                                    keithley_b: KeithleySourceMeter, keithley_t: KeithleySourceMeter,
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
    
    saving_file = sample.data_path+'/RMCD/Esweep/'+file_save    
    tb.make_rmcd_saving_file(saving_file,'Esweep')
    
    tb.init_plot_params()
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('RMCD %')
    
    tb.configure_keithley(keithley_b)
    tb.configure_keithley(keithley_t)
    
    rmcd_list = []
    d_b = sample.d_b
    d_t = sample.d_t
    
    for E in E_array:
        
        V_b = E*d_b
        V_t = -V_b*d_t/d_b
        
        keithley_b.source_voltage = V_b             # Set output voltage
        keithley_t.source_voltage = V_t             # Set output voltage
        time.sleep(0.3)                          # Allow output and DUT to settle
        Vb_meas, Ib_meas = tb.measure_V_I(keithley_b)
        Vt_meas, It_meas = tb.measure_V_I(keithley_t)
        elec_data = [V_b,Vb_meas,V_t,Vt_meas,Ib_meas,It_meas]
        
        lockin.sleep(lockin.delay)
        lockin.reset_buffer()
        rmcd_data = tb.read_lockin_rmcd_data(lockin)
        rmcd_list.append(rmcd_data[4]/rmcd_data[0]*100)
        
        data_row = elec_data + rmcd_data
        np.savetxt(saving_file, data_row, fmt="%.9f", mode='a')
        
        ax.plot(E_array[0:len(rmcd_list)],rmcd_list)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    plt.ioff()
    plt.show()
    
    return None

def plot_rmcd_map(scan_array,x_step,y_step,plot_type='RMCD'):
    y_points,x_points = np.shape(scan_array)
    fig, ax = plt.subplots()
    im = ax.imshow(scan_array, cmap='viridis', interpolation='none')
    cbar=plt.colorbar(im, ax=ax)
    ax.set_xlabel('$V_x$'),ax.set_ylabel('$V_y$')
    xticks = np.linspace(0, x_points - 1, num=5, dtype=int)  # 5 ticks evenly spaced
    yticks = np.linspace(0, y_points - 1, num=5, dtype=int)
    xlabels = [round(0 + (x_points - 1 - i) * x_step, 2) for i in xticks]
    ylabels = [round(0 + j * y_step, 2) for j in yticks]
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)
    if plot_type == 'RMCD':
        cbar.set_label('RMCD %')
    elif plot_type == 'dR':
        cbar.set_label('dR')
    elif plot_type == 'R':
        cbar.set_label('R')
    elif plot_type == 'theta':
        cbar.set_label(r'$\theta$')
    return fig,ax,im

def replot_rmcd_map(data_file,plot_type='RMCD'):
    data = np.loadtxt(data_file)
    x,y,r,dr = data[:,0], data[:,1],data[:,2], data[:,6]
    rmcd = dr/r*100
    x_points,y_points = np.unique(x), np.unique(y)
    xstep = x_points[1]-x_points[0]
    ystep = y_points[1]-y_points[0]

    if plot_type == 'RMCD':
        grid = rmcd
    elif plot_type == 'R':
        grid = r
    elif plot_type == 'dR':
        grid = dr
    scan_array = np.fliplr(grid.reshape((len(y_points), len(x_points))))
    fig,ax,im=plot_rmcd_map(scan_array,xstep,ystep,plot_type)
    return fig,ax,im


def replot_rmcd_bfield_scan(data_file):
    
    data = np.loadtxt(data_file)
    b_field, r, dr, theta_dr  = data[:,0], data[:,1],data[:,5], data[:,7]
    rmcd = dr/r*100
    # s6 sixlayer
    rmcd[np.where(theta_dr>50)] *= -1
    rmcd[0:8] = rmcd[8] -(rmcd[0:8] - rmcd[8])
    rmcd[80:96] = rmcd[80] - (rmcd[80:96]-rmcd[80])
    rmcd[-8:] = rmcd[8] - (rmcd[-8:] - rmcd[8])    

    diffs = np.diff(b_field)
    try:
        transition_index = np.where((diffs[:-1] > 0) & (diffs[1:] < 0))[0][0]+1
    except:
        transition_index=len(b_field)
    b_field_ascend = b_field[0:transition_index]
    b_field_descend = b_field[transition_index:]
    rmcd_ascend = rmcd[0:transition_index]
    rmcd_descend = rmcd[transition_index:]
    
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    
    ax.plot(b_field_ascend, rmcd_ascend, color='black', label=r'$\rightarrow$',marker='.')
    ax.plot(b_field_descend, rmcd_descend, color='r', label=r'$\leftarrow$',marker='.')
    ax.set_xlabel('B (T)'), ax.set_ylabel('RMCD %')
    ax.set_xlim(min(b_field),max(b_field))
    # ax.legend(loc='upper left')
    
    return fig,ax,b_field,theta_dr
    

if __name__ == "__main__":
    # 
    path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4/RMCD/bfield_scan/'
    path_s6 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/6-18-sample-for-afm-and-rmcd/RMCD/bfield_scan/'
    file = path_s6+'sixlayer-scan3.txt'
    # file = path_s6+'map1_0T.txt'
    tb.init_plot_params()

        
    # fig,ax,im = replot_rmcd_map(file,'RMCD')
    fig,ax,b_field,theta_dr = replot_rmcd_bfield_scan(file)
    tb.plot_arrow_legend(ax,r'$B_{\perp}$',x1=1.3,y1=-8,ls=18,yratio=.058,xratio=.12,wratio=.0872)

    plt.savefig(path_s6+'sixlayer-scan3-rmcd.png',dpi=500)
    plt.show()