#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 09:42:58 2025

@author: carterfox
"""


import numpy as np
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
from pymeasure.instruments.keithley import Keithley2400, Keithley2450
import helper_function_library as hf

def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,file='Vb'):
    
    if file == 'Vb':
        #function for making a file to save Gr resistance measurement data, from which the linear curve will be fit
        filename_a = filename.split('.txt')
        filename = filename_a + '_VI_data_Vb'+str(int(Vb/1000))+'mV_.txt'
        header = '# Rbox (Ohm) = {Rbox}'.format(Rbox)
        header += '\n' + '# Lockin wait time (ms) = {delay}'.format(delay)
        header += '\n' + '# Vb (V) = {Vb}'.format(Vb)
        header += '\n' + '# Vref(V) Vbox(V) Ibox(uA) Rdev(Ohm) theta(deg)'
    
    elif file == 'full':
        #file save for full sweep
        header = '#Vb_set(V) Vb_meas(V) R_Gr(kOhm) Ib(kA)'

    np.savetxt(filename, [], header=header)
    return None


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


def Gr_resistance_Vb_sweep(lockin,keithley,Rbox,Vb_array,Vsin_min,Vsin_max,Vsin_step,file_save):
    
    make_Gr_resistance_saving_file(file_save,Rbox,lockin.delay,lockin.sin_freq,0,file='full')
    
    configure_keithley()
    
    Vb_meas_list, Ib_meas_list = [],[]
    R_Gr_list, R_Gr_std_list = [],[]
    
    Vsin_list = np.ararnge(Vsin_min,Vsin_max+Vsin_step,Vsin_step)

    for Vb in Vb_array: # sweep Vb 
    
        make_Gr_resistance_saving_file(file_save,Rbox,lockin.delay,lockin.sin_freq,Vb,file='full')
            
        keithley.source_voltage = Vb             # Set output voltage
        time.sleep(0.3)                          # Allow output and DUT to settle
        keithley.reset_buffer()                  # Clear buffer before new measurement
        keithley.start_buffer()                  # Begin buffered measurement
        keithley.wait_for_buffer()               # Wait until buffer is full
    
        # Read averaged values from buffer and add to lists
        v_meas = keithley.mean_voltage
        I_meas = keithley.mean_current
        Vb_meas_list.append(v_meas)
        Ib_meas_list.append(I_meas)
        
        Vsin = 0
        
        I_Gr_list, Vbox_list, V_Gr_list, theta_list = [],[],[],[]
        
        for Vsin in Vsin_list: # sweep Vsin and measure Vgr,Igr to determine Rgr at that Vb
            
            #set sin out 
            time.sleep(lockin.delay)
            
            mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs, delay=lockin.delay)
            
            V_Gr = mean_R_chan[0]
            theta = mean_R_chan[1]
            
            Vbox = Vsin - V_Gr
            I_Gr = Vbox/Rbox * 10**3  #kA
                        
            I_Gr_list.append(I_Gr)
            Vbox_list.append(Vbox)
            V_Gr_list.append(V_Gr)
            theta_list.append(theta)
            
        p,c = curve_fit(hf.line, I_Gr_list, V_Gr_list,p0=[1200,0])
        R_Gr = p[0]
        R_Gr_std = np.sqrt(np.diag(c))[0]
        
        R_Gr_list.append(R_Gr)
        R_Gr_std_list.append(R_Gr_std)
    
    return None
    
    
