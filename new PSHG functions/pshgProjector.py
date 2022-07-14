# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 16:05:17 2022

@author: Ben
"""
from skimage.morphology import disk
from skimage.filters import median
import numpy as np


def pshgProjector(pshg, angles):
    

    anglesArr = np.zeros((len(pshg),512,512))

    for idx in range(len(angles)):
        anglesArr[idx,:,:] = np.ones((512,512))*angles[idx]

    cos2 = np.cos(2*anglesArr)
    cos4 = np.cos(4*anglesArr)
    sin2 = np.sin(2*anglesArr)
    sin4 = np.sin(4*anglesArr)

    a0 = 1*np.mean(pshg,0) + 1
    a2 = 2*np.mean(pshg*cos2,0)
    a4 = 2*np.mean(pshg*cos4,0)
    b2 = 2*np.mean(pshg*sin2,0)
    b4 = 2*np.mean(pshg*sin4,0)

    # newA0c = signal.fftconvolve(newA0,kernel, mode ='same') 
    a0c = median(a0, disk(3)) 
    a2c = median(a2, disk(3)) / a0c
    a4c = median(a4, disk(3)) / a0c
    b2c = median(b2, disk(3)) / a0c
    b4c = median(b4, disk(3)) / a0c


    I2 = np.sqrt(a2c**2 + b2c**2)
    Phi = 0.5*np.arctan2(b2c,a2c)*180/np.pi
    Phi2 = (Phi>=0)*Phi + (Phi<=0)*(Phi+180)
    
    return I2, Phi2