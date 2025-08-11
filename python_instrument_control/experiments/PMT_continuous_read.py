# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 11:48:23 2025

@author: Prof. Wang
"""
from homemade_servers.H11890PMT import HamamatsuH11890
import matplotlib.pylab as plt
import time
import numpy as np
import os

def main(pmt,gate_time_ms,num_gates,file_save=None):
    counts = []
    gates = []

    plt.ion()
    fig, ax = plt.subplots()
    plt.show(block=False)
    try:
        fig.canvas.manager.window.raise_()  # Works on Qt
        fig.canvas.manager.window.activateWindow()
    except Exception as e:
        print("Window raise failed:", e)
    line, = ax.plot([], [], lw=2)
    ax.set_xlabel("Gate")
    ax.set_ylabel("Photon Count")

    pmt.set_hv(on=True)
    pmt.set_it(ms=gate_time_ms)
    if num_gates==0:
        rn=9999
    else:
        rn = num_gates
    pmt.set_rn(rn=rn)
    time.sleep(.5)
    pmt.start_counting()
    gate_num = 0
    try:
        while gate_num < rn:
            line, gates, counts = update(pmt, fig, ax, line, gates, counts)
            gate_num += 1
    except KeyboardInterrupt:
        print('stopped')
    finally:
        pmt.stop_counting()
        pmt.set_hv(on=False)
        plt.ioff()
        plt.show()
    gates_clean = np.array(gates)-np.array(gates[0])
    
    if file_save != None:
        if os.path.exists(file_save):
            while os.path.exists(file_save):     
                file_save = file_save.replace(".txt", "_new.txt")
            
        header = '# Num Gates = {}'.format(num_gates)
        header += '\n' + '# Gate time (ms) = {}'.format(gate_time_ms)
        with open(file_save, 'a') as file:
            file.write(header + '\n') 
            for g,c in zip(gates_clean,counts):
                file.write("{} {} \n".format(g,c))
        
    return gates_clean, counts

def update(pmt, fig, ax, line, gates, counts):
    try:
        gate, photons, is_old = pmt.read_data()
        if not is_old:
            gates.append(gate)
            counts.append(photons)

            # Keep only last 200 points
            # gates[:] = gates[-200:]
            # counts[:] = counts[-200:]

            line.set_data(gates, counts)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
    except RuntimeError:
        pass  # Handle PMT read errors gracefully
    return line, gates, counts

if __name__ == "__main__":
    pmt = HamamatsuH11890()
    try:
        gates,counts = main(pmt,gate_time_ms=200,num_gates=0)
        pmt.close()
        
    except:
        pmt.close()
