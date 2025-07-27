#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:52:53 2024

@author: carterfox

sweep bottom gate voltage and measure top Gr resistance
"""


import numpy as np
import os
from pymeasure.instruments.keithley import Keithley2400,Keithley2450
from time import sleep 
import time

keithley2450 = Keithley2450("GPIB0::1::INSTR") # bottom gate
keithley2400 = Keithley2400("GPIB1::16::INSTR") # top Gr
keithley2400.use_front_terminals()
keithley2450.use_front_terminals()
keithley2450.compliance_current = 1e-5
keithley2400.compliance_current = 1e-5
keithley2400.compliance_voltage = 10 #V
max_resistance=210e6

Vb_start = -.1 #V
Vb_end = .1
Vb_stepsize = .2
loop = True
Vb_array = np.arange(Vb_start,Vb_end+Vb_stepsize,Vb_stepsize)
loop = False
if loop:
    Vb_array = np.append(Vb_array,np.arange(Vb_end,Vb_start-Vb_stepsize,-Vb_stepsize))
num_Vb_meas_averages = 10

Vt_start = 0 #V
Vt_end = .2
Vt_numsteps = 20
Vt_array = np.append(np.linspace(Vt_start,Vt_end,Vt_numsteps),np.linspace(Vt_end,Vt_start,Vt_numsteps))
num_VI_loops = 2
for x in range(0,num_VI_loops-1):
    Vt_array = np.append(Vt_array,Vt_array)
num_It_meas_averages = 10

Vb_meas_list, Ib_meas_list, Vb_meas_std_list, Ib_meas_std_list = [], [], [], []
It_meas_full_list, It_meas_std_full_list = [], []
Vt_full_list = []

keithley2400.enable_source()

for Vb in Vb_array:
    #configure Vb for voltage output and voltage,current measurements
    keithley2450.apply_voltage(compliance_current=keithley2450.compliance_current)
    keithley2450.measure_current()
    sleep(0.1)
    #apply the voltage and collect the data
    keithley2450.enable_source()
    keithley2450.source_voltage = Vb
    Ib_meas = keithley2450.current
    keithley2450.measure_voltage()
    sleep(0.1)
    Vb_meas = keithley2450.voltage
    Vb_meas_list.append(Vb_meas)
    Ib_meas_list.append(Ib_meas)
    
    It_meas_list, It_meas_std_list = [], []
    Vt_list = []
    
    # keithley2400.reset()
    keithley2400.apply_current(compliance_voltage=keithley2400.compliance_voltage)
    keithley2400.measure_current(nplc=.1)
    print(time.time())
    for Vt in Vt_array:

        keithley2400.config_buffer(num_It_meas_averages)

        keithley2400.source_voltage = Vt

        keithley2400.start_buffer()
        keithley2400.wait_for_buffer()

        Vt_list.append(Vt)
        It_meas = keithley2400.mean_current 
        # It_meas_std = keithley2400.std_current
        It_meas_list.append(It_meas)
        keithley2400.disable_buffer()
        # It_meas_std_list.append(It_meas_std)
    print(time.time())
    It_meas_full_list.append(It_meas_list)
    Vt_full_list.append(Vt_list)
    # It_meas_std_full_list.append(It_meas_std_list)



#example


