"""
NIFChildren takes two strings: the name of a brain region and the location of the owl ontology file. 
it returns a list of strings of the children of this brain region according to the ontology.
NIFParents does the same, but finds the parents.
NIFfindNodes has two modes: 
-children mode (default): if startNode or synonyms appear in target, it will return list of matches. otherwise, it will search recursively
for children and test if they are in target. will return list of matches within the first generation that has matches. if no matches
are found, it will return an empty list
-parent mode (if 4th input == 'parents'): same as children mode but performs search in opposite direction
"""

import rdflib
from expand_syn import*

atlas_file = 'HarvardOxford-Cortical.xml'
atlas_dir = '/Applications/fmri_progs/fsl/data/atlases/'
tree = ET.parse(os.path.join(atlas_dir, atlas_file))
root = tree.getroot()
targets = [x.text.lower() for x in root[1]]

owl_file = '/Users/jbwexler/poldrack_lab/cs/other/NIF-GrossAnatomy_reasoner.owl'
g = rdflib.Graph()
g.load(owl_file)


def NIFchildren(graph, startNode):
    children = []
    for row in graph.query(
            """
            SELECT (str(?chiLabel) as ?chiLabelString) WHERE {
            ?region rdfs:label ?s
            FILTER(lcase(str(?s))="%s").
            ?restriction owl:onProperty ro:proper_part_of;
            owl:someValuesFrom ?region.
            ?children rdfs:subClassOf ?restriction. 
            ?children rdfs:label ?chiLabel
            }"""%startNode
            ):
        children.append(str(row.chiLabelString))
    return children

def NIFparents(graph, startNode): 
    parents = []
    for row in graph.query(
            """
            SELECT (str(?parLabel) as ?parLabelString) WHERE {
            ?region rdfs:label ?s
            FILTER(lcase(str(?s))="%s").
            ?restriction owl:onProperty ro:has_proper_part;
            owl:someValuesFrom ?region.
            ?parents rdfs:subClassOf ?restriction. 
            ?parents rdfs:label ?parLabel
            }"""%startNode
            ):
        parents.append(str(row.parLabelString))
    return parents


def NIFfindNodes(graph, startNode, targets, direction = 'children'):
    synAndTargets = [e for e in getSynonyms(startNode) if e in targets]
    if len(synAndTargets) > 0:
        return synAndTargets
    else:
        matchingRelatives = []
        if direction == 'parents':
            for child in NIFparents(graph, startNode):
                print child, NIFfindNodes(graph, child.lower(), targets, direction)
                matchingRelatives += NIFfindNodes(graph, child.lower(), targets, direction)
        else:
            for child in NIFchildren(graph, startNode):
                print child, NIFfindNodes(graph, child.lower(), targets, direction)
                matchingRelatives += NIFfindNodes(graph, child.lower(), targets, direction)
        return matchingRelatives
    
# print NIFchildren(g,"frontal lobe")
# print NIFparents(g, "frontal lobe")
print NIFfindNodes(g, "basal ganglia", targets)
