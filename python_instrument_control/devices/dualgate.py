#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:27:27 2024

@author: carterfox

read data from lock in amp 
"""


import numpy as np
import os
import logging

class DualGate():
    
    def __init__(self, sample_name,d_b,d_t,d_flake,data_path):
        
        self.sample_name = sample_name
        self.d_b = d_b
        self.d_t = d_t
        self.data_path = data_path
        self.Rbox = 0 # resistance used in voltage divider for graphene polarization sensing measurement 
        self.d_flake = d_flake #thickness of material (such as the twisted Cri3 thickness)
        
        logging.info("Initiated device: {}".format(sample_name))     

class DualGate_MLGsense():
    
    def __init__(self, sample_name,d_b,d_m,d_t,d_flake,data_path):
        
        self.sample_name = sample_name
        self.d_b = d_b
        self.d_m = d_m
        self.d_t = d_t
        self.data_path = data_path
        self.Rbox = 0 # resistance used in voltage divider for graphene polarization sensing measurement 
        self.d_flake = d_flake #thickness of material (such as the twisted Cri3 thickness)
        
        logging.info("Initiated device: {}".format(sample_name))     

