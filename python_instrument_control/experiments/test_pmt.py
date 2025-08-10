# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 11:48:23 2025

@author: Prof. Wang
"""
from homemade_servers.H11890PMT import HamamatsuH11890
import time

pmt = HamamatsuH11890()

pmt.set_hv(on=True)

counts = pmt.run_collection(gate_time_ms=200,num_gates=10)
        
pmt.set_hv(on=False)

print(counts)


pmt.close()
