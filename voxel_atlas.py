"""
returns voxels in an image that correspond to a certain value in an atlas
"""

import nibabel
import xml.etree.ElementTree as ET
import numpy
from __builtin__ import True


atlas=nibabel.load('/Applications/fmri_progs/fsl/data/atlases//HarvardOxford/HarvardOxford-cort-maxprob-thr25-2mm.nii.gz')
atlas_data=atlas.get_data()

def getAtlasVoxels(region, xmlFile):
    tree = ET.parse('/Applications/fmri_progs/fsl/data/atlases/' + xmlFile)
    root = tree.getroot()
    name_value = 0
    print "Region: %s"%region
    for i in range(len(root[1])):
        #idx = int(root[1][i].attrib['index'])
        name = root[1][i].text.split('(')[0].replace("'",'').rstrip(' ').lower()
        print "Name: %s"%name
        if name == region:
            name_value = i+1
    voxels = numpy.where(atlas_data==name_value)
    return voxels
        
#voxels = getAtlasVoxels('occipital pole','HarvardOxford-Cortical.xml')
#print voxels
#for i in range(len(voxels[0])):
#    if voxels[0][i] == 40 and voxels[1][i] == 15 and voxels[2][i] == 49:
#        print "yay!"
