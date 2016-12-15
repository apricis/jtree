# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-14 14:05:22
# @Last Modified by:   Dmytro Kalpakchi
# @Last Modified time: 2016-12-15 10:09:04

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import csv
from pgmpy.models import *
from pgmpy.factors import Factor, TabularCPD


def readAdjList(file):
	edges = []
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		vertices = next(reader)
		for row in reader:
			if not row:
				break
			v = row[0]
			for w in row[1:]:
				edges.append((v, w))
		
		# reading CPD if any
		card = {}
		cpds = []
		for row in reader:
			depend = row[0].split("|")
			var = depend[0]
			evidence = depend[1].split(".") if len(depend) > 1 else []
			card[var] = int(row[1])
			cpd = [map(float, x.split("|")) for x in row[2].split("||")]
			cpds.append(TabularCPD(var, card[var], cpd, evidence=evidence, evidence_card=[card[e] for e in evidence]))
	return vertices, edges, cpds


V, E, CPD = readAdjList("./student_adjlist_dgm.csv")

# G = BayesianModel()
# G.add_nodes_from(V)
# G.add_edges_from(E)
# nx.draw(G, with_labels=True, node_color="white")

# G = MarkovModel()
# G.add_nodes_from(V)
# G.add_edges_from(E)
# phi = [Factor(edge, [2, 2], np.random.rand(4)) for edge in G.edges()]
# G.add_factors(*phi)
# jtree = G.to_junction_tree()
# nx.draw(G, with_labels=True, node_color="white")
# plt.draw()
# plt.show()
# nx.draw(jtree, with_labels=True, node_color="white", node_shape='s', node_size=8000)
# plt.draw()
# plt.show()