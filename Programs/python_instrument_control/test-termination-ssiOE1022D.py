#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 17:25:15 2025

@author: carterfox
"""

import visa

def test_termination(resource_name, command='*IDN?'):
    rm = visa.ResourceManager()
    terminations = {
        'LF': '\n',
        'CR': '\r',
        'CRLF': '\r\n'
    }

    for label, term in terminations.items():
        print(f"\nTesting termination: {label}")
        try:
            inst = rm.open_resource(resource_name)
            inst.baud_rate = 9600
            inst.timeout = 2000
            inst.write_termination = term
            inst.read_termination = term

            inst.write(command)
            response = inst.read()
            print(f"Response with {label}: {response}")
            inst.close()
        except Exception as e:
            print(f"Error with {label}: {e}")

# Replace 'ASRL3::INSTR' with your actual COM port resource name
test_termination('ASRL3::INSTR')
