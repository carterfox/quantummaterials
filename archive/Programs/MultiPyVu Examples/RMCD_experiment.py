#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:09:25 2024

@author: carterfox

RMCD experiment 
"""


import MultiPyVu as mpv
import os 
import numpy as np
import time
import matplotlib.pyplot as plt
import pyvisa
import SSI_OE1022D

lockin = SSI_OE1022D.LockInOE1022D('ASRL12::INSTR')
opticool = mpv.Client('169.254.170.239',5000)


B_start = -1 * 10000
B_end = 1 * 10000
B_step = 0.2 * 10000
B_array = np.append(np.arange(B_start,B_end+B_step,B_step),np.arange(B_end,B_start-B_step,-1*B_step))

num_lockin_avgs = 150

R, theta_R, R_std, theta_R_std = [], [], [], []
dR, theta_dR, dR_std, theta_dR_std = [], [], [], []

R_chan,dR_chan = 1,2
lockin.set_sensitivity([0,1],["5 mV/nA","200 uV/pA"])
lockin.set_harmonic(dR_chan, "2")
lockin.autophase()

#set data reading params and all. none of this happens in the labview one so maybe not necessary


current_temp = opticool.get_temperature()
current_field = opticool.get_field()
if current_field != B_start:
    current_field = opticool.set_field(B_start, 110, opticool.field.approach_mode.linear)

for b in B_array:
    lockin.reset_buffer()
    current_field = opticool.set_field(b, 110, opticool.field.approach_mode.linear)
    opticool.wait_for(5, 0, opticool.field.waitfor)
    
    #measurement. need to figure out how to get mayn measurements. loop myself like we do in labview or have it give me x measurements right away?
    R = lockin.read_data(R_chan,["R","theta"])
    dR = lockin.read_data(dR_chan,["Rh1","thetah1"])


    