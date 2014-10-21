

import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import cPickle as pickle
import networkx as nx
import timeit
import cPickle as pickle

import networkx as nx

with open('networkxGraph.pkl', 'rb') as input:
    netx = pickle.load(input)
    
for x in netx.successors_iter('intermediate hypothalamic region'):
    print x



