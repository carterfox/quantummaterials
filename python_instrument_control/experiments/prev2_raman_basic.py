# file: raman_basic.py

import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.ThorlabsKCube import RotationMount
import toolbelt as tb
import time
import os # <-- Import the os module for path operations

tb.init_plot_params()


# --- CHANGE 1: Add a 'polarization' argument to the function ---
def angle_sweep(cam_spec: AndorCamSpec, waveplate: RotationMount, exposure_time, averages, angles, polarization='POL'):
    """
    Performs a Raman measurement sweep, plotting each result and saving it to a .txt file.
    """
    cam_spec.set_exposure(exposure_time)
    
    # --- CHANGE 2: Define the save path and create the directory ---
    save_dir = r'C:\Users\Public\OneDrive\Desktop\TAI8'
    os.makedirs(save_dir, exist_ok=True) # This creates the folder if it doesn't exist
    
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title(f"Angle-Dependent Raman Spectra ({polarization})")
    ax.set_xlabel("Raman Shift (cm$^{-1}$)")
    ax.set_ylabel("Counts")
    ax.grid(True)
    
    all_data = []
    summed_spectra_data = []
    
    initial_pos = None
    if waveplate:
        initial_pos = waveplate.get_pos()
        print(f"Rotation mount connected. Initial position: {initial_pos:.2f}°")

    print(f"\nStarting Raman sweep from {angles[0]}° to {angles[-1]}°...")
    
    raman_shift_axis = None

    for angle in angles:
        
        if waveplate:
            print(f"\nMoving to {angle}°...")
            waveplate.move_to(angle)
            current_pos = waveplate.get_pos()
            print(f"Move complete. Current position: {current_pos:.2f}°")

        print(f"Acquiring {averages} frames at {exposure_time}s exposure...")
        collected_frames = []
        for i in range(averages):
            data = cam_spec.acquire_image()
            collected_frames.append(data)
            
        frames_array = np.array(collected_frames)    
        summed_spectrum = np.sum(frames_array, axis=0)
        
        if raman_shift_axis is None:
            raman_shift_axis = np.arange(len(summed_spectrum))
            
        ax.plot(raman_shift_axis, summed_spectrum, label=f'{angle}°')
        ax.legend()
        plt.pause(0.01)

        all_data.append(collected_frames)
        summed_spectra_data.append(summed_spectrum)
        
        # --- CHANGE 3: Format the data and save it to a file ---
        try:
            filename = f"TAI_{angle}_{polarization}.txt"
            full_path = os.path.join(save_dir, filename)
            
            # Stack the Raman shift (x-axis) and Counts (y-axis) into two columns
            data_to_save = np.column_stack((raman_shift_axis, summed_spectrum))
            
            # Save the data as a tab-delimited text file with a header
            np.savetxt(full_path, data_to_save, delimiter='\t', header='Raman Shift (cm-1)\tCounts')
            
            print(f"✅ Data for {angle}° saved successfully to {full_path}")
            
        except Exception as e:
            print(f"❌ Error saving data for {angle}°: {e}")

    if waveplate and initial_pos is not None:
        print(f"\nSweep finished. Moving back to initial position ({initial_pos:.2f}°)...")
        waveplate.move_to(initial_pos)
        print("Move complete.")

    print("\nAll measurements complete.")
    plt.ioff()
    plt.show()
    
    return all_data, summed_spectra_data