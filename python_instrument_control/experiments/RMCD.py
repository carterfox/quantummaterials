#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:09:25 2024

@author: carterfox

RMCD experiment 
"""
from typing import Union
import numpy as np
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
    Performs a magnetic field-dependent RMCD (Reflective Magnetic Circular Dichroism) scan
    by sweeping through a list of magnetic field values, collecting data at each point using
    a lock-in amplifier, and saving the results to a file.

    Parameters:
    ----------
    lockin : object
        Lock-in amplifier interface used to collect RMCD data.
    opticool : object
        Magnetic field controller (OptiCool) used to set and stabilize the field.
    bfield_array : list or np.ndarray
        Array of magnetic field values (in Tesla or Gauss, depending on system units) to scan.
    file_save : str
        Path to the file where scan data will be saved.

    Returns:
    -------
    None
    """
    saving_file = sample.data_path+'/RMCD/bfield_scan/'+file_save
    tb.make_rmcd_saving_file(saving_file,'bscan')
        
    for b in bfield_array:
        
        lockin.reset_buffer()
        current_field = opticool.set_field(b*10000, 110, opticool.field.approach_mode.linear)
        opticool.wait_for(lockin.delay, 0, opticool.field.waitfor) 
        
        data = tb.read_lockin_rmcd_data(lockin) #THIS FUNCTION IS UNFINISHED. NEEDS TETSING
        data_row = data.insert(0,current_field)        
        np.savetxt(saving_file, data_row, fmt="%.9f", mode='a')
        
    return None


def RMCD_mapping(sample, lockin: LockInOE1022D, ANC: ANC300, x_start, x_end, y_start, y_end, points, returnsteps,delay,file_save):
    
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
    scannerx = ANC.submodules['axis1']
    scannery = ANC.submodules['axis2']
    
    saving_file = sample.data_path+'/RMCD/mapping/'+file_save    
    tb.make_rmcd_saving_file(saving_file,'mapping')
    
    y_points = points
    x_points = points
   
    stepx = (x_end-x_start)/x_points
    stepy = (y_end-y_start)/y_points

    scan_array = np.zeros((y_points, x_points))
    return_step_size = -(x_end - x_start) / returnsteps
    
    
    plt.ion()
    fig, ax = plt.subplots()
    im = ax.imshow(scan_array, cmap='viridis', interpolation='none')
    plt.colorbar(im, ax=ax)

    
    for j in range(y_points):
        y = y_start + j * stepy
        scannery.offset(y)

        # Forward scan
        for i in range(x_points):
            
            lockin.reset_buffer()
            x = x_start + i * stepx
            scannerx.offset(x)
            time.sleep(delay)
            data = tb.read_lockin_rmcd_data(lockin)
            data_row = data.insert(0,y)
            data_row = data.insert(0,x)
            np.savetxt(saving_file, data_row, fmt="%.9f", mode='a')
            
            rmcd_value = data[4]/data[0]
            scan_array[j, i] = rmcd_value
                        
            im.set_data(scan_array)
            im.set_clim(vmin=np.min(scan_array), vmax=np.max(scan_array))
            plt.draw()


        # Return path (no data stored)
        for r in range(1, returnsteps + 1):
            x_back = x_end + r * return_step_size
            scannerx.offset(x_back)
            time.sleep(0.2)
            
        
    plt.ioff()
    plt.show()

    return scan_array


def RMCD_dualgate_pure_Efield_sweep(sample: DualGate, lockin: LockInOE1022D,
                                    keithley_b: KeithleySourceMeter, keithley_t: KeithleySourceMeter,
                                    E_array,file_save):
    
    saving_file = sample.data_path+'/RMCD/Esweep/'+file_save    
    tb.make_rmcd_saving_file(saving_file,'Esweep')
    
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
        plt.draw()
    
    plt.ioff()
    plt.show()
    
    return None
    
    
    
    