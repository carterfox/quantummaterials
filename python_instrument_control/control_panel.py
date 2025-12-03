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
from experiments import SHG_polarization_scan, SHG_CD_Efield_4term, PMT_continuous_read
# from experiments import raman_basic, Gr_polarization_sensing, Gr_polarization_sensing_singlepoint
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
    time.sleep(.1)
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
    keithley_b = None #get_keithley('GPIB0::1::INSTR')
    # keithley_b.compliance_current = 100*10**(-6)
    keithley_t = get_keithley('GPIB1::16::INSTR')
    keithley_t.compliance_current = 100*10**(-6)

    pmt=get_PMT()
    servers_to_close = [pmt,qwp,keithley_t]
    # servers_to_close = [pmt,qwp]

    Ey = np.arange(-12,.1,1)
    # Ey = np.append(Ey,np.flip(Ey))
    # Ey = np.arange(-11,-12.1,-0.5)
    # Ey = np.ones(5)*(0)
    Ex=np.zeros_like(Ey)
    
    filesave = 'goingback.txt'
    # filesave = 'test.txt'
    
    try:
        res = SHG_CD_Efield_4term.main(sample, keithley_b, keithley_t, pmt, qwp,
                        qwp_angles=(qwp_C1,qwp_C2), Ex_array=Ex, Ey_array=Ey,
                        gate_time_ms=200,num_gates=40,laser_power=1.5,file_save=filesave)
        # qwp.move_to(qwp_C2)
        # pmt.set_hv(True)
        # for x in range(0,15):
        #     a = pmt.run_collection(num_gates=20)
        #     print(np.mean(a))
        # pmt.set_hv(False)
        
    except Exception: traceback.print_exc()
    finally: exit_session()