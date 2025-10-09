import numpy as np
from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors
import logging
import time
import pylablib as pll
from pylablib.devices import Andor


class AndorCamSpec:
    def __init__(self, exposure=1.0, temperature=-85, accumulations=3, excitation_nm=632.8):
        pll.par["devices/dlls/andor_sdk2"] = 'C:/Program Files/Andor SDK'
        pll.par["devices/dlls/andor_shamrock"] = 'C:/Program Files/Andor SDK/Shamrock64'
        
        self.sdk = atmcd()  # Load the atmcd library
        self.codes = atmcd_codes
        ret = self.sdk.Initialize("") 
        (ret, iSerialNumber) = self.sdk.GetCameraSerialNumber()
        ret = self.sdk.CoolerON()
        ret = self.sdk.SetTemperature(temperature)
        ret = self.sdk.SetAcquisitionMode(self.codes.Acquisition_Mode.SINGLE_SCAN)
        ret = self.sdk.SetReadMode(self.codes.Read_Mode.FULL_VERTICAL_BINNING)
        ret = self.sdk.SetTriggerMode(self.codes.Trigger_Mode.INTERNAL)
        ret = self.sdk.SetVSSpeed(2)
        (ret, self.xpixels, self.ypixels) = self.sdk.GetDetector()
        
        self.spec = Andor.ShamrockSpectrograph(0)
        self.excitation_nm = excitation_nm
        self.central_wavelength = 644.21e-9
        self.grating = 3
        self.configure_spectrometer(grating=self.grating, central_wl=self.central_wavelength)
        self.accumulations = accumulations
        # Camera setup
        # we want the cooler to stay on when we do measurements and only turn off after 
        # all the measurements are done and we decide it is time to turn it off.
        # To accomplish that, the control panel has 'open_instruments' and leave_servers_open' booleans
        # that ask if the servers should be left opened and if they should be left open.
        # logging.info('Connected to Andor CamSpec. Temp = ',self.sdk.GetTemperature())

    def close(self):
        self.spec.close()
        self.sdk.ShutDown()
        logging.info('Disconnecting from Andor CamSpec')
        
    def set_exposure(self,exposure_time):
        self.sdk.SetExposureTime(exposure_time)
        
    def acquire_image(self):
        self.sdk.PrepareAcquisition()
        self.sdk.StartAcquisition()
        self.sdk.WaitForAcquisition()
        ret, fullFrameBuffer = self.sdk.GetMostRecentImage(self.xpixels)
        return np.ctypeslib.as_array(fullFrameBuffer)
    
    def acquire_multiple_images(self,num_images):
        images =[]
        for i in range(num_images):
            data = self.acquire_image()
            images.append(data)
        return images
    
    def configure_spectrometer(self, grating=3, central_wl=644.21e-9):
        self.spec.set_grating(grating)
        self.spec.set_wavelength(central_wl)
        re,detx,dety= self.sdk.GetDetector()
        (ret,xsize,ysize) = self.sdk.GetPixelSize()
        self.spec.set_pixel_width(xsize)
        self.spec.set_number_pixels(detx)
        # self.wavelengths = self.spec.get_calibration()
        # self.raman_shifts = self.wavelength_to_raman_shift(self.wavelengths)
        # self.spec.set_slit_width(slit_width)
    
    def wavelength_to_raman_shift(self, wavelengths_nm):
        excitation_cm = 1e7 / self.excitation_nm
        measured_cm = 1e7 / np.array(wavelengths_nm)
        return excitation_cm - measured_cm

        
    # def remove_spikes(self,data):
        #insert later... 
        # return filtered_data

    
    
    
    
