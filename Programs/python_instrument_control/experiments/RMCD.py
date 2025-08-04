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


def make_saving_file(filename):
    
    header = "#B(Oe) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    
    if not os.path.exists(filename):
        np.savetxt(filename, [], header=header)
    else:
        print('file already exists. making a new one with add on to name')
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        np.savetxt(filename, [], header=header)
        

def save_rmcd_data_row(data,file_save):
        
    np.savetxt(file_save, data, fmt="%.9f", mode='a')
    
    return None

    

def RMCD_bfield_scan(lockin,opticool,bfield_array,file_save):

    delay = 5    
    make_saving_file(file_save)
        
    for b in bfield_array:
        
        lockin.reset_buffer()
        current_field = opticool.set_field(b, 110, opticool.field.approach_mode.linear)
        opticool.wait_for(delay, 0, opticool.field.waitfor) 
        
        data = read_lockin_rmcd_data(lockin) #THIS FUNCTION IS UNFINISHED. NEEDS TETSING
        data_row = data.insert(0,current_field)        
        save_rmcd_data_row(data_row,file_save)
        
    return None


    