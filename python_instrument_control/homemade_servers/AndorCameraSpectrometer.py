import numpy as np
import pylablib as pll
from pylablib.devices import Andor
import logging
import time

class AndorCamSpec:
    def __init__(self, exposure=1.0, temperature=-85, n_avg=3, excitation_nm=632.8):
        pll.par["devices/dlls/andor_sdk2"] = 'C:/Program Files/Andor SDK'
        pll.par["devices/dlls/andor_shamrock"] = 'C:/Program Files/Andor SDK/Shamrock64'
        self.cam = Andor.AndorSDK2Camera(temperature=temperature,fan_mode='full',)
        self.spec = Andor.ShamrockSpectrograph()
        self.excitation_nm = excitation_nm
        self.n_avg = n_avg

        # Camera setup
        # we want the cooler to stay on when we do measurements, but we want it to turn off after. 
        # but we dont want it to turn off after each measurement. So we cannot close the connection each time.
        # this means i need to ammend the structure so servers aren't closed every time
        
        self.cam.set_cooler(True)
        self.cam.set_temperature(temperature)
        self.cam.set_exposure(exposure)
        self.cam.set_read_mode('fvb')
        self.cam.set_acquisition_mode('accum')
        logging.info('Connected to Andor CamSpec. Temp = ',self.cam.get_temperature())

    def close(self):
        self.cam.set_temperature(0) 
        while True:
            temp = self.cam.get_temperature()
            if temp >= -50:
                break
            time.sleep(2)
        self.cam.set_cooler(False)
        self.cam.close()
        self.spec.close()
        logging.info('Disconnecting from Andor CamSpec')
        
    def configure_spectrometer(self, grating=1, central_wl=550, slit_width=50):
        self.spec.set_grating(grating)
        self.spec.set_central_wavelength(central_wl)
        self.spec.set_slit_width(slit_width)

    def acquire_spectrum(self):
        spectra = [self.cam.get_spectrum() for _ in range(self.n_avg)]
        return np.mean(spectra, axis=0)

    def acquire_dark(self):
        input("Close shutter or block laser, then press Enter...")
        dark_frames = [self.cam.get_spectrum() for _ in range(self.n_avg)]
        return np.mean(dark_frames, axis=0)

    def wavelength_to_raman_shift(self, wavelengths_nm):
        excitation_cm = 1e7 / self.excitation_nm
        measured_cm = 1e7 / np.array(wavelengths_nm)
        return excitation_cm - measured_cm

    def run(self, subtract_dark=False):
        wavelengths = self.cam.get_wavelengths()
        spectrum = self.acquire_spectrum()

        if subtract_dark:
            dark = self.acquire_dark()
            spectrum -= dark

        raman_shift = self.wavelength_to_raman_shift(wavelengths)

        metadata = {
            "grating": self.spec.get_grating(),
            "central_wavelength": self.spec.get_central_wavelength(),
            "slit_width": self.spec.get_slit_width(),
            "exposure_time": self.cam.get_exposure_time(),
            "temperature": self.cam.get_temperature()
        }

        return raman_shift, spectrum, metadata
