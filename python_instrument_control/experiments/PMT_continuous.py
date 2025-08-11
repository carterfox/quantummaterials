# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 11:48:23 2025

@author: Prof. Wang
"""
from homemade_servers.H11890PMT import HamamatsuH11890
import matplotlib.pylab as plt
import time

def update():
    global first
    try:
        gate, photons, is_old = pmt.read_data()
        if not is_old:
            if first:
                first = False
                return line,
            gates.append(gate)
            counts.append(photons)

            # Keep only last 200 points
            gates[:] = gates[-200:]
            counts[:] = counts[-200:]

            line.set_data(gates, counts)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
    except RuntimeError:
        pass  # Handle PMT read errors gracefully
    return line,

if __name__ == "__main__":
    
    first = True
    counts = []
    gates = []
    
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlabel("Gate")
    ax.set_ylabel("Photon Count")
    
    pmt = HamamatsuH11890()
    pmt.set_hv(on=True)
    
    pmt.set_it(ms=200)
    pmt.set_rn(rn=100)  # Large number for continuous mode
    pmt.start_counting()
    
    try:
        while True:
            update()
    except KeyboardInterrupt:
        pmt.stop_counting()
        print("Stopped.")
    
    pmt.stop_counting()
    
    plt.ioff()
    plt.show()
    
    pmt.set_hv(on=False)
    pmt.close()

