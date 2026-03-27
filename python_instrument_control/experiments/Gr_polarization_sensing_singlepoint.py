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
from devices.dualgate import DualGate,DualGate_MLGsense
import toolbelt as tb
import os
from matplotlib.lines import Line2D
from sklearn.linear_model import HuberRegressor
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)


def sweep_Efield(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter, keithley_t: KeithleySourceMeter,E_array,file_save='test.txt'):
    plt.ion()
    fig,ax1,lineup,linedown = init_plot(sample,E_array,'Efield')    
    saving_file = make_files(sample,lockin,file_save,'Efield')
    sample.Vsin = lockin.get_sine_output(1)['amplitude_v']
    setup_keithleys(keithley_b,keithley_t)
    
    d_b = sample.d_b + sample.d_m + sample.d_flake 
    d_t = sample.d_t
    E_list, E_list_up, E_list_down, R_Gr_list, R_Gr_list_up, R_Gr_list_down = [],[],[],[],[],[]

    for E in E_array:
        
        Vb,Vt = E*d_b, -E*d_t
        V_b_meas, I_b_meas, V_t_meas, I_t_meas = set_gates(keithley_b,keithley_t,Vb,Vt)
        
        time.sleep(lockin.delay)
        mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
        V_Gr, V_Gr_std = mean_R_chan[0]*10**6, std_R_chan[0]*10**6   #uV
        Vbox = sample.Vsin*10**6 - V_Gr  #uV
        I_Gr = Vbox/sample.Rbox *10**3 #nA  . Rbox should be in ohm
        
        R_Gr,R_Gr_std = V_Gr/I_Gr, V_Gr_std/I_Gr
        print(round(E,3),round(I_b_meas,3),round(I_t_meas,3),round(V_Gr,4),round(I_Gr,4),round(R_Gr,3))
        
        if len(E_list) != 0:
            if E >= E_list[-1]: E_list_up.append(E), R_Gr_list_up.append(R_Gr)
            if E <= E_list[-1]: E_list_down.append(E), R_Gr_list_down.append(R_Gr)
        else:
            if E<0: E_list_up.append(E), R_Gr_list_up.append(R_Gr)
            elif E>0: E_list_down.append(E), R_Gr_list_down.append(R_Gr)
                        
        E_list.append(E), R_Gr_list.append(R_Gr) #kOhm
        save_data([Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr,I_Gr,Vbox,Vt,V_t_meas,I_t_meas,E],saving_file)
        update_plot(sample,lineup,linedown,E_list_up,R_Gr_list_up,E_list_down,R_Gr_list_down,ax1,fig,'Efield')

    plt.ioff()
    plt.savefig(saving_file.replace('.txt','_R_plot.png'),dpi=500)
    plt.show()
    

