# -*- encoding: utf-8 -*-
#
# Social Network Analysis anonymization
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# pip install networkx
#

# Import libraries
import networkx as nx

# Load the file
print ""
print "Loading the data..."
graph01 = nx.read_gexf("filename.gexf")

# Convert names to hash
mapping = {}

# Create mapping of nodes and relabel labels
for i in graph01.nodes_iter(data=True):
	mapping[i[0]] = hash(i[0])
	graph01.node[i[0]]["label"] = hash(i[0])

# Relabel nodes
graph02 = nx.relabel_nodes(graph01,mapping)

# Save the new anonymized graph		
print ""
print "Saving the anonymized data..."
nx.write_gexf(graph02, "filename_anonymized.gexf")