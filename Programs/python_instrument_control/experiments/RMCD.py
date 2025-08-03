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



def make_bfield_list(b_start,b_end,b_step):
    
    bfield_list = np.append(np.arange(b_start,b_end+b_step,b_step),np.arange(b_end,b_start-b_step,-1*b_step))

    return bfield_list

def read_lockin_rmcd_data(lockin):
    
    R_cur, theta_R_cur = lockin.read_multiple(lockin.R_chan,[2,3])
    dR_cur, theta_dR_cur = lockin.read_multiple(lockin.dR_chan,[7,8])
    
    R_cur_mean, R_cur_std = np.mean(R_cur), np.std(R_cur)
    dR_cur_mean, dR_cur_std = np.mean(dR_cur), np.std(dR_cur)
    theta_R_cur_mean, theta_R_cur_std = np.mean(theta_R_cur), np.std(theta_R_cur)
    theta_dR_cur_mean, theta_dR_cur_std = np.mean(theta_dR_cur), np.std(theta_dR_cur)

    return R_cur_mean, R_cur_std, dR_cur_mean, dR_cur_std, theta_R_cur_mean, theta_R_cur_std, theta_dR_cur_mean, theta_dR_cur_std


def RMCD_bfield_scan(lockin,opticool,bfield_array):

    delay = 5    
    R, theta_R, R_std, theta_R_std = [], [], [], []
    dR, theta_dR, dR_std, theta_dR_std = [], [], [], []
            
        
    for b in bfield_array:
        
        lockin.reset_buffer()
        current_field = opticool.set_field(b, 110, opticool.field.approach_mode.linear)
        opticool.wait_for(delay, 0, opticool.field.waitfor) 
        
        data = read_lockin_rmcd_data(lockin) #THIS FUNCTION IS UNFINISHED. NEEDS TETSING
        R_cur_mean, R_cur_std, dR_cur_mean, dR_cur_std, theta_R_cur_mean, theta_R_cur_std, theta_dR_cur_mean, theta_dR_cur_std = data
        
        R.append(R_cur_mean)
        R_std.append(R_cur_std)
        dR.append(dR_cur_mean)
        dR_std.append(dR_cur_std)
        theta_R.append(theta_R_cur_mean)
        theta_R_std.append(theta_R_cur_std)
        theta_dR.append(theta_dR_cur_mean)
        theta_dR_std.append(theta_dR_cur_std)
        
    scan_data_pack = [R,R_std,dR,dR_std,theta_R,theta_R_std,theta_dR,theta_dR_std]
        
    return scan_data_pack
        


    