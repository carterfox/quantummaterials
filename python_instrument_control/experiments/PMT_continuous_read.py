# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 11:48:23 2025

@author: Prof. Wang
"""
from homemade_servers.H11890PMT import HamamatsuH11890
import matplotlib.pylab as plt
import time

def update(pmt, fig, ax, line, gates, counts, first_flag):
    try:
        gate, photons, is_old = pmt.read_data()
        if not is_old:
            if first_flag[0]:
                first_flag[0] = False
                return line, gates, counts
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
    return line, gates, counts

def run_continuous_pmt_plot(pmt,gate_time_ms):
    counts = []
    gates = []
    first_flag = [True]

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlabel("Gate")
    ax.set_ylabel("Photon Count")

    pmt.set_hv(on=True)
    pmt.set_it(ms=gate_time_ms)
    pmt.set_rn(rn=9999)
    pmt.start_counting()

    try:
        while True:
            line, gates, counts = update(pmt, fig, ax, line, gates, counts, first_flag)
    except KeyboardInterrupt:
        pmt.stop_counting()
        pmt.set_hv(on=False)
    finally:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    pmt = HamamatsuH11890()
    run_continuous_pmt_plot(pmt,gate_time_ms=100)
    pmt.close()
