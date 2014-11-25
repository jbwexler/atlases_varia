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
		if '2mm' in images.find('summaryimagefile').text:
			summaryimagefile = images.find('summaryimagefile').text
			
	atlas_name = summaryimagefile + '.nii.gz'
	atlas=nibabel.load(os.path.join(dir, atlas_name[1:]))
	atlas_data=atlas.get_data()
	name_value = 0

	for i in range(len(root[1])):
		name = root[1][i].text.split('(')[0].replace("'",'').rstrip(' ').lower()
		print name
		if name == region.lower():
			name_value = i+1
			voxels = numpy.where(atlas_data==name_value)
			return voxels
	raise ValueError('"{region}" not in "{atlas_file}"'.format(region=region, atlas_file=atlas_file))
       
        
# voxels = getAtlasVoxels('Corticospinal tract L','JHU-tracts.xml')



def voxelToRegion(X,Y,Z,atlas_file, dir = '/Applications/fmri_progs/fsl/data/atlases/'):
	tree = ET.parse(os.path.join(dir, atlas_file))
	root = tree.getroot()
	summaryimagelist = []
	summaryimagefile = ''
	root_header = root.find('header')
	for images in root_header.findall('images'):
		if '2mm' in images.find('summaryimagefile').text:
			summaryimagefile = images.find('summaryimagefile').text
			
	atlas_name = summaryimagefile + '.nii.gz'
	atlas=nibabel.load(os.path.join(dir, atlas_name[1:]))
	atlas_data=atlas.get_data()
	atlasRegions = [x.text.lower() for x in root[1]]
	index = atlas_data[X,Y,Z] - 1
	print index
	if index == -1:
		return 'none'
	else:
		return atlasRegions[index]

	
print voxelToRegion(45, 16, 36,'HarvardOxford-Cortical.xml')
	
	