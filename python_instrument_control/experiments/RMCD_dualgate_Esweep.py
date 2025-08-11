#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:09:25 2024

@author: carterfox

RMCD experiment 
"""
from typing import Union
import numpy as np
import logging
import time
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from homemade_servers.QDopticool import Opticool
from devices.dualgate import DualGate
from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300
import toolbelt as tb
from tqdm import tqdm


def RMCD_dualgate_pure_Efield_sweep(sample: DualGate, lockin: LockInOE1022D,
                                    keithley_b: KeithleySourceMeter, keithley_t: KeithleySourceMeter,
                                    E_array,file_save):
    
    """
    Perform a pure out-of-plane electric field sweep using a dual-gated sample
    and record RMCD data at each field point.

    Parameters
    ----------
    sample : DualGate
        Sample object containing geometry and file path info, including gate thicknesses.
    lockin : LockInOE1022D
        Lock-in amplifier used to collect RMCD signals.
    keithley_b : KeithleySourceMeter
        Source meter connected to the bottom gate.
    keithley_t : KeithleySourceMeter
        Source meter connected to the top gate.
    E_array : array-like
        List or array of electric field values (in V/nm) to apply.
    file_save : str
        Filename for saving the sweep data.

    Returns
    -------
    None
    """
    
    saving_file = sample.data_path+'/RMCD/Esweep/'+file_save    
    tb.make_rmcd_saving_file(saving_file,'Esweep')
    
    tb.init_plot_params()
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel('E (V/nm)')
    ax.set_ylabel('RMCD %')
    
    tb.configure_keithley(keithley_b)
    tb.configure_keithley(keithley_t)
    
    rmcd_list = []
    d_b = sample.d_b
    d_t = sample.d_t
    
    for E in E_array:
        
        V_b = E*d_b
        V_t = -V_b*d_t/d_b
        
        keithley_b.source_voltage = V_b             # Set output voltage
        keithley_t.source_voltage = V_t             # Set output voltage
        time.sleep(0.3)                          # Allow output and DUT to settle
        Vb_meas, Ib_meas = tb.measure_V_I(keithley_b)
        Vt_meas, It_meas = tb.measure_V_I(keithley_t)
        elec_data = [V_b,Vb_meas,V_t,Vt_meas,Ib_meas,It_meas]
        
        lockin.sleep(lockin.delay)
        lockin.reset_buffer()
        rmcd_data = tb.read_lockin_rmcd_data(lockin)
        rmcd_list.append(rmcd_data[4]/rmcd_data[0]*100)
        
        data_row = elec_data + rmcd_data
        np.savetxt(saving_file, data_row, fmt="%.9f", mode='a')
        
        ax.plot(E_array[0:len(rmcd_list)],rmcd_list)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    plt.ioff()
    plt.show()
    
    return None


if __name__ == "__main__":
    # 
    print('test')