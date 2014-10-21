
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

nodesAndParents = {}

for x in g.query(
           """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ro: <http://www.obofoundry.org/ro/ro.owl#>
            PREFIX ont: <http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#>
            SELECT (str(?label) as ?stringlabel) (str(?parlabel) as ?stringparlabel) (str(?chilabel) as ?stringchilabel)
            WHERE { 
            ?region rdfs:subClassOf+ ont:birnlex_1167.
            ?region rdfs:label ?label.
            OPTIONAL {
            ?region rdfs:subClassOf ?restrictionPar.
            ?restrictionPar owl:onProperty ro:proper_part_of.
            ?restrictionPar owl:someValuesFrom ?parent.
            ?parent rdfs:label ?parlabel.}
            OPTIONAL {?region rdfs:subClassOf ?restrictionChi.
            ?restrictionChi owl:onProperty ro:has_proper_part.
            ?restrictionChi owl:someValuesFrom ?child.
            ?child rdfs:label ?chilabel.
            }} """):

    
    nodesAndParents[str(x.stringlabel).lower()] = [str(x.stringparlabel).lower(), str(x.stringchilabel).lower()]
    print nodesAndParents[str(x.stringlabel).lower()]
    
for x in nodesAndParents:
    netx.add_node(x)

for x in nodesAndParents:
    if len(nodesAndParents[x][0]) != 'none':
        netx.add_edge(nodesAndParents[x])
        

with open('networkxGraph2.pkl','wb') as output:
    pickle.dump(netx, output, -1)


