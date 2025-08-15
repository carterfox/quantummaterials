# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 12:37:29 2025

@author: Prof. Wang
"""

import matplotlib.pyplot as plt
import numpy as np
import time

def run_experiment():
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    line, = ax.plot([], [], 'b-')

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1)

    for i in range(10):
        x_data.append(i)
        y_data.append(np.random.rand())

        line.set_xdata(x_data)
        line.set_ydata(y_data)

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()

        time.sleep(0.1)

    plt.ioff()
    plt.show()

run_experiment()