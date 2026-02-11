# file: raman_basic.py

import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.ThorlabsKCube import RotationMount
from homemade_servers.KeithleySourceMeter import KeithleySourceMeter
import toolbelt as tb
import time
import os 

tb.init_plot_params()

def angle_sweep(cam_spec: AndorCamSpec, waveplate: RotationMount, exposure_time, averages, angles, polarization='POL', save_path=None):
    """
    Performs a Raman measurement sweep. 
    Optimized for consecutive measurements: skips motor delays if angle hasn't changed.
    """
    cam_spec.set_exposure(exposure_time)
    
    # Use the provided save_path, or fall back to default if None
    if save_path is None:
        save_dir = r'D:\LabData\XiaoWang_Group_data_2024on\Hongrui\Raman\collabration\Zizhong\D3\2k\d_raman_map_xy_240s'
    else:
        save_dir = save_path

    os.makedirs(save_dir, exist_ok=True)
    
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
    previous_angle = None # To track the last angle and avoid redundant moves

    for i, angle in enumerate(angles):
        
        # --- OPTIMIZATION 1: Only move motor if the angle actually changes ---
        if waveplate:
            if angle != previous_angle:
                print(f"\nMoving to {angle}°...")
                waveplate.move_to(angle)
                # We only check position when we actually move to save time
                current_pos = waveplate.get_pos()
                print(f"Move complete. Current position: {current_pos:.2f}°")
                previous_angle = angle
            else:
                # If angle is the same, skip the communication delay
                print(f"\nAngle unchanged ({angle}°). Skipping motor move.")

        print(f"Acquiring {averages} frames at {exposure_time}s exposure...")
        collected_frames = []
        for j in range(averages):
            data = cam_spec.acquire_image()
            collected_frames.append(data)
            
        frames_array = np.array(collected_frames)    
        summed_spectrum = np.sum(frames_array, axis=0)
        
        if raman_shift_axis is None:
            raman_shift_axis = np.arange(len(summed_spectrum))
            
        ax.plot(raman_shift_axis, summed_spectrum, label=f'{angle}° ({i+1})')
        # ax.legend() # Optional: Comment out if legend gets too crowded/slow
        
        # --- OPTIMIZATION 2: Non-blocking plot update ---
        # plt.pause(0.01)  <-- Removed this slow pause
        fig.canvas.draw()
        fig.canvas.flush_events() 

        all_data.append(collected_frames)
        summed_spectra_data.append(summed_spectrum)
        
        try:
            # Filename includes index 'i' to prevent overwriting
            filename = f"D3_PtPrT_D_{angle}_{polarization}_{i}.txt"
            full_path = os.path.join(save_dir, filename)
            
            data_to_save = np.column_stack((raman_shift_axis, summed_spectrum))
            np.savetxt(full_path, data_to_save, delimiter='\t', header='Raman Shift (cm-1)\tCounts')
            
            print(f"✅ Saved: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving data for {angle}°: {e}")

    # Return to initial position only if we actually moved significantly
    # (Optional: you can comment this out if you want to stay at the last angle)
    if waveplate and initial_pos is not None and previous_angle != initial_pos:
        print(f"\nSweep finished. Moving back to initial position ({initial_pos:.2f}°)...")
        waveplate.move_to(initial_pos)
        print("Move complete.")

    print("\nAll measurements complete.")
    plt.ioff()
    plt.show()
    
    return all_data, summed_spectra_data

def dual_gap_raman_map_NOTTESTED(cam_spec: AndorCamSpec,keithley_x: KeithleySourceMeter, keithley_y: KeithleySourceMeter, Vx_array, Vy_array, exposure_time, averages, save_path=None):
    
    if save_path is None:
        save_dir = r'D:\LabData\XiaoWang_Group_data_2024on\Hongrui\Raman\collabration\Zizhong\D3\2k\d_raman_map_xy_240s'
    else:
        save_dir = save_path

    os.makedirs(save_dir, exist_ok=True)
    
    keithley_x.enable_source()
    keithley_y.enable_source()
    keithley_x.apply_voltage(compliance_current=keithley_x.compliance_current)
    keithley_y.apply_voltage(compliance_current=keithley_y.compliance_current)
    
    cam_spec.set_exposure(exposure_time)
    all_data = []
    avg_spectra_data = []
    
    for Vx,Vy in zip(Vx_array,Vy_array):
                
        keithley_x.source_voltage = Vx
        keithley_y.source_voltage = Vy
        
        Ix_meas = 10**9 * keithley_x.measure_current_avg(10)
        Iy_meas = 10**9 * keithley_y.measure_current_avg(10)
        
        time.sleep(.1)
        
        collected_frames = []
        
        for j in range(averages):
            data = cam_spec.acquire_image()
            collected_frames.append(data)
        frames_array = np.array(collected_frames)    
        avg_spectrum = np.average(frames_array, axis=0)
        raman_shift_axis = np.arange(len(avg_spectrum))
        
        all_data.append(frames_array)
        avg_spectra_data.append(avg_spectrum)
        
        try:
            # Filename includes index 'i' to prevent overwriting
            Vxstr = str(round(Vx,3)).replace('-','m').reaplce('.','p')
            Vystr = str(round(Vy,3)).replace('-','m').reaplce('.','p')
            filename = "2dmapping_Vx_"+Vxstr+"_Vy_"+Vystr+".txt"
            full_path = os.path.join(save_dir, filename)
            
            data_to_save = np.column_stack((raman_shift_axis, avg_spectrum))
            np.savetxt(full_path, data_to_save, delimiter='\t', header='Raman Shift (cm-1)\tCounts')
            
            print(f"✅ Saved: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving data for Vx={Vx} , Vy={Vy}°: {e}")
        
        