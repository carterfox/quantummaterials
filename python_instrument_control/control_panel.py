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
import QDopticool
import RMCD
from pymeasure.instruments.keithley import Keithley2400,Keithley2450
from pymeasure.instruments.attocube import ANC300Controller
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import MultiPyVu as mpv

servers = []
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
    servers.append(lockin)
    return lockin

def get_opticool(opticool_ip='169.254.170.239', port=5000):
    opticool = QDopticool.Opticool(opticool_ip,port)
    current_temp = opticool.get_temperature()
    current_field = opticool.get_field()
    servers.append(opticool)
    return opticool, current_temp, current_field

def get_kiethley2450(resource_name="GPIB0::1::INSTR"):
    keithley2450 = Keithley2450(resource_name)
    servers.append(keithley2450)
    return keithley2450 

def get_kiethley2400(resource_name="GPIB0::16::INSTR"):
    keithley2400 = Keithley2400(resource_name)
    servers.append(keithley2400)
    return keithley2400

def get_ANC300(resource_name='ASRL11'):
    ANC = ANC300(name='ANC300',address=resource_name)
    servers.append(ANC)
    return ANC

def close_all():
    for server in servers:
        server.close()



##run experiments here by running the file 
if __name__ == "__main__":
    
    sample = 'dualgate-s1'
    data_saving_path = ''

    
    # """
    lockin = get_lockin()
    opticool, current_temp, current_field = get_opticool()
    ANC = get_ANC300()
    # bfield_array = RMCD.make_bfield_list(-1, 1, 0.1)
    # rmcd_scan_data = RMCD.RMCD_bfield_scan(lockin, opticool,bfield_array)
    close_all()
    # """

    



    


