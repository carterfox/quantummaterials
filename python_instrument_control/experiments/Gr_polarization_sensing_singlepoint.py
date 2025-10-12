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


def main(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter,Vb_array,Vsin,file_save):
    
    # lockin.set_sine_output(channel=lockin.R_chan,amplitude_v=Vsin)
    Rbox = sample.Rbox
    d_b = sample.d_b
    saving_file = make_files(sample,lockin,file_save)

    plt.ion()
    fig,ax1,lineup,linedown = init_plot()
    ax1.set_ylim(0,2)
    ax1.set_xlim(np.min(Vb_array)*1.1,1.1*np.max(Vb_array))
    Vb_list, R_Gr_list = [],[]
    Vb_list_up, Vb_list_down, R_Gr_list_up, R_Gr_list_down = [],[],[],[]
    
    for Vb in Vb_array: # sweep Vb 
        keithley_b.source_voltage = Vb
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)
        
        time.sleep(lockin.delay)
        mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
        V_Gr, V_Gr_std = mean_R_chan[0], std_R_chan[0]
        V_Gr = V_Gr*10**6   #uV 
        V_Gr_std = V_Gr_std*10**6
        Vbox = Vsin*10**6 - V_Gr  #uV
        I_Gr = Vbox/Rbox *10**3 #nA  . Rbox should be in ohm
        
        R_Gr = V_Gr/I_Gr
        R_Gr_std = V_Gr_std/I_Gr
        print(round(V_b_meas,3),round(I_b_meas,3),round(V_Gr,4),round(I_Gr,4),round(R_Gr,3))
        
        
        if len(Vb_list) != 0:
            if Vb >= Vb_list[-1]:
                Vb_list_up.append(Vb)
                R_Gr_list_up.append(R_Gr)
            if Vb <= Vb_list[-1]:
                Vb_list_down.append(Vb)
                R_Gr_list_down.append(R_Gr)
        else:
            if Vb <0:
                Vb_list_up.append(Vb)
                R_Gr_list_up.append(R_Gr)
            elif Vb>0:
                Vb_list_down.append(Vb)
                R_Gr_list_down.append(R_Gr)
        Vb_list.append(Vb)
        R_Gr_list.append(R_Gr) #kOhm
        save_data([Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr,I_Gr,Vbox],saving_file)
        update_plot(lineup,linedown,Vb_list_up,R_Gr_list_up,Vb_list_down,R_Gr_list_down,ax1,fig)
    plt.ioff()
    plt.savefig(saving_file.replace('.txt','_R_plot.png'),dpi=500)
    plt.show()
    
    return Vb_list, R_Gr_list
    
    

def save_data(data_save,saving_file):
    with open(saving_file, 'a') as file:
        file.write(' '.join(f"{d:.9f}" for d in data_save) + '\n') 
        
def update_plot(lineup: Line2D,linedown: Line2D, xup_data, yup_data, xdown_data, ydown_data, 
                ax: plt.Axes, fig: plt.Figure, pause_time: float = 0.05):
    lineup.set_data(xup_data, yup_data)
    linedown.set_data(xdown_data, ydown_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)

def init_plot():
    fig, ax1 = plt.subplots()
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_xlabel(r'V$_{b}$ (V)')
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    lineup = Line2D([], [], color='red',marker='.',markersize=3)
    linedown = Line2D([], [], color='blue',marker='.',markersize=3)
    ax1.add_line(lineup)
    ax1.add_line(linedown)
    # ax1.legend()
    return fig,ax1,lineup,linedown

def make_files(sample,lockin,file_save):
    if not os.path.exists(sample.data_path+"/GrSensorSingle"):
        os.makedirs(sample.data_path+"/GrSensorSingle")
    gen_path = sample.data_path+'/GrSensorSingle/'+file_save
    saving_file = make_Gr_resistance_saving_file(gen_path,sample.Rbox,lockin.delay,lockin.sine_out_freq,0,lockin.num_avgs,file='full')
    return saving_file


def make_Gr_resistance_saving_file(filename,Rbox,delay,freq,Vb,num_avg,file='Vb'):
    if file == 'full':
        while os.path.exists(filename):            
            filename = filename.replace(".txt", "_new.txt")
        header = '#Vb_set(V) Vb_meas(V) Ib_meas(nA) R_Gr(kOhm) R_Gr_std(kOhm) V_Gr(uV) I_Gr(nA) Vbox(uV)'
        with open(filename, 'a') as file:
            header1 = '# Rbox (Ohm) = {}'.format(Rbox)
            header2 = '# Lockin wait time (s) = {}'.format(delay)
            header3 = '# Lockin averages = {}'.format(num_avg)
            file.write(header1 + '\n') 
            file.write(header2 + '\n') 
            file.write(header3 + '\n') 
            file.write(header + '\n') 
    return filename


if __name__ == "__main__":
    tb.init_plot_params()
    # path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/GrSensorSingle/295K/measurements2/'    
    path = '/Users/carterfox/My Drive (cdfox@wisc.edu)/StackingTransitions/CrI3/round7/d3/GrSensorSingle/2K/'    
    # path = 'D:/LabData/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round7/d3/GrSensorSingle/'
    file = path+'measurements1/sweep1_2K_0T.txt'
    # file = path+'slow-scan2_295K_8-25.txt'
    # file = path+'sweep3_2K_0T_floatVc.txt'
    file = path+'sweep1_2K_0T.txt'
    data = np.loadtxt(file)
    Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4]
    db = 18.45
    # db = 9.41
    dt = 7.93
    dc = 0.7*4
    db = db+dt+dc

    
    diffs = np.diff(Vb)
    change_indices = np.where(diffs < 0)[0]  # descending starts here
    if len(change_indices)==0:
        change_indices = np.array([len(Vb)-1])
    Vb_ascend = Vb[:change_indices[0] + 1]
    Vb_descend = Vb[change_indices[0]:]
    E_ascend = Vb_ascend/db
    E_descend = Vb_descend/db
    
    plot = 'R' #'R'
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    ascend = R_Gr[:change_indices[0] + 1]
    descend = R_Gr[change_indices[0]:]
    std_ascend = R_Gr_std[:change_indices[0] + 1]
    std_descend = R_Gr_std[change_indices[0]:]
    ax.set_xlabel('$V_{b}/d$ (V$~$nm$^{-1}$)'), ax.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    ax.set_xlim(-.45,.4)

        
    if plot == 'G':
        ascend = 1000/ascend
        descend = 1000/descend
        # std_ascend = 1000*R_Gr_std[:change_indices[0] + 1]/(R_Gr[:change_indices[0] + 1])**2
        # std_descend = 1000*R_Gr_std[change_indices[0] + 1:]/(R_Gr[change_indices[0] + 1:])**2
        ax.set_xlabel('$V_{b}/d$ (V$~$nm$^{-1}$)'), ax.set_ylabel(r'G$_{Gr}$ ($\mu S$)')
    
    ax.errorbar(E_ascend, ascend,yerr=std_ascend,color='r',marker='.',ms=3,label=r'$\rightarrow$')
    ax.errorbar(E_descend, descend,yerr=std_descend,color='b',marker='.',ms=3,label=r'$\leftarrow$')
    ax.legend(loc='upper left')
    # plt.savefig(file.replace('.txt','_{}_plot.png'.format(plot)),dpi=500)
    plt.show()
    

