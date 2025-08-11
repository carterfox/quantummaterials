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
    
def main(sample, lockin: LockInOE1022D, ANC: ANC300, x_start, x_end, y_start=None, y_end=None, points=5, returnsteps=30,file_save='test.txt'):
    
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
            rmcd_value = data[4]/data[0]*100
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
    x,y,r,dr,theta_dr = data[:,0], data[:,1],data[:,2], data[:,6], data[:,8]
    rmcd = dr/r*100
    rmcd[np.where(theta_dr>0)] *= -1
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


if __name__ == "__main__":
    # 
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4/RMCD/bfield_scan/'
    path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/RMCD/mapping/'
    # path_s6 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/6-18-sample-for-afm-and-rmcd/RMCD/bfield_scan/'
    # file = path_s6+'sixlayer-scan3.txt'
    # file = path_s6+'fourlayer-scan1.txt'
    # file = path_s6+'map1_0T.txt'
    file = path_d3+'map1_0T_after_m2T.txt'
    tb.init_plot_params()

    fig,ax,im = replot_rmcd_map(file,'RMCD')

    # fig,ax,b_field,theta_dr = replot_rmcd_bfield_scan(file)
    # tb.plot_arrow_legend(ax,r'$B_{\perp}$',x1=1.7,y1=-7,ls=18,yratio=.058,xratio=.12,wratio=.0872)
    
    title = file.split('/')[-1].split('.txt')[0]
    plt.title(title)
    
    plt.savefig(file.replace('.txt','_plot.png'),dpi=500)
    plt.show()