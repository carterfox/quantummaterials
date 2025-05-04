#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 19:24:22 2025

@author: carterfox
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.cm as cm
from matplotlib_scalebar.scalebar import ScaleBar
import hdf5plugin
import h5py  
from readMDA import readMDA
import matplotlib.patches as mpatches

#%% plotting and figures

def init_plot_params():
    mpl.rcParams.update(mpl.rcParamsDefault)
    fontsize = 18
    plt.rcParams["lines.marker"] = '.'
    plt.rcParams["lines.linewidth"] = 2
    plt.rcParams["axes.labelpad"] = 4
    plt.rcParams["font.size"] = fontsize
    plt.rcParams["lines.markersize"] = 10
    plt.rcParams["figure.figsize"] = [6,4]
    plt.rcParams["savefig.dpi"] = 500
    plt.rcParams["savefig.format"] = "png"  # "svg"
    plt.rcParams["image.cmap"] = "magma"
    plt.rcParams["figure.constrained_layout.use"] = True
    plt.rcParams["legend.fontsize"] = 0.7 * fontsize
    plt.rcParams["legend.handlelength"] = 0.9
    plt.rcParams["legend.handletextpad"] = 0.5
    plt.rcParams["xtick.direction"] = 'in'
    plt.rcParams["ytick.direction"] = 'in'
    plt.rcParams["savefig.bbox"] = "tight"
    
def init_fig(figtype=None,figsize=(6,5)):
    fig, ax = plt.subplots(1,1,figsize=figsize)
    if figtype == 'RMCD':
        ax.set_xlabel(r'$B$ (T)')
        ax.set_ylabel("RMCD %",rotation=90)
    return ax

def plot_arrow_legend(ax,label,x1=None,y1=None,ls=18,yratio=.058,xratio=.12,wratio=.0872):
    
    xrange = ax.get_xlim()[1] - ax.get_xlim()[0]
    yrange = ax.get_ylim()[1] - ax.get_ylim()[0]
    if x1 == None and y1 == None:
        x1 = xrange*(1.5/4.2)
        y1 = yrange*(-8/24.77)
    xlen = xrange*xratio
    ylen = yrange*yratio
    x2 = x1-xlen
    y2 = y1-ylen
    yavg = (y1+y2)/2
    w = yrange*wratio
    arrow2 = mpatches.Arrow(x1,y1,-xlen,0,width=w,color='r')
    arrow = mpatches.Arrow(x2,y2,xlen,0,width=w,color='black')
    ax.add_patch(arrow)
    ax.add_patch(arrow2)
    ax.text(x1,yavg,r'$+$'+label,fontsize=ls,va='center',ha='left')
    ax.text(x2,yavg,r'$-$'+label+r'  ',fontsize=ls,va='center',ha='right')
    return ax

#%% helpful math functions

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b
  
#%% SHG analysis functions 

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
    
def initiate_SHG_fig(title):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_title(title, va='top')
    ax.set_rlabel_position(-10)
    ax.set_xticks(np.arange(0, np.radians(360),np.radians(45),),fontsize=4)  # Less radial ticks# ax.set_rlabel_position(20)  # Move radial labels away from plotted line
    return fig,ax
    
def plotseveralSHG(title,files,labels,ms=10,el=.5,append=False,order=None,factor=None,legend=True,normalize=True,subtract_substrate=False,colors = ['b','brown','gray']):
    
    fig,ax = initiate_SHG_fig(title)
    angles_list= []
    means_list = []
    stds_list = []
    maxval_list=[]
    
    for i in range(0,len(files)):
        f = files[i]
        try:
            data = np.loadtxt(f,skiprows=5)
        except:
            data = np.loadtxt(f,skiprows=7)
        angles = (data[:,0])*np.pi/180*2
        means = data[:,1]
        stds = data[:,2]
        if factor != None:
            means = means*factor[i]
            stds = stds*factor[i]
        if append:
            angles = np.append(angles,angles[0])
            means = np.append(means,means[0])
            stds = np.append(stds,stds[0])
        
        angles_list.append(angles)
        means_list.append(means)
        stds_list.append(stds)
        maxval_list.append(np.max(means))
        
    if subtract_substrate:
        means_list = means_list[0:-1] - means_list[-1]
        stds_list = stds_list[0:-1] - stds_list[-1]
        maxval_list = np.max(means_list)

    if normalize:
        maxval = np.max(maxval_list)
        means_list = means_list/maxval
        stds_list = stds_list/maxval

    # print(maxval)
    if order == None:
        order = np.linspace(len(files),1,1*len(files))

    for angle,mean,std,lb,o,cs in zip(angles_list,means_list,stds_list,labels,order,colors):
        ax.errorbar(angle,mean,yerr=std,marker='.',markersize=ms,elinewidth=el,label=lb,zorder=o,c=cs)

    if legend:
        ax.legend(loc='upper left', bbox_to_anchor=(.85,1.2),fontsize=10)
    if normalize:
        ax.set_rticks([0.0,.55,1.1],['','',''])
        
    return fig,ax,angles_list, means_list, stds_list

