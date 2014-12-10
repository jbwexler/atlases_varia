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
	keywordQuery = keyword
	keywordQuery = keywordQuery.replace(' ', '%20')
	keywordQuery = keywordQuery.replace('/', '')
	keywordQuery = keywordQuery.replace('\\', '')
	hdr = {'Accept': 'ext/html,application/xhtml+xml,application/xml,*/*'}
	target_url = 'http://nif-services.neuinfo.org/servicesv1/v1/literature/search?q=' + keywordQuery
	request = urllib2.Request(target_url,headers=hdr)
	synFile = urllib2.urlopen(request)
	tree = ET.parse(synFile)
	root = tree.getroot()
	syn_list_loc = root.findall('query/clauses/clauses/expansion/expansion')
	syn_list = []
	for syn in syn_list_loc:
		syn_list.append(syn.text)
	syn_list.append(keyword)
	return syn_list
	
# print getSynonyms('Fornix (cres)  Stria terminalis / sdfggggggggggggggggggggggg/ ')

