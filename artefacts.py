import plotting
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tqdm import tqdm

def absolute_symmetry(value1, value2, margin):
    if abs(value1) == abs(value2) or abs(value1) == abs(value2) + margin or abs(value1) == abs(value2) - margin:
        return True
    else:
        return False

def check_for_symmetry(peaksmax, peaksmin, margin_of_error):
    center_index = None
    min_start1 = 0
    min_start2 = 1
    symmetry = False
    
    for i in range(len(peaksmax)):
        if peaksmax[i] == 0:
            center_index = i
    
    if center_index == None:
        print("Center index = null")
        return False
    
    for i in range(len(peaksmin)):
        if peaksmin[i] > 0 and peaksmin[min_start2] < 0:
            min_start1 = i
            break
        min_start2 += 1
        
    if absolute_symmetry(peaksmax[center_index - 1], peaksmax[center_index + 1], margin_of_error) and absolute_symmetry(peaksmin[min_start1], peaksmin[min_start2], margin_of_error):
        symmetry = True
    
    return symmetry

full_data = False #Ändra till false om man inte vill dela upp hela datan
file_path = "C:/Users/joaki/Pictures/Q1-latest-whigal-85.fits"

if full_data:
    data_list = []
    xslice = 10000
    yslice = 7000

    with fits.open(file_path, use_fsspec=True, fsspec_kwargs={"anon": True}) as hdul:  
       #cutout = hdul[0].section[0:1750, 0:2500] 
        for i in tqdm(range(0, int(7000/yslice))):
            for j in tqdm(range(0, int(120000/xslice))):
                cutout = hdul[0].section[yslice*i:yslice*i + yslice, xslice*j:xslice*j+xslice]
                data_list.append(cutout)
else:
    x_low = 15470*5
    x_high = 15495*5
    y_low = 575*5
    y_high = 595*5
    data = fits.getdata(file_path)
    #x_low = 11840*5
    #x_high = 11875*5
    #y_low = 725*5
    #y_high = 755*5
    data = data[y_low:y_high, x_low:x_high]
    

maxim = data.argmax()
index = np.unravel_index(maxim, data.shape)
print(index)
plotting.plot_figure(data,"Artefakt")

size = 40

datap = data[index[0], (index[1]-size):(index[1]+size)]
X = np.linspace(0,2*size-1, num=2*size)

peaksh, _ = find_peaks(datap) #List of local maxima
peaksl, _ = find_peaks(-datap) #List of local minima


print(size-peaksl)
print(size-peaksh)
print(check_for_symmetry((size-peaksh), (size-peaksl), 1))

plt.plot(peaksh, datap[peaksh], "x")
plt.plot(peaksl, datap[peaksl], 'x')
plt.plot(X,datap)
plt.show()

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    maski = dist_from_center <= (radius-1)
    masko = dist_from_center <= radius
    mask = masko^maski
    return mask

h = y_high - y_low   
w = x_high - x_low
center = (index[1], index[0])

def check_circular(data, radius_max):
    aver = np.zeros(radius_max)
    for r in range(1,radius_max):
        mask = create_circular_mask(h,w, center = center, radius = r)
        aver[r] = np.mean(mask*data)
        #plotting.plot_figure(mask*data,'test')
    aver[0] = data[index[0],index[1]]
    return aver
    
aver = check_circular(data, 40)
plt.plot(range(len(aver)), aver)
plt.show()


'''
    x_low = 15470*5
    x_high = 15495*5
    y_low = 575*5
    y_high = 595*5

    x_low = 11540*5
    x_high = 11565*5
    y_low = 636*5
    y_high = 656*5
    
    x_low = 11840*5
    x_high = 11875*5
    y_low = 725*5
    y_high = 755*5
'''