##SHG CD

def CD(A,B,errA,errB,absolute=False):
    CD = (A-B)/(A+B)*100
    if absolute:
        CD = abs(CD)
    CD_err = np.sqrt( (2*B*errA/(A+B)**2)**2 + (2*A*errB/(A+B)**2)**2 )*100
    return CD, CD_err
def get_CD_data(file):
    data = np.loadtxt(file,comments='#',skiprows=7)[:,1]
    mean,std = np.mean(data),np.std(data)
    return mean,std

#%%  Nano XRD data analysis

def get_stressmap_data(file):
    data = np.load(file)
    I = data['I']
    d = data['d']
    tilt_lr = data['tilt_lr']
    tilt_ud = data['tilt_ud']
    return I,d,tilt_lr,tilt_ud,data

def create_vector_map(grid,dx,dy,binning):
    r, c = np.min(np.shape(grid)),np.min(np.shape(grid))
    if r % 2 != 0:
        r = r-1
        c = c-1
    Y, X = np.mgrid[0:r:binning, 0:c:binning]+.5
    dX = dx[0:r:binning,0:c:2]*0
    dY = dy[0:r:binning,0:c:2]*0
    # print(np.shape(dY))
    # print(np.shape(dy))
    for x in range(binning):
        for y in range(binning):
            dX = dX + dx[x:x+r:binning,y:y+c:binning]
            dY = dY + dy[x:x+r:binning,y:y+c:binning]
    dX = dX/(binning**2)
    dY = dY/(binning**2)
    return X,Y,dX,dY

def plot_xrd_roi(data,x_len,y_len,roi_xi,roi_xf,roi_yi,roi_yf):
    img = []
    for x in data:
        b=np.add.reduceat(x,[roi_xi,roi_xf])
        c=np.add.reduceat(b,[roi_yi,roi_yf],1)
        img.append(c[0][0])
    try:
        img = np.array(img).reshape(y_len,x_len)
    except:
        while len(img) < (y_len*x_len):
            img.append(0)
        img = np.array(img).reshape(y_len,x_len)
    
    return img

def get_scan_data(h5file,mdafile,verbose=0):
    '''
    Parameters
    ----------
    h5file 
    mdafile

    Returns
    -------
    data : data cube where axis 0 is the flat area of scan points, axis 1-2 is the detector image at a given scan point 

    '''
    mdainfo = readMDA(mdafile,verbose=0)
    dim_y, dim_x = mdainfo[0]['dimensions']
    xpos = np.array(mdainfo[-2].p[0].data).flatten()
    ypos = np.array(mdainfo[-1].p[0].data).flatten()
    x_min, x_max = min(xpos), max(xpos)
    y_min, y_max = min(ypos), max(ypos)
    
    scalex = (x_max-x_min)/np.min([dim_x,dim_y])
    scaley = (y_max-y_min)/np.min([dim_x,dim_y])
    
    d = h5py.File(h5file)
    scannum = h5file.split('/')[-1].split('_')[1]
    data = np.array(d['entry']['data']['data'])
    
    return data, dim_x, dim_y, scalex, scannum

