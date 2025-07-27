#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 12:49:24 2024

@author: carterfox
keithley functions
"""

import numpy as np
import os
import pymeasure as pym



def reset(client):
    client.reset()
    
def front_terminals(client):
    client.use_front_terminals()
    
def wires(client,num_wires=2):
    client.wires = num_wires


def set_compliance(client, current=None,voltage=None):
    if current != None:
        client.compliance_current = current
    if voltage != None:
        client.compliance_voltage = voltage


def turn_on(client):
    client.enable_source()

def turn_off(client):
    client.disable_source()
    
def read_current(client):
    return client.mean_current(), client.std_current()

def read_voltage(client):
    return client.mean_voltage(), client.std_voltage()

def read_resistance(client):
    return client.mean_resistance(), client.std_resistance()

def read_all(client):
    return client.means(), client.standard_devs()
    
def config_current_meas(client):
    client.measure_current() 
    
def config_voltage_meas(client):
    client.measure_voltage() 

def config_resistance_meas(client,max_resistance=210e6):
    client.measure_resistance(resistance=max_resistance) 
    
def config_current_source(client):
    client.apply_current(compliance_voltage = client.compliance_voltage)

def config_voltage_source(client):
    client.apply_voltage(compliance_current = client.compliance_current)
    
def set_current(client,current):
    client.source_current(current)

def set_voltage(client,voltage):
    client.source_voltage(voltage)
    
def shutdown(client):
    client.shutdown()
    
def config_buffer(client,num_points):
    client.config_buffer()
    
def start_buffer(client):
    client.start_buffer()
    
def stop_buffer(client):
    client.stop_buffer()
    
def reset_buffer(client):
    client.reset_buffer()
    
def wait_for_buffer(client):
    client.wait_for_buffer()
    
def ramp_to_voltage(client,final_voltage,steps,pause=0.02):
    client.ramp_to_voltage(final_voltage,steps,pause)

def ramp_to_current(client,final_current,steps,pause=0.02):
    client.ramp_to_current(final_current,steps,pause)



#keithley.apply_current()                # Sets up to source current
#keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
#keithley.source_current = 0             # Sets the source current to 0 mA

#keithley.measure_voltage()              # Sets up to measure voltage

#keithley.ramp_to_current(5e-3)          # Ramps the current to 5 mA
#print(keithley.voltage)                 # Prints the voltage in Volts

#keithley.shutdown()



#example

#keithley2450 = pym.instruments.keithley.Keithley2450("GPIB::1")
#set_current_compliance(keithley2450, current_limit=2e-8)
#set_voltage_compliance(keithley2450, voltage_limit=0.1):