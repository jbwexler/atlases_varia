

import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import networkx as nx
import cPickle as pickle
from networkx import NetworkXError
from expand_syn import getSynonyms

# from parent_children_graph import toAtlas



with open('networkxGraph2.pkl','rb') as input:
    netx = pickle.load(input)

atlas_file = 'HarvardOxford-Cortical.xml'
atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'
tree = ET.parse(os.path.join(atlas_dir, atlas_file))
root = tree.getroot()
targets = [x.text.lower() for x in root[1]]


print [n for n,d in netx.nodes_iter(data=True) if d['name'] == 'frontal lobe']

    
def findNodes(graph, startNode, atlasRegions, direction = 'children'):
    synAndTargets = [e for e in getSynonyms(graph.node[startNode]['name']) if e in atlasRegions]
    print netx.node[startNode]['name']
    if len(synAndTargets) > 0:
        print synAndTargets
        return synAndTargets
    else:
        matchingRelatives = []
        if direction == 'parents':
            if len(graph.successors(startNode)) == 0:
                print 'STOP'
            for child in graph.predecessors_iter(startNode):
                matchingRelatives += findNodes(graph, child, atlasRegions, direction)
        else:
            if len(graph.successors(startNode)) == 0:
                print 'STOP'
            for child in graph.successors_iter(startNode):
                matchingRelatives += findNodes(graph, child, atlasRegions, direction)
        return matchingRelatives

if raw_input('Recursion? (y/n) ') == 'y':

    while True:
        startNode = raw_input("startNode: ").lower()
        direction = raw_input("direction: (p/c) ")
        region_id = [n for n,d in netx.nodes_iter(data=True) if d['name'] == startNode][0]
        print
        try:
            if direction == 'c':
                for x in findNodes(netx, region_id, targets):
                    print '\t' + x
            else:
                for x in findNodes(netx, region_id, targets, 'parents'):
                    print '\t' + x
        except NetworkXError:
            print "not in fuckin' graph"   

else:
        
    while True:
        startNode = raw_input("startNode: ").lower()
        direction = raw_input("direction: (p/c) ")
        region_id = [n for n,d in netx.nodes_iter(data=True) if d['name'] == startNode][0]
        print
        try:
            if direction == 'c':
                for x in netx.successors_iter(region_id):
                    print netx.node[x]['name']
            else:
                for x in netx.predecessors_iter(region_id):
                    print netx.node[x]['name']
        except NetworkXError:
            print "not in fuckin' graph"
   
  
# print toAtlas('frontal lobe', netx, 'HarvardOxford-Cortical.xml')



# for node, d in netx.nodes_iter(data=True):
#     try:
#         john = d['name']
#     except KeyError:
#         print node, d
#         print "AHHHHHHH!HHH!H!H!"