def plot_XRD_scan(img,scale,sample,reflection,vmin=None,vmax=None):
    
    title = sample + " \t  " +reflection
    plot = plt.imshow(img,origin='lower',vmin=vmin,vmax=vmax,cmap=cm.viridis)
    scalebar = ScaleBar(scale,"um",box_alpha=0,color='white',location='lower right')
    cbar=plt.colorbar()
    cbar.set_label('Intensity',fontsize=12)
    plt.gca().add_artist(scalebar)
    plt.xticks([]),plt.yticks([])
    plt.title(title,fontsize=12)
    return 0 

#%% RMCD analysis functions

def get_rmcd_data(file,phase=None,ineq='>',background=0):
    data = np.loadtxt(fname=file,comments='#')

    b_field,r,r_std,theta_r,theta_r_std, = data[:,0],data[:,1],data[:,2],data[:,3],data[:,4]
    dr,dr_std,theta_dr,theta_dr_std = data[:,5],data[:,6],data[:,7],data[:,8]

    dr_over_r = 1*dr/r*100 
    dr_over_r_std = A_over_B_error_prop(dr, r, dr_std, r_std)*100
    mid = int(np.ceil(len(b_field)/2))
    b_field_low_to_high,b_field_high_to_low = b_field[0:mid]/10000, b_field[mid:]/10000
    dr_over_r_low_to_high, dr_over_r_high_to_low = dr_over_r[0:mid], dr_over_r[mid:] 
    theta_dr_std_low_to_high,theta_dr_high_to_low = theta_dr_std[0:mid], theta_dr[mid:] 
    theta_dr_std_high_to_low,theta_dr_low_to_high = theta_dr_std[mid:], theta_dr[0:mid] 
    dr_over_r_std_low_to_high,dr_over_r_std_high_to_low = dr_over_r_std[0:mid], dr_over_r_std[mid:]
    
    if phase != None:
        if ineq == '<=':
            dr_over_r_low_to_high[np.where(theta_dr_low_to_high<=phase)] = dr_over_r_low_to_high[np.where(theta_dr_low_to_high<=phase)]*-1 
            dr_over_r_high_to_low[np.where(theta_dr_high_to_low<=phase)] = dr_over_r_high_to_low[np.where(theta_dr_high_to_low<=phase)]*-1 
        if ineq == '>=':
            dr_over_r_low_to_high[np.where(theta_dr_low_to_high>=phase)] = dr_over_r_low_to_high[np.where(theta_dr_low_to_high>=phase)]*-1 
            dr_over_r_high_to_low[np.where(theta_dr_high_to_low>=phase)] = dr_over_r_high_to_low[np.where(theta_dr_high_to_low>=phase)]*-1 
        if ineq == '<':
            dr_over_r_low_to_high[np.where(theta_dr_low_to_high<phase)] = dr_over_r_low_to_high[np.where(theta_dr_low_to_high<phase)]*-1 
            dr_over_r_high_to_low[np.where(theta_dr_high_to_low<phase)] = dr_over_r_high_to_low[np.where(theta_dr_high_to_low<phase)]*-1 
        if ineq == '>':
            dr_over_r_low_to_high[np.where(theta_dr_low_to_high>phase)] = dr_over_r_low_to_high[np.where(theta_dr_low_to_high>phase)]*-1 
            dr_over_r_high_to_low[np.where(theta_dr_high_to_low>phase)] = dr_over_r_high_to_low[np.where(theta_dr_high_to_low>phase)]*-1 
        if ineq == ['>=','<=']:
            dr_over_r_low_to_high[np.where((theta_dr_low_to_high>=phase[0]) & (theta_dr_low_to_high<=phase[1]))] = dr_over_r_low_to_high[np.where((theta_dr_low_to_high>=phase[0]) & (theta_dr_low_to_high<=phase[1]))]*-1 
            dr_over_r_high_to_low[np.where((theta_dr_high_to_low>=phase[0]) & (theta_dr_high_to_low<=phase[1]))] = dr_over_r_high_to_low[np.where((theta_dr_high_to_low>=phase[0]) & (theta_dr_high_to_low<=phase[1]))]*-1 
        
        dr_over_r_low_to_high = dr_over_r_low_to_high -background
        dr_over_r_high_to_low = dr_over_r_high_to_low -background
    
    return b_field_low_to_high, b_field_high_to_low, dr_over_r_low_to_high, dr_over_r_high_to_low




