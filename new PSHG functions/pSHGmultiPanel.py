# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 22:33:24 2021

@author: Ben
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from binary_mask import binary_mask
from skimage.morphology import disk
from skimage.filters import median

def pSHGmultiPanel(allSum, phi2, I2, intensityThresh, data_path):
    
    mask = binary_mask(intensityThresh, allSum)    #binary_mask(thresh,im):
    im = median(mask*phi2, disk(3))
    im = np.ma.masked_where(im == 0, im)
    
    mycm = plt.cm.get_cmap("hsv").copy()
    mycm.set_bad(color='black')    
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18, 6))
    
    p1 = ax1.imshow(allSum*mask, cmap = 'gray', vmin = 0, vmax = np.max(allSum))
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax1. axis('off')
    ax1.set_title('SHG intensity')
    plt.colorbar(p1, cax=cax, format = '%.0e')     

    p2 = ax2.imshow(phi2, cmap = 'hsv', vmin = 0, vmax = 180)
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax2. axis('off')
    ax2.set_title('Phi2 (degrees)')
    plt.colorbar(p2, cax=cax)    
    
    p3 = ax3.imshow(im, cmap = mycm,  vmin = 0, vmax = 180)
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax3. axis('off')
    ax3.set_title('Phi2 intensity thresholded')
    plt.colorbar(p3, cax=cax)
        
    im = median(mask*I2, disk(3))
    im = np.ma.masked_where(im == 0, im)
    
    mycm = plt.cm.get_cmap("hot").copy()
    mycm.set_bad(color='black') 
    
    p4 = ax4.imshow(im, cmap = mycm, vmin = 0, vmax = np.max(im))
    divider = make_axes_locatable(ax4)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax4. axis('off')
    plt.colorbar(p4, cax=cax)
    ax4. set_title('I2 intensity thresholded')
    
    plt.savefig(data_path + '\\' + 'pSHG multipanel.png', bbox_inches='tight',pad_inches=0)
    
    return mask