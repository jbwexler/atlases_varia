"""
NIFChildren takes two strings: the name of a brain region and the location of the owl ontology file. 
it returns a list of strings of the children of this brain region according to the ontology.
NIFParents does the same, but finds the parents.
"""

import rdflib


def NIFChildren(region, file):
    g = rdflib.Graph()
    g.load(file)
    
    children = []
    for row in g.query(
            """
            SELECT (str(?chiLabel) as ?chiLabelString) WHERE {
            ?region rdfs:label ?s
            FILTER(str(?s)="Hypothalamus").
            ?restriction owl:onProperty ro:proper_part_of;
            owl:someValuesFrom ?region.
            ?children rdfs:subClassOf ?restriction. 
            ?children rdfs:label ?chiLabel
            }"""
            ):
        children.append(str(row.chiLabelString))
    return children

def NIFParents(region, file):
    g = rdflib.Graph()
    g.load(file)
    
    parents = []
    for row in g.query(
            """
            SELECT (str(?parLabel) as ?parLabelString) WHERE {
            ?region rdfs:label ?s
            FILTER(str(?s)="Hypothalamus").
            ?restriction owl:onProperty ro:has_proper_part;
            owl:someValuesFrom ?region.
            ?parents rdfs:subClassOf ?restriction. 
            ?parents rdfs:label ?parLabel
            }"""
            ):
        parents.append(str(row.parLabelString))
    return parents

print NIFChildren('Frontal lobe', '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl' )
print NIFParents('Frontal lobe', '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl' )