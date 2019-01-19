#!/usr/bin/env python

import pandas
from datetime import datetime
import dtreeAlgo

class Tree(object):
	max_depth = 8
	def __init__(self, depth):
		self.data = None
		self.link = []
		self.link_name = []
		self.split_point = None
		self.timestamp = str(datetime.now()).split('.')[1]
		self.depth = depth

	def create_tree(self,data,algo, depth):
		root = Tree(depth + 1) 
		
		if root.depth >= Tree.max_depth:
			root.data = data['target'].value_counts().idxmax()
			return root

		if len(data['target'].unique()) == 1:
			root.data = data['target'].unique()[0]
			return root

		leaf = True
		for column in data.columns:
			if (column != 'target' and len(data[column].unique()) > 1):
				leaf = False

		if leaf == True:
			root.data = data['target'].value_counts().idxmax()
			return root

		splitting_attribute = None
		split_point = None
		if algo == 'ID3':
			splitting_attribute,split_point = dtreeAlgo.ID3(data)
		elif algo == 'C4.5':
			splitting_attribute,split_point = dtreeAlgo.C45(data)
		elif algo == 'CBDSDT':
			splitting_attribute,split_point = dtreeAlgo.CBDSDT(data)

		#print splitting_attribute,split_point

		
		if splitting_attribute == None:
			root.data = data['target'].value_counts().idxmax()
			return root
		## assigning the best splitting attribute to current node
		root.data = splitting_attribute
		if split_point == None:
			values = data[splitting_attribute].unique()

			## partitioning the data on all possible values of the splitting attribute and recursive induction of the decision tree
			for value in values:
				root.link_name.append(value)
				root.link.append(self.create_tree(data[data[splitting_attribute] == value].drop([splitting_attribute],1),algo,root.depth))

		else:
			root.split_point = split_point
			root.link_name.append(' A <=' + str(split_point))
			root.link.append(self.create_tree(data[data[splitting_attribute] <= split_point].drop([splitting_attribute],1),algo,root.depth))
			root.link_name.append('A > '+ str(split_point))
			root.link.append(self.create_tree(data[data[splitting_attribute] >  split_point].drop([splitting_attribute],1),algo,root.depth))
		return root
