from skimage.filters import gaussian, threshold_local
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from astropy.io import fits
import numpy as np
from sys import exit
import time
file_path = ""
data = fits.getdata(file_path)
x_low = 0
x_high = 20000
y_low = 0
y_high = 10000
data = data[y_low:y_high, x_low:x_high]

def gaussian_threshold(data, sigma, offset):
    g = gaussian(data, sigma=sigma)
    binary = data > (g + offset)
    return g, binary

def imshow(data, norm_low, norm_high, cmap="hot", dpi=15, figsize=(50, 50)):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.imshow(data, cmap=cmap, origin='lower', interpolation="none", norm=Normalize(norm_low, norm_high))
    plt.show()

""""
g, binary = gaussian_threshold(data, 5, 1)
imshow(data, 0, 70)
imshow(g, 0, 70)
imshow(data - g, 0, 1)
imshow(binary, 0, 1, "gray")
"""

g_blur, _ = gaussian_threshold(data, 10, 1)
final_mask = np.full(np.shape(g_blur), False)

sigma = 10
check_distance = 50
mult = 2
lower_peak_val = 5

g, binary = gaussian_threshold(data, sigma, 1)
rows, cols = np.where(binary == True)
g_test_left = np.transpose([g_blur[rows,np.minimum((cols + i), [len(data[0]) - 1]*len(cols))] for i in range(-check_distance, 0)])
g_test_right = np.transpose([g_blur[rows,np.minimum((cols + i), [len(data[0]) - 1]*len(cols))] for i in range(0, check_distance)])
print("Retrieved surrounding pixels")
padded = np.expand_dims(data[rows, cols],1)
padded = np.pad(padded, [[0, 0], [0, check_distance - 1]], 'edge')
print("Padding done")
g_check_left = padded > g_test_left * mult
g_check_left = np.any(g_check_left, axis=1)
print("Check left done")
g_check_right = padded > g_test_right * mult
g_check_right = np.any(g_check_right, axis=1)
print("Check right done")
#g_check = np.bitwise_and([True]*len(g_check_right), g_check_right)
g_check = np.bitwise_and(g_check_left, g_check_right)
g_peak_check = data[rows, cols] > lower_peak_val
print("Check peak done")
g_check = np.bitwise_and(g_check, g_peak_check)
indicies = np.transpose([rows[g_check], cols[g_check]])
print("Indicies done")
final_mask[rows[g_check], cols[g_check]] =True

imshow(g_blur, 0, 70)
imshow(binary, 0, 1)
imshow(data, 0, 70)
imshow(final_mask, 0, 1)

        
        
    
    
