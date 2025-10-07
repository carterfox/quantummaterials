# measurement_script.py
import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.ThorlabsKCube import RotationMount
import toolbelt as tb
import time
tb.init_plot_params()


exposure_time = 1
averages = 10
angles = np.arange(0,200,20)

cam_spec = AndorCamSpec()
waveplate = RotationMount()

cam_spec.set_accumulations(averages)
cam_spec.set_exposure(exposure_time)
raman_shifts = cam_spec.raman_shifts
raman_range_cm = (10,600)
mask = (raman_shifts >= raman_range_cm[0]) & (raman_shifts <= raman_range_cm[1])


plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([],[])
line.set_xdata(raman_shifts[mask])
ax.set_title("Live Summed Spectrum")
ax.set_xlabel("Raman Shift (cm$^{-1}$)"),ax.set_ylabel("Counts")
ax.grid(True)


for angle in angles:
    
    waveplate.move_to(angle)
    collected_frames = []
    
    while len(collected_frames) < averages:
        frames = cam_spec.read_multiple_images(timeout=1)
        if frames: 
            collected_frames.extend(frames)
            frames_array = np.array(collected_frames)    
            summed_spectrum = np.sum(frames_array, axis=0)
            line.set_ydata(summed_spectrum[mask])
            ax.relim()
            ax.autoscale_view()
        else: 
            time.sleep(0.1) # no new frames yet, wait a bit
    

plt.ioff()
plt.show()
# Cleanup
# cam_spec.cam.abort_acquisition()
# cam_spec.close()
