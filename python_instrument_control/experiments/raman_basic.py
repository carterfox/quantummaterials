# measurement_script.py
import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.ThorlabsKCube import RotationMount
import toolbelt as tb
import time
tb.init_plot_params()




def angle_sweep(cam_spec: AndorCamSpec, waveplate: RotationMount, exposure_time,averages,angles):
    cam_spec.set_exposure(exposure_time)

    # raman_shifts = cam_spec.raman_shifts
    # raman_range_cm = (10,600)
    # mask = (raman_shifts >= raman_range_cm[0]) & (raman_shifts <= raman_range_cm[1])
    
    
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    line, = ax.plot([],[])
    # print(cam_spec.wavelengths)
    line.set_xdata(np.arange(0,2000,1))
    ax.set_title("Live Summed Spectrum")
    ax.set_xlabel("Raman Shift (cm$^{-1}$)"),ax.set_ylabel("Counts")
    ax.grid(True)
    
    all_data = []
    summed_spectra_data = []
    
    for angle in angles:
        
        # waveplate.move_to(angle)
        collected_frames = []
        
        for i in range(averages):
            data = cam_spec.acquire_image()
            collected_frames.append(data)
            frames_array = np.array(collected_frames)    
            summed_spectrum = np.sum(frames_array, axis=0)
            line.set_ydata(summed_spectrum)
            ax.relim()
            ax.autoscale_view()
            
        all_data.append(collected_frames)
        summed_spectra_data.append(summed_spectrum)
    
    plt.ioff()
    plt.show()
    
    return all_data, summed_spectra_data
# Cleanup
# cam_spec.cam.abort_acquisition()
# cam_spec.close()
