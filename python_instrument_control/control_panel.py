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
import pyvisa
import time
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logging.getLogger('matplotlib').setLevel(logging.WARNING)
from homemade_servers.SSI_OE1022D import LockInOE1022D
# from homemade_servers.QDopticool import Opticool
# from homemade_servers.H11890PMT import HamamatsuH11890
# from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
# from homemade_servers.ThorlabsKCube import RotationMount
from devices.dualgate import DualGate, DualGate_MLGsense
# from devices.optical import Optical
# from devices.transport import FourTerminal
# from experiments import RMCD_bfield_scan, RMCD_mapping, RMCD_dualgate_Esweep
# from experiments import SHG_CD_Efield_4term
# from experiments import PMT_continuous_read, SHG_polarization_scan, 
from experiments import Gr_polarization_sensing, Gr_polarization_sensing_singlepoint
# from experiments import raman_basic

tb.init_plot_params()
if 'servers' not in globals(): 
    global servers
    servers = []
labdata = 'D:/LabData/XiaoWang_Group_data_2024on/'

def get_lockin(resource_name='ASRL9::INSTR', R_chan=1, dR_chan=2, num_avgs=25,delay=1):  
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
    return opticool


def get_rotation_stage(serial,home=0):
    rot = RotationMount(serial)
    servers.append(rot)
    rot.home=home
    return rot 

def get_keithley(resource_name="GPIB0::16::INSTR",model='2450',compliance_current=None):
    keithley = KeithleySourceMeter(resource_name,model)
    if compliance_current != None:
        keithley.compliance_current = compliance_current
    servers.append(keithley)
    return keithley

def get_ANC300(resource_name='ASRL11'):
    ANC = ANC300(name='ANC300',address=resource_name)
    servers.append(ANC)
    return ANC

def get_AndorCamSpec(temperature=-80):
    andor = AndorCamSpec(temperature=temperature)
    servers.append(andor)
    return andor

def get_PMT():
    PMT = HamamatsuH11890()
    servers.append(PMT)
    return PMT

# def close_all():
#     for server in servers:
#         server.close()
#     servers.clear()
#     print('exited all servers safely')
    
def exit_session():
    time.sleep(.1)
    for s in servers_to_close:
        if s != None:
            s.close()
        
    
def list_visa_resources():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(resources)
    print('lockin usually 12 or 3')
    
def loop(start,stop,step):
    array = np.arange(start,stop+step/10,step)
    return np.round(np.append(array,np.flip(array)),4)
def ramp(start,stop,step):
    array = np.arange(start,stop+step/10,step)
    return np.round(array,4)


if __name__ == "__main__":
    ###### add it to servers_to_close if you want them to close each time. 
    ###### at this point only cam_spec should not be in it
    base = "G:/Other computers/My Computer/XiaoWang_Group_data_2024on/StackingTransitions/option4-chip1/twoterm_Rgr_V1V3/"
    sample = DualGate_MLGsense(sample_name='option4_chip1', d_b=31, d_m=0,d_t=0, d_flake=0, data_path=base)
    # sample = DualGate_MLGsense(sample_name='option1_BM', d_b=28, d_m=0,d_t=0, d_flake=0, data_path=base)
    lockin = get_lockin(resource_name='ASRL5::INSTR',num_avgs=50,delay=3)
    sample.Vsin = .1
    sample.Rbox=1e6
    sample.temperature=295
    keithley_b = get_keithley('GPIB0::16::INSTR','2400',compliance_current=None)
    keithley_b.compliance_current=1e-6
    servers_to_close = [lockin,keithley_b]
    # keithley_b.enable_source()
    # keithley_b.compliance_current=5e-8
    
    try:        
        filesave = 'goingback.txt'
        # filesave = 'loop2.txt'
        Eb_array = np.arange(0,-.21,-.01)
        # Eb_array = np.array([0,0])
        # a = np.arange(-.2,.2025,.0025) 
        # b = np.arange(.2,-.0025,-.0025)
        # Eb_array = np.concatenate((a, b))
        Vb_array = Eb_array*(sample.d_b+sample.d_m+sample.d_flake)
        # Vb_array = np.append(Vb_array,np.flip(Vb_array))
        Gr_polarization_sensing_singlepoint.main(sample, lockin, keithley_b,Vb_array,filesave)
            
        
    except Exception: traceback.print_exc()
    finally: exit_session()
    
    
