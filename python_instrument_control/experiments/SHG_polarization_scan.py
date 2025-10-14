#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 13:55:45 2025
SHG polarization scanning
@author: carterfox

experiment file for measuring SHG while rotating HWPs in the incident and/or detection path

"""

from typing import Union
import numpy as np
import logging
import time
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import toolbelt as tb
from tqdm import tqdm
from homemade_servers.H11890PMT import HamamatsuH11890
from homemade_servers.ThorlabsKCube import RotationMount

def main(sample, pmt: HamamatsuH11890, exc_hwp: RotationMount, det_hwp: RotationMount, exc_angles, det_angles, gate_time_ms, num_gates, file_save):
    
    update_rotation_stages(exc_hwp,det_hwp,exc_angles[0],det_angles[0])  #move rotation stages to starting positions
    
    
    ### turn on PMT high voltage
    pmt.set_hv(on=True)
    time.sleep(.5)
    
    means, std_errs, full_data = [], [], []
    
    for exc_ang,det_ang in zip(exc_angles,det_angles):
        
        update_rotation_stages(exc_hwp,det_hwp,exc_ang,det_ang)
        
        data = pmt.run_collection(gate_time_ms,num_gates,remove_first=True)
        means.append(np.mean(data))
        std_errs.append(np.std(data)/np.sqrt(num_gates))
        full_data.append(data)
    
    
    
    pmt.set_hv(on=False)
    
    return 0







def update_rotation_stages(exc_hwp: RotationMount, det_hwp: RotationMount,exc_angle,det_angle):
    if exc_hwp != None:
        exc_hwp.move_to(exc_angle)
    if det_hwp != None:
        det_hwp.move_to(det_angle)
    return None
    
    
    
    
    
    
    
    
    
    
    
    
    