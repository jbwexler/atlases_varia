"""
converts the NIF-GrossAnatomy_reasonar.owl ontology into a networkx graph and saves the graph object as a .pkl file. using a networkx graph to find parents, children, etc. is much, much faster 
for our purposes than using rdflib to do a SPARQL query on the .owl.
update: now that there are separate queries checking for parent relationships and child relationships, using the reasoner on the owl file is no longer necessary
"""

import rdflib
import nibabel
import os.path
import networkx as nx
import cPickle as pickle
import timeit


def storeOntAsGraph(owlPath, pklFile, pklDir = ''):
    t = timeit.Timer
    g = rdflib.Graph()
    g.load(owlPath)
    netx = nx.DiGraph()
    
    # query owl file for all regions that are subclasses of birnlex_1167 (aka 'regional part of brain')
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
    
    # query for all regions that have some sort of parent relationship and also finds the parent region
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
    
    # query for all regions that have some sort of child relationship and also finds the child region
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
    
    # adding nodes to graph for all regions in 'regional part of brain' and includes their name
    for x in allQuery:
        node = str(x.stringregion).lower()
        print node
        node_name = str(x.stringlabel).lower()
        netx.add_node(node, {'name':node_name})
    
    # adding edges for all pairs found from parentQuery
    for x in parentsQuery:
        node = str(x.stringregion).lower()
        parent = str(x.stringparent).lower()
        netx.add_edge(parent, node)    
    
    # adding edges for all pairs found from childQuery
    for x in childrenQuery:
        node = str(x.stringregion).lower()
        child = str(x.stringchild).lower()
        netx.add_edge(node, child)    
     
    with open(os.path.join(pklDir, pklFile),'wb') as output:
        pickle.dump(netx, output, -1)
    
t = storeOntAsGraph('http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#', 'networkxGraph2.pkl')



