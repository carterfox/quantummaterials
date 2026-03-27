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


def dirac_resistance(Vg, R0, B, V_D, n0):
    """
    Graphene Dirac resistance vs gate voltage.

    Parameters
    ----------
    Vg : array-like
        Gate voltage.
    R0 : float
        Background/contact resistance.
    B : float
        Amplitude scaling factor.
    V_D : float
        Dirac point gate voltage.
    n0 : float
        Residual carrier density parameter (rounding).

    Returns
    -------
    array-like
        Resistance R(Vg).
    """
    return R0 + B / np.sqrt(n0**2 + (Vg - V_D)**2)



def lorentzian_linear_bg(x, A, x0, gamma, m, b):
    """
    Lorentzian peak with linear background.

    Parameters
    ----------
    x : array-like
        Input x values.
    A : float
        Amplitude of the Lorentzian peak.
    x0 : float
        Center position of the peak.
    gamma : float
        Full width at half maximum (FWHM).
    m : float
        Slope of the linear background.
    b : float
        Intercept of the linear background.

    Returns
    -------
    array-like
        Lorentzian + linear background evaluated at x.
    """
    lor = A * (0.5 * gamma)**2 / ((x - x0)**2 + (0.5 * gamma)**2)
    return lor + (m * x + b)


def lorentzian(x, A, x0, gamma, C):
    """
    Lorentzian peak function.

    Parameters
    ----------
    x : array-like
        Input x values.
    A : float
        Amplitude of the peak.
    x0 : float
        Center position of the peak.
    gamma : float
        Full width at half maximum (FWHM).
    C : float
        Constant baseline offset.

    Returns
    -------
    array-like
        Lorentzian evaluated at x.
    """
    return A * (0.5 * gamma)**2 / ((x - x0)**2 + (0.5 * gamma)**2) + C


def to_superscript(expr):
    superscripts = {
        "-": "⁻",
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹"
    }
    return "".join(superscripts.get(ch, ch) for ch in expr)


def create_axes_with_exact_size(ax_width_in, ax_height_in, margins_in=(0.1,0.1), dpi=500,proj='rectilinear'):
    """
    Create a figure where the axes area is exactly ax_width_in × ax_height_in inches.
    margins_in = (horizontal_margin, vertical_margin) in inches
    """
    fig_width = ax_width_in + 2 * margins_in[0]
    fig_height = ax_height_in + 2 * margins_in[1]

    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    ax = fig.add_axes([
        margins_in[0] / fig_width,  # left
        margins_in[1] / fig_height,  # bottom
        ax_width_in / fig_width,    # width
        ax_height_in / fig_height   # height
    ],projection=proj)
    return fig, ax



def make_bfield_list(b_start,b_end,b_step):
    bfield_list = np.append(np.arange(b_start,b_end,b_step),np.arange(b_end,b_start-b_step,-1*b_step))
    return bfield_list

def read_lockin_rmcd_data(lockin: LockInOE1022D):
    start= time.time()
    mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2,3,7,8],num_avgs=lockin.num_avgs)
    R_cur_mean, R_cur_std = mean_R_chan[0], std_R_chan[0]
    dR_cur_mean, dR_cur_std = mean_dR_chan[2], std_dR_chan[2]
    theta_R_cur_mean, theta_R_cur_std = mean_R_chan[1], std_R_chan[1]
    theta_dR_cur_mean, theta_dR_cur_std = mean_dR_chan[3], std_dR_chan[3]
    pack = [R_cur_mean,R_cur_std,theta_R_cur_mean,theta_R_cur_std,dR_cur_mean,dR_cur_std,theta_dR_cur_mean,theta_dR_cur_std]
    return pack
    

def make_rmcd_saving_file(filename,experiment):
    
    if experiment == 'bscan':
        header = "#B(T) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"
    elif experiment == 'mapping':
        header = "#X(V) Y(V) R_mean(V) R_std(V) thetaR_mean(deg) thetaR_std(deg) dR_mean(V) dR_std(V) thetadR_mean(deg) thetadR_std(deg)"
    elif experiment == 'Esweep-Vb':
        header = "#Vb_set(V) Vb(V) Ib(nA) R(V) R_std(V) thetaR(deg) thetaR_std(deg) dR(V) dR_std(V) thetadR(deg) thetadR_std(deg)"

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

