"""
takes string of brain region from data and returns list of relevant brain region(s) that are in atlas
"""

import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
from expand_syn import*
import networkx as nx
import cPickle as pickle

def ontToGraph(ont_file, ont_dir = '/Users/jbwexler/poldrack_lab/cs/other'):
    
    ont_file = os.path.join(ont_dir, ont_file)
    f=open(ont_file)
    f.readline().strip().split('\t')
    lines=[i.strip().split('\t') for i in f.readlines()]
    f.close()
            
    g = nx.DiGraph()
    for line in lines:
        if line[0] != '':
            node_name = line[2].replace('"', '')
            node_id = int(line[0])
            g.add_node(node_id, {'name':node_name})
        
    for line in lines:
        if line[0] != '':
            cur_id = int(line[0])
            if line[8] != '':
                parent_id = int(line[8])
                g.add_edge(parent_id, cur_id)
    return g

def findNodes(graph, startNode, targets, direction = 'children'):
    synAndTargets = [e for e in getSynonyms(graph.node[startNode]['name']) if e in targets]
    if len(synAndTargets) > 0:
        return synAndTargets
    else:
        matchingRelatives = []
        if direction == 'parents':
            for child in graph.predecessors_iter(startNode):
                matchingRelatives += findNodes(graph, child, targets, direction)
        else:
            for child in graph.successors_iter(startNode):
                matchingRelatives += findNodes(graph, child, targets, direction)
        return matchingRelatives


def toAtlas(region, graph, atlas_file, atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'):
    
    tree = ET.parse(os.path.join(atlas_dir, atlas_file))
    root = tree.getroot()
    targets = [x.text.lower() for x in root[1]]
    final_list = []
    
#checking if region or synonyms exist in atlas. if so, simply return region
    synonyms = getSynonyms(region)
    for name in targets:
        if name in synonyms:
            final_list.append(name)
            return final_list
        
    
    
    
    region_id = [n for n,d in graph.nodes_iter(data=True) if d['name'] == region][0]
    
    matchingChildren = findNodes(graph, region_id, targets)

    if len(matchingChildren) > 0:
        return matchingChildren
    else:
        matchingParents = findNodes(graph, region_id, targets, 'parents')
        if len(matchingParents) > 0:
            return matchingParents
    return 'none'
   
 


# with open('networkxGraph1.pkl','rb') as input:
#     graph = pickle.load(input)
# ont_file = 'allen_brain_atlas_human_ontology_fixed.txt'
# graph = ontToGraph(ont_file)
# 
# 
# print toAtlas('frontal lobe', graph, 'HarvardOxford-Cortical.xml')
