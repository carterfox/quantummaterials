# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 11:32:02 2025

@author: test anc
"""

from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300

ANC = ANC300(name='ANC300',address='ASRL11')

scannerx = ANC.submodules['axis1']
scannery = ANC.submodules['axis2']
stepperx = ANC.submodules['axis3']
steppery = ANC.submodules['axis4']

axes = [scannerx,scannery,stepperx,steppery]
for ax in axes:
    ax.mode('gnd')
# axis4.mode('gnd')
# scannery.mode('off')
# scannery.offset(0)

# stepperx.mode('stp')
# stepperx.move(-10)
# steppery.waitMove()

# axes = [scannerx,scannery,stepperx,steppery]
# for ax in axes:
#     ax.mode('gnd')
    
ANC.close()