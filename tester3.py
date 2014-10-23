"""
converts the NIF-GrossAnatomy_reasonar.owl ontology into a networkx graph and saves the graph object as a .pkl file. using a networkx graph to find parents, children, etc. is much, much faster 
for our purposes than using rdflib to do a SPARQL query on the .owl.
"""

import rdflib
import nibabel
import networkx as nx
import cPickle as pickle



owl_file = '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl'
g = rdflib.Graph()
g.load(owl_file)
netx = nx.DiGraph()

nodesAndParents = {}
parentNames = {}

proper_part_ofQuery = g.query(
           """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ro: <http://www.obofoundry.org/ro/ro.owl#>
            PREFIX ont: <http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#>
            SELECT (str(?label) as ?stringlabel) (str(?parlabel) as ?stringparlabel) (str(?region) as ?stringregion) (str(?parent) as ?stringparent) 
            WHERE { 
            ?region rdfs:subClassOf+ ont:birnlex_1167.
            ?region rdfs:label ?label.
            OPTIONAL {
            ?region rdfs:subClassOf ?restrictionPar.
            ?restrictionPar owl:onProperty ro:proper_part_of.
            ?restrictionPar owl:someValuesFrom ?parent.
            ?parent rdfs:label ?parlabel.}
             }
            """)

count = 0
for x in proper_part_ofQuery:
    count += 1
    node = str(x.stringregion).lower()
    node_name = str(x.stringlabel).lower()
    parent = str(x.stringparent).lower()
    parentName = str(x.stringparlabel).lower()
    print parent
    print parentName
    if not node in nodesAndParents.keys():
        nodesAndParents[node] = [node_name, set([parent])]
    else:
        nodesAndParents[node][1].add(parent)
    if parent != 'none':
        parentNames[parent] = parentName
    
    if count == 50:
        break

for parent, name in parentNames.items():
    if parent not in nodesAndParents.keys():
        nodesAndParents[parent] = [name, set(['none'])]
     
for node in nodesAndParents.keys():
    node_name = nodesAndParents[node][0]
    netx.add_node(node, {'name':node_name})
 
for child, values in nodesAndParents.items():
    parents = values[1]
    for parent in parents:
        if parent != 'none':
            netx.add_edge(parent, child)
             
        
pkl_file = 'networkxGraph2.pkl'
 
with open(pkl_file,'wb') as output:
    pickle.dump(netx, output, -1)
     
with open(pkl_file,'rb') as input:
    graph = pickle.load(input)

# print 'yoooooo'
# for x in graph:
#     print x

