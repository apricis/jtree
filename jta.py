# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-14 14:05:22
# @Last Modified by:   dmytro
# @Last Modified time: 2016-12-14 14:34:08

import csv
from pgmpy.models import *


def readAdjList(file):
	edges = []
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		vertices = next(reader)
		for row in reader:
			v = row[0]
			for w in row[1:]:
				edges.append((v, w))
	return vertices, edges


V, E = readAdjList("./extstudent_adjlist.csv")

G = MarkovModel()
G.add_nodes_from(V)
G.add_edges_from(E)
print len(G)