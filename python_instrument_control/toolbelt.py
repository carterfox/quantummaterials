#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 21:25:45 2025

@author: carterfox
"""

from matplotlib_scalebar.scalebar import ScaleBar; import matplotlib.patches as mpatches
import numpy as np
import os
import time
import logging
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib as mpl
from pymeasure.instruments.keithley import Keithley2400, Keithley2450
from homemade_servers.SSI_OE1022D import LockInOE1022D
from typing import Union
import astropy.constants as cont
import astropy.units as uu

def make_bfield_list(b_start,b_end,b_step):
    bfield_list = np.append(np.arange(b_start,b_end,b_step),np.arange(b_end,b_start-b_step,-1*b_step))
    return bfield_list

def read_lockin_rmcd_data(lockin: LockInOE1022D):
    
    mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2,3,7,8],num_avgs=lockin.num_avgs,delay=0.02)
    
    R_cur_mean, R_cur_std = mean_R_chan[0], std_R_chan[0]
    dR_cur_mean, dR_cur_std = mean_dR_chan[2], std_dR_chan[2]
    
    theta_R_cur_mean, theta_R_cur_std = mean_R_chan[1], std_R_chan[1]
    theta_dR_cur_mean, theta_dR_cur_std = mean_dR_chan[3], std_dR_chan[3]

    return [R_cur_mean,R_cur_std,theta_R_cur_mean,theta_R_cur_std,dR_cur_mean,dR_cur_std,theta_dR_cur_mean,theta_dR_cur_std]
    


def make_rmcd_saving_file(filename,experiment):
    
    if experiment == 'bscan':
        header = "#B(Oe) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"
    elif experiment == 'mapping':
        header = "#X(V) Y(V) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    elif experiment == 'Esweep':
        header = "#Vb_set(V) Vb(V) Vt_set(V) Vt(V) Ib(uA) It(uA) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"

    if not os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write(header + '\n') 
    else:
        print('file already exists. making a new one with add on to name')
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        with open(filename, 'a') as file:
            file.write(header + '\n') 
    return filename

def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,file='Vb'):
    
    if file == 'Vb':
        filename_a = filename.split('.txt')
        filename = filename_a + '_VI_data_Vb'+str(int(Vb/1000))+'mV_.txt'
        header = '# Rbox (Ohm) = {}'.format(Rbox)
        header += '\n' + '# Lockin wait time (ms) = {}'.format(delay)
        header += '\n' + '# Vb (V) = {}'.format(Vb)
        header += '\n' + '# V_sin(V) V_Gr(V) I_Gr(kA) theta(deg)'
    
    elif file == 'full':
        header = '#Vb_set(V) Vb_meas(V) Ib_meas(kA) R_Gr(kOhm) R_Gr_std(kOhm)'

    np.savetxt(filename, [], header=header)
    return filename

def E_dualgate(V_b,V_t,d_b,d_t):
    
    E = (-V_t/d_t + V_b/d_b)/2
    
    return E

def n_dualgate(V_b,V_t,d_b,d_t):
    eps_0 = cont.eps0
    eps_bn = 4
    e = cont.e.si
    n = eps_bn*eps_0 * (V_t/d_t + V_b/d_b)/e
    return n.value

    
def configure_keithley(keithley,num_points=10):
    keithley.apply_voltage(compliance_current=keithley.compliance_current)
    keithley.enable_source()
    keithley.measure_voltage()
    keithley.measure_current()
    keithley.filter_state = 'ON'
    keithley.filter_type = 'REP'
    keithley.filter_count = num_points
    keithley.config_buffer(points=num_points, delay=0)
    
    return None

def measure_V_I(keithley):
    keithley.reset_buffer()                  # Clear buffer before new measurement
    keithley.start_buffer()                  # Begin buffered measurement
    keithley.wait_for_buffer()               # Wait until buffer is full
    # Read averaged values from buffer and add to lists
    v_meas = keithley.mean_voltage
    I_meas = keithley.mean_current
    return v_meas, I_meas


def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b


def init_plot_params():
    mpl.rcParams.update(mpl.rcParamsDefault)
    fontsize = 18
    plt.rcParams["lines.marker"] = '.'
    plt.rcParams["lines.linewidth"] = 2
    plt.rcParams["axes.labelpad"] = 4
    plt.rcParams["font.size"] = fontsize
    plt.rcParams["lines.markersize"] = 10
    plt.rcParams["figure.figsize"] = [6,4]
    plt.rcParams["savefig.dpi"] = 500
    plt.rcParams["savefig.format"] = "png"  # "svg"
    plt.rcParams["image.cmap"] = "magma"
    plt.rcParams["figure.constrained_layout.use"] = True
    plt.rcParams["legend.fontsize"] = 0.7 * fontsize
    plt.rcParams["legend.handlelength"] = 0.9
    plt.rcParams["legend.handletextpad"] = 0.5
    plt.rcParams["xtick.direction"] = 'in'
    plt.rcParams["ytick.direction"] = 'in'
    plt.rcParams["savefig.bbox"] = "tight"
    # plt.rcParams['text.usetex'] = True
    # plt.rcParams['text.latex.preamble'] =r"\usepackage{xcolor} "
    # plt.rcParams.update({
    # "text.usetex": True,
    # "font.family": "Helvetica"})
    
def plot_arrow_legend(ax,label,x1=None,y1=None,ls=18,yratio=.058,xratio=.12,wratio=.0872):
    xrange = ax.get_xlim()[1] - ax.get_xlim()[0]
    yrange = ax.get_ylim()[1] - ax.get_ylim()[0]
    if x1 == None and y1 == None:
        x1 = xrange*(1.6/4.2)
        y1 = yrange*(-9.4/24.77)
    xlen = xrange*xratio*.7
    ylen = yrange*yratio*.6
    x2 = x1-xlen
    y2 = y1-ylen
    yavg = (y1+y2)/2
    w = yrange*wratio*.7
    arrow2 = mpatches.Arrow(x1,y1,-xlen,0,width=w,color='red')
    arrow = mpatches.Arrow(x2,y2,xlen,0,width=w,color='black')
    ax.add_patch(arrow), ax.add_patch(arrow2)
    ax.text(x1,yavg,r'$+$'+label,fontsize=ls,va='center',ha='left')
    ax.text(x2,yavg,r'$-$'+label+r'  ',fontsize=ls,va='center',ha='right')
    return ax

