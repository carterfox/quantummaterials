#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 12:32:27 2025

@author: carterfox
"""

# import MultiPyVu as mpv
import numpy as np
import matplotlib.pyplot as plt
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb
import traceback
import logging
import time
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
from homemade_servers.SSI_OE1022D import LockInOE1022D
from homemade_servers.QDopticool import Opticool
from homemade_servers.H11890PMT import HamamatsuH11890
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from devices.dualgate import DualGate
from experiments import RMCD_bfield_scan, RMCD_mapping, RMCD_dualgate_Esweep
from experiments import PMT_continuous_read, Gr_polarization_sensing, Gr_polarization_sensing_singlepoint
tb.init_plot_params()
servers = []
labdata = 'D:/LabData/XiaoWang_Group_data_2024on/'
### functions for getting instruments
def get_lockin(resource_name='ASRL12::INSTR', R_chan=1, dR_chan=2, num_avgs=25,delay=1):  
    lockin = LockInOE1022D(resource_name)
    lockin.R_chan, lockin.dR_chan = R_chan, dR_chan
    lockin.num_avgs = num_avgs
    lockin.delay=delay
    # lockin.set_sensitivity(R_chan,sensitivities[0])
   # lockin.set_sensitivity(dR_chan,sensitivities[1])
    servers.append(lockin)
    return lockin

def get_opticool(opticool_ip='169.254.170.239', port=5000):
    opticool = Opticool(opticool_ip,port)
    current_temp = opticool.get_temperature()
    current_field = opticool.get_field()
    servers.append(opticool)
    return opticool, current_temp, current_field

def get_keithley(resource_name="GPIB0::16::INSTR",model='2450'):
    keithley = KeithleySourceMeter(resource_name,model)
    # keithley.compliance_current = 10**(-6)
    servers.append(keithley)
    return keithley

def get_ANC300(resource_name='ASRL11'):
    ANC = ANC300(name='ANC300',address=resource_name)
    servers.append(ANC)
    return ANC

def get_PMT():
    PMT = HamamatsuH11890()
    servers.append(PMT)
    return PMT

def close_all():
    for server in servers:
        server.close()
    servers.clear
    print('exited all servers safely')
    
        

##run experiments here by running the file 
if __name__ == "__main__":
    
    open_servers = True #can be changed to False after servers have been opened
    if open_servers:
        lockin = get_lockin(delay=1.5,num_avgs=50)
        keithley_b = get_keithley('GPIB::1','2450')
    leave_servers_open = True
    
    sample = DualGate(sample_name='d3', d_b=9.41, d_t=7.93, data_path=labdata+'StackingTransitions/CrI3/round7/d3')
    sample.Rbox = 2e6
    keithley_b.compliance_current = 6e-9
    keithley_b.apply_voltage(compliance_current=keithley_b.compliance_current)
    Vb_array = np.arange(-6.2,7,.02)
    Vb_full = np.concatenate((Vb_array,Vb_array[::-1]))
    try:
        
        Vblist,Rgrlist = Gr_polarization_sensing_singlepoint.main(sample,lockin,keithley_b, 
                          Vb_full,Vsin=0.1,file_save="slow-scan3_295K_8-25.txt")
        
        
    except Exception as e: traceback.print_exc()
    finally:
        if leave_servers_open: print('experiment done. servers left open')
        else: close_all()
        
        
        
        
        
        
        
        
        
        
        
        
        


