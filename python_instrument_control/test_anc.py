# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 11:32:02 2025

@author: test anc
"""

from qcodes_contrib_drivers.drivers.Attocube.ANC300 import ANC300

ANC = ANC300(name='ANC300',address='ASRL11')

axis1 = ANC.submodules['axis1']
axis2 = ANC.submodules['axis2']
axis3 = ANC.submodules['axis3']
axis4 = ANC.submodules['axis4']

axes = [axis1,axis2,axis3,axis4]
for ax in axes:
    ax.mode('gnd')
# axis4.mode('gnd')
# axis1.mode('off')
# axis1.offset(1)

axis3.mode('stp')
axis3.move(10)
# axis4.waitMove()

axes = [axis1,axis2,axis3,axis4]
for ax in axes:
    ax.mode('gnd')
    
ANC.close()