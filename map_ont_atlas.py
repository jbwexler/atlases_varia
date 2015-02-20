"""
maps each region in an ontology graph to its best matching region in the atlas (using toAtlas).
output is a dictionary with atlas regions as keys and list of corresponding ontology regions as values.
"""

import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import networkx as nx
import cPickle as pickle
from networkx import NetworkXError
from parent_children_graph import * 
from expand_syn import getSynonyms
from boto.s3.multipart import Part
import xlwt
from itertools import izip_longest

def mapOntAtlas(graph, atlas_file, parentChildren, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'):
    tree = ET.parse(os.path.join(atlas_dir, atlas_file))
    root = tree.getroot()
    atlasRegions = [x.text.lower() for x in root[1]]
    
    synonymsDict = {}
    for region in atlasRegions:
        synonymsDict[region] = getSynonyms(region)
    
    mapDict = {}
    
    for region in atlasRegions:
            mapDict[region] = []
    
    for node in graph:
        nodeName = graph.node[node]['name']
        matches = toAtlas(nodeName, graph, atlasRegions, synonymsDict, parentChildren)
        if matches != 'none':
            for region in matches:
                mapDict[region].append(nodeName)
    return mapDict
        


def dontMap(graph, atlas_file, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'):
    map = mapOntAtlas(graph, atlas_file, atlas_dir)
    dontMapList = [key for key, value in map.items() if value == []]
    return dontMapList

def createMap(graph, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/', parentChildren = True):
    fullMap = {}
    for file in os.listdir(atlas_dir):
        if '.xml' in file and file != 'Talairach.xml': 
            map = mapOntAtlas(graph, file, parentChildren, atlas_dir)
            for key, value in map.items():
                fullMap[key] = value
    return fullMap


with open('NIFgraph.pkl','rb') as input:
    nif = pickle.load(input)
    
excel = xlwt.Workbook()
sheet1 = excel.add_sheet('sheet1')
justSyn = createMap(nif, parentChildren=False)
parChi = createMap(nif)
excelList = [[],[],[]]

# for atlasRegion in justSyn.keys():
#     sortedZip = izip_longest(justSyn[atlasRegion].sort(), parChi[atlasRegion].sort())
#     for (justRegion, parRegion) in sortedZip:
#         excelList[0].append(atlasRegion)
#         excelList[1].append(justRegion)
#         excelList[2].append(parRegion)
# for node in nif:
#     nodeName = nif.node[node]['name']
#     if nodeName .

totalDict = {}
mappedOntRegions = set()
for node in nif:
    nodeName = nif.node[node]['name']
    totalDict[nodeName] = {}
    totalDict[nodeName]['parChi'] = []
    totalDict[nodeName]['justSyn'] = []
for atlasRegion in parChi.keys():
    for ontRegion in parChi[atlasRegion]:
        totalDict[ontRegion]['parChi'].append(atlasRegion)
        mappedOntRegions.add(ontRegion)
for atlasRegion in justSyn.keys():
    for ontRegion in justSyn[atlasRegion]:
        totalDict[ontRegion]['justSyn'].append(atlasRegion)
        
count = 1
for ontRegion, dict in totalDict.items():
    sortedZip = izip_longest(sorted(dict['parChi']), sorted(dict['justSyn']))
    print sortedZip
    for (parChiRegion, justSynRegion) in sortedZip:
        sheet1.write(count,1, ontRegion)
        sheet1.write(count,2, justSynRegion)
        sheet1.write(count,3, parChiRegion)
        count += 1

for node in nif:
    nodeName = nif.node[node]['name']
    if nodeName not in mappedOntRegions:
        sheet1.write(count,1, nodeName)
        count +=1

excel.save('/Users/jbwexler/poldrack_lab/cs/other/ontmap.xls')  
    
        
    

