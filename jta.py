# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-14 14:05:22
# @Last Modified by:   Dmytro Kalpakchi
# @Last Modified time: 2016-12-15 23:03:01

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


def jta(ugm, jtree, evidence):
	def collect_distribute(order, messages):
		messaged = []
		for v in order:
			for n in jtree.neighbors(v):
				if n not in messaged:
					messages[(v, n)] = factors[",".join(v)]
					for edge, m in messages.iteritems():
						if edge[1] == v and edge[0] != n:
							messages[(v, n)] *= m
					diff = get_different(get_different(v, e), get_different(n, e))
					messages[(v, n)] = messages[(v, n)].marginalize(diff, inplace=False)
			messaged.append(v)
		return messages

	factors = dict([(",".join(f.scope()), f.copy()) for f in jtree.get_factors()])
	e = map(itemgetter(0), evidence) # evidence scope
	for f in factors.values():
		separator = get_separator(e, f.scope())
		if separator:
			f.reduce([x for x in evidence if x[0] in separator], inplace=True)

	jtree_nodes = jtree.nodes()
	root = jtree_nodes[0]

	# collect phase
	messages = collect_distribute(nx.dfs_postorder_nodes(jtree, source=root), {})
	
	# distribute phase
	messages = collect_distribute(nx.dfs_preorder_nodes(jtree, source=root), messages)

	# get beliefs for each cluster from messages
	beliefs = {}
	for v in jtree_nodes:
		beliefs[v] = factors[",".join(v)]
		for edge, m in messages.iteritems():
			if edge[1] == v:
				beliefs[v] *= m
	
	marg = {}
	for m in get_different(ugm.nodes(), e):
		for v in jtree_nodes:
			if m in v:
				diff = get_different(get_different(v, e), m)
				marg[m] = beliefs[v].marginalize(diff, inplace=False).normalize(inplace=False)
				break
	return marg.itervalues()