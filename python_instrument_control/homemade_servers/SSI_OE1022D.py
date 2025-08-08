#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:27:27 2024

@author: carterfox

read data from lock in amp 
"""


import numpy as np
import os
import pyvisa
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LockInOE1022D():
    
    def __init__(self, resource_name="ASRL12::INSTR"):
        
        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(resource_name)
        self.instrument.baud_rate = 9600
        self.instrument.timeout = 2000
        self.instrument.read_termination = '\r' 
        self.instrument.write_termination = '\r'
        self.sensitivities = np.array(["1 nV", "2 nV", "5 nV", "10 nV", "20 nV", "50 nV", "100 nV", "200 nV", "500 nV",
                         "1 uV", "2 uV", "5 uV", "10 uV", "20 uV", "50 uV", "100 uV", "200 uV", "500 uV",
                         "1 mV", "2 mV", "5 mV", "10 mV", "20 mV", "50 mV", "100 mV", "200 mV", "500 mV","1 V"])
        self.parameters = np.array(["X","Y","R","theta","Frequency","Xh1","Yh1","Rh1","thetah1","Xh2","Yh2","Rh2","thetah2", "Noise","A1","A2","A3","A4","E1","E2","E3","E4"])
        self.R_chan = 1 #channels: 1 is channel A. 2 is channel B 
        self.dR_chan = 2
        self.num_avgs = 150
        logging.info("Connected to OE1022D LockIn")     
        
    # --- Generic Commands ---
    def query(self, command):
        try:
            return self.instrument.query(command)
        except Exception as e:
            logging.error(f"Query error: {e}")
            return None

    def write(self, command):
        try:
            self.instrument.write(command)
        except Exception as e:
            logging.error(f"Write error: {e}")

    def close(self):
        logging.info("Disconnecting from OE1022D LockIn")
        self.instrument.close()

    def identify(self):
        return self.query("*IDND?")    

    # --- Data Reading and storage ---
    def read_single(self, channel=1, param=2):
        """Read a single parameter (e.g., R, X, Y, θ)"""
        raw = self.query(f"OUTPD? {channel},{param}")
        clean = float(raw.replace('\x00','').strip())
        return clean

    def read_multiple(self, channel=1, params=[0, 1, 2, 3]):
        """Read multiple parameters simultaneously"""
        param_str = ",".join(map(str, params))
        raw = self.query(f"SNAPD? {channel},{param_str}")
        clean = raw.replace('\x00','').strip()#.split(','),dtype=float)
        return clean
    
        
    def read_average_dual(self, params=[0, 1, 2, 3], num_avgs=100, delay=0.02):
        """
        Read and average multiple measurements from both channels.
        Returns:
            - mean_R_chan, std_R_chan: mean and std for R channel parameters
            - mean_dR_chan, std_dR_chan: mean and std for dR channel parameters 
        """
        data_R_chan = []
        data_dR_chan = []
    
        for _ in range(num_avgs):
            try:
                values_R_chan = self.read_multiple(self.R_chan, params)
                values_dR_chan = self.read_multiple(self.dR_chan, params)
                if values_R_chan:
                    data_R_chan.append([float(v) for v in values_R_chan.strip().split(',')])
                if values_dR_chan:
            except Exception as e:
                logging.error(f"Error reading data: {e}")
            time.sleep(delay)
    
        mean_R_chan = np.mean(data_R_chan, axis=0) if data_R_chan else None
        std_R_chan = np.std(data_R_chan, axis=0) if data_R_chan else None
        mean_dR_chan = np.mean(data_dR_chan, axis=0) if data_dR_chan else None
        std_dR_chan = np.std(data_dR_chan, axis=0) if data_dR_chan else None
    
        return mean_R_chan, std_R_chan, mean_dR_chan, std_dR_chan
    
    def reset_buffer(self,channels=[1,2]):
        for chan in channels:
            self.write(f"RESTD {chan}")
            logging.info(f"Buffer reset: Channel {chan}")
    
    # --- Auto Configuration ---
    
    def auto_scale(self, channel=1):
        self.write(f"ASCLD {channel}")
        logging.info(f"Auto scale: Channel {channel}")
        
    def auto_gain(self, channel=1):
        self.write(f"AGAND {channel}")
        logging.info(f"Auto gain: Channel {channel}")

    def auto_reserve(self, channel=1):
        self.write(f"ARSVD {channel}")
        logging.info(f"Auto reserve: Channel {channel}")

    def auto_phase(self, channel=1):
        self.write(f"APHSD {channel}")
        logging.info(f"Auto phase: Channel {channel}")

    def auto_phase_all(self):
        self.auto_phase(1)
        self.auto_phase(2)
        logging.info("Auto phase applied to both channels")
        
    # --- Configuration ---
    
    def set_reference_source(self, channel=1, mode=1):
        self.write(f"FMODD {channel},{mode}")
        logging.info(f"Reference source set: Channel {channel}, Mode {mode}")

    def set_reference_frequency(self, channel=1, freq_hz=1000):
        self.write(f"FREQD {channel},{freq_hz}")
        logging.info(f"Reference frequency set: Channel {channel}, {freq_hz} Hz")

    def set_phase_shift(self, channel=1, degrees=0.0):
        self.write(f"PHASD {channel},{degrees}")
        logging.info(f"Phase shift set: Channel {channel}, {degrees}°")

    def set_sensitivity(self, channel=1, sensitivity="5 mV"):
        """Index from 0 to 27 (see manual for mapping)"""
        if sensitivity in self.sensitivities:
            index = str(np.where(self.sensitivities == sensitivity)[0][0])
            self.write(f"SENSD {channel},{index}")
            logging.info(f"Sensitivity set: Channel {channel}, {sensitivity}")
        else:
            logging.warning(f"Invalid sensitivity: {sensitivity}")

    def set_time_constant(self, channel=1, index=13):
        self.write(f"OFLTD {channel},{index}")
        logging.info(f"Time constant set: Channel {channel}, Index {index}")

    def set_filter_slope(self, channel=1, db_per_oct=3):
        self.write(f"OFSLD {channel},{db_per_oct}")
        logging.info(f"Filter slope set: Channel {channel}, {db_per_oct} dB/oct")
    

    def set_sync_filter(self, channel=1, enable=True):
        self.write(f"SYNCD {channel},{1 if enable else 0}")
        logging.info(f"Sync filter {'enabled' if enable else 'disabled'}: Channel {channel}")

    def set_harmonic(self, channel=1, slot=1, order=3):
        self.write(f"HARMD {channel},{slot},{order}")
        logging.info(f"Harmonic set: Channel {channel}, Slot {slot}, Order {order}")
        
    def set_sine_output(self, channel=1, amplitude_v=1.0, offset_v=0.0, waveform_type=0):
        """
        Configure the SINE OUT signal using SLVLD, SVLLD, and SWVTD commands.
    
        Parameters:
            channel (int): Channel number (1 or 2)
            amplitude_v (float): Peak amplitude in volts
            offset_v (float): DC offset in volts
            waveform_type (int): 0 = sine, 1 = square, 2 = triangle (if supported)
        """
        try:
            self.write(f"SLVLD {channel},{amplitude_v}")
            self.write(f"SVLLD {channel},{offset_v}")
            self.write(f"SWVTD {channel},{waveform_type}")
            logging.info(f"SINE OUT configured: Channel {channel}, Amplitude={amplitude_v} V, Offset={offset_v} V, Waveform={waveform_type}")
        except Exception as e:
            logging.error(f"Error configuring SINE OUT: {e}")
        