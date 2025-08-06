import pandas as pd
import matplotlib.pyplot as plt

#READ_LAYERS: reads profile data from an ImageJ CSV file

#path = '/Users/name/file location'
#data = path + 'file name'


#Read data from a csv file (ImageJ format)
def read(filename):
    file = pd.read_csv(filename)
    x = file['Distance_(pixels)']
    y = file['Gray_Value']
    return x, y



#Choose a starting value, ending value, and range. This function averages the grayscale values
#at the start and end values over the range, then subtracts them and outputs the contrast as
#a % of the starting value. Note that several papers use an alternative way to determine
#contrast: (m1-m2)/(m1+m2) instead of (m1-m2)/m1
def EdgeFit(filename, s1, s2, r):
    x, y = read(filename)

    start_range_x = x.iloc[s1-r:s1+r]
    end_range_x = x.iloc[s2-r:s2+r]
    start_range_y = y.iloc[s1-r:s1+r]
    end_range_y = y.iloc[s2-r:s2+r]

    m1 = start_range_y.mean()
    m2 = end_range_y.mean()
    contrast = 100*abs((m1-m2)/m1)

    return start_range_x, end_range_x, start_range_y, end_range_y, contrast



#Plots data from csv file with option to display contrast between a start and end region
#Data points being averaged are shown in red
def DataPlot(filename, title, edgefit = False, s1 = 0, s2 = 0, r = 0):
    x, y = read(filename)

    plt.plot(x, y, 'b')
    plt.xlabel('Distance (pixels)')
    plt.ylabel('Grayscale value')
    plt.title(title)

    if edgefit:
        srx, erx, sry, ery, contrast = EdgeFit(filename, s1, s2, r)
        plt.plot(srx, sry, 'r')
        plt.plot(erx, ery, 'r')
        plt.title(title + ' (contrast = %.1f'%contrast+'%)')

    plt.show()

################################################################################
#Evaluate

#Plot data
#DataPlot(data, 'Title')

#Plot data with start and end regions selected to show contrast
#DataPlot(data, 'Title', True, start, end, range)