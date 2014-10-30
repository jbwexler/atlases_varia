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
from parent_children_graph import toAtlas
from expand_syn import getSynonyms

with open('networkxGraph2.pkl','rb') as input:
    graph = pickle.load(input)

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
        

final = mapOntAtlas(graph, 'HarvardOxford-Cortical.xml')

for key, value in final.items():
    print key, value