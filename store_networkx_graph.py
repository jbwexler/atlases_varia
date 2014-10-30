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
nodesAndChildren = {}


allQuery = g.query(
           """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ro: <http://www.obofoundry.org/ro/ro.owl#>
            PREFIX ont: <http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#>
            SELECT (str(?label) as ?stringlabel)  (str(?region) as ?stringregion) 
            WHERE { 
            ?region rdfs:subClassOf+ ont:birnlex_1167.
            ?region rdfs:label ?label.
             }
            """)

parentsQuery = g.query(
           """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ro: <http://www.obofoundry.org/ro/ro.owl#>
            PREFIX ont: <http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#>
            SELECT (str(?label) as ?stringlabel) (str(?region) as ?stringregion) (str(?parent) as ?stringparent) 
            WHERE { 
            ?region rdfs:subClassOf+ ont:birnlex_1167.
            ?region rdfs:label ?label.
           
            ?region rdfs:subClassOf ?restrictionPar.
            {?restrictionPar owl:onProperty ro:proper_part_of}
            UNION  {?restrictionPar owl:onProperty ro:located_in}
            UNION  {?restrictionPar owl:onProperty ro:contained_in}
            UNION  {?restrictionPar owl:onProperty ro:integral_part_of}
            ?restrictionPar owl:someValuesFrom ?parent.
            ?parent rdfs:subClassOf+ ont:birnlex_1167.
             }
            """)

childrenQuery = g.query(
            """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ro: <http://www.obofoundry.org/ro/ro.owl#>
            PREFIX ont: <http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#>
            SELECT (str(?label) as ?stringlabel)  (str(?region) as ?stringregion) (str(?child) as ?stringchild) 
            WHERE { 
            ?region rdfs:subClassOf+ ont:birnlex_1167.
            ?region rdfs:label ?label.
            ?region rdfs:subClassOf ?restrictionChi.
            {?restrictionChi owl:onProperty ro:has_integral_part}
            UNION  {?restrictionChi owl:onProperty ro:has_part}
            UNION  {?restrictionChi owl:onProperty ro:has_proper_part}
            ?restrictionChi owl:someValuesFrom ?child.
            ?child rdfs:subClassOf+ ont:birnlex_1167.
             }
             """)


for x in allQuery:
    node = str(x.stringregion).lower()
    node_name = str(x.stringlabel).lower()
    print node
    print node_name
    netx.add_node(node, {'name':node_name})
    
for x in parentsQuery:
    node = str(x.stringregion).lower()
    parent = str(x.stringparent).lower()
    print parent, node
    netx.add_edge(parent, node)    
    
for x in childrenQuery:
    node = str(x.stringregion).lower()
    child = str(x.stringchild).lower()
    print child, node
    netx.add_edge(node, child)    
        
pkl_file = 'networkxGraph2.pkl'
 
with open(pkl_file,'wb') as output:
    pickle.dump(netx, output, -1)
    