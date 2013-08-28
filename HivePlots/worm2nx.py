""" 
worm2nx.py
Simple script for turning connectome tables into NetworkX graphs.

Note that the tables were extracted manually from the connectivity spreadsheet
of the c. elegans and should accompany this script.

Author: Pedro Tabacof (tabacof at gmail dot com)
        Stephen Larson (stephen@openworm.org)
License: Public Domain
"""

# -*- coding: utf-8 -*- 

import csv

import urllib2

import networkx as nx

worm = nx.DiGraph()

# Neuron table
csvfile = urllib2.urlopen('https://raw.github.com/openworm/data-viz/master/HivePlots/neurons.csv')

reader = csv.reader(csvfile, delimiter=';', quotechar='|')
for row in reader:
    neurontype = ""
    # Detects neuron function
    if "sensory" in row[1].lower():
        neurontype += "sensory"
    if "motor" in row[1].lower():
        neurontype += "motor"    
    if "interneuron" in row[1].lower():
        neurontype += "interneuron"
    if len(neurontype) == 0:
        neurontype = "unknown"
        
    if len(row[0]) > 0: # Only saves valid neuron names
        worm.add_node(row[0], ntype = neurontype)

# Connectome table
csvfile = urllib2.urlopen('https://raw.github.com/openworm/data-viz/master/HivePlots/connectome.csv')

reader = csv.reader(csvfile, delimiter=';', quotechar='|')
for row in reader:
    worm.add_edge(row[0], row[1], weight = row[3])
    worm[row[0]][row[1]]['synapse'] = row[2]
    worm[row[0]][row[1]]['neurotransmitter'] = row[4]

print "******DEGREES OF TOP FOUR INTERNEURONS*******"
print "Degree of AVAL: " + str(worm.degree('AVAL'))
print "Degree of AVAR: " + str(worm.degree('AVAR'))
print "Degree of AVBL: " + str(worm.degree('AVBL'))
print "Degree of AVBR: " + str(worm.degree('AVBR'))

print "******DEGREES OF NEXT FOUR INTERNEURONS*******"
print "Degree of PVCR: " + str(worm.degree('PVCR'))
print "Degree of PVCL: " + str(worm.degree('PVCL'))
print "Degree of AVDR: " + str(worm.degree('AVDR'))
print "Degree of AVER: " + str(worm.degree('AVER'))

print "******DEGREE OF TOP SENSORY NEURON*******"
print "Degree of ADEL: " + str(worm.degree('ADEL'))
print "******DEGREE OF TOP MOTOR NEURON*******"
print "Degree of RIMR: " + str(worm.degree('RIMR'))

def GJ_degree(node):
    count = 0
    for item in worm.in_edges_iter(node,data=True):
        if 'GapJunction' in item[2]['synapse']:
            count = count + 1
    for item in worm.out_edges_iter(node,data=True):
        if 'GapJunction' in item[2]['synapse']:
            count = count + 1
    return count

def Syn_degree(node):
    count = 0
    for item in worm.in_edges_iter(node,data=True):
        if 'Send' in item[2]['synapse']:
            count = count + 1
    for item in worm.out_edges_iter(node,data=True):
        if 'Send' in item[2]['synapse']:
            count = count + 1
    return count

ids = {}
ids_GJ = {}
ids_Syn = {}
for item in worm.nodes_iter(data=True):
    if item[0] in ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PVCR', 'PVCL', 'AVDR', 'AVER']:
        if 'interneuron' in item[1]['ntype']:
            ids[item[0]] = worm.degree(item[0])
            ids_GJ[item[0]] = GJ_degree(item[0])
            ids_Syn[item[0]] = Syn_degree(item[0])

import operator

ids = sorted(ids.iteritems(), key=operator.itemgetter(1))
ids_GJ = sorted(ids_GJ.iteritems(), key=operator.itemgetter(1))
ids_Syn = sorted(ids_Syn.iteritems(), key=operator.itemgetter(1))

from pylab import *

pos = arange(len(ids))+1    # the bar centers on the y axis

#fig = figure(figsize=(20,20))
fig = figure(figsize=(10,10))
ax = fig.add_subplot(111)

p1 = bar(pos,[x[1] for x in ids], align='center', color='r')

p2 = bar(pos,[x[1] for x in ids_Syn], align='center')

p3 = bar(pos,[x[1] for x in ids_GJ], align='center', color='y')

xlabel('Interneurons')
ylabel('Degree')
xticks( pos, [x[0] for x in ids])
title('Interneurons by node degree')
legend( (p1[0], p2[0], p3[0]), ('All edges', 'Synapses only', 'Gap junctions only'), loc=2)
setp(ax.get_xticklabels(), fontsize=12, rotation='vertical')

show()