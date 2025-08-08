#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 09:42:58 2025

@author: carterfox
"""


import numpy as np
import time
import matplotlib.pyplot as plt
import os
from pymeasure.instruments.keithley import Keithley2400, Keithley2450

def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,):
    #function for making a file to save Gr resistance measurement data, from which the linear curve will be fit
    
    header = '# Rbox (Ohm) = {Rbox}'.format(Rbox)
    header += '\n' + '# Lockin wait time (ms) = {delay}'.format(delay)
    header += '\n' + '# Vb (V) = {Vb}'.format(Vb)
    header += '\n' + '# Vref(V) Vbox(V) Ibox(uA) Rdev(Ohm) theta(deg)'
    
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


def Gr_resistance_Vb_sweep(lockin,keithley,Rbox,Vb_array,Vsin_min,Vsin_max,Vsin_step):
    
    configure_keithley()
    
    Vb_meas_list, Ib_meas_list = [],[]
    
    Vsin_list = np.ararnge(Vsin_min,Vsin_max+Vsin_step,Vsin_step)

    for Vb in Vb_array: # sweep Vb 
        
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
            R_std = std_R_chan[0]
            theta_mean = std_R_chan[1]
            
            Vbox = Vsin - V_Gr
            I_Gr = Vbox/Rbox * 10**9
                        
            I_Gr_list.append(I_Gr)
            Vbox_list.append(Vbox)
            V_Gr_list.append(V_Gr)
            theta_list.append(theta)
    
    return None
    
    
