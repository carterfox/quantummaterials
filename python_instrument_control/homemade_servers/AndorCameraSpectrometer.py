import numpy as np
import pylablib as pll
from pylablib.devices import Andor

import logging
import time

class AndorCamSpec:
    def __init__(self, exposure=1.0, temperature=-85, accumulations=3, excitation_nm=632.8):
        pll.par["devices/dlls/andor_sdk2"] = 'C:/Program Files/Andor SDK'
        pll.par["devices/dlls/andor_shamrock"] = 'C:/Program Files/Andor SDK/Shamrock64'
        self.cam = Andor.AndorSDK2Camera(temperature=temperature,fan_mode='full')
        self.spec = Andor.ShamrockSpectrograph()

        self.excitation_nm = excitation_nm
        self.central_wavelength = 550
        self.grating = 3
        self.configure_spectrometer(grating=self.grating, central_wl=self.central_wavelength)
        self.accumulations = accumulations
        self.set_exposure(exposure)

        # Camera setup
        # we want the cooler to stay on when we do measurements and only turn off after 
        # all the measurements are done and we decide it is time to turn it off.
        # To accomplish that, the control panel has 'open_instruments' and leave_servers_open' booleans
        # that ask if the servers should be left opened and if they should be left open.
        self.cam.set_cooler(True)
        self.cam.set_temperature(temperature)
        
        self.cam.set_read_mode('fvb')
        self.cam.set_acquisition_mode("kinetic series")
        self.cam.set_number_kinetic_series_images(self.accumulations)
        logging.info('Connected to Andor CamSpec. Temp = ',self.cam.get_temperature())

    def close(self):
        self.cam.set_temperature(0) 
        while True:
            temp = self.cam.get_temperature()
            if temp >= -50: break
            time.sleep(2)
        self.cam.set_cooler(False)
        self.cam.close()
        self.spec.close()
        logging.info('Disconnecting from Andor CamSpec')
        
    def set_exposure(self,exposure_time):
        self.cam.set_exposure(exposure_time)
        
    def read_multiple_images(self,rng=None):
        self.cam.read_multiple_images(rng)
        
    def set_accumulations(self,accumulations):
        self.accumulations = accumulations
        self.cam.set_number_kinetic_series_images(self.accumulations)
    
    def configure_spectrometer(self, grating=3, central_wl=550):
        self.spec.set_grating(grating)
        self.spec.set_central_wavelength(central_wl)
        self.spec.setup_pixels_from_camera(self.cam)
        self.wavelengths = self.spec.get_calibration()
        self.raman_shifts = self.wavelength_to_raman_shift(self.wavelengths)
        # self.spec.set_slit_width(slit_width)
    
    def wavelength_to_raman_shift(self, wavelengths_nm):
        excitation_cm = 1e7 / self.excitation_nm
        measured_cm = 1e7 / np.array(wavelengths_nm)
        return excitation_cm - measured_cm

    def get_metadata(self):
        metadata = { "grating": self.spec.get_grating(), 
                    "central_wavelength": self.spec.get_central_wavelength(),
                    "slit_width": self.spec.get_slit_width(),
                    "temperature": self.cam.get_temperature(),
                    "exposure_time": self.cam.get_exposure_time(),
                    "kinetic mode params (num_cycle, cycle_time, num_acc, cycle_time_acc, num_prescan)": self.cam.get_kinetic_mode_parameters()
                    }
        return metadata
        
    # def remove_spikes(self,data):
        #insert later... 
        # return filtered_data

    
    
    
    
