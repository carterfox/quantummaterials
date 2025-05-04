#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 09:32:22 2024

@author: carterfox
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:59:10 2023

@author: carterfox

data analysis of SHG measurements
"""

import numpy as np
import matplotlib.pylab as plt

def get_power_and_gate_time(file):
    with open(file, "r") as f:
        for line in f:
            if line.startswith ('#Laser'):
                a=line.split('\t')[1]
                a=a.split('\n')[0]
            if line.startswith ('#Gate'):
                b=line.split('\t')[1]
                b=b.split('\n')[0]
        f.close()
    return a,b 
    
def get_data(file, sample, temp):
    power,gate_time = get_power_and_gate_time(file)
    data = np.loadtxt(file,skiprows=5)
    angles = data[:,0]*np.pi/180*2
    means = data[:,1]
    stds = data[:,2]

    angles = np.append(angles,angles[0])
    means = (np.append(means,means[0]) )#- np.average(substrate_means))
    # means = means/np.max(means)
    stds = np.append(stds,stds[0])
    return power, gate_time, angles, means, stds, sample, temp

def plot_shg(data,rmax=None,rmin=None,save=False):
    power, gate_time, angles, means, stds, sample, temp = data

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.errorbar(angles,means,stds,c='b',marker='.',markersize=5,elinewidth=.5)
    ax.set_rmin(0)
    ax.set_title(sample+'\n SHG Intensity ('+power+'mW - '+temp+'K - '+gate_time+'ms) \n' , va='top')
    
    temp = temp.replace('.','p')
    power = power.replace('.','p')
    if rmax!=None:
        ax.set_rmax(rmax)
    if rmin!=None:
        ax.set_rmin(rmin)
    if save:
        plt.savefig(path+'SHG_plot_'+sample+'_'+power+'mW_'+gate_time+'ms',bbox_inches='tight',dpi=300)
    # plt.close()

    

labdata = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/'
path = labdata + 'StackingTransitions/CrI3/dual_gate_devices_round1/SHG/'
path = labdata + 'Collaborations/YH_WSe2_2M/2-29-24/'

BN_l1_p1 = get_data(path + 'BN_location2_p5mW_rotateincidentpol_nodetectionpol.txt','BN l1','293')
BN_l2_p1= get_data(path + 'BN_location2_1mW_rotateincidentpol_nodetectionpol.txt','BN l2','293')
bulk = get_data(path + 'bulk_1mW_rotateincidentpol_nodetectionpol.txt','bulk','293')
substrate = get_data(path + 'substrate_1mW_rotateincidentpol_nodetectionpol.txt','substrate','293')
WSe2_l1_p1= get_data(path + 'WSe2_location1_1mW_rotateincidentpol_nodetectionpol.txt','WSe2 l1 p1','293')
WSe2_l2_p1= get_data(path + 'WSe2_location2_1mW_rotateincidentpol_nodetectionpol.txt','WSe2 l2 p1','293')
WSe2_l1_p2= get_data(path + 'WSe2_p5mW_location1_rotateincidentpol_nodetectionpol.txt','WSe2 l1 p2','293')

# stacked_v1 = get_data(path+'D2_stacked_3mW_rotateincident_nodetectionpol.txt','D2_stacked','80')
# stacked_v2 = get_data(path+'D2_stacked_v2_3mW_rotateincident_nodetectionpol.txt','D2_stacked_p2','80')
# unstacked_v1 = get_data(path+'D2_unstacked_3mW_rotateincident_nodetectionpol.txt','D2_unstacked_p3','80')
# BNs_v1 = get_data(path+'D2_BN_bottommiddles_3mW_rotateincident_nodetectionpol.txt','D2_BNs','80')
# BNs_v2 = get_data(path+'D2_BN_bottommiddles_v2_3mW_rotateincident_nodetectionpol.txt','D2_BNs_p4','80')
# stacked_region2 = get_data(path+'D2_stacked_region2_3mW_rotateincident_nodetectionpol.txt','D2_stacked p5','80')
# stacked_region3 = get_data(path+'D2_stacked_region3_3mW_rotateincident_nodetectionpol.txt','D2_stacked p6','80')
# stacked_region4 = get_data(path+'D2_stacked_region4_3mW_rotateincident_nodetectionpol.txt','D2_stacked p7','80')
# unstacked_region2 = get_data(path+'D2_unstacked_region2_3mW_rotateincident_nodetectionpol.txt','D2_unstacked p8','80')
# gr_region = get_data(path+'D2_Gr_region_3mW_rotateincident_nodetectionpol.txt','D2_Gr p9','80')

file_to_plot = BN_l1_p1
plot_shg(file_to_plot,save=True,rmax=40,rmin=0)



#ax.set_xticklabels(np.arange(0,360,15))            # This argument controls azimuthal tick labels)
# ax.grid(True)
# ax.set_title(sample+'\n', va='top')
# ax.set_title(sample+'\n SHG Intensity ('+power+' - '+temp+') \n' , va='top')
# ax.set_title(sample+'\n SHG Intensity ('+power+' - '+temp+') \n' + config + '\n' , va='top')

# temp = temp.replace('.','p')
# power = power.replace('.','p')
# plt.savefig(path+'SHG_plot_'+sample,bbox_inches='tight',dpi=300)

# plt.show()