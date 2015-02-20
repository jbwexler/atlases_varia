from nose.tools import eq_, ok_, istest
import nose
from parent_children_graph import ontToGraph, toAtlas
# from store_nif_graph import *




class test_parent_children_graph_allen:
    ont_file = 'allen_brain_atlas_human_ontology_fixed.txt'
    graph = ontToGraph(ont_file)
    def test_onToGraph_frontal_lobe_parents(self):
        frontalLobeID = [n for n,d in graph.nodes_iter(data=True) if d['name'] == 'frontal lobe'][0]
        assert graph.predecessors(frontalLobeID) == [4008]
    def test_onToGraph1_thalamus_children(self):
        thalamusID = [n for n,d in graph.nodes_iter(data=True) if d['name'] == 'thalamus'][0]
        assert graph.successors(thalamusID) == [4504, 4393]
    def test_toAtlas_amygdala(self):
        assert toAtlas('amygdala', graph, 'HarvardOxford-Cortical.xml') == 'none'
    def test_toAtlas_error(self):
        try:
            print toAtlas('fail me!', graph, 'HarvardOxford-Cortical.xml')
        except IndexError:
            assert True
    def test_toAtlas_angular_gyrus(self):
        assert toAtlas('angular gyrus', graph, 'HarvardOxford-Cortical.xml') == ['angular gyrus']
    def test_toAtlas_angular_gyrus(self):
        assert toAtlas('angular gyrus', graph, 'HarvardOxford-Cortical.xml') == ['angular gyrus']
        
    
        
    