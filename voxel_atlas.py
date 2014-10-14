"""
returns voxels in an image that correspond to a certain value in an atlas
"""

import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True





def getAtlasVoxels(region, atlas_file, dir = '/Applications/fmri_progs/fsl/data/atlases/'):
	tree = ET.parse(os.path.join(dir, atlas_file))
	root = tree.getroot()
	summaryimagelist = []
	summaryimagefile = ''
	root_header = root.find('header')
	for images in root_header.findall('images'):
		print images
		if '2mm' in images.find('summaryimagefile').text:
			summaryimagefile = images.find('summaryimagefile').text
			
	atlas_name = summaryimagefile + '.nii.gz'
	atlas=nibabel.load(os.path.join(dir, atlas_name[1:]))
	atlas_data=atlas.get_data()
	name_value = 0
	data = root.find
	
	for i in range(len(root[1])):
		name = root[1][i].text.split('(')[0].replace("'",'').rstrip(' ').lower()
		if name == region.lower():
			name_value = i+1
			voxels = numpy.where(atlas_data==name_value)
			return voxels
	raise ValueError('"{region}" not in "{atlas_file}"'.format(region=region, atlas_name=atlas_file))
       
        
voxels = getAtlasVoxels('Corticospinal tract L','JHU-tracts.xml')
print voxels
for i in range(len(voxels[0])):
    if voxels[0][i] == 120 and voxels[1][i] == 54 and voxels[2][i] == 33:
        print "yay!"
