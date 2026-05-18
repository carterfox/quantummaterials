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
    scannerx.mode('off')
    scannery.mode('off')
    
    if not os.path.exists(sample.data_path+"/RMCD/mapping"):
        os.makedirs(sample.data_path+"/RMCD/mapping")
    
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
    fig.canvas.manager.window.move(1920, 100)
    plt.show(block=False)
    try:
        fig.canvas.manager.window.raise_()  # Works on Qt
        fig.canvas.manager.window.activateWindow()
    except Exception as e:
        print("Window raise failed:", e)

    for j in tqdm(range(y_points)):
        y = round(y_start + j * stepy,2)
        scannery.offset(y)
        
        for i in range(x_points):
            lockin.reset_buffer()
            x = round(x_start + i * stepx,2)
            scannerx.offset(x)
            time.sleep(lockin.delay)
            data = tb.read_lockin_rmcd_data(lockin)
            
            for attempt in range(10): 
                try: 
                    with open(saving_file, 'a') as file:
                        file.write(str(x)+' '+str(y)+' ') 
                        file.write(' '.join(f"{d:.9f}" for d in data) + '\n') 
                    break 
                except FileNotFoundError: time.sleep(0.2)
                
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


def plot_rmcd_map(scan_array,x_step,y_step,plot_type='RMCD',cmin=None,cmax=None):
    y_points,x_points = np.shape(scan_array)
    fig, ax = plt.subplots()
    # fig.canvas.manager.window.move(1920, 100)
    im = ax.imshow(scan_array, cmap='viridis', interpolation='none',vmin=cmin,vmax=cmax)
    cbar=plt.colorbar(im, ax=ax)
    # if cmin!=None:
        # cbar.set_clim(cmin,cmax)
    ax.set_xlabel(r'X ($\mu$m)'),ax.set_ylabel(r'Y ($\mu$m)')
    # print(x_points)
    xticks = np.linspace(0, x_points - 1, num=5)  # 5 ticks evenly spaced
    yticks = np.linspace(0, y_points - 1, num=5)
    scale=.2
    xlabels = [round(0 + (x_points - 1 - i) * x_step*scale, 2) for i in xticks]
    ylabels = [round(0 + j * y_step*scale, 2) for j in yticks]
    # print(xticks,xlabels)
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

def replot_rmcd_map(data_file,plot_type='RMCD',cmin=None,cmax=None):
    data = np.loadtxt(data_file)
    x,y,r,dr,theta_dr = data[:,0], data[:,1],data[:,2], data[:,6], data[:,8]
    rmcd = dr/r*100
    rmcd[np.where(theta_dr>0)] *= -1
    x_points,y_points = np.unique(x), np.unique(y)
    xstep = x_points[1]-x_points[0]
    ystep = y_points[1]-y_points[0]
    
    # if file2[0] != None:
    #     data2 = np.loadtxt(data_file2)
    #     x2,y2,r2,dr2,theta_dr2 = data2[:,0], data2[:,1],data2[:,2], data2[:,6], data2[:,8]
    #     rmcd2 = dr2/r2*100
    #     rmcd2[np.where(theta_dr2>0)] *= -1
    #     rmcd = rmcd-rmcd2
    
    if plot_type == 'RMCD':
        grid = rmcd
    elif plot_type == 'R':
        grid = r
    elif plot_type == 'dR':
        grid = dr
    elif plot_type == 'thetadR':
        grid = theta_dr
    scan_array = np.fliplr(grid.reshape((len(y_points), len(x_points))))
    fig,ax,im=plot_rmcd_map(scan_array,xstep,ystep,plot_type,cmin,cmax)
    return fig,ax,im


if __name__ == "__main__":
    # 
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4/RMCD/bfield_scan/'
    # path_d3 = '/Users/carterfox/Google Drive/My Drive/StackingTransitions/CrI3/round7/d3/RMCD/mapping/'
    data_path="I:/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round8/c6_2L2L_3-1/RMCD/mapping/"
    # file = path_s6+'sixlayer-scan3.txt'
    # file = path_s6+'fourlayer-scan1.txt'
    # file = path_s6+'map1_0T.txt'
    file = data_path+'test_new.txt'
    # file = data_path+'map_after_m2T_8-19.txt'
    tb.init_plot_params()

    plottype = 'RMCD'
    # fig,ax,im = replot_rmcd_map(file,plottype,0,2.1)
    fig,ax,im = replot_rmcd_map(file,'thetadR')

    # fig,ax,b_field,theta_dr = replot_rmcd_bfield_scan(file)
    # tb.plot_arrow_legend(ax,r'$B_{\perp}$',x1=1.7,y1=-7,ls=18,yratio=.058,xratio=.12,wratio=.0872)
    
    title = file.split('/')[-1].split('.txt')[0]
    plt.title(title)
    # plt.xlim(0,40)
    # plt.ylim(40,0)
    # plt.savefig(file.replace('.txt','_{}_plot.png'.format(plottype)),dpi=500)
    plt.show()