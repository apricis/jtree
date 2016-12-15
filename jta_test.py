# -*- coding: utf-8 -*-
# @Author: Dmytro Kalpakchi
# @Date:   2016-12-15 22:38:36
# @Last Modified by:   Dmytro Kalpakchi
# @Last Modified time: 2016-12-15 23:38:41

import matplotlib.pyplot as plt
import networkx as nx
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from jta import readAdjList, jta, get_different

if __name__ == '__main__':
	V, E, CPD = readAdjList("./simple_adjlist_dgm.csv")

	print "Results of the implemented JTA"

	DGM = BayesianModel()
	DGM.add_nodes_from(V)
	DGM.add_edges_from(E)
	DGM.add_cpds(*CPD)

	UGM = DGM.to_markov_model()
	jtree = UGM.to_junction_tree()

	evidence = {}

	marginal = jta(UGM, jtree, evidence.items())
	for m in marginal:
		print m

	print "\n=======================================\n"

	print "Results of the Variable Elimination from pgmpy"

	inference = VariableElimination(DGM)
	for v in get_different(DGM.nodes(), evidence):
		print inference.query(variables=[v], evidence=evidence)[v]

	# visualization part
	# nx.draw(jtree, with_labels=True, node_color="white", node_shape='s', node_size=8000)
	# plt.draw()
	# plt.show()