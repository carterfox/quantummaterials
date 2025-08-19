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

def main(sample, lockin: LockInOE1022D,opticool: Opticool,bfield_array,file_save):
    
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
    if not os.path.exists(sample.data_path+"/RMCD/bfield_scan"):
        os.makedirs(sample.data_path+"/RMCD/bfield_scan")

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
    fig.canvas.manager.window.move(1920, 100)
    plt.show(block=False)
    try:
        fig.canvas.manager.window.raise_()  # Works on Qt
        fig.canvas.manager.window.activateWindow()
    except Exception as e:
        print("Window raise failed:", e)
    ax.set_xlabel('B (T)'), ax.set_ylabel('RMCD %')
    ax.set_xlim(min(bfield_array)/10000,max(bfield_array)/10000)
    line_up = Line2D([], [], color='black', label=r'$\rightarrow$',marker='.')
    line_down = Line2D([], [], color='r', label=r'$\leftarrow$',marker='.')
    ax.add_line(line_up)
    ax.add_line(line_down)
    ax.legend()
    return fig,ax,line_up,line_down
    

def replot_rmcd_bfield_scan(data_file):
    
    data = np.loadtxt(data_file)
    b_field, r, dr, theta_dr  = data[:,0], data[:,1],data[:,5], data[:,7]
    rmcd = dr/r*100
    # s6 sixlayer
    rmcd[np.where(theta_dr>0)] *= -1
    # rmcd[0:8] = rmcd[8] -(rmcd[0:8] - rmcd[8])
    # rmcd[80:96] = rmcd[80] - (rmcd[80:96]-rmcd[80])
    # rmcd[-8:] = rmcd[8] - (rmcd[-8:] - rmcd[8])   
    # dr[np.where(theta_dr>0)] *= -1
    # dr[0:8] = dr[8] -(dr[0:8] - dr[8])
    # dr[80:96] = dr[80] - (dr[80:96]-dr[80])
    # dr[-8:] = dr[8] - (dr[-8:] - dr[8])   

    diffs = np.diff(b_field)
    try:
        transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+1
    except:
        transition_index=len(b_field)
    b_field_ascend = b_field[0:transition_index]
    b_field_descend = b_field[transition_index:]
    rmcd_ascend = rmcd[0:transition_index]
    rmcd_descend = rmcd[transition_index:]
    
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    
    ax.plot(b_field_ascend, rmcd_ascend, color='black', label=r'$\rightarrow$',marker='.',ms=10,lw=3)
    ax.plot(b_field_descend, rmcd_descend, color='r', label=r'$\leftarrow$',marker='.',ms=10,lw=3)
    ax.set_xlabel(r'$B$ (T)',fontsize=24)
    ax.set_ylabel("RMCD %",rotation=90,fontsize=24,labelpad=-10)
    ax.set_xlim(min(b_field),max(b_field))
    # ax.legend(loc='upper left')
    
    return fig,ax,b_field,theta_dr,dr,r
    

if __name__ == "__main__":
    # 
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4/RMCD/bfield_scan/'
    path_d3 = '/Users/carterfox/Google Drive/My Drive/StackingTransitions/CrI3/round7/d3/RMCD/bfield_scan/'
    # path_s6 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/6-18-sample-for-afm-and-rmcd/RMCD/bfield_scan/'
    # file = path_s6+'sixlayer-scan3.txt'
    # file = path_s6+'fourlayer-scan1.txt'
    # file = path_s6+'map1_0T.txt'
    file = path_d3+'bilayer_scan_p5-nogates.txt'
    # path_s6 = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/6-18-sample-for-afm-and-rmcd/RMCD/bfield_scan/'
    # file = path_s6+'sixlayer-scan3.txt'
    # file = path_s6+'fourlayer-scan1.txt'
    # file = path_s6+'map1_0T.txt'
    # file = path_d3+'map1_0T_after_m2T.txt'
    # file = path_s6+'sixlayer-scan3.txt'
    tb.init_plot_params()

    
    fig,ax,b_field,theta_dr,dr,r = replot_rmcd_bfield_scan(file)
    tb.plot_arrow_legend(ax,r'B',x1=.8,y1=-12,ls=18,yratio=.058,xratio=.12,wratio=.0872)
    
    # title = file.split('/')[-1].split('.txt')[0]
    # plt.title(title)
    
    # plt.savefig(file.replace('.txt','_paper_plot.png'),dpi=500)
    plt.savefig(file.replace('.txt','_plot.png'),dpi=500)
    plt.show()