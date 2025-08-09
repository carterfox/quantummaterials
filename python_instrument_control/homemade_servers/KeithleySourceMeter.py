#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 21:44:12 2025

@author: carterfox
"""

from pymeasure.adapters import VISAAdapter
from pymeasure.instruments.keithley import Keithley2400, Keithley2450
import logging

def KeithleySourceMeter(resource_name, model="2450"):
    adapter = VISAAdapter(resource_name)

    if model == "2450":
        base_class = Keithley2450
    elif model == "2400":
        base_class = Keithley2400
    else:
        raise ValueError(f"Unsupported model: {model}")

    class Keithley(base_class):
        def __init__(self):
            super().__init__(adapter)

        def close(self):
            """Only closes the VISA connection. Does NOT change instrument state."""
            self.adapter.connection.close()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    return Keithley()
