# -*- coding: utf-8 -*-
# @Author: dmytro
# @Date:   2016-12-12 15:46:11
# @Last Modified by:   dmytro
# @Last Modified time: 2016-12-12 22:29:28
import random

x = [0, 1, 2, 3, 4, 5]
# theta = [0.1, 0.4, 0.55, 0.7, 0.8, 1.0]
theta = [0.1, 0.3, 0.15, 0.15, 0.1, 0.2]


def F(x, ind):
	if ind < 0:
		return 0
	elif ind > len(x):
		return 1
	else:
		return sum(theta[:ind + 1])


def inv_bin_search(u, x, F, a, b):
	if a > b:
		return -1

	m = (a + b) / 2

	if u < F(x, m):
		if u >= F(x, m - 1):
			return x[m]
		return inv_bin_search(u, x, F, a, m - 1)
	else:
		if u == F(x, m):
			return x[m]

		if u < F(x, m + 1):
			return x[m + 1]
		return inv_bin_search(u, x, F, m + 1, b)


def divider(x, sample, err, n=6):
	if err > 0 or (n == 0 and x > 1.0):
		return 1
	sample.append(x)
	for i in xrange(n):
		err = divider((i +  x) / 2.0, sample, err, n - 1)
	return err

sample = []
print divider(43, sample, 0)
print sample
