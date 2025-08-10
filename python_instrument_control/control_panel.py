#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 12:32:27 2025

@author: carterfox
"""

# import MultiPyVu as mpv
import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.SSI_OE1022D import LockInOE1022D
from homemade_servers.QDopticool import Opticool
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from devices.dualgate import DualGate
import RMCD
import Gr_polarization_sensing
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


servers = []
### functions for getting instruments
def get_lockin(resource_name='ASRL12::INSTR', R_chan=1, dR_chan=2, num_avgs=25,sensitivities=["10 mV","1 mV"]):  
    lockin = LockInOE1022D(resource_name)
    lockin.R_chan, lockin.dR_chan = R_chan, dR_chan
    lockin.num_avgs = num_avgs
    lockin.delay=1
    lockin.set_sensitivity(R_chan,sensitivities[0])
    lockin.set_sensitivity(dR_chan,sensitivities[1])
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
    keithley.compliance_current = 10**(-6)
    servers.append(keithley)
    return keithley

def get_ANC300(resource_name='ASRL11'):
    ANC = ANC300(name='ANC300',address=resource_name)
    servers.append(ANC)
    return ANC

def close_all():
    for server in servers:
        server.close()
        

##run experiments here by running the file 
if __name__ == "__main__":
    
    tb.init_plot_params()
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4'
    # sample = DualGate(sample_name='d4', d_b=18.45, d_t=5.67, data_path=path_d4)
    
    path_s6 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/6-18-sample-for-afm-and-rmcd/'
    sample = DualGate(sample_name='s6', d_b=0, d_t=0, data_path=path_s6)
    
    lockin = get_lockin()
    lockin.delay=1
    lockin.num_avgs=100
    opticool, current_temp, current_field = get_opticool()
    ANC = get_ANC300()
    try:
        bfield_array = tb.make_bfield_list(-22000, 22000, 500)
        rmcd_scan_data = RMCD.RMCD_bfield_scan(sample, lockin,opticool,bfield_array,
                                               'fourlayer-scan1.txt')
    
        
        # RMCD.RMCD_mapping(sample, lockin, ANC, x_start=0, x_end=60, points=61, 
                          # file_save='map1_m2p2T.txt')
    
    except Exception as e:
        print(e)
    finally:
        close_all()
    



    


