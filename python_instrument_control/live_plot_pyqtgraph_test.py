import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import numpy as np
import sys

# Create application
app = QtWidgets.QApplication(sys.argv)

# Create a window and plot widget
win = pg.GraphicsLayoutWidget(title="Live Plot")
win.show()

# Bring window to front
win.raise_()                     # Raise above other windows
win.activateWindow()             # Request focus
win.setWindowState(QtCore.Qt.WindowActive)  # Ensure it's active

plot = win.addPlot(title="Real-Time Sine Wave")
curve = plot.plot(pen='y')

# Timer-based update
data = np.linspace(0, 2*np.pi, 100)
i = 0

def update():
    global i
    y = np.sin(data + i * 0.1)
    curve.setData(data, y)
    i += 1

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

sys.exit(app.exec_())
