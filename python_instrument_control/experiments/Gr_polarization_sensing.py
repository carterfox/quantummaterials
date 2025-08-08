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
from homemade_servers.SSI_OE1022D import LockInOE1022D
    

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


def Gr_resistance_Vb_sweep(lockin: LockInOE1022D,keithley: Keithley2450,Rbox,Vb_array,Vsin_min,Vsin_max,Vsin_step,file_save):
    
    file_full = make_Gr_resistance_saving_file(file_save,Rbox,lockin.delay,lockin.sin_freq,0,file='full')
    
    configure_keithley()
    Vsin_list = np.ararnge(Vsin_min,Vsin_max+Vsin_step,Vsin_step)

    for Vb in Vb_array: # sweep Vb 
    
        file_Vb = make_Gr_resistance_saving_file(file_save,Rbox,lockin.delay,lockin.sin_freq,Vb,file='Vb') # make file for this Vb
        keithley.source_voltage = Vb             # Set output voltage
        time.sleep(0.3)                          # Allow output and DUT to settle
        v_meas, I_meas = measure_V_I(keithley)
        
        Vsin = 0
        I_Gr_list, V_Gr_list = [],[]
        
        for Vsin in Vsin_list: # sweep Vsin and measure Vgr,Igr to determine Rgr at that Vb
            
            lockin.set_sine_output(channel=lockin.R_chan,amplitude=Vsin)
            time.sleep(lockin.delay)
            
            mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs, delay=lockin.delay)
            
            V_Gr, theta = mean_R_chan[0], mean_R_chan[1]
            
            Vbox = Vsin - V_Gr
            I_Gr = Vbox/Rbox * 10**3  #kA
                        
            I_Gr_list.append(I_Gr)
            V_Gr_list.append(V_Gr)
            
            np.savetxt(file_Vb, [Vsin,V_Gr,I_Gr,theta], fmt="%.9f", mode='a')
            
        p,c = curve_fit(hf.line, I_Gr_list, V_Gr_list,p0=[1,0])  # fit for Gr resistance and save to file
        R_Gr,  R_Gr_std = p[0], np.sqrt(np.diag(c))[0]
        
        np.savetxt(file_full, [Vb,v_meas,I_meas,R_Gr,R_Gr_std], fmt="%.9f", mode='a')
        
    
    return None
    
    
