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

servers = []
### functions for getting instruments
def get_lockin(resource_name='ASRL12::INSTR', R_chan=1, dR_chan=2, num_avgs=25,sensitivities=["10 mV","100 uV"]):  
    lockin = LockInOE1022D(resource_name)
    lockin.R_chan, lockin.dR_chan = R_chan, dR_chan
    # lockin.num_avgs = num_avgs
    # lockin.delay=1
    #lockin.set_sensitivity(R_chan,sensitivities[0])
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
    
        

##run experiments here by running the file 
if __name__ == "__main__":
    
    tb.init_plot_params()
    # path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4'
    path_d4 = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d4'
    sample = DualGate(sample_name='d4', d_b=18.45, d_t=5.67, data_path=path_d4)
    #sample = DualGate(sample_name='d3', d_b=9.41, d_t=7.93, data_path=path_d3)
    sample.Rbox = 2e6
    lockin = get_lockin()
    lockin.delay=1.5
    lockin.num_avgs=100
    lockin.time_constant=100
    keithley_b = get_keithley('GPIB::1','2450')
    keithley_b.enable_source()
    keithley_b.compliance_current = 7.5e-9
    keithley_b.apply_voltage(compliance_current=keithley_b.compliance_current)
   # lockin.set_reference_frequency(1,35.50)
    # lockin.set_time_constant(1,8)
   # lockin.set_sine_output(1,.1,0,0)
    #lockin.set_sensitivity(1,'500 uV')
    # time.sleep(4)
    # Vsin_array = np.linspace(0.010,0.025,15)
    # Vb_array = np.array([0,-.1,-.2,-.3,-.4,-.5,-.6])#np.arange(0,1.4,0.2)
    # Vb_array_full = np.arange(-5.4,.2,.2)
  #  Vb_array = np.array([0,-.2,-.4,-.6,-.8,-.8,-.6,-.4,-.2,0,0,0,0,0,0,0])
    Vb_array_full = np.zeros(50)
    # Vb_array = np.concatenate((Vb_array1,Vb_array2,Vb_array3))
  #  Vb_array_full = np.concatenate((Vb_array,Vb_array[::-1]))
    # keithley_b.compliance_current = 1e-8
    try:
        # V,I,R,R_std=Gr_polarization_sensing.main(sample,lockin,keithley_b,Vb_array_full,Vsin_array,
                                                   # 'sweep12_2K_0T.txt')
        Vsin=0.1
        Vblist,Rgrlist = Gr_polarization_sensing_singlepoint.main(sample,lockin,keithley_b,Vb_array_full,Vsin,
                                                    'after-negative-timeseries.txt')
        # for x in np.flip(np.negative([0,-.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.3])):
        #     keithley_b.source_voltage = x
        #     v=keithley_b.measure_voltage_avg(10)
        #     print(v)
        #     time.sleep(.51)
    except Exception as e:
        traceback.print_exc()
    finally:
        close_all()
        print('exited safely')