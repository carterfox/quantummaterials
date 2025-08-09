#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 21:25:45 2025

@author: carterfox
"""


import numpy as np
import os
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from pymeasure.instruments.keithley import Keithley2400, Keithley2450
from homemade_servers.SSI_OE1022D import LockInOE1022D
from typing import Union
import astropy.constants as cont
import astropy.units as uu

def make_bfield_list(b_start,b_end,b_step):
    bfield_list = np.append(np.arange(b_start,b_end+b_step,b_step),np.arange(b_end,b_start-b_step,-1*b_step))
    return bfield_list


def read_lockin_rmcd_data(lockin: LockInOE1022D):
    
    mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2,3,7,8],num_avgs=100,delay=0.02)
    
    R_cur_mean, R_cur_std = mean_R_chan[0], std_R_chan[0]
    dR_cur_mean, dR_cur_std = mean_dR_chan[2], std_dR_chan[2]
    
    theta_R_cur_mean, theta_R_cur_std = mean_R_chan[1], std_R_chan[1]
    theta_dR_cur_mean, theta_dR_cur_std = mean_dR_chan[3], std_dR_chan[3]

    return R_cur_mean,R_cur_std,theta_R_cur_mean,theta_R_cur_std,dR_cur_mean,dR_cur_std,theta_dR_cur_mean,theta_dR_cur_std
    


def make_rmcd_saving_file(filename,experiment):
    
    if experiment == 'bscan'   :
        header = "#B(Oe) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"
    elif experiment == 'mapping':
        header = "#X(V) Y(V) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    elif experiment == 'Esweep':
        header = "#Vb_set(V) Vb(V) Vt_set(V) Vt(V) Ib(uA) It(uA) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"
    
    if not os.path.exists(filename):
        np.savetxt(filename, [], header=header)
    else:
        print('file already exists. making a new one with add on to name')
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        np.savetxt(filename, [], header=header)
    return None


def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,file='Vb'):
    
    if file == 'Vb':
        filename_a = filename.split('.txt')
        filename = filename_a + '_VI_data_Vb'+str(int(Vb/1000))+'mV_.txt'
        header = '# Rbox (Ohm) = {Rbox}'.format(Rbox)
        header += '\n' + '# Lockin wait time (ms) = {delay}'.format(delay)
        header += '\n' + '# Vb (V) = {Vb}'.format(Vb)
        header += '\n' + '# V_sin(V) V_Gr(V) I_Gr(kA) theta(deg)'
    
    elif file == 'full':
        header = '#Vb_set(V) Vb_meas(V) Ib_meas(kA) R_Gr(kOhm) R_Gr_std(kOhm)'

    np.savetxt(filename, [], header=header)
    return filename

def E_dualgate(V_b,V_t,d_b,d_t):
    
    E = (-V_t/d_t + V_b/d_b)/2
    
    return E

def n_dualgate(V_b,V_t,d_b,d_t):
    eps_0 = cont.eps0
    eps_bn = 4
    e = cont.e.si
    n = eps_bn*eps_0 * (V_t/d_t + V_b/d_b)/e
    return n.value

    
def configure_keithley(keithley,num_points=10):
    keithley.apply_voltage(compliance_current=keithley.compliance_current)
    keithley.enable_source()
    keithley.measure_voltage()
    keithley.measure_current()
    keithley.filter_state = 'ON'
    keithley.filter_type = 'REP'
    keithley.filter_count = num_points
    keithley.config_buffer(points=num_points, delay=0)
    
    return None

def measure_V_I(keithley):
    keithley.reset_buffer()                  # Clear buffer before new measurement
    keithley.start_buffer()                  # Begin buffered measurement
    keithley.wait_for_buffer()               # Wait until buffer is full
    # Read averaged values from buffer and add to lists
    v_meas = keithley.mean_voltage
    I_meas = keithley.mean_current
    return v_meas, I_meas


def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

