# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 22:00:13 2018

@author: Ben
"""

import numpy as np

def binary_mask(thresh,im):
    
    img = np.copy(im)
    thresh_idx = img < thresh
    img[thresh_idx] = 0
    thresh_idx = img >= thresh
    img[thresh_idx] = 1
    
    return img