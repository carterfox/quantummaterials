#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 12:32:27 2025

@author: carterfox
"""

# import MultiPyVu as mpv
import numpy as np
import matplotlib.pyplot as plt
# from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb
import traceback
import logging
import pyvisa
import time
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
# from homemade_servers.SSI_OE1022D import LockInOE1022D
# from homemade_servers.QDopticool import Opticool
from homemade_servers.H11890PMT import HamamatsuH11890
# from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.ThorlabsKCube import RotationMount
# from devices.dualgate import DualGate
# from devices.optical import Optical
from devices.transport import FourTerminal
# from experiments import RMCD_bfield_scan, RMCD_mapping, RMCD_dualgate_Esweep
from experiments import raman_basic, SHG_polarization_scan, SHG_CD_Efield_4term
# from experiments import PMT_continuous_read, Gr_polarization_sensing, Gr_polarization_sensing_singlepoint
tb.init_plot_params()
if 'servers' not in globals(): 
    global servers
    servers = []
labdata = 'D:/LabData/XiaoWang_Group_data_2024on/'

def get_lockin(resource_name='ASRL15::INSTR', R_chan=1, dR_chan=2, num_avgs=25,delay=1):  
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


def get_rotation_stage(serial):
    rot = RotationMount(serial)
    servers.append(rot)
    return rot 

def get_keithley(resource_name="GPIB0::16::INSTR",model='2450'):
    keithley = KeithleySourceMeter(resource_name,model)
    # keithley.compliance_current = 10**(-6)
    servers.append(keithley)
    return keithley

def get_ANC300(resource_name='ASRL11'):
    ANC = ANC300(name='ANC300',address=resource_name)
    servers.append(ANC)
    return ANC

def get_AndorCamSpec(temperature=-85):
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
    for s in servers_to_close:
        s.close()
        
    
def list_visa_resources():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(resources)
    print('lockin usually 12 or 3')


if __name__ == "__main__":
    
    ###### add it to servers_to_close if you want them to close each time. 
    ###### at this point only cam_spec should not be in it
    data_path="I:/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/NbOI2/Lvgroup/Efield-samples-for-optics/90deg_3L3L_4term_S1"
    sample = FourTerminal('4termNbOI290degS1', 5, data_path)
    qwp = get_rotation_stage('27261255')
    qwp.home = 0
    qwp_C1 = 43.5 ##
    qwp_C2 = -46.5
    keithley_b = get_keithley('GPIB0::1::INSTR')
    keithley_t = get_keithley('GPIB1::16::INSTR')
    pmt=None
    #cam_spec = get_AndorCamSpec()
    servers_to_close = [qwp,keithley_b,keithley_t]
    ######
    #initial_pos = waveplate.get_pos()
    #if initial_pos != 0:
    #    waveplate.move_to(initial_pos)
    angles = np.arange(0, 91, 2.5)
    Ex=np.array([0,1,2])
    Ey=np.array([0,2,3])
    
    try:
        SHG_CD_Efield_4term.main(sample, keithley_b, keithley_t, pmt, qwp, 
                                 qwp_angles=(qwp_C1,qwp_C2), Ex_array=Ex, Ey_array=Ey)
        # all_data, summed_spectra_data = raman_basic.angle_sweep(cam_spec, waveplate, exposure_time=300, averages=3, angles=angles)
        # print(all_data)
        print('')
        
    except Exception: traceback.print_exc()
    finally: exit_session()