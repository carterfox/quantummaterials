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
    
    def __init__(self, sample_name,d_b,d_t,data_path):
        
        self.sample_name = sample_name
        self.d_b = d_b
        self.d_t = d_t
        self.data_path = data_path
        
        logging.info("Initiated device: {}".format(sample_name))     

    

        