#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 12:32:27 2025

@author: carterfox
"""

# import MultiPyVu as mpv
import numpy as np
import time
import matplotlib.pyplot as plt
import SSI_OE1022D
import RMCD
from pymeasure.instruments.keithley import Keithley2400,Keithley2450
from pymeasure.instruments.attocube import ANC300Controller


### functions for getting instruments
def get_lockin(resource_name='ASRL12::INSTR', R_chan=1, dR_chan=2, num_avgs=150,sensitivities=["5 mV","200 uV"]):  
    lockin = SSI_OE1022D.LockInOE1022D(resource_name)
    lockin.R_chan = R_chan
    lockin.dR_chan = dR_chan
    lockin.num_avgs = num_avgs
    lockin.set_sensitivity(R_chan,sensitivities[0])
    lockin.set_sensitivity(dR_chan,sensitivities[1])
    lockin.set_harmonic(dR_chan, 1, 2)
    lockin.auto_phase_all()
    return lockin

def get_opticool(opticool_ip='169.254.170.239', port=5000):
    import MultiPyVu as mpv
    opticool = mpv.Client(opticool_ip,port)
    current_temp = opticool.get_temperature()
    current_field = opticool.get_field()
    return opticool, current_temp, current_field


def get_kiethley2450(resource_name="GPIB0::1::INSTR"):
    keithley2450 = Keithley2450(resource_name)
    return keithley2450 

def get_kiethley2400(resource_name="GPIB0::16::INSTR"):
    keithley2400 = Keithley2400(resource_name)
    return keithley2400


def get_anc300(resource_name='ASRL12::INSTR'):
    anc300 = ANC300Controller(resource_name, axisnames=['scanx', 'scany','stepperx','steppery'])
    return anc300



### functions for running experiments

def RMCD_experiment(b_start,b_end,b_step):
    
    lockin = get_lockin()
    opticool, current_temp, current_field = get_opticool()
    bfield_array = RMCD.make_bfield_list(b_start, b_end, b_step)
    
    rmcd_scan_data = RMCD.RMCD_bfield_scan(lockin, opticool,bfield_array)
    
    return rmcd_scan_data


##run experiments here by running the file 
if __name__ == "__main__":
    
    sample = 'dualgate-s1'
    # lockin = get_lockin()
    # lockin.close()
    # data_saving_path = ''

    # rmcd_scan_data = RMCD_experiment(-1,1,0.1)
    
    #save data...
    


