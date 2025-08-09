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
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from homemade_servers.QDopticool import Opticool
from devices.dualgate import DualGate
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb

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
    
    tb.init_plot_params()
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('B (T)'), ax.set_ylabel('RMCD %')
    ax.set_xlim(min(bfield_array)/10000,max(bfield_array)/10000)
    
    b_list, rmcd_list,b_list_ascend, b_list_descend, rmcd_list_ascend,rmcd_list_descend = [],[],[],[],[],[]
    for b in bfield_array:
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
        # np.savetxt(saving_file, data_row, fmt="%.9f", mode='a')
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
        ax.plot(b_list_ascend, rmcd_list_ascend, 'b-',label=r'$\rightarrow$')
        ax.plot(b_list_descend, rmcd_list_descend, 'r-',label=r'$\leftarrow$')
        if len(rmcd_list)>1: ax.set_ylim(min(rmcd_list)*1.1, max(rmcd_list)*1.1)        
        ax.legend(loc='upper left')
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    plt.ioff()
    plt.show()
    
    return None


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
    fig, ax = plt.subplots()
    im = ax.imshow(scan_array, cmap='viridis', interpolation='none')
    cbar=plt.colorbar(im, ax=ax)
    ax.set_xlabel('$V_x$'),ax.set_ylabel('$V_y$')
    xticks = np.linspace(0, x_points - 1, num=5, dtype=int)  # 5 ticks evenly spaced
    yticks = np.linspace(0, y_points - 1, num=5, dtype=int)
    xlabels = [round(x_start + (x_points - 1 - i) * stepx, 2) for i in xticks]
    ylabels = [round(y_start + j * stepy, 2) for j in yticks]
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)
    cbar.set_label('RMCD %')

    
    for j in range(y_points):
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
        time.sleep(0.2)
            
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
    
    
    
    