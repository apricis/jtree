# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-14 14:05:22
# @Last Modified by:   Dmytro Kalpakchi
# @Last Modified time: 2016-12-15 22:27:32

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


def get_different(scope1, scope2):
	return list(set(scope1) - set(scope2))


def collect(v, parent):
	pass


def distribute(v):
	pass


def jta(ugm, jtree, evidence):
	factors = dict([(",".join(f.scope()), f.copy()) for f in jtree.get_factors()])
	e = map(itemgetter(0), evidence) # evidence scope
	for f in factors.values():
		separator = get_separator(e, f.scope())
		if separator:
			f.reduce([x for x in evidence if x[0] in separator], inplace=True)

	messages = {}

	# collect phase
	collected = []
	for v in nx.dfs_postorder_nodes(jtree):
		for n in jtree.neighbors(v):
			if n not in collected:
				messages[(v, n)] = factors[",".join(v)]
				for edge, m in messages.iteritems():
					if edge[1] == v and edge[0] != n:
						messages[(v, n)].product(m)
				diff = get_different(get_different(v, e), get_different(n, e))
				messages[(v, n)] = messages[(v, n)].marginalize(diff, inplace=False)
		collected.append(v)
	
	# distribute phase
	distributed = []
	for v in nx.dfs_preorder_nodes(jtree):
		for n in jtree.neighbors(v):
			if n not in distributed:
				messages[(v, n)] = factors[",".join(v)]
				for edge, m in messages.iteritems():
					if edge[1] == v and edge[0] != n:
						messages[(v, n)] *= m
				diff = get_different(get_different(v, e), get_different(n, e))
				messages[(v, n)] = messages[(v, n)].marginalize(diff, inplace=False)
		distributed.append(v)

	beliefs = {}
	for v in jtree.nodes():
		beliefs[v] = factors[",".join(v)]
		for edge, m in messages.iteritems():
			if edge[1] == v:
				beliefs[v] *= m

	for i, m in messages.iteritems():
		print i, m

	print "================================"
	
	marg = {}
	for m in get_different(ugm.nodes(), e):
		for v in jtree.nodes():
			if m in v:
				diff = get_different(get_different(v, e), m)
				marg[m] = beliefs[v].marginalize(diff, inplace=False)
				break
	return marg.itervalues()


V, E, CPD = readAdjList("./student_adjlist_dgm.csv")

DGM = BayesianModel()
DGM.add_nodes_from(V)
DGM.add_edges_from(E)
DGM.add_cpds(*CPD)

UGM = DGM.to_markov_model()
jtree = UGM.to_junction_tree()

marginal = jta(UGM, jtree, [('I', 1)])
for m in marginal:
	print m

# nx.draw(jtree, with_labels=True, node_color="white", node_shape='s', node_size=8000)
# plt.draw()
# plt.show()