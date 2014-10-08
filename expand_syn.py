"""
takes string of keyword and returns list of strings of synonyms of the keyword
"""

import nibabel
import xml.etree.ElementTree as ET
import numpy
import os.path
import urllib2
from __builtin__ import True

def getSynonyms(keyword):
	keyword_no_white = ''
	for c in keyword:
		if c == ' ':
			keyword_no_white += '%20'
		else:
			keyword_no_white += c
	hdr = {'Accept': 'ext/html,application/xhtml+xml,application/xml,*/*'}
	target_url = 'http://nif-services.neuinfo.org/servicesv1/v1/literature/search?q=' + keyword_no_white
	req = urllib2.Request(target_url,headers=hdr)
	file = urllib2.urlopen(req)
	tree = ET.parse(file)
	root = tree.getroot()
	syn_list_loc = root.findall('query/clauses/clauses/expansion/expansion')
	syn_list = []
	for syn in syn_list_loc:
		syn_list.append(syn.text)
	return syn_list
	
print getSynonyms('cerebral cortex')
