# measurement_script.py
import numpy as np
import matplotlib.pyplot as plt
from homemade_servers.AndorCameraSpectrometer import AndorCamSpec
from homemade_servers.ThorlabsKCube import RotationMount
import toolbelt as tb
tb.init_plot_params()


def plot_raman(cam_spec, raman_shift, spectrum, raman_range_cm=(100, 3500)):
    mask = (raman_shift >= raman_range_cm[0]) & (raman_shift <= raman_range_cm[1])
    raman_filtered = raman_shift[mask]
    spectrum_filtered = spectrum[mask]

    #plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots(1,1,figsize=(6,5))
    
    ax.plot(raman_filtered, spectrum_filtered, color='b')
    ax.set_xlabel("Raman Shift (cm⁻¹)")
    ax.set_ylabel("Intensity (a.u.)")
    # fig.title(f"Raman Spectrum (Excitation: {cam_spec.excitation_nm} nm)")
    # plt.grid(True)
    plt.tight_layout()
    plt.show()



# Measurement

exposure_time = 1
averages = 10
angles = np.arange(0,200,20)


cam_spec = AndorCamSpec()
waveplate = RotationMount()

cam_spec.set_accumulations(averages)
cam_spec.set_exposure(exposure_time)

spectra, raman_shifts, metadatas = []

for angle in angles:
    
    waveplate.move_to(angle)
    
    raman_shift, spectrum, metadata = cam_spec.run(subtract_dark=False)
    
    spectra.append(spectrum)
    raman_shifts.append(raman_shift)
    metadatas.append(metadata)



# Plotting
plot_raman(cam_spec, raman_shift, spectrum, raman_range_cm=(100, 3000), metadata=metadata)

# Cleanup
# cam_spec.close()
