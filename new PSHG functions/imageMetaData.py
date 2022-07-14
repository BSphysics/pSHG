# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:58:03 2022

@author: Ben
"""

from ScanImageTiffReader import ScanImageTiffReader

def imageMetaData(data_path, files_tiff):    
    
    filename = data_path + r'/' + files_tiff[0]
    # vol = ScanImageTiffReader(filename).data();
    # des = ScanImageTiffReader(filename).description(0);
    md = ScanImageTiffReader(filename).metadata();

    slices = md.find('numSlices')
    zoom = md.find('scanZoomFactor')
    acqState = md.find('acqState')
    trig = md.find('trigAcqEdge')

    # print(md[slices : slices+14])
    # print(md[zoom:zoom+19])
    # print(md[acqState:acqState+17])
    # print(md[trig:trig+23])

    lines = [md[slices : slices+14] , md[zoom:zoom+19] , md[acqState:acqState+18], md[trig:trig+24]]

    filename = data_path + '/Image meta data.txt'
    with open(filename, 'w') as f:
        f.writelines(lines)
    f.close()