def main(sample: DualGate, lockin: LockInOE1022D, keithley_b: KeithleySourceMeter,Vb_array,file_save='test.txt',scanaxis='Vb'):
    if scanaxis == 'Vb': sample.d = (sample.d_b+sample.d_m+sample.d_flake) # sample.d = sample.d_b
    elif scanaxis == 'Vt': sample.d = sample.d_t

    plt.ion()
    fig,ax1,lineup,linedown = init_plot(sample,Vb_array,scanaxis)
    saving_file = make_files(sample,lockin,file_save)
    sample.Vsin = lockin.get_sine_output(1)['amplitude_v']
    
    setup_keithleys(keithley_b)

    Vb_list, R_Gr_list, Vb_list_up, Vb_list_down, R_Gr_list_up, R_Gr_list_down = [],[],[],[],[],[]
    
    print('Eb(V/nm)  Vb(V)  Ib(nA)  Vgr(V)  Igr(nA)  Rgr(Kohm)')
    
    for Vb in Vb_array: # sweep Vb 
        Eb = Vb/sample.d
        V_b_meas,I_b_meas,_,_ = set_gates(keithley_b,None,Vb,0)
        time.sleep(lockin.delay)
        
        mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
        V_Gr, V_Gr_std = mean_R_chan[0]*10**6, std_R_chan[0]*10**6   #uV
        Vbox = sample.Vsin*10**6 - V_Gr  #uV
        I_Gr = Vbox/sample.Rbox *10**3 #nA  . Rbox should be in ohm
        
        R_Gr,R_Gr_std = V_Gr/I_Gr, V_Gr_std/I_Gr
        print(round(Eb,3),round(V_b_meas,3),round(I_b_meas,3),round(V_Gr,4),round(I_Gr,4),round(R_Gr,3))
        
        if len(Vb_list) != 0:
            if Vb >= Vb_list[-1]: Vb_list_up.append(Vb), R_Gr_list_up.append(R_Gr)
            if Vb <= Vb_list[-1]: Vb_list_down.append(Vb), R_Gr_list_down.append(R_Gr)
        else:
            if Vb<0: Vb_list_up.append(Vb), R_Gr_list_up.append(R_Gr)
            elif Vb>0: Vb_list_down.append(Vb), R_Gr_list_down.append(R_Gr)
                
        Vb_list.append(Vb), R_Gr_list.append(R_Gr) #kOhm
        save_data([Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr,I_Gr,Vbox],saving_file)
        update_plot(sample,lineup,linedown,Vb_list_up,R_Gr_list_up,Vb_list_down,R_Gr_list_down,ax1,fig,scanaxis)
    
    plt.ioff()
    plt.savefig(saving_file.replace('.txt','_R_plot.png'),dpi=500)
    plt.show()
    
    return Vb_list, R_Gr_list
    
    
def setup_keithleys(keithley_b=None,keithley_t=None):
    if keithley_b!=None:
        keithley_b.enable_source() 
        keithley_b.apply_voltage(compliance_current=keithley_b.compliance_current)
    if keithley_t!=None:
        keithley_t.enable_source() 
        keithley_t.apply_voltage(compliance_current=keithley_t.compliance_current)
        
def set_gates(keithley_b=None,keithley_t=None,Vb=0,Vt=0):
    
    if keithley_b !=None:
        keithley_b.source_voltage = Vb
        V_b_meas = keithley_b.measure_voltage_avg(10)
        I_b_meas = 10**9 * keithley_b.measure_current_avg(20)
    else: 
        V_b_meas,I_b_meas=0,0
    
    if keithley_t !=None:
        keithley_t.source_voltage = Vt
        V_t_meas = keithley_t.measure_voltage_avg(10)
        I_t_meas = 10**9 * keithley_t.measure_current_avg(20)
    else: 
        V_t_meas,I_t_meas = 0,0
    
    return V_b_meas, I_b_meas, V_t_meas, I_t_meas

def save_data(data_save,saving_file):
    with open(saving_file, 'a') as file:
        file.write(' '.join(f"{d:.9f}" for d in data_save) + '\n') 
        
