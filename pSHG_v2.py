# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 21:49:31 2021
@author: Ben

 Code to analyse polarisation resolved second harmonic generation data set acquired in Physics 123D

"""
import os
scriptDir = os.getcwd()
import sys
sys.path.append(os.path.join(scriptDir,"new pSHG functions" ))
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from tiff_loader import tiff_loader
plt.close('all')

#%% Select folder where pSHG data is saved and read all images into memory
from pSHG_GUI import pSHGGUI


defaultDir = scriptDir + '\\Test data'
initialDir = r'C:\Users\bs426\OneDrive - University of Exeter\!Work\Work.2022\Data\123D'
defaultThreshold = 1e2

[data_path, plotHistograms, pSHGFitViewer, plotPolarHistogram, arrowPlot, uselassoROI, useSlider, thresh] = pSHGGUI(initialDir, defaultDir, defaultThreshold)
    
#%%
[filenames, imgs] = [[],[]]
filenames, imgs = tiff_loader(data_path)

from imageMetaData import imageMetaData
imageMetaData(data_path, filenames)

#%% 
[pshg, ptpf, sumSHG, sumTPF, I2, Phi2] = [[],[],[],[],[],[]]

for idx in range(len(imgs)-2): #MAIN LOOP

    im = imgs[idx]
    if im.ndim>2:
        shg = im[0,:,:]
        tpf = im[1,:,:]
        shg[shg<0] = 0
        tpf[tpf<0] = 0
    
    else:
        shg = im
        shg[shg < 0] = 0
        tpf=0

    pshg.append(shg)
    ptpf.append(tpf)
    sumSHG.append(np.sum(shg))
    sumTPF.append(np.sum(tpf))

pshg = np.asarray(pshg)    
allSum = np.sum(pshg,0)

from pshgProjector import pshgProjector
delta = 25
angles = (np.arange(0,len(pshg))*15 - delta) *np.pi/180
[I2, Phi2] = pshgProjector(pshg, angles)

#%%
if useSlider==True:
    from slider_thresh import sliderThresh
    plt.ion()
    slide = sliderThresh(allSum)
    plt.show()
    plt.pause(0.1)
    while True:
        if plt.waitforbuttonpress(): break  # Exit loop if user presses a key.
    print('\n Threshold = ' + str(np.round(slide.val)))
    plt.close(fig = 1)
    thresh = slide.val
#%%
from pSHGmultiPanel import pSHGmultiPanel
mask = pSHGmultiPanel(allSum, Phi2, I2, thresh, data_path)
#%%
if arrowPlot == True:
    from pSHG_arrows import pSHGArrows
    pSHGArrows(I2, Phi2, allSum, mask, data_path)
#%% View individual pixel fits
if pSHGFitViewer == True:
    from pSHGfitviewer import pSHGFitViewer
    pSHGFitViewer(pshg, I2, Phi2, mask, angles, data_path)
    
#%% Plot pSHG histograms

from pSHG_histograms import pSHGhistograms
if plotHistograms == True:
      
    [bins , binCounts] = pSHGhistograms(Phi2, mask,'Phi2', data_path)
    [bins , binCounts] = pSHGhistograms(I2, mask,'I2', data_path)

if plotPolarHistogram == True: 
    from pSHGpolar import pSHGpolar
    pSHGpolar(binCounts, data_path)         # Plot plot of the Phi2 histogram

#%%
plt.close('all')
if uselassoROI == True:
   
    from lassoROI import lassoROI  
    
    time2wait = 10
    [ROI , lassoSavePath] = lassoROI(allSum, Phi2, I2, mask, time2wait, data_path) #ROI is a mask than is 0 outside, and 1 inside the hand draw region
                          # lassoROI(im, phi2, I2, mask, time2wait, data_path)
    ROI[ROI==0] = np.inf
    [bins , binCounts] = pSHGhistograms(Phi2*ROI, mask, 'Phi2', lassoSavePath)
    [bins , binCounts] = pSHGhistograms(I2*ROI, mask, 'I2', lassoSavePath)
   
plt.close('all')
path = os.path.realpath(data_path)
os.startfile(path)   

#%%

from binary_mask import binary_mask
mask = binary_mask(thresh, allSum) 

allSumThresh = np.zeros((512,512)) 

allSumThresh[allSum > thresh] = 1









