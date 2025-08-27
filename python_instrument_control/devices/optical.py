# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 11:06:38 2025

@author: Prof. Wang
"""


import numpy as np
import os
import logging

class Optical():
    
    def __init__(self, sample_name,data_path):
        
        self.sample_name = sample_name
        self.data_path = data_path
        self.d_flake = 0 #thickness of material (such as the twisted Cri3 thickness)
        
        logging.info("Initiated device: {}".format(sample_name))     

