#!/usr/bin/env python

from __future__ import division
import pandas
import math
import Tree 
import graphviz as gv
import plotGraph
import globalFunc
import collections 

def display(dtree,visualization):
	if len(dtree.link) != 0:
		#print dtree.data
		visualization.node(dtree.timestamp,label = str(dtree.data))
		for (l,ln) in zip(dtree.link,dtree.link_name):
			visualization.node(l.timestamp,label = str(l.data))
			#print l.data
			visualization.edge(dtree.timestamp,l.timestamp,label = str(ln))
			display(l,visualization)

def preprocess(data):
	for column in data.columns:
		if(len(data[column].unique()) <= 13):
			data[column] = data[column].astype(object)
	equiv = {0:'0',1:'1'}
	data['target'] = data['Survived'].map(equiv)
	return data.drop(['Survived'], axis=1)

# dataset = 'german'
data = pandas.read_csv('titanic_train.csv')
data = preprocess(data)
print data.info()

test = pandas.read_csv('titanic_test.csv')
test = preprocess(test)

# training_frac = [0.1,0.2,0.3,0.4,0.5,0.6]
training_frac = [1]
# algos = ['ID3','C4.5','CBDSDT']
algos = ['C4.5']
algo_accuracy = collections.OrderedDict()
algo_ms_cost = {}
algo_cc_benefit = {}

# test = data.sample(frac=0.4)
# data = data.drop(test.index)

print 'algorithm\tfraction\taccuracy\tmissclassification cost\t\tcorrect classification benefit'

for frac_val in training_frac:
	# train = data.sample(frac=frac_val)
	train = data
	for algo in algos:
		dtree = Tree.Tree(0)
		dtree = dtree.create_tree(train,algo,dtree.depth)
		accuracy,ms_cost,cc_benefit = globalFunc.calculateAccuracy(test,dtree,algo)
		print '%9s\t%8s\t%8s\t%23s\t\t%30s'%(algo,(frac_val * 100),accuracy,ms_cost,cc_benefit)
		visualization = gv.Digraph(format='png')
		display(dtree,visualization)
		# visualization.render('dtree/'+algo+'-'+str(frac_val))
		visualization.render('dtree/' + algo +'-' + str(frac_val) + '-' + str(Tree.max_depth) + '-' + str(accuracy))

		if algo not in algo_accuracy:
			algo_accuracy[algo] = collections.OrderedDict()
			algo_ms_cost[algo] = collections.OrderedDict()
			algo_cc_benefit[algo] = collections.OrderedDict()

		algo_accuracy[algo][frac_val] = accuracy
		algo_ms_cost[algo][frac_val] = ms_cost * frac_val
		algo_cc_benefit[algo][frac_val] = cc_benefit * frac_val
	print '\n*************************************************************************************************************************************\n'

# plotGraph.accuracy(algo_accuracy)
# plotGraph.ms_cost(algo_ms_cost)
# plotGraph.cc_benefit(algo_cc_benefit)
