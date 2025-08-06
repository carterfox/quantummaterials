#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:59:10 2023

@author: carterfox

data analysis of SHG measurements
"""

import numpy as np
import matplotlib.pylab as plt
import scipy
def get_power(file):
    with open(file, "r") as f:
        for line in f:
            if line.startswith ('#Laser'):
                a=line.split('\t')[1]
                a=a.split('\n')[0]
        f.close()
    return a 

def get_gatetime(file):
    with open(file, "r") as f:
        for line in f:
            if line.startswith ('#GateTime'):
                a=line.split('\t')[1]
                a=a.split('\n')[0]
        f.close()
    return a
    
def ellipse(theta,a,b,offset):
    return a*b/np.sqrt((b*np.sin(theta-offset))**2 + (a*np.cos(theta-offset))**2)

def SHG_ED_term(theta, phi, A, B, C, D, h):
    x = theta+phi
    return ( A*np.sin(3*x) + B*np.sin(x) + C*np.cos(3*x) + D*np.cos(x) )**2 + h



labdata = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1-8q9lGFnGNt4mDzcxXwdk43m1aVWT66q/XiaoWang_Group_data_2024on/'
path = labdata+'lab_troubleshooting/BN_SHG/'
# path = labdata+'Collaborations/CuCrP2S6_maryland/mainTscan/parallel/rawdata_parallel/'

temp = '300K'
sample = r'BN '+temp
# sample = r'CrI3 d4 '+temp
# config = 'perpendicular'
config = 'parallel'

file_path1 = path+'BN_noanalyzer.txt'

data = np.loadtxt(file_path1,skiprows=5)

power = get_power(file_path1) +'mW'
time = float(get_gatetime(file_path1))/1000
time_str = str(time)+'s'

angles= (data[:,0])*np.pi/180*2

# model = np.append(model,ellipse(angles4,1,.5,5.55)*1850+ellipse(angles4,1,.4,-5.8)*250)
# model = np.append(model,ellipse(angles5,1,.6,5.43)*1790)#+ellipse(angles5,1,.3,-5.65)*480)
# model = np.append(model,ellipse(angles2,1,.5,5.55)*1850+ellipse(angles2,1,.3,-5.65)*480)
# model = model/(np.max(model))
# scale=True
scale = False
if not scale:
    model = 1
means = data[:,1]/model#/time
stds = data[:,2]/model#/time
f=scipy.interpolate.interp1d(angles,means/max(means))
# means_sum = data[:,1]+data2[:,1]
angles2 = np.linspace(0,np.pi*2,50)
# angles2 =  (data2[:,0])*np.pi/180*2
# means2 = data2[:,1]#/time
# stds2 = data2[:,2]#/time
# means3 = data3[:,1]#/time
# stds3 = data3[:,2]#/time

# if True:
#     angles[-1]=angles[0]
#     means[-1]=means[0]
#     stds[-1]=stds[0]
#     stds2[-1]=stds2[0]
#     means2[-1]=means2[0]
#     stds3[-1]=stds3[0]
#     means3[-1]=means3[0]


# means3 = data3[:,1]#/time
# stds3 = data3[:,2]#/time
# angles = np.append(angles,angles[0])
# stds = np.append(stds,stds[0])

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
# ax.scatter(angles, means)
#means = means/np.max(means)


# ax.scatter(angles,model)

ax.scatter(angles2,f(angles2))
# ax.errorbar(angles,means,stds,c='b',marker='.',markersize=5,elinewidth=.5,zorder=3,label='Stacked')
# ax.errorbar(angles,means_sum,stds*0,c='b',marker='.',markersize=5,elinewidth=.5,zorder=3,label='Stacked')
# ax.errorbar(angles2,means2,stds2,c='r',marker='.',markersize=5,elinewidth=.5,zorder=3,label='Natural')
# ax.set_rmin(0)
# ax.set_rmax(2100)
# ax.set_rscale('symlog')         # This argument controls azimuthal tick labels)
# ax.set_rticks([0,500,1000,1500,2000])   
# ax.set_xticks(np.arange(0, np.radians(360),np.radians(15),))  # Less radial ticks# ax.set_rlabel_position(20)  # Move radial labels away from plotted line
# ax.set_rlabel_position(60)
# ax.set_rgrids([0,50,100,150,200],fontsize=0)
# ax.set_title('80K SHG Intensity (a.u.)')#+time_str+'   '+power+'\n'+sample, va='top')
# ax.set_title('SHG Counts \n Td-WTe2 S3')#+time_str+'   '+power+'\n'+sample, va='top')
# ax.set_title(sample+'\n SHG Counts/3sec ('+power+' - '+temp+') \n' , va='top')
# ax.set_title(sample+'\n SHG Intensity ('+power+' - '+temp+') \n' + 'config: '+config + '\n' , va='top')
# maxval=2311.825
# rdata = means/maxval
# sdata = stds/maxval
# ax.errorbar(angles,rdata,sdata,c='b',marker='.',markersize=5,elinewidth=.5,zorder=3,label='Stacked')
# ax.errorbar(angles,means,stds,c='b',marker='.',markersize=2,elinewidth=.5,zorder=0)
# ax.errorbar(angles,means2,stds2,c='r',marker='.',markersize=2,elinewidth=.5,zorder=3,label='-12V')
# ax.errorbar(angles,means3,stds3,c='g',marker='.',markersize=2,elinewidth=.5,zorder=3,label='0V')
# ax.set_title('SHG Intensity - '+str(temp)+' \n' , va='top')

# ax.set_rlabel_position(-8)
ax.set_rmin(0)
# ax.set_rmax(1.0)
ax.set_xticks(np.arange(0, np.radians(360),np.radians(30),))  # Less radial ticks# ax.set_rlabel_position(20)  # Move radial labels away from plotted line

# ax.set_rticks([.2,.4,.6,.8,1])
# plt.savefig('SHG_plot_'+str(temp)+'_'+config,bbox_inches='tight',dpi=300)
# ax.legend(loc='upper left', bbox_to_anchor=(0.85,1.2),fontsize=9)# temp = temp.replace('.','p')
# power = power.replace('.','p')
# plt.savefig(path+'SHG_plot_'+sample+'_'+config,bbox_inches='tight',dpi=300)
# plt.savefig(path+'SHG_plot_'+sample,bbox_inches='tight',dpi=300)
# plt.savefig(path1+'SHG_plot_'+power+'_'+'_'+temp+'_'+sample,bbox_inches='tight',dpi=300)
# plt.savefig(path+'SHG_plot_together',bbox_inches='tight',dpi=300)

plt.show()