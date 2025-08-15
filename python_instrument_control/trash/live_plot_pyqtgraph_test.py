import pyqtgraph as pg
from PyQt5 import QtWidgets
import numpy as np
import sys
import time

# Create application and window
app = QtWidgets.QApplication(sys.argv)
win = pg.GraphicsLayoutWidget(show=True, title="Live Updating Plots")

# === Plot 1: Scatter Only ===
plot1 = win.addPlot(title="Plot 1: Scatter Only")
scatter1 = pg.ScatterPlotItem(symbol='o', brush='b', size=10)
plot1.addItem(scatter1)

# === Plot 2: Scatter + Line ===
win.nextRow()
plot2 = win.addPlot(title="Plot 2: Scatter + Line")
line2 = plot2.plot(pen='r')
scatter2 = pg.ScatterPlotItem(symbol='t', brush='g', size=12)
plot2.addItem(scatter2)

# === Live Update Loop ===
x = np.linspace(0, 10, 100)
for i in range(100):
    # Generate new data
    y1 = np.sin(x + i * 0.1)
    y2 = np.cos(x + i * 0.1)

    # Update Plot 1 (scatter only)
    scatter1.setData(x[::5], y1[::5])  # downsample for clarity

    # Update Plot 2 (line + scatter)
    line2.setData(x, y2)
    scatter2.setData(x[::10], y2[::10])  # fewer points for scatter

    # Process GUI events and pause
    QtWidgets.QApplication.processEvents()
    time.sleep(0.1)

sys.exit(app.exec_())
