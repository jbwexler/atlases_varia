"""
converts the NIF-GrossAnatomy_reasonar.owl ontology into a networkx graph and saves the graph object as a .pkl file. using a networkx graph to find parents, children, etc. is much, much faster 
for our purposes than using rdflib to do a SPARQL query on the .owl.
"""

import rdflib
import nibabel as nb
import networkx as nx
import cPickle as pickle
import xml.etree.ElementTree as ET
from xml.dom import minidom

xmlFile = '/Applications/fmri_progs/fsl/data/atlases/HarvardOxford-Cortical.xml'
tree = ET.parse(xmlFile)
root = tree.getroot()
indices = [int(line.get('index')) for line in root[1]]
regions = [line.text.split('(')[0].replace("'",'').rstrip(' ').lower() for line in root[1]]

# dom = minidom.parse(xmlFile)


for x in root.find('data').findall('label'):
    print x.get('index')