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


class LockInOE1022D():
    
    def __init__(self, port, name="SSI OE1022D"):
        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(port)
        self.instrument.read_termination = '\r'
        self.sensitivities = np.array(["1 nV/fA", "2 nV/fA", "5 nV/fA", "10 nV/fA", "20 nV/fA", "50 nV/fA", "100 nV/fA", "200 nV/fA", "500 nV/fA",
                         "1 uV/pA", "2 uV/pA", "5 uV/pA", "10 uV/pA", "20 uV/pA", "50 uV/pA", "100 uV/pA", "200 uV/pA", "500 uV/pA",
                         "1 mV/nA", "2 mV/nA", "5 mV/nA", "10 mV/nA", "20 mV/nA", "50 mV/nA", "100 mV/nA", "200 mV/nA", "500 mV/nA",
                         "1 V/uA"])
        self.parameters = np.array(["X","Y","R","theta","Frequency","Xh1","Yh1","Rh1","thetah1",
                      "Xh2","Yh2","Rh2","thetah2", "Noise","A1","A2","A3","A4","E1","E2","E3","E4"])
        
         #channels: 1 is channel A. 2 is channle B 
    
    def query_lockin(self, channel, parameter='sensitivity'):
        if parameter=='sensitivity':
            command = 'SENSD? '+str(channel)+';'
        if parameter=='harmonic1':
            command = 'HARMD? '+str(channel)+',1;'
        query = self.instrument.query(command).split('\x00')[-1]
        return query
    
    def set_sensitivity(self,channels=[1,2],sensitivities=["5 mV/nA","200 uV/pA"]):
        for chan,sensitivity in zip(channels,sensitivities):
            sensd_index = str(np.where(self.sensitivities==sensitivity)[0][0])
            command = "SENSD " + str(chan) + ", " + sensd_index+';'
            self.instrument.write(command)
        
    def set_harmonic(self,channel,harmonic,harmonic_port="1"):
        command = "HARMD " + str(channel) + " " + harmonic_port + "_" + str(harmonic) + ';'
        self.instrument.write(command)
    
    def autophase(self,channels=[1,2]):
        for chan in channels:
            command = "APHSD "+ str(chan) + ';'
            self.instrument.write(command)
        

    def reset_buffer(self,channels=[1,2]):
        for chan in channels:
            command = "RESTD " + str(chan) + ';'
            self.instrument.write(command)


    def read_data(self,channel, params=["R","theta"],num_avgs=100):
        data_list = []
        param_list = []
        command = "SNAPD? "+str(channel)
        parameters = np.array(["X","Y","R","theta","Frequency","Xh1","Yh1","Rh1","thetah1",
                      "Xh2","Yh2","Rh2","thetah2", "Noise","A1","A2","A3","A4","E1","E2","E3","E4"])
        # print(command)
        for x in params:
            # print(command)
            param = str(np.where(parameters==x)[0][0])
            command = command+","+param
            # print(command)
        command = command+';'
        # print(command)
        for i in range(num_avgs):
            data= self.instrument.query(command).split('\x00')[-1]
            data_list.append(data)
        return data_list
# def open_lockin(port):
#     rm = pyvisa.ResourceManager()
#     lockin = rm.open_resource(port)
#     lockin.read_termination = '\r'
#     return lockin

# def query_lockin(instrument, channel,parameter='sensitivity'):
#     if channel == "A":
#         chan = "1"
#     if channel =="B":
#         chan = "2"    
#     if parameter=='sensitivity':
#         command = 'SENSD? '+chan+';'
#     if parameter=='harmonic1':
#         command = 'HARMD? '+chan+',1;'
#     instrument.query(command).split('\x00')[-1]

# def sensd_command(channel,sensitivity):
#     if channel == "A":
#         chan = "1"
#     if channel =="B":
#         chan = "2"
#     sensitivities = np.array(["1 nV/fA", "2 nV/fA", "5 nV/fA", "10 nV/fA", "20 nV/fA", "50 nV/fA", "100 nV/fA", "200 nV/fA", "500 nV/fA",
#                      "1 uV/pA", "2 uV/pA", "5 uV/pA", "10 uV/pA", "20 uV/pA", "50 uV/pA", "100 uV/pA", "200 uV/pA", "500 uV/pA",
#                      "1 mV/nA", "2 mV/nA", "5 mV/nA", "10 mV/nA", "20 mV/nA", "50 mV/nA", "100 mV/nA", "200 mV/nA", "500 mV/nA",
#                      "1 V/uA"])
#     sensd_index = str(np.where(sensitivities==sensitivity)[0][0])
#     command = "SENSD " + chan + ", " + sensd_index+':'
#     return command
    
    
    
# def harmd_command(channel,harmonic,harmonic_port="1"):
#     if channel == "A":
#         chan = "1"
#     if channel =="B":
#         chan = "2"
#     command = "HARMD " + chan + " " + harmonic_port + "_" + str(harmonic)
#     return command
    

# def restd_command(channel):
#     if channel == "A":
#         chan = "1"
#     if channel =="B":
#         chan = "2"
#     command = "RESTD " + chan
#     return command


# def read_data_command(channel, params=["R","theta"]):
#     if channel == "A":
#         chan = "1"
#     if channel =="B":
#         chan = "2"
#     param_list = []
#     command = "SNAPD "+chan
#     parameters = np.array(["X","Y","R","theta","Frequency","Xh1","Yh1","Rh1","thetah1",
#                   "Xh2","Yh2","Rh2","thetah2", "Noise","A1","A2","A3","A4","E1","E2","E3","E4"])
#     for x in params:
#         param = str(np.where(parameters==x)[0][0])
#         param_list.append(" "+param)
#         command = command+" "+param
#     return command