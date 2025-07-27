import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.pyplot import cm



def read(filename):
    file = pd.read_csv(filename)
    x = file['Distance_(pixels)']
    y = file['Gray_Value']
    return x, y


def EdgeFit(filename, center, width):
    x, y = read(filename)
    start_range_x = x.iloc[center-width:center+width]
    # end_range_x = x.iloc[s2-r2:s2+r2]
    start_range_y = y.iloc[center-width:center+width]
    # end_range_y = y.iloc[s2-r2:s2+r2]
    mean = start_range_y.mean()
    # m2 = end_range_y.mean()
    # contrast = (m1 - m2)/np.max([m1,m2])*100
    # print('Contrast = ' + str(contrast))
    return start_range_x, start_range_y, mean


def DataPlot(filename, title, edgefit = False, centers = [], ranges = [], normalize=True,save=False):
    xtest, ytest = read(filename)
    plt.figure()
    plt.plot(xtest, ytest, 'gray',linewidth=1)
    plt.xlabel('Distance (pixels)')
    plt.ylabel('Grayscale value')
    plt.title(title)
    colors = ['r','g','b','purple','orange','black']
    maxmean = 1.0
    
    if edgefit:
        if normalize:
            means = []
            for c,w,color in zip(centers,ranges,colors):
                srx_, sry_, mean_ = EdgeFit(filename, c ,w)
                means.append(mean_)
            maxmean = np.max(means)
            lgd_title = 'Contrast'
        else:
            lgd_title = 'Region Means'
        for c,w,color in zip(centers,ranges,colors):
            srx, sry, mean = EdgeFit(filename, c ,w)
            if normalize:
                lbl = str(round((maxmean-mean)/maxmean*100,2))+'%'
            else:
                lbl = str(round(mean,2))
            plt.plot(srx, sry, color,label=lbl)
            # plt.plot(erx, ery, 'r')
            xtest1,ytest1 = xtest.values, ytest.values
            # contrast_str = 'Contrast = ' + str(abs(round(contrast,1)))+'%'
            lower_x = xtest1[0] + 0.75*(xtest1[-1]-xtest1[0])
            lower_y = np.max(ytest1) - 0.25*(np.max(ytest1)-np.min(ytest1))
            
            # plt.text(x=125,y=94,s=mean)
        plt.legend(title=lgd_title,fontsize=10,loc='best')
    if save:
        file_to_save = os.path.splitext(filename)[0] + '_layer_analysis.jpg'
        plt.savefig(file_to_save)
    plt.show()
    
path = '/Users/carterfox/Library/CloudStorage/GoogleDrive-cdfox@wisc.edu/.shortcut-targets-by-id/1riZacJd_1_jmKfGgrjDuP7KcecvMS3i2/Xiao research group/Lab Data (Xiao and Wang groups)/StackingTransitions/CrI3/contrast_tests/'
# mono2 = path+'mono2.csv'
# mono2bi = path+'mono2_bilayer.csv'
# mono2_small_mono = path+'mono2-smallmono.csv'
# mono1 = path+'mono1.csv'
# CrPS4 = path+'crps4.csv'
CrI3 = path+'CrI3-CCFC_3_MM_50x-2_linecut.csv'

#CrSBr 95deg
DataPlot(CrI3, 'CrI3',edgefit=True, centers=[26,94,140], ranges=[20,15,20],normalize=True, save=True)
# DataPlot(mono2, 'Bilayer2',True, 20, 70, 15,15,True)
# DataPlot(mono2_small_mono, 'True Monolayer', True, 50, 34, 8,4,True)
# DataPlot(mono2bi, 'Trilayer',True, 20, 90, 15,15,True)

# CrI3
# DataPlot(CrPS4, 'CrPS4 Monolayer',True,35,240,30,20,True)
# DataPlot(CrPS4, 'CrPS4 Bilayer',True,35,137,30,4,True)






