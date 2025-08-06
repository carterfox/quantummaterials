#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 18:46:49 2023

@author: carterfox
plotting for signal mapping
"""
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm


path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1riZacJd_1_jmKfGgrjDuP7KcecvMS3i2/Xiao research group/Lab Data (Xiao and Wang groups)/UCLA_Duan_Intercalated_Samples_Collab/CoMoS2/8-10_batch/chip2/RMCD/mapping2k/'

temp = '2K'
files = ['_flake647_map_m24000.txt','_flake647_map_m12000.txt',
         '_flake647_map_000.txt',
          '_flake647_map_p12000.txt',
         '_flake647_map_p24000.txt','_flake647_map_p12000_down.txt',
         '_flake647_map_000_down.txt','_flake647_map_m12000_down.txt',
         '_flake647_map_m24000_down.txt']
fields = ['-2.4T','-1.2T',
          '0T','1.2T',
          '2.4T','1.2T',
          '0T','-1.2T',
          '-2.4T']

subfigs = len(fields)
fig, axes = plt.subplots(3,int(subfigs/2)+1,figsize=(14*.8,7.5*.8))
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([1.0, 0.125, 0.02, 0.75])
sample = r'CoMoS2'

to_right=0
axes[0,int(subfigs/2)].set_axis_off()
axes[2,int(subfigs/2)].set_axis_off()
axes[1,0].set_axis_off()
axes[1,1].set_axis_off()
axes[1,2].set_axis_off()
axes[1,3].set_axis_off()
cbarmax=1.0
axis2=0
for x in range(len(fields)):
    
    axis1 = x
    field = fields[x]
    
    file_path = path+temp+files[x]
    
    
    data = np.loadtxt(file_path,skiprows=1)
    xvoltages = data[:,1]
    yvoltages = data[:,0]
    num_x_points = int(np.sqrt(len(xvoltages)))
    num_y_points = num_x_points
    R = data[:,2]
    dR = data[:,3]
    theta_r = data[:,4]
    theta_dr = data[:,5]
    dR_over_R = dR/R*100
    
    nrows, ncols = num_x_points, num_y_points
    
    grid = dR_over_R.reshape((nrows, ncols))
    grid=np.rot90(grid)
    max_val = round(np.max(grid),3)
    
    if x>=int(subfigs/2):
        if axis2==0:
            axis2=1
            axes[axis2,axis1].set_xlabel('Axis2 (V)',fontsize=14)
            axes[axis2,axis1].set_ylabel('Axis1 (V)',fontsize=14)
            
        else:
            axis2=2
        axis1 = int(subfigs/2) - to_right
        to_right=to_right+1
    
    im=axes[axis2,axis1].imshow(grid, cmap=cm.magma,vmin=-0,vmax=cbarmax)
    xyticks = np.linspace(np.min(yvoltages)-0.5,np.max(yvoltages)-0.5,num_y_points)
    axes[axis2,axis1].set_yticks(np.linspace(-0.5,num_y_points-0.5,4),[30,20,10,0])
    axes[axis2,axis1].set_xticks(np.linspace(-0.5,num_y_points-0.5,4),[0,10,20,30])
    axes[axis2,axis1].set_title('B = '+field)
    fig.colorbar(im, cax=cbar_ax)
    
    
    
    # plt.ylim(0,5)
    # plt.xlim(0,5)
    # cbar=plt.colorbar()
    # thecb = axes[axis2,axis1].cax.colorbar(im)
    # thecb.set_label_text(r'$\Delta R/R $ %')
    
    # field=field.replace('.','p')
    # plt.savefig(path+'RMCD_map_'+sample+'_'+temp+'_'+field,bbox_inches='tight')
# fig.supxlabel('Axis2 (V)',fontsize=14)
# fig.supylabel('Axis1 (V)',fontsize=14)
plt.text(4.05,cbarmax/2,r'$\Delta R/R $ %',verticalalignment='center',horizontalalignment='center',rotation=90,fontsize=14)
plt.tight_layout()
cbarmax = str(cbarmax).replace('.','p')
# plt.savefig(path+'RMCD_mapping_'+sample+'_'+temp+'_'+cbarmax,bbox_inches='tight')
plt.show()


