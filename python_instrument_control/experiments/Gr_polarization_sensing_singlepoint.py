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
import math
import glob
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
    plt.ion()
    fig,ax1,lineup,linedown = init_plot(sample,Vb_array,scanaxis)
    saving_file = make_files(sample,lockin,file_save)
    sample.Vsin = lockin.get_sine_output(1)['amplitude_v']
    
    setup_keithleys(keithley_b)
    
    if scanaxis == 'Vb': sample.d = (sample.d_b+sample.d_m+sample.d_flake) # sample.d = sample.d_b
    elif scanaxis == 'Vt': sample.d = sample.d_t

    Vb_list, R_Gr_list, Vb_list_up, Vb_list_down, R_Gr_list_up, R_Gr_list_down = [],[],[],[],[],[]
    
    for Vb in Vb_array: # sweep Vb 
    
        V_b_meas,I_b_meas,_,_ = set_gates(keithley_b,None,Vb,0)
        time.sleep(lockin.delay)
        
        mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan = lockin.read_average_dual(params=[2, 3], num_avgs=lockin.num_avgs)
        V_Gr, V_Gr_std = mean_R_chan[0]*10**6, std_R_chan[0]*10**6   #uV
        Vbox = sample.Vsin*10**6 - V_Gr  #uV
        I_Gr = Vbox/sample.Rbox *10**3 #nA  . Rbox should be in ohm
        
        R_Gr,R_Gr_std = V_Gr/I_Gr, V_Gr_std/I_Gr
        print(round(V_b_meas,3),round(I_b_meas,3),round(V_Gr,4),round(I_Gr,4),round(R_Gr,3))
        
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
        keithley_b.apply_voltage()
    if keithley_t!=None:
        keithley_t.enable_source() 
        keithley_t.apply_voltage()
        
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
                ax: plt.Axes, fig: plt.Figure, pause_time: float = 0.05, scanaxis='Vb'):
    if scanaxis == 'Efield': xup_data,xdown_data = np.asarray(xup_data), np.asarray(xdown_data) 
    else: xup_data,xdown_data = np.asarray(xup_data)/sample.d , np.asarray(xdown_data)/sample.d 
    lineup.set_data(xup_data, yup_data)
    linedown.set_data(xdown_data, ydown_data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(pause_time)

def init_plot(sample,X_array,scanaxis):
    fig, ax1 = plt.subplots()
    fig.canvas.manager.window.move(1920, 100)  # (x, y) position in pixels
    ax1.set_ylabel(r'R$_{Gr}$ (k$\Omega$)')
    lineup = Line2D([], [], color='red',marker='.',markersize=3)
    linedown = Line2D([], [], color='blue',marker='.',markersize=3)
    ax1.add_line(lineup)
    ax1.add_line(linedown)
    if scanaxis == 'Efield': 
        ax1.set_xlabel('$E_\perp$ (V nm$^{-1}$)')
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


def plot_2dmap(folder_path,d_b,d_t):
    files = np.array([Path(p) for p in glob.glob(str(Path(folder_path) / "*.txt"))])
    Vtvals = []
    for f in files:
        fss = float(str(f).split('/')[-1].replace('_0p','_0.').replace('_m0p','_-0.').split('_')[3])
        Vtvals.append(fss)
    Vtvals = np.asarray(Vtvals)
    Vtvalssort = np.argsort(Vtvals)
    Vt = np.sort(Vtvals)
    sorted_files = files[Vtvalssort]
    
    Vb=np.loadtxt(files[0])[:,0]
    xs,ys,R_Gr_vals_ascend,R_Gr_vals_descend = np.array([]),np.array([]),np.array([]),np.array([])
    
    for fs,Vt in zip(sorted_files,Vt):
        data = np.loadtxt(fs)
        Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5]
        diffs = np.diff(Vb)
        change_indices = np.where(diffs < 0)[0]  # descending starts here
        if len(change_indices)==0: change_indices = np.array([len(Vb)-1])
        # print(change_indices)
        Vb_ascend, Vb_descend = Vb[:change_indices[0]], Vb[change_indices[0]:]
        R_Gr_ascend, R_Gr_descend = R_Gr[:change_indices[0]], R_Gr[change_indices[0]:]
        xs = np.append(xs,Vb_ascend/d_b)
        ys = np.append(ys,np.ones_like(Vb_ascend)*Vt/d_t)
        R_Gr_vals_ascend = np.append(R_Gr_vals_ascend,R_Gr_ascend)
        R_Gr_vals_descend = np.append(R_Gr_vals_descend,np.flip(R_Gr_descend))
        # print(Vt)
    # print(np.shape(Vb_ascend),np.shape(Vb_descend))
    x_unique, y_unique = np.unique(xs), np.unique(ys)
    image_Rgr_a = np.zeros((len(x_unique), len(y_unique)))
    image_Rgr_d = np.zeros((len(x_unique), len(y_unique)))
    image_Rgr_hyst = np.zeros((len(x_unique), len(y_unique)))
    # 
    # print(x_unique,y_unique)    
    for x, y, Ra,Rd in zip(xs, ys, R_Gr_vals_ascend,R_Gr_vals_descend):
        xi,yi = np.where(x_unique == x)[0][0],np.where(y_unique == y)[0][0]
        image_Rgr_a[xi, yi] = Ra
        image_Rgr_d[xi, yi] = Rd
        image_Rgr_hyst[xi, yi] = Rd-Ra
        
    image_Rgr_a=np.transpose(image_Rgr_a)    
    image_Rgr_d=np.transpose(image_Rgr_d)    
    fs=8
    bw=0.5

    fig1,ax1 = tb.create_axes_with_exact_size(1.35, 1.2)
    im1=ax1.imshow(image_Rgr_a,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=95,vmax=205)
    cbar = fig1.colorbar(im1, ax=ax1, location="right", fraction=0.05,pad=0.03) 
    cbar.set_label('$R_{Gr}$ (k$\Omega$)', ha='center',fontsize=fs)
    cbar.ax.tick_params(labelsize=fs,length=1)
    cbar.set_ticks([100,125,150,175,200])
    ax1.set_xlabel("V$_b$ (V)",fontsize=fs)
    ax1.set_ylabel("V$_t$ (V)",fontsize=fs,labelpad=0)  
    ax1.set_xticks([-.08,0,.08],[-0.08,0,0.08])
    ax1.set_yticks([-.14,-.07,0,.07,.14])
    ax1.tick_params(axis="both", labelsize=fs,length=2,color='k') 
    cbar.outline.set_linewidth(bw)
    for spine in ax1.spines.values(): spine.set_linewidth(bw) 
    ax1.annotate( "", xy=(.08, -.14), xytext=(-.08, -.14), arrowprops=dict(arrowstyle="simple,head_length=0.2,head_width=0.1,tail_width=0.015",linestyle="-", color='white', linewidth=0.02) )    
    ax1.annotate( "", xy=(-.08, -.14), xytext=(-.08, .14), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='white', linewidth=.3) )    
    ax1.annotate( "", xy=(-.08, .14), xytext=(-.08, .13), arrowprops=dict(arrowstyle="simple,head_length=0.2,head_width=0.1,tail_width=0.04",linestyle="--", color='white', linewidth=0.03) )    

    fig2,ax2 = tb.create_axes_with_exact_size(1.35, 1.2)
    im2=ax2.imshow(image_Rgr_d,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=95,vmax=205)
    cbar2 = fig2.colorbar(im2, ax=ax2, location="right", fraction=0.05,pad=0.03) 
    cbar2.set_label('$R_{Gr}$ (k$\Omega$)', ha='center',fontsize=fs)
    cbar2.ax.tick_params(labelsize=fs,length=1)
    cbar2.set_ticks([100,125,150,175,200])
    ax2.set_xlabel("V$_b$ (V)",fontsize=fs)
    ax2.set_ylabel("V$_t$ (V)",fontsize=fs,labelpad=0)  
    ax2.set_xticks([-.08,0,.08],[-0.08,0,0.08])
    ax2.set_yticks([-.14,-.07,0,.07,.14])
    ax2.tick_params(axis="both", labelsize=fs,length=2,color='k') 
    cbar2.outline.set_linewidth(bw)
    for spine in ax2.spines.values(): spine.set_linewidth(bw) 
    ax2.annotate( "", xy=(-.08, -.14), xytext=(.08, -.14), arrowprops=dict(arrowstyle="simple,head_length=0.2,head_width=0.1,tail_width=0.015",linestyle="-", color='white', linewidth=0.02) )    
    ax2.annotate( "", xy=(-.08, -.14), xytext=(-.08, .14), arrowprops=dict(arrowstyle="->,head_width=0.001,head_length=0.001",linestyle="--", color='white', linewidth=.3) )    
    ax2.annotate( "", xy=(-.08, .14), xytext=(-.08, .13), arrowprops=dict(arrowstyle="simple,head_length=0.2,head_width=0.1,tail_width=0.04",linestyle="--", color='white', linewidth=0.03) )    

    fig3,ax3 = tb.create_axes_with_exact_size(1.35, 1.2)
    im3=ax3.imshow(image_Rgr_hyst,origin='lower',extent=[x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()],vmin=-5,vmax=5)
    cbar3 = fig3.colorbar(im3, ax=ax3, location="right", fraction=0.05,pad=0.03) 
    cbar3.set_label('$\Delta R_{Gr}$ (k$\Omega$)', ha='center',fontsize=fs)
    cbar3.ax.tick_params(labelsize=fs,length=1)
    # cbar3.set_ticks([100,125,150,175,200])
    ax3.set_xlabel("V$_b$ (V)",fontsize=fs)
    ax3.set_ylabel("V$_t$ (V)",fontsize=fs,labelpad=0)  
    ax3.set_xticks([-.08,0,.08],[-0.08,0,0.08])
    ax3.set_yticks([-.14,-.07,0,.07,.14])
    ax3.tick_params(axis="both", labelsize=fs,length=2,color='k') 
    cbar3.outline.set_linewidth(bw)
    for spine in ax3.spines.values(): spine.set_linewidth(bw) 
    ax3.annotate( "", xy=(-.08, -.14), xytext=(.08, -.14), arrowprops=dict(arrowstyle="simple,head_length=0.2,head_width=0.1,tail_width=0.015",linestyle="-", color='white', linewidth=0.02) )    
    
    fig1.savefig(folder_path+'R_Gr_map_Vb_ascend.png',dpi=500)
    fig2.savefig(folder_path+'R_Gr_map_Vb_descend.png',dpi=500)
    fig3.savefig(folder_path+'R_Gr_map_Vb_hyst.png',dpi=500)
    
    return image_Rgr_a


