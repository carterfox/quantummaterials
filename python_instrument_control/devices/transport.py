#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 13:53:56 2025

@author: carterfox
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import logging

class FourTerminal():
    
    def __init__(self, sample_name,channel_width,data_path):
        
        self.sample_name = sample_name
        self.channel_width = channel_width
        self.data_path = data_path
        self.d_flake = 0 #thickness of material (such as the twisted Cri3 thickness)
        
        logging.info("Initiated device: {}".format(sample_name))     

