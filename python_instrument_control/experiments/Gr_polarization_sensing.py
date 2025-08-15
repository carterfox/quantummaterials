#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 09:42:58 2025

@author: carterfox
"""


import numpy as np
import time
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
from homemade_servers.SSI_OE1022D import LockInOE1022D
from devices.dualgate import DualGate
import toolbelt as tb
import os
from matplotlib.lines import Line2D
from sklearn.linear_model import HuberRegressor


def main(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter,Vb_array,Vsin_array,file_save):
    """
    Sweeps back gate and measures resistance of a graphene flake using lock-in technique.

    Parameters
    ----------
    sample : DualGate
        Graphene device object containing metadata and configuration (e.g., Rbox, data path).
    lockin : LockInOE1022D
        Lock-in amplifier interface used to measure V_Gr and phase.
    keithley_b : KeithleySourceMeter
        Source meter used to apply and measure back-gate voltage and current.
    Vb_array : array-like
        Array of back-gate voltages to sweep (in volts).
    Vsin_array : array-like
        Array of sine excitation voltages to sweep (in volts).
    file_save : str
        Filename for saving the measurement data.

    Returns
    -------
    V_Gr_list : list of float
        Final list of measured graphene voltages (in µV) from the last Vb sweep.
    I_Gr_list : list of float
        Final list of calculated graphene currents (in nA) from the last Vb sweep.
    R_Gr_list : list of float
        List of extracted graphene resistances (in kΩ) for each Vb.
    R_Gr_std_list : list of float
        List of standard deviations of the resistance fits (in kΩ) for each Vb.

    Notes
    -----
    - Live plots are updated during acquisition using matplotlib.
    - Data is saved in two formats: per-Vb sweep and full summary.
    - Resistance is fit using Huber regression with outlier rejection.
    - The figure window is initialized and positioned manually (see `init_plot()`).
    """
    
    lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin_array[0])
    Rbox = sample.Rbox
    d_b = sample.d_b
    save_file_Vb_gen, saving_file = make_files(sample,lockin,file_save)

    plt.ion()
    fig,ax1,ax2,line1,line2,line3 = init_plot()
    
    keithley_b.enable_source()
    keithley_b.apply_voltage(compliance_current=keithley_b.compliance_current)
    
    Vb_list, R_Gr_list, R_Gr_std_list = [],[],[]

    for Vb in Vb_array: # sweep Vb 

        keithley_b.source_voltage = Vb
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)
        print(Vb,V_b_meas,I_b_meas)
        file_Vb = make_Gr_resistance_saving_file(save_file_Vb_gen,Rbox,lockin.delay,lockin.sine_out_freq,Vb,file='Vb') # make file for this Vb
        
        time.sleep(0.3)
        I_Gr_list, V_Gr_list = [],[]
        line3.set_data([],[])
        
        for Vsin in Vsin_array: # sweep Vsin and measure Vgr,Igr to determine Rgr at that Vb
            
            lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin)
            time.sleep(lockin.delay)
            mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
            V_Gr, theta = mean_R_chan[0], mean_R_chan[1]
            V_Gr = V_Gr*10**6   #uV 
            Vbox = Vsin*10**6 - V_Gr  #uV
            I_Gr = Vbox/Rbox *10**3 #nA  . Rbox should be in ohm
                        
            I_Gr_list.append(I_Gr) #nA
            V_Gr_list.append(V_Gr) #uV
            line2.set_data(I_Gr_list,V_Gr_list)
            update_plot(line2,I_Gr_list,V_Gr_list,ax2,fig)
            save_data([Vsin,V_Gr,I_Gr,theta],file_Vb)
                
        lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin_array[0])
        time.sleep(3)

        R_Gr,  R_Gr_std, fit = fit_resistance(I_Gr_list,V_Gr_list,Vb)
        update_plot(line3,I_Gr_list,fit,ax2,fig)
        
        Vb_list.append(Vb)
        R_Gr_list.append(R_Gr) #kOhm
        R_Gr_std_list.append(R_Gr_std) #kOhm
        save_data([Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std],saving_file)
        update_plot(line1,Vb_list,R_Gr_list,ax1,fig)

    plt.ioff()
    plt.show()
    
    return V_Gr_list,I_Gr_list,R_Gr_list,R_Gr_std_list
    
    

def save_data(data_save,saving_file):
    with open(saving_file, 'a') as file:
        file.write(' '.join(f"{d:.9f}" for d in data_save) + '\n') 
        
def update_plot(line: Line2D, x_data, y_data, ax: plt.Axes, fig: plt.Figure, pause_time: float = 0.05):
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)

def init_plot():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,8))
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_xlabel(r'V$_{b}$ (V)')
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    line1 = Line2D([], [], color='blue',marker='.')
    ax1.add_line(line1)
    ax2.set_xlabel(r'I$_{Gr}$ (nA)')
    ax2.set_ylabel(r'V$_{Gr}$ ($\mu$V)')
    line2 = Line2D([], [], color='red',marker='.',linewidth=0)
    ax2.add_line(line2)
    line3 = Line2D([], [], color='red',marker='')
    ax2.add_line(line3)
    return fig,ax1,ax2,line1,line2,line3

def fit_resistance(I_Gr_list,V_Gr_list,Vb):
    model = HuberRegressor()
    I_Gr_list2 = np.array(I_Gr_list).reshape(len(I_Gr_list),1)
    model.fit(I_Gr_list2,V_Gr_list)
    pred = model.predict(I_Gr_list2)
    residuals = abs(pred-V_Gr_list)
    outliers = np.where(residuals>=.8)
    if len(outliers[0]) !=0:
        rem = np.array(V_Gr_list)[outliers]
        print('removing Vref = ',rem, '   in Vb = ',str(Vb))
    Igr_noout = np.array(I_Gr_list)[np.where(residuals<1)]
    Vgr_noout = np.array(V_Gr_list)[np.where(residuals<1)]
    
    p, c = curve_fit(tb.line, Igr_noout, Vgr_noout)
    R_Gr,  R_Gr_std = p[0], np.sqrt(np.diag(c))[0]
    fit = tb.line(np.array(I_Gr_list),p[0],p[1])
    return R_Gr, R_Gr_std, fit

def make_files(sample,lockin,file_save):
    if not os.path.exists(sample.data_path+"/GrSensor"):
        os.makedirs(sample.data_path+"/GrSensor")
    if not os.path.exists(sample.data_path+"/GrSensor/"+file_save.split('.txt')[0]):
        os.makedirs(sample.data_path+"/GrSensor/"+file_save.split('.txt')[0]+'_VI_data')
    gen_path = sample.data_path+'/GrSensor/'+file_save
    save_file_Vb_gen = sample.data_path+'/GrSensor/'+file_save.split('.txt')[0]+'_VI_data/'
    saving_file = make_Gr_resistance_saving_file(gen_path,sample.Rbox,lockin.delay,lockin.sine_out_freq,0,file='full')
    return save_file_Vb_gen, saving_file


def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,file='Vb'):
    
    if file == 'Vb':
        filename = filename + 'VI_data_Vb'+str(int(Vb*1000))+'mV_.txt'
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        with open(filename, 'a') as file:
            header1 = '# Rbox (Ohm) = {}'.format(Rbox)
            header2 = '# Lockin wait time (ms) = {}'.format(delay)
            header3 = '# Vb (V) = {}'.format(Vb)
            header4 = '# V_sin(V) V_Gr(uV) I_Gr(nA) theta(deg)'
            file.write(header1 + '\n') 
            file.write(header2 + '\n') 
            file.write(header3 + '\n') 
            file.write(header4 + '\n') 
    
    elif file == 'full':
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        header = '#Vb_set(V) Vb_meas(V) Ib_meas(nA) R_Gr(kOhm) R_Gr_std(kOhm)'
        with open(filename, 'a') as file:
            file.write(header + '\n') 
    return filename


if __name__ == "__main__":

    path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/GrSensor/'    
    file = path+'sweep7_reverse_electrodes.txt'
    
    data = np.loadtxt(file)
    Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4]
    
    diffs = np.diff(Vb)
    try:
        transition_index = np.where((diffs[:-1] >= 0) & (diffs[1:] <= 0))[0][0]+1
    except:
        transition_index=len(Vb)
        
    
    Vb_ascend = Vb[0:transition_index]
    Vb_descend = Vb[transition_index:]
    R_Gr_ascend = R_Gr[0:transition_index]
    R_Gr_descend = R_Gr[transition_index:]
    R_Gr_std_ascend = R_Gr_std[0:transition_index]
    R_Gr_std_descend = R_Gr_std[transition_index:]
    
    
    tb.init_plot_params()
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    ax.errorbar(Vb_ascend, R_Gr_ascend, yerr=R_Gr_std_ascend,color='black',marker='.',ms=5,label=r'$\rightarrow$',elinewidth=0)
    ax.errorbar(Vb_descend, R_Gr_descend, yerr=R_Gr_std_descend,color='r',marker='.',ms=5,label=r'$\leftarrow$',elinewidth=0)
    ax.legend()
    ax.set_xlabel('V$_{b}$ (V)'), ax.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    # ax.set_xlim(-.5,2)
    # ax.set_ylim(1.95,2.24)
    plt.savefig(file.replace('.txt','_plot.png'),dpi=500)
    plt.show()
    

