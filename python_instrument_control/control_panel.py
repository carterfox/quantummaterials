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
from experiments import PMT_continuous_read, Gr_polarization_sensing

servers = []
### functions for getting instruments
def get_lockin(resource_name='ASRL12::INSTR', R_chan=1, dR_chan=2, num_avgs=25,sensitivities=["10 mV","100 uV"]):  
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
    
        

##run experiments here by running the file 
if __name__ == "__main__":
    
    tb.init_plot_params()
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4'
    path_d3 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3'
    # sample = DualGate(sample_name='d4', d_b=18.45, d_t=5.67, data_path=path_d4)
    sample = DualGate(sample_name='d3', d_b=9.41, d_t=7.93, data_path=path_d3)
    
    lockin = get_lockin()
    lockin.set_sensitivity(lockin.R_chan,"50 uV")
    lockin.delay=3
    lockin.num_avgs=100
    lockin.sine_out_freq=1000
    sample.Rbox = 2e6
    # opticool, current_temp, current_field = get_opticool()
    # ANC = get_ANC300()
    # PMT = get_PMT()
    keithley_b = get_keithley('GPIB::1','2450')
    
    Vsin_array = np.linspace(0.001,0.012,5)
    
    Vb_array = np.array([0,.1])
    # Vb_array = np.arange(0,3,.2)
   # Vb_array_full = np.concatenate((Vb_array,Vb_array[::-1]))
    keithley_b.compliance_current = 1e-8
    try:
        # rmcd_scan_data = RMCD_bfield_scan.main(sample,lockin,opticool,bfield_array,
        #                                         'bilayer_scan_p5-nogates.txt')
    
        # E,rmcd =RMCD_dualgate_Esweep.main(sample,lockin,keithley_b,
        #                                     E_back,'back.txt')
        
        V,I,R,R_std=Gr_polarization_sensing.main(sample,lockin,keithley_b,Vb_array,Vsin_array,'testmpl6.txt')
        
        
        
    except Exception as e:
        traceback.print_exc()
    finally:
        close_all()
        print('exited safely')
    



    


