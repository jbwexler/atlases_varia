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

with open('networkxGraph2.pkl','rb') as input:
    nif = pickle.load(input)

ont_file = 'allen_brain_atlas_human_ontology_fixed.txt'
allen = ontToGraph(ont_file)


def mapOntAtlas(graph, atlas_file, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'):
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
        matches = toAtlas(nodeName, graph, atlasRegions, synonymsDict)
        if matches != 'none':
            for region in matches:
                mapDict[region].append(nodeName)
    return mapDict
        


def dontMap(graph, atlas_file, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'):
    map = mapOntAtlas(graph, atlas_file, atlas_dir)
    dontMapList = [key for key, value in map.items() if value == []]
    return dontMapList

# atlas = 'Juelich.xml'
# nifDont = dontMap(nif, atlas)
# allenDont = dontMap(allen, atlas)
# allenMap = mapOntAtlas(allen, atlas)
# 
# print 'NIF \n'
# 
# for region in nifDont:
#     print region
# 
# print
# print 'Allen \n'
# for region in allenDont:
#     print region
# print
# 
# print 'dif \n'
# for region in nifDont:
#     if region not in allenDont:
#         print '----%s----' % region
#         for part in allenMap[region]:
#             print part
#         print