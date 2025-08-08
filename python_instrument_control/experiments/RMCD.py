#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:09:25 2024

@author: carterfox

RMCD experiment 
"""


import numpy as np
import time
import matplotlib.pyplot as plt
import os


def make_bfield_list(b_start,b_end,b_step):
    bfield_list = np.append(np.arange(b_start,b_end+b_step,b_step),np.arange(b_end,b_start-b_step,-1*b_step))
    return bfield_list

def read_lockin_rmcd_data(lockin):
    
    mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2,3,7,8],num_avgs=100,delay=0.02)
    
    R_cur_mean, R_cur_std = mean_R_chan[0], std_R_chan[0]
    dR_cur_mean, dR_cur_std = mean_dR_chan[2], std_dR_chan[2]
    
    theta_R_cur_mean, theta_R_cur_std = mean_R_chan[1], std_R_chan[1]
    theta_dR_cur_mean, theta_dR_cur_std = mean_dR_chan[3], std_dR_chan[3]

    return R_cur_mean,R_cur_std,theta_R_cur_mean,theta_R_cur_std,dR_cur_mean,dR_cur_std,theta_dR_cur_mean,theta_dR_cur_std


def make_rmcd_saving_file(filename,experiment):
    
    if experiment == 'bscan'   :
        header = "#B(Oe) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    elif experiment == 'mapping':
        header = "#X(V) Y(V) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    
    if not os.path.exists(filename):
        np.savetxt(filename, [], header=header)
    else:
        print('file already exists. making a new one with add on to name')
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        np.savetxt(filename, [], header=header)
    return None

def save_rmcd_data_row(data,file_save):
    np.savetxt(file_save, data, fmt="%.9f", mode='a')
    return None

    

def RMCD_bfield_scan(lockin,opticool,bfield_array,file_save):
    
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

    delay = 5    
    make_rmcd_saving_file(file_save,'bscan')
        
    for b in bfield_array:
        
        lockin.reset_buffer()
        current_field = opticool.set_field(b*10000, 110, opticool.field.approach_mode.linear)
        opticool.wait_for(delay, 0, opticool.field.waitfor) 
        
        data = read_lockin_rmcd_data(lockin) #THIS FUNCTION IS UNFINISHED. NEEDS TETSING
        data_row = data.insert(0,current_field)        
        save_rmcd_data_row(data_row,file_save)
        
    return None


def rmcd_mapping(lockin, ANC, x_start, x_end, y_start, y_end, points, returnsteps,delay,file_save):
    
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
    
    make_rmcd_saving_file(file_save,'mapping')
    
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
            data = read_lockin_rmcd_data(lockin)
            data_row = data.insert(0,y)
            data_row = data.insert(0,x)
            save_rmcd_data_row(data_row,file_save)
            
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
    