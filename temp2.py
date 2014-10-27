
import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import cPickle as pickle
import networkx as nx
from parent_children_graph import ontToGraph, toAtlas

ont_file = 'allen_brain_atlas_human_ontology_fixed.txt'
graph = ontToGraph(ont_file)

frontalLobeID = [n for n,d in graph.nodes_iter(data=True) if d['name'] == 'thalamus'][0]
# print toAtlas('amygdala', graph, 'HarvardOxford-Cortical.xml')
print toAtlas('external capsule, left', graph, 'HarvardOxford-Cortical.xml')


