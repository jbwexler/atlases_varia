
import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import cPickle as pickle
import networkx as nx


owl_file = '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl'
g = rdflib.Graph()
g.load(owl_file)
netx = nx.DiGraph()

for c in "Hey baby! How are you today?":
    netx.add_node(c, {'name': c + '-yeah'})



with open('networkxGraph.pkl','wb') as output:
    pickle.dump(netx, output, -1)
 
 
with open('networkxGraph.pkl','rb') as input:
    graph = pickle.load(input)


for z in graph:
    print z
    print graph.node[z]['name']