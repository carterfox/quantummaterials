#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 19:24:22 2025

@author: carterfox
"""
from scipy.interpolate import UnivariateSpline; from scipy.optimize import curve_fit; from scipy import ndimage
from matplotlib_scalebar.scalebar import ScaleBar; import matplotlib.patches as mpatches
import matplotlib.pylab as plt; import matplotlib as mpl; import matplotlib.cm as cm
import hdf5plugin; import h5py; from readMDA import readMDA
import numpy as np; import glob; import time; from tqdm import tqdm

#%% miscellaneous plotting and helpful functions  


def test():
    print('here')
    return None

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
    # plt.rcParams['text.usetex'] = True
    # plt.rcParams['text.latex.preamble'] =r"\usepackage{xcolor} "
    # plt.rcParams.update({
    # "text.usetex": True,
    # "font.family": "Helvetica"})
    
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
        x1 = xrange*(1.6/4.2)
        y1 = yrange*(-9.4/24.77)
    xlen = xrange*xratio*.7
    ylen = yrange*yratio*.6
    x2 = x1-xlen
    y2 = y1-ylen
    yavg = (y1+y2)/2
    w = yrange*wratio*.7
    arrow2 = mpatches.Arrow(x1,y1,-xlen,0,width=w,color='red')
    arrow = mpatches.Arrow(x2,y2,xlen,0,width=w,color='black')
    ax.add_patch(arrow), ax.add_patch(arrow2)
    ax.text(x1,yavg,r'$+$'+label,fontsize=ls,va='center',ha='left')
    ax.text(x2,yavg,r'$-$'+label+r'  ',fontsize=ls,va='center',ha='right')
    return ax

## helpful math functions

def A_over_B_error_prop(A,B,stdA,stdB):
    return (A/B)*np.sqrt( (stdA/A)**2 + (stdB/B)**2 )

def line(x,m,b):
    return m*x+b

#%%  Nano XRD data analysis
 
class XRD_ScanAnalyzer:
    def __init__(self,path,sample,reflection,scan_number):
        """
        Initialize the XRD_ScanAnalyzer object with metadata and load scan data.

        Parameters:
            path (str): Base directory containing h5 and mda subfolders.
            sample (str): Sample name or identifier.
            reflection (str): Reflection label (e.g., '(1,-1,0)' ).
            scan_number (int): Scan number to load from file.
        """
        self.path = path
        self.h5file, self.mdafile, self.data, self.x_len, self.y_len, self.scalex, self.scannum = self.get_scan_data(scan_number)
        self.scale = self.scalex
        self.sample = sample
        self.reflection = 'r'+reflection 
        self.scannum = 'scan'+self.h5file.split('scan_')[1].split('_')[0]

        self.theta = None
        self.twotheta = None
        self.gamma = None
        self.axes = np.array(['x','y'])
        self.x_len_copy, self.y_len_copy, self.scale_copy = np.copy(self.x_len), np.copy(self.y_len), np.copy(self.scale)
    
    def get_scan_data(self,scan_number,asarray=False):
        """
        Load scan data from .h5 and .mda files for a given scan.

        Parameters:
            scan_number (int): Identifier number of the scan.
            asarray (bool): Whether to convert h5 data to NumPy array.

        Returns:
            tuple: (h5 filename, mda filename, scan data, x size, y size, scale factor, scan number)
        """
        h5folder = self.path+'h5'
        mdafolder = self.path+'mda'
        prefixh5 = 'scan_'+str(scan_number)
        prefixmda = '26idbSOFT_0'+str(scan_number)
        h5file = glob.glob(f'{h5folder}/{prefixh5}*')[0]
        mdafile = glob.glob(f'{mdafolder}/{prefixmda}*')[0]
        
        mdainfo = readMDA(mdafile,verbose=0)
        dim_y, dim_x = mdainfo[0]['dimensions']
        xpos = np.array(mdainfo[-2].p[0].data).flatten()
        ypos = np.array(mdainfo[-1].p[0].data).flatten()
        x_min, x_max = min(xpos), max(xpos)
        y_min, y_max = min(ypos), max(ypos)
        
        scalex = (x_max-x_min)/np.min([dim_x,dim_y])
        # scaley = (y_max-y_min)/np.min([dim_x,dim_y])
        
        d = h5py.File(h5file)
        scannum = h5file.split('/')[-1].split('_')[1]
        if asarray == True: data = np.array(d['entry']['data']['data'])
        else: data = d['entry']['data']['data']
        
        return h5file, mdafile, data, dim_x, dim_y, scalex, scannum
    
    def set_roi(self,x_start,x_end,y_start,y_end):
        """
        Define a region of interest (ROI) from the scan data and load only that data into roi_data 

        Parameters:
            x_start, x_end (int): X-axis pixel boundaries of ROI.
            y_start, y_end (int): Y-axis pixel boundaries of ROI.

        Returns:
            None
        """
        self.roi_xi, self.roi_xf = x_start, x_end
        self.roi_yi, self.roi_yf = y_start, y_end        
        self.roi_data = self.data[:,self.roi_yi:self.roi_yf,self.roi_xi:self.roi_xf]
        self.roi_raw_data_copy = np.copy(self.roi_data)
        return None
    
    def bin_roi_data(self,binning=2):
        """
        Performs spatial binning on the region-of-interest (ROI) data.
    
        This method reshapes the flattened ROI data into a 4D array representing a 2D spatial grid
        with additional data dimensions (diffraction image). It then bins the data along the spatial dimensions 
        using the specified binning factor and sums over the binning blocks 
        to reduce spatial resolution, while preserving the diffraction data dimensions.

        Parameters:
        ----------
        binning : int, optional (default=2)
            The size of the binning block along both the x and y spatial dimensions.
    
        Modifies:
        ---------
        self.roi_data : np.ndarray
            The binned and summed ROI data with shape (new_y * new_x, channels, features).
        self.y_len : int
            The new height of the binned image grid.
        self.x_len : int
            The new width of the binned image grid.
    
        Returns:
        -------
        None
        """
        data = self.roi_raw_data_copy
        data=data.reshape(self.y_len_copy,self.x_len_copy,data.shape[1],data.shape[2])
        new_y = data.shape[0] // binning
        new_x = data.shape[1] // binning
        data = data[:new_y * binning, :new_x * binning]
        
        binned = data.reshape(new_y, binning, new_x, binning, data.shape[2], data.shape[3])
        binned_sum = binned.sum(axis=(1, 3))
        binned_data = binned_sum.reshape(new_y*new_x,data.shape[2],data.shape[3])
        
        self.roi_data = binned_data
        self.y_len,self.x_len = new_y, new_x
        self.scale = self.scale_copy*self.x_len_copy/self.x_len
        
        return None
    
    def make_saving_string(self,method):
        """
        Construct a filename-friendly string for saving images with important info in the name.

        Parameters:
            method (str): Processing method label (e.g., 'Intensity', 'COMx').

        Returns:
            str: Formatted string for saving.
        """
        samplestr = self.sample.replace('$','').replace('^','').replace("\\circ",'').replace('0.','p').replace(' ','')
        reflectionstr = self.reflection.replace(')','').replace('(','').replace('-','m').replace(',','')
        return samplestr+'_'+reflectionstr+'_'+str(self.scannum)+'_'+method
    
    def reshape_image_array(self,img):
        """
        Reshape a flat image array to match scan dimensions.

        Parameters:
            img (list or array): Flat image data.

        Returns:
            np.ndarray: Reshaped image array of shape (y_len, x_len).
        """
        try: 
            img = np.array(img).reshape(self.y_len,self.x_len)
        except:
            while len(img) < (self.y_len*self.x_len): img.append(0)
            img = np.array(img).reshape(self.y_len,self.x_len)
        return img
    
    def plot_scan_image(self,img,cbarlabel='Intensity',vmin=None,vmax=None,save=True,threshold=-1):
        """
        Display and optionally save the scan image.

        Parameters:
            img (np.ndarray): 2D image array to plot.
            cbarlabel (str): Colorbar label.
            vmin, vmax (float): Plot intensity limits.
            save (bool): Whether to save the image to disk.
            threshold: only plot pixels where their summed intensity is above the threshold

        Returns:
            None
        """
        summed_img = self.reshape_image_array(np.sum(self.roi_data,axis=(1,2)))
        mask = summed_img > threshold
        img = np.ma.masked_array(data=img, mask=~mask)
            
        plt.figure()
        plt.imshow(img,origin='lower',vmin=vmin,vmax=vmax,cmap=cm.viridis)
        scalebar = ScaleBar(self.scale,"um",box_alpha=0,color='white',location='lower left',font_properties={"size": 12})
        cbar=plt.colorbar()
        cbar.set_label(cbarlabel,fontsize=12)
        ax = plt.gca()
        ax.add_artist(scalebar)
        plt.xticks([]),plt.yticks([])
        plt.title(self.reflection+'              '+self.sample,fontsize=12)
        if save:            
            file_to_save_string = self.make_saving_string(cbarlabel)
            plt.savefig(self.path+file_to_save_string,bbox_inches='tight',dpi=500)
        return None
    
    def image_roi_sum(self,vmin=None,vmax=None,save=True):
        """
        Calculate total ROI intensity per pixel and display image.

        Parameters:
            vmin, vmax (float): Optional intensity limits.
            save (bool): Whether to save the image.

        Returns:
            None
        """
        img = np.sum(self.roi_data,axis=(1,2))
        img = self.reshape_image_array(img)
        self.plot_scan_image(img,'Intensity',vmin,vmax,save)
        self.sum_img = img
        return None
            
    
    def image_roi_com(self,axis='x',vmin=None,vmax=None,save=True):
        """
        Compute the center of mass of ROI intensity per pixel.

        Parameters:
            axis (str): Either 'x' or 'y' direction.
            vmin, vmax (float): Optional intensity limits.
            save (bool): Whether to save the image.

        Returns:
            None
        """
        axis_int = np.where(self.axes==axis)[0][0]
        x_points, y_points = np.arange(self.roi_yi,self.roi_yf,1), np.arange(self.roi_xi,self.roi_xf,1)
        points = [y_points,x_points][axis_int]
        
        img = [] 
        sumaxis = np.sum(self.roi_data,axis_int+1)
        img = np.sum(sumaxis*points,1)/np.sum(sumaxis,1)
        
        img = self.reshape_image_array(img)
        self.plot_scan_image(img,'COM'+axis,vmin,vmax,save)
        self.com_img = img
        return None
    
    def image_roi_shift(self,axis='x',vmin=None,vmax=None,threshold=0,normed_prof=[],save=True):
        """
        Fit the profile within each pixel's ROI and extract shift.

        Parameters:
            axis (str): Axis along which the shift is computed.
            vmin, vmax (float): Plot range.
            threshold (float): Minimum intensity required to fit.
            normed_prof (list): Nrmalized profile to fit against. If already saved, can be inputted here to speed it up 
            save (bool): Whether to save the image.

        Returns:
            None
        """
        axis_int =np.where(self.axes==axis)[0][0]
        points, normed_prof, fit_func = self.get_roi_line_fit_func(axis_int=axis_int,normed_prof=normed_prof)
        if axis == 'x':
            self.normed_prof_x = normed_prof
            self.points_x = points
        elif axis == 'y':
            self.normed_prof_y = normed_prof
            self.points_y = points
        img = [] 
        img_std = []
        summed_img = []
        
        for x in tqdm(self.roi_data):
            summed = np.sum(x,axis_int)
            try:
                p,c = curve_fit(fit_func,points,summed/np.max(summed))
                shift = p[0]
                shift_std = np.sqrt(np.diag(c))[0]
            except:
                shift = np.nan
                shift_std = 0
                
            img.append(shift)
            summed_img.append(np.sum(summed))
            img_std.append(shift_std)
                        
        img, img_std = self.reshape_image_array(img), self.reshape_image_array(img_std)
        self.plot_scan_image(img,'SHIFT'+axis,vmin,vmax,save,threshold=threshold)
        if axis == 'x':
            self.shift_img_x = img
            self.img_std_x = img_std
        elif axis == 'y':
            self.shift_img_y = img
            self.img_std_y = img_std
        
        return None
        
    def sum_images(self):
        """
        Sum all diffraction images to get the summed diffraction image showing all the informatoin.

        Parameters:
            None
        Returns:
            summed image
        """
        self.summed_images = np.sum(self.data,0)
        return self.summed_images
    
    def plot_sum_images(self,vmin=None,vmax=None,zoom_roi=False,save=False):
        """
        Plot the summed diffraction images

        Parameters:
            vmin, vmax (float): Plot range.
            zoom_roi: whether to zoom in on the roi or not 
            save (bool): Whether to save the image.

        Returns:
            None
        """
        plt.figure()
        plt.imshow(self.summed_images,origin='lower',vmin=vmin,vmax=vmax,cmap=cm.viridis)
        cbar=plt.colorbar()
        cbar.set_label('Intensity',fontsize=12)
        
        if zoom_roi:
            plt.xlim(self.roi_xi,self.roi_xf)
            plt.ylim(self.roi_yi,self.roi_yf)
        
        plt.xticks([]),plt.yticks([])
        plt.title(self.reflection+'        '+self.sample)
        
        if save:            
            file_to_save_string = self.make_saving_string('sum_images')
            plt.savefig(self.path+file_to_save_string,bbox_inches='tight',dpi=500)
            
        return None
    
    def get_roi_line_fit_func(self,axis_int=1,normed_prof=[]):    
        """
        Generate a shifted spline function for ROI profile fitting.

        Parameters:
            axis_int (int): Axis index (0 for x, 1 for y).
            normed_prof (list): Optional normalized profile.

        Returns:
            tuple: (points, normed profile, shifted spline function)
        """
        x_points, y_points = np.arange(self.roi_yi,self.roi_yf,1), np.arange(self.roi_xi,self.roi_xf,1)
        points = [y_points,x_points][axis_int]

        if normed_prof == []:
            print('getting full profile')
            roi = np.sum(self.data[:,self.roi_yi:self.roi_yf,self.roi_xi:self.roi_xf],0)
            summed = np.sum(roi,axis_int)
            normed_prof = summed/np.max(summed)
        
        spl = UnivariateSpline(points,normed_prof,k=3,s=0)
        def shifted_spline(x,dx):
            return spl(x-dx)
        
        return points, normed_prof, shifted_spline
    
    def plot_roi_profile(self,axis='x'):
        plt.figure(figsize=(6,2))
        if axis == 'x':
            points,prof = self.points_x, self.normed_prof_x
            plt.xlabel('x')
        if axis == 'y':
            points,prof = self.points_y, self.normed_prof_y
            plt.xlabel('y')
        plt.ylabel('Intensity')
        plt.plot(points,prof,marker='.')


def get_stressmap_data(file):
    """
    Load stress map data from  data5D.npz file.

    Parameters:
        file (str): Path to the `.npz` file containing stress map data.

    Returns:
        I (ndarray): Intensity map.
        d (ndarray): Displacement or strain-related map.
        tilt_lr (ndarray): Left-right tilt component.
        tilt_ud (ndarray): Up-down tilt component.
        data (NpzFile): Full loaded data object (acts like a dict).
    """
    data = np.load(file)
    I = data['I']
    d = data['d']
    tilt_lr = data['tilt_lr']
    tilt_ud = data['tilt_ud']
    return I,d,tilt_lr,tilt_ud,data

def create_vector_map(grid,dx,dy,binning):
    """
    Generates a binned vector field map from displacement data (from xrd tilt series Analyze5D data)

    Parameters:
    -----------
    grid : np.ndarray
        A 2D array used to determine the shape of the output grid.
    dx : np.ndarray
        A 2D array representing x-direction displacements.
    dy : np.ndarray
        A 2D array representing y-direction displacements.
    binning : int
        The binning factor used to downsample the displacement data.

    Returns:
    --------
    X : np.ndarray
        2D array of x-coordinates for the vector field grid.
    Y : np.ndarray
        2D array of y-coordinates for the vector field grid.
    dX : np.ndarray
        2D array of averaged x-displacements for each binned region.
    dY : np.ndarray
        2D array of averaged y-displacements for each binned region.
    
    Notes:
    ------
    - The function ensures the grid dimensions are even for consistent binning.
    - Displacement vectors are averaged over each binning window to reduce noise and resolution.
    """

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

#%% SHG analysis functions 


class SHG_ScanAnalyzer:
    def __init__(self,path,scan_file):
        """
        Initialize the SHG_ScanAnalyzer object with metadata and load scan data.

        Parameters:
            path (str): Base directory containing h5 and mda subfolders.
            scan_file (int): Scan file to load
        """
        self.path = path
        self.power, self.gate_time, self.sample, self.polarizer_config, self.analyzer_config = self.get_scan_data(scan_file)
        
    def get_scan_data(self,file):
        with open(file, "r") as f:
            for line in f:
                if line.startswith ('#Laser'):
                    power=line.split('\t')[1].split('\n')[0]
                if line.startswith ('#GateTime'):
                    gate_time=line.split('\t')[1].split('\n')[0]
                if line.startswith ('#Sample'):
                    sample=line.split('\t')[1].split('\n')[0]
                if line.startswith ('#Polarizer'):
                    polarizer_config=line.split('\t')[1].split('\n')[0]
                if line.startswith ('#Analyzer'):
                    analyzer_config=line.split('\t')[1].split('\n')[0]             
            f.close()
        return power, gate_time, sample, polarizer_config, analyzer_config 

    
    
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
    # ax.set_theta_zero_location("N")
    ax.set_title(title, va='top')
    ax.set_rlabel_position(-10)
    ax.set_xticks(np.arange(0, np.radians(360),np.radians(45),),fontsize=4)  # Less radial ticks# ax.set_rlabel_position(20)  # Move radial labels away from plotted line
    return fig,ax
    
def plotseveralSHG(title,files,labels,ms=10,el=.4,append=False,order=None,factor=np.array([1]),legend=True,normalize=True,subtract_substrate=False,divide_substrate=False,lw=2,colors = ['b','brown','gray']):
    
    fig,ax = initiate_SHG_fig(title)
    angles_list= []
    means_list = []
    stds_list = []
    maxval_list=[]
    
    for i in range(0,len(files)):
        f = files[i]

        try:
            data = np.loadtxt(f,skiprows=5)
            lines=[]
            with open(f, 'r') as ff:
                for k in range(0,4):
                    lines.append(ff.readline())
            num_gates = float(lines[2].split('\t')[1].split('\n')[0])

        except:
            data = np.loadtxt(f,skiprows=7)
        angles = (data[:,0])*np.pi/180*2
        means = data[:,1]
        stds = data[:,2]
        if any(factor != 1):
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
        stds_list = stds_list/np.sqrt(num_gates)
    
    if divide_substrate:
        means_list = means_list/(means_list[-1]/np.max(means_list[-1]))
        # stds_list = stds_list #- stds_list[-1]
        maxval_list = np.max(means_list)

    # print(maxval)
    if order == None:
        order = np.linspace(len(files),1,1*len(files))

    for angle,mean,std,lb,o,cs in zip(angles_list,means_list,stds_list,labels,order,colors):
        ax.errorbar(angle,mean,yerr=std,marker='.',markersize=ms,elinewidth=el,label=lb,zorder=o,c=cs,linewidth=lw)

    if legend:
        ax.legend(loc='upper left', bbox_to_anchor=(.85,1.2),fontsize=10)
    if normalize:
        ax.set_rticks([0.0,.55,1.1],['','',''])
        
    return fig,ax,angles_list, means_list, stds_list

## SHG CD

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

#%% TEM data analysis

def get_TEM_diff(emd_file):
    f = h5py.File(emd_file)
    data = f['Data']
    img_data_name = list(data['Image'].keys())[0]
    img_data = data['Image'][img_data_name]['Data']
    return img_data

#%% RMCD analysis functions

def get_rmcd_data_jose(file_inc, file_dec):
    data_inc, data_dec = np.loadtxt(fname=file_inc,comments='#'), np.loadtxt(fname=file_dec,comments='#')
    b_field_low_to_high, b_field_high_to_low = data_inc[:,0], data_dec[:,0]
    dr_over_r_low_to_high, dr_over_r_high_to_low = data_inc[:,1], data_dec[:,1]

    return b_field_low_to_high, b_field_high_to_low, dr_over_r_low_to_high, dr_over_r_high_to_low


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

def plot_state(ax,state,x,y,xstep=0.1,h='right',f=18):
    xcur = x
    for a in state:
        if a == 'up':
            ax.text(xcur,y,r'$\uparrow$',c='darkblue',ha=h,fontsize=f)
        if a == 'down':
            ax.text(xcur,y,r'$\downarrow$',c='firebrick',ha=h,fontsize=f)
        xcur = xcur+xstep


#%% AFM analysis functions

def get_afm_profile(file,prof_number,start=0,end=-1):
    data = np.loadtxt(file,skiprows=4)
    index = prof_number-1
    xs = np.trim_zeros(data[:,int(index*2)], trim='b')*10**6
    heights = np.trim_zeros(data[:,int(1+index*2)], trim='b')*10**9
    if start != 0 or end != -1:
        xs = xs[start:end]
        heights = heights[start:end]
    return xs, heights


def sum_of_line_and_tanh(x, slope, intercept, tanh_center, tanh_amplitude, tanh_steepness):
    """
    Calculates the sum of a linear function and a hyperbolic tangent function.

    Args:
        x (float or array-like): The input value(s) for the function.
        slope (float): The slope of the linear component.
        intercept (float): The y-intercept of the linear component.
        tanh_center (float): The x-value where the tanh function is centered (i.e., its inflection point).
        tanh_amplitude (float): The maximum height/depth of the tanh function from its center.
                                A positive value makes the tanh function increase,
                                a negative value makes it decrease.
        tanh_steepness (float): Controls the steepness of the tanh transition.
                                Larger values make the transition sharper.

    Returns:
        float or array-like: The resulting y-value(s) of the summed function.
    """

    # Calculate the linear component
    linear_component = slope * x + intercept

    # Calculate the hyperbolic tangent component
    # The tanh function returns values between -1 and 1.
    # We scale and shift it according to the tanh_amplitude and tanh_center.
    tanh_component = 0.5*tanh_amplitude * np.tanh(tanh_steepness * (x - tanh_center))

    # Return the sum of the two components
    return linear_component + tanh_component

def tanh(x, xcenter,ycenter, tanh_amplitude, tanh_steepness):
    """
    Calculates the  hyperbolic tangent function.

    Args:
        x (float or array-like): The input value(s) for the function.
        tanh_center (float): The x-value where the tanh function is centered (i.e., its inflection point).
        tanh_amplitude (float): The maximum height/depth of the tanh function from its center.
                                A positive value makes the tanh function increase,
                                a negative value makes it decrease.
        tanh_steepness (float): Controls the steepness of the tanh transition.
                                Larger values make the transition sharper.

    Returns:
        float or array-like: The resulting y-value(s) of the summed function.
    """


    # Calculate the hyperbolic tangent component
    # The tanh function returns values between -1 and 1.
    # We scale and shift it according to the tanh_amplitude and tanh_center.
    tanh_component = ycenter + 0.5*tanh_amplitude * np.tanh(tanh_steepness * (x - xcenter))

    return  tanh_component


