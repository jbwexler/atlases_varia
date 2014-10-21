"""
converts the NIF-GrossAnatomy_reasonar.owl ontology into a networkx graph and saves the graph object as a .pkl file. using a networkx graph to find parents, children, etc. is much, much faster 
for our purposes than using rdflib to do a SPARQL query on the .owl.
"""

import rdflib
import nibabel
import cPickle as pickle
import networkx as nx


owl_file = '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl'
g = rdflib.Graph()
g.load(owl_file)
netx = nx.DiGraph()

nodesAndParents = {}

query = g.query(
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
            }} """)

for x in query:
    
    node = str(x.stringlabel).lower()
    parent = str(x.stringparlabel).lower()
    if not node in nodesAndParents.keys():
        nodesAndParents[node] = set([parent])
    else:
        nodesAndParents[node].add(parent)

for nodes in nodesAndParents.keys():
    netx.add_node(nodes)

for child, parents in nodesAndParents.items():
    for parent in parents:
        if parent != 'none':
            netx.add_edge(parent, child)

with open('networkxGraph.pkl','wb') as output:
    pickle.dump(netx, output, -1)


