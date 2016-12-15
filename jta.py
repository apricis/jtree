# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-14 14:05:22
# @Last Modified by:   Dmytro Kalpakchi
# @Last Modified time: 2016-12-15 19:10:14

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import csv
from pgmpy.models import *
from pgmpy.factors.discrete import TabularCPD
from operator import itemgetter


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
			card[var] = np.int(row[1])
			cpd = [map(np.float, x.split("|")) for x in row[2].split("||")]
			cpds.append(TabularCPD(var, card[var], cpd, evidence=evidence, evidence_card=[card[e] for e in evidence]))
	return vertices, edges, cpds


def get_separator(scope1, scope2):
	return list(set(scope1) & set(scope2))


def jta(jtree, evidence):
	factors = jtree.get_factors()
	evidence_scope = map(itemgetter(0), evidence)
	for f in factors:
		separator = get_separator(evidence_scope, f.scope())
		if separator:
			f.reduce([x for x in evidence if x[0] in separator], inplace=True)
	


V, E, CPD = readAdjList("./student_adjlist_dgm.csv")

DGM = BayesianModel()
DGM.add_nodes_from(V)
DGM.add_edges_from(E)
DGM.add_cpds(*CPD)

UGM = DGM.to_markov_model()
jtree = UGM.to_junction_tree()

jta(jtree, [('I', 1)])

# nx.draw(jtree, with_labels=True, node_color="white", node_shape='s', node_size=8000)
# plt.draw()
# plt.show()