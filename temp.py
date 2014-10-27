

import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import networkx as nx
import cPickle as pickle
from networkx import NetworkXError

# from parent_children_graph import toAtlas



with open('networkxGraph1.pkl','rb') as input:
    netx = pickle.load(input)


# for z in graph:
#     print z
#     print graph.node[z]['name']

    
        
while True:
    startNode = raw_input("startNode: ").lower()
    direction = raw_input("direction: (p/c) ")
    print
    try:
        if direction == 'c':
            for x in netx.successors_iter(startNode):
                print x
        else:
            for x in netx.predecessors_iter(startNode):
                print x
    except NetworkXError:
        print "not in fuckin' graph"
   
  
print toAtlas('frontal lobe', netx, 'HarvardOxford-Cortical.xml')



# for node, d in netx.nodes_iter(data=True):
#     try:
#         john = d['name']
#     except KeyError:
#         print node, d
#         print "AHHHHHHH!HHH!H!H!"