def update_plot(sample, lineup: Line2D,linedown: Line2D, xup_data, yup_data, xdown_data, ydown_data, 
                ax: plt.Axes, fig: plt.Figure, scanaxis='Vb'):
    if scanaxis == 'Efield': xup_data,xdown_data = np.asarray(xup_data), np.asarray(xdown_data) 
    else: xup_data,xdown_data = np.asarray(xup_data)/sample.d , np.asarray(xdown_data)/sample.d 
    lineup.set_data(xup_data, yup_data)
    linedown.set_data(xdown_data, ydown_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(.05)

def init_plot(sample,X_array,scanaxis):
    fig, ax1 = plt.subplots()
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    lineup = Line2D([], [], color='red',marker='.',markersize=3)
    linedown = Line2D([], [], color='blue',marker='.',markersize=3)
    ax1.add_line(lineup)
    ax1.add_line(linedown)
    if scanaxis == 'Efield': 
        ax1.set_xlabel('$E_{⟂}$ (V nm$^{-1}$)')
        xmin,xmax = np.min(X_array),np.max(X_array)
        ax1.set_xlim(xmin - .1*abs(xmin), xmax + .1*abs(xmax))
    else: 
        ax1.set_xlabel(r'$V_{}/d_{}$ (V)'.format(scanaxis[-1],scanaxis[-1]))
        xmin,xmax = np.min(X_array/sample.d),np.max(X_array/sample.d)
        ax1.set_xlim(xmin - .1*abs(xmin), xmax + .1*abs(xmax))
    return fig,ax1,lineup,linedown

def make_files(sample,lockin,file_save,sweeptype='singlegate'):
    gen_path = sample.data_path+file_save
    saving_file = make_Gr_resistance_saving_file(gen_path,sample,lockin,sweeptype)
    return saving_file


def make_Gr_resistance_saving_file(filename,sample,lockin,sweeptype='singlegate'):
    while os.path.exists(filename):            
        filename = filename.replace(".txt", "_new.txt")
    if sweeptype=='singlegate':
        h = '#Vb_set(V) Vb_meas(V) Ib_meas(nA) R_Gr(kOhm) R_Gr_std(kOhm) V_Gr(uV) I_Gr(nA) Vbox(uV)'
    elif sweeptype=='Efield':
        h = '#Vb_set(V) Vb_meas(V) Ib_meas(nA) R_Gr(kOhm) R_Gr_std(kOhm) V_Gr(uV) I_Gr(nA) Vbox(uV) Vt_set(V) Vt_meas(V) It_meas(nA) E_set(V/nm)'
    with open(filename, 'a') as file:
        h0 = '# Rbox (Ohm) = {}'.format(sample.Rbox)
        h1 = '# Vsin (V) = {}'.format(sample.Vsin)
        h2 = '# Lockin wait time (s) = {}'.format(lockin.delay)
        h3 = '# Lockin averages = {}'.format(lockin.num_avgs)
        h4 = '# Lockin frequency = {} Hz'.format(lockin.get_reference_frequency(1))
        h5 = '# Top BN = {} nm'.format(sample.d_t)
        h6 = '# Middle BN = {} nm'.format(sample.d_m)
        h7 = '# Bottom BN = {} nm'.format(sample.d_b)
        h8 = '# Flake = {} nm'.format(sample.d_flake)
        h9 = '# Temperature = {} nm'.format(sample.temperature)
        for h in [h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h]:
            file.write(h + '\n') 
    return filename


if __name__ == "__main__":


    tb.init_plot_params()
    base = "I:/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round8/c5_2L2L_big_3-1/"
    data_path=base+"GrSensorSingle/"
    sample = DualGate_MLGsense('CrI3_2L_MLG', d_b=20, d_m=7.4, d_t=6.6, d_flake=1.4, data_path=base)
    file = data_path+'fineloop1_200k.txt'
    data = np.loadtxt(file)
    Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5]
    db = sample.d_b
    dt = sample.d_t
    dc = sample.d_flake
    db = db+dt+dc

    
    diffs = np.diff(Vb)
    change_indices = np.where(diffs < 0)[0]  # descending starts here
    if len(change_indices)==0: change_indices = np.array([len(Vb)-1])
    Vb_ascend, Vb_descend = Vb[:change_indices[0] + 1], Vb[change_indices[0]:]
    E_ascend, E_descend = Vb_ascend/db, Vb_descend/db
    
    plot = 'R' #'R'
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    Vsin=0.1
    Rbox=1e6
    
    # V_Gr = V_Gr/(1e6)
    # ascend,descend = R_Gr[:change_indices[0]+1], R_Gr[change_indices[0]:]
    # std_ascend,std_descend = R_Gr_std[:change_indices[0]+1],R_Gr_std[change_indices[0]:]
    # ax.set_xlabel('$V_{b}/d_b$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    # ax.set_xlabel('$V_{b}/d_t$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    # ax.set_xlabel('$E_{⟂}$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    
    # ax.errorbar(E_ascend, ascend,yerr=std_ascend,color='r',marker='.',ms=3,label=r'$\rightarrow$',elinewidth=0)
    # ax.errorbar(E_descend, descend,yerr=std_descend,color='b',marker='.',ms=3,label=r'$\leftarrow$',elinewidth=0)
    # ax.legend(loc='upper left')
    # plt.savefig(file.replace('.txt','_{}_plot.png'.format(plot)),dpi=500)
    # plt.show()
    