if __name__ == "__main__":


    tb.init_plot_params()
    path="/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/StackingTransitions/CrI3/round8/c4_2L_2-10/GrSensorSingle/2K/2dmap/"
    sample = DualGate_MLGsense('CrI3_2L_MLG', d_b=20, d_m=7.4, d_t=6.6, d_flake=1.4, data_path=path)
    # file = path+'2dmap/'
    # data = np.loadtxt(file)
    # Vb,V_b_meas,I_b_meas,R_Gr,R_Gr_std,V_Gr = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5]
    # db = sample.d_b
    # dt = sample.d_t
    # dc = sample.d_flake
    # db = db+dt+dc
    
    image_Rgr_a=plot_2dmap(path, d_b=sample.d_b+sample.d_m+sample.d_flake, d_t=sample.d_t)

    
    # diffs = np.diff(Vb)
    # change_indices = np.where(diffs < 0)[0]  # descending starts here
    # if len(change_indices)==0: change_indices = np.array([len(Vb)-1])
    # Vb_ascend, Vb_descend = Vb[:change_indices[0] + 1], Vb[change_indices[0]:]
    # E_ascend, E_descend = Vb_ascend/db, Vb_descend/db
    
    # fig, ax = plt.subplots(1,1,figsize=(6,5))
    # Vsin=0.1
    # Rbox=1e6
    
    # V_Gr = V_Gr/(1e6)
    # ascend,descend = R_Gr[:change_indices[0]+1], R_Gr[change_indices[0]:]
    # std_ascend,std_descend = R_Gr_std[:change_indices[0]+1],R_Gr_std[change_indices[0]:]
    # ax.set_xlabel('$V_{b}/d_b$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    # ax.set_xlabel('$V_{b}/d_t$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    # ax.set_xlabel('$E_{\perp}$ (Vnm$^{-1}$)'), ax.set_ylabel(r'$R_{Gr}$ (k$\Omega$)')
    # ax.set_xlim(-.105,.105)
    
    # ax.errorbar(E_ascend, ascend,yerr=std_ascend,color='r',marker='.',ms=3,label=r'$\rightarrow$',elinewidth=0)
    # ax.errorbar(E_descend, descend,yerr=std_descend,color='b',marker='.',ms=3,label=r'$\leftarrow$',elinewidth=0)
    # ax.legend(loc='upper left')
    # plt.savefig(file.replace('.txt','_{}_plot.png'.format(plot)),dpi=500)
    plt.show()
    