def E_dualgate(V_b,V_t,sample,no_middle_gr=False):
    d_b = sample.d_b
    d_t = sample.d_t
    if no_middle_gr:
        d_flake = sample.d_flake
        E = (V_b+V_t)/(d_b+d_t+d_flake)
    else:
        E = (-V_t/d_t + V_b/d_b)/2
    return E


def n_dualgate(V_b,V_t,d_b,d_t):
    eps_0 = cont.eps0
    eps_bn = 4
    e = cont.e.si
    n = eps_bn*eps_0 * (V_t/d_t + V_b/d_b)/e
    return n.value

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


def CD(A,B,errA,errB,num_gates,absolute=False):
    CD = (A-B)/(A+B)*100
    if absolute:
        CD = abs(CD)
    CD_err = np.sqrt( (2*B*errA/(A+B)**2)**2 + (2*A*errB/(A+B)**2)**2 )*100/np.sqrt(num_gates)
    return CD, CD_err

def get_CD_data(file):
    try:
        data = np.loadtxt(file,comments='#',skiprows=4)[:,1]
    except:
        data = np.loadtxt(file,comments='#',skiprows=7)[:,1]
    num_gates = len(data)
    mean,std = np.mean(data),np.std(data)
    return mean,std,num_gates


def init_plot_params():
    mpl.rcParams.update(mpl.rcParamsDefault)
    fontsize = 18
    plt.rcParams["lines.marker"] = '.'
    plt.rcParams["lines.linewidth"] = 2
    plt.rcParams["axes.labelpad"] = 4
    plt.rcParams['font.family'] = 'Arial' 
    # plt.rcParams['mathtext.sans-serif'] = ['Arial'] 
    plt.rcParams['mathtext.rm'] = 'Arial' 
    plt.rcParams['mathtext.it'] = 'Arial:italic' 
    plt.rcParams['mathtext.bf'] = 'Arial:bold'
    plt.rcParams['mathtext.sf'] = 'Arial' 
    plt.rcParams['mathtext.tt'] = 'Arial' 
    plt.rcParams['mathtext.cal'] = 'Arial' 
    plt.rcParams['mathtext.default'] = 'it' 
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
    
    
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase

class BarWithDotHandler(HandlerBase):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        
        bar_color, dot_color = orig_handle
        
        # Bar rectangle (fills most of the legend box)
        bar = Rectangle(
            (xdescent, ydescent),
            width,
            height,
            facecolor=bar_color,
            edgecolor='none',
            transform=trans,alpha=.27
        )
        
        # Dot centered inside the rectangle
        dot = Line2D(
            [xdescent + width/2],
            [ydescent + height/2],
            marker='.',
            markersize=3,
            color=dot_color,
            linestyle='',
            transform=trans
        )
        return [bar, dot]
    
def plot_arrow_legend(ax,label,x1=None,y1=None,ls=18,yratio=.058,xratio=.12,wratio=.0872,colora='black',colord='red'):
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
    w = yrange*wratio*.55
    arrow2 = mpatches.Arrow(x1,y1,-xlen,0,width=w,color=colord)
    arrow = mpatches.Arrow(x2,y2,xlen,0,width=w,color=colora)
    ax.add_patch(arrow), ax.add_patch(arrow2)
    if label != None:
        ax.text(x1,yavg,r'$+$'+label,fontsize=ls,va='center',ha='left')
        ax.text(x2,yavg,r'$-$'+label+r'  ',fontsize=ls,va='center',ha='right')
    return ax

def plot_arrow(ax,x,y,dx,dy,w=1,c='r'):    
    arrow = mpatches.Arrow(x,y,dx,dy,width=w,color=c)
    ax.add_patch(arrow)
    return ax

def plot_rmcd_state(ax,state,x,y,xstep=0.1,h='right',f=18):
    xcur = x
    for a in state:
        if a == 'up':
            ax.text(xcur,y,r'$\uparrow$',c='mediumblue',ha=h,fontsize=f)
        if a == 'down':
            ax.text(xcur,y,r'$\downarrow$',c='firebrick',ha=h,fontsize=f)
        xcur = xcur+xstep
