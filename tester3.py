import rdflib
import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
from __builtin__ import True
import cPickle as pickle
import networkx as nx
import timeit


john = 'omg!!!!!!!'

with open('networkxGraphTest.pkl','wb') as output:
    pickle.dump(john, output, -1)