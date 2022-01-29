# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# Note:
# We have simploified the inhibitory system with only 1 inhibitory cell (instead of 2). 
# Accordingly, the methods "make_triangle", "ring2ring_connectE",
# "ring2ring_connectI" and "cell2ring_connect" have changed.
# The modifications are located by the keyword "PATCH".

# Note:
# All connections that have a "new" in their names refer to the current trial,
# where no additional cell is reqired to implement the inhibitory structure.


# ******* #
# IMPORTS #
# ******* #

import os
import csv

import numpy as np
from RNN_simulator import *


# ********** #
# Class Cell #
# ********** #

class Cell():
	"""
	Implements a cell given by its activation function and threshold.
	The name of the synfire ring whose cell belongs to is an attribute.
	"""

	def __init__(self, threshold=1.0, activation_function="theta", ring_name=""):
		"""Constructor"""

		self.threshold = threshold
		self.activation_function = activation_function
		self.ring_name = ring_name


# ********** #
# Class Ring #
# ********** #

class Ring(Cell):
	"""
	Implements a synfire ring given by its width, length and layer-to-layer synaptic weights.
	The cells composing the synfire ring are given by their activation functions and thresholds.
	"""

	def __init__(self, width=2, length=5, weight=1.0, 
				 threshold=1.0, activation_function="theta", 
				 name=""):
		"""Constructor"""

		Cell.__init__(self, threshold, activation_function)

		self.width = width
		self.length = length
		self.weight = weight
		self.name = name
		self.nodes = []
		self.edges = []

		for i in range(length):
			for j in range(width):
				self.nodes.append(Cell(self.threshold, self.activation_function, self.name))
		
		for k in range(1, length + 1):
			for i in range((k - 1) * width, k * width):
				for j in range(k * width, (k + 1) * width):
					j = j % (width * length)
					self.edges.append(((self.nodes[i],self.nodes[j]), weight))
	

	def make_triangle_original(self, excitatory=1.0, inhibitory=-10.0):
		"""
		Adds a triangular structure to a synfire ring.
		The triangular structure consists of 2 additional cells C1 and C2.
		All cells of the ring are connected to C1 with excitatory weights.
		The cells from the activation layer of the ring are connected to C2
		with excitatory weights. C1 is connected to C2 with an inhibitory weight.
		This is the original "make_triangle" function. In order to make it work, 
		rename it as "make_triangle" and comment the next one.
		(Comment the 2 lines "new triangular structure" and uncomment the 
		"old triangular structure" to come back to the original situation.)
		"""

		C1 = Cell(self.threshold, self.activation_function, self.name)
		C2 = Cell(self.threshold, self.activation_function, self.name)

		for C in self.nodes:
			self.edges.append( ((C, C1), excitatory) )
			#self.edges.append( ((C, C2), excitatory) )	# old triangular structure
		
		for C in self.nodes[0:self.width]:				# new triangular structure
			self.edges.append( ((C, C2), excitatory) )	# new triangular structure
		
		self.edges.append( ((C1, C2), inhibitory) )
		self.nodes.append(C1)
		self.nodes.append(C2)


	def make_triangle(self):
		"""
		Adds a new triangular structure to a synfire ring - which is not triangular anymore.
		The triangular structure consists of 1 additional cell C1 only.
		The various ring-to-ring connectivity patterns (defined in the Network class) 
		will determine various synaptic patterns from and to this additional cell C1.
		"""

		C1 = Cell(self.threshold, self.activation_function, self.name)

		self.nodes.append(C1)


	def add_satellite(self, inh_layer=2, weight=-10.0):
		"""
		Adds a satellite synfire ring Rbis which serves as an inhibitory system.
		The satellite ring has the same width as the ring but bas a lenght of 2 less.
		The inhibitory layer of the original ring is connected to that 
		of the satellite ring with inhibitory weights. 
		"""

		Rbis = Ring(width=self.width, length=self.length - 2, name=self.name + "_sat")

		for c in Rbis.nodes:
			self.nodes.append(c)
		for e in Rbis.edges:
			self.edges.append(e)

		for k in range(Rbis.width):
			self.edges.append( ( ( self.nodes[((inh_layer - 1) * self.width) + k] , Rbis.nodes[((inh_layer - 1) * Rbis.width) + k] ), weight ) )


	def satellite(self):
		"""
		Retreives the satellite ring (nodes and edges) of a synfire ring.
		"""

		nodes, edges = [], []
		
		if self.nodes == self.width * self.length:
			return False
		else:
			for n in self.nodes[self.width * self.length : ]: # satellite's nodes
				nodes.append(n)
			for e in self.edges[self.width**2 * self.length : self.width**2 * self.length + self.width**2 * (self.length - 2) ]: # satellite's edges
				edges.append(e)
			return (nodes, edges)


# ************* #
# Class Network #
# ************* #

class Network():
	"""
	Implements a neural network composed of synfire rings.
	"""

	def __init__(self):
		"""Constrructor"""

		self.nodes = []
		self.edges = []


	def add_cell(self, C):
		"""
		Add a cell to the network.
		"""

		self.nodes.append(C)


	def add_ring(self, R):
		"""
		Add a synfire ring to the network.
		"""

		self.nodes += R.nodes
		self.edges += R.edges
	

	def ring2ring_connectE(self, R1, R2, weight=1.0, layer=1):
		"""
		Creates ring-to-ring excitatory connections.
		Connects all layers of R1 to the n-th layer of R2 with excitatory weights.
		In addition, connects all layers of R1 to the cell C1 (inhibitory system) of R2 
		with excitatory weights also, but of smaller intensities.
		"""

		for l in range(R1.length):

			k = 0

			for N in R1.nodes[l * R1.width : l * R1.width + R1.width]:

				self.edges.append( ((N, R2.nodes[((layer - 1) * R2.width) + k]), weight) )
				k += 1
				# *** PATCH ***
				# connections to the new inhibitory cell C1
				# (comment to come back to the original situation)
				self.edges.append( ((N, R2.nodes[-1]), weight/float(R1.width)) )


	def ring2ring_connectE2(self, R1, R2, weight=1.0, layer=1):
		"""
		Creates ring-to-ring excitatory connections.
		Connects the cell C1 (inhibitory system) of R1 to the n-th layer of R2.
		"""

		C = R1.nodes[-1] # last cell of R1

		for N in R2.nodes[(layer - 1) * R2.width : (layer - 1) * R2.width + R2.width]:

			self.edges.append( ((C, N), weight) )


	def ring2ring_connectE_new(self, R1, R2, weight=1.0, layer=1):
		"""
		Creates ring-to-ring excitatory connections.
		Connect all layers of R1 to the n-th layer of R2
		as well as to the n-th layer of the satellite of R2.
		"""

		for l in range(R1.length):

			k = 0
			
			for k in range(R1.width):

				self.edges.append( ( ( R1.nodes[(l * R1.width) + k] , R2.nodes[((layer - 1) * R2.width) + k] ), weight ) )
				self.edges.append( ( ( R1.nodes[(l * R1.width) + k] , R2.satellite()[0][((layer - 1) * R2.width) + k] ), weight ) )
				k += 1


	def ring2ring_connectI(self, R1, R2, weight=-10.0):
		"""
		Creates ring-to-ring inhibitory connections.
		Connect the cell C1 of R1 (inhibitory system) to all layers of R2
		as well as to the cell C1 of R2.
		"""

		C = R1.nodes[-1] # cell C1 of R1
		
		for N in R2.nodes:

			self.edges.append( ((C, N), weight) )
			# *** PATCH *** 
			# note that his method doesn't change with the new inhibition system


	def ring2ring_connectI_new(self, R1, R2, weight=-10.0, layer=2):
		"""
		Creates ring-to-ring inhibitory connections.
		Connect the inhibition layer of R1's satellite ring to all layers of R2.
		"""

		for l in range(R2.length):

			k = 0
			
			for k in range(R1.width):
			
				self.edges.append( ( ( R1.satellite()[0][(layer - 1) * R1.width + k] , R2.nodes[(l * R2.width) + k] ), weight ) )
				k += 1

	def cell2ring_connect_no_inhibitory_system(self, C, R, weight=1.0):
		"""
		Creates cell-to-ring excitatory connections.
		Connects cell C to the first layer of ring R.
		We assume that the ring is not associated with any inhibitory system.
		"""

		for n in R.nodes[0:R.width]:

			self.edges.append( ((C, n), weight) )

	def cell2ring_connect(self, C, R, weight=1.0):
		"""
		Creates cell-to-ring excitatory connections.
		Connects cell C to the first layer of ring R. 
		"""

		for n in R.nodes[0:R.width]:

			self.edges.append( ((C, n), weight) )
		# *** PATCH ***
		# add a connection to C1: new inhibitory system
		# comment this to come back to the original situation
		self.edges.append( ((C, R.nodes[-1]), weight) )


	def cell2ring_connect_new(self, C, R, weight=1.0, layer=1):
		"""
		Creates cell-to-ring excitatory connections.
		Connects cell C to the first layer of ring R as well as 
		to the first layer of its satellite ring. 
		"""

		for k in range(R.width):
			self.edges.append( ( (C, R.nodes[(layer - 1) * R.width + k]), weight ) )
			self.edges.append( ( (C, R.satellite()[0][(layer - 1) * R.width + k]), weight ) )


	def ring2cell_connect(self, C, R, weight=1.0):
		"""
		Creates ring-to-cell excitatory connections.
		Connects all cells of ring R to cell C. 
		"""

		for n in R.nodes:

			self.edges.append( ((n, C), weight) )


	def cell2cell_connect(self, C1, C2, weight=1.0):
		"""
		Creates cell-to-cell excitatory connections.
		Connects cell C1 to cell C2. 
		"""

		self.edges.append( ((C1, C2), weight) )


	def remove_ring(self, R):
		"""
		Removes a synfire ring.
		"""

		for n in R.nodes:

			self.edges.remove(n)

		for e in R.edges:

			if e[0][0] in R.nodes or e[0][1] in R.nodes:

				self.edges.remove(e)


	def matrix(self):
		"""
		Computes the adjacency matrix of the network.
		"""

		M = np.zeros([len(self.nodes), len(self.nodes)])
		
		for e in self.edges:

			M[self.nodes.index(e[0][0])][self.nodes.index(e[0][1])] = e[1]

		return M


	def simulate(self, input_dico, nb_epochs=300):
		"""
		Simulates the network during nb_epochs time steps.
		Returns the raster array of the simulated network.
		"""

		# input dico of the form: {time_step: input_vector, ...}
		dim_input = input_dico[0].shape[0]
		# dim_input = input_dico.values()[0].shape[0]
		M = self.matrix()
		A = M[dim_input:, dim_input:]
		B1 = M[0:dim_input, dim_input:]
		B2 = np.zeros([A.shape[0], dim_input])
		C = np.zeros([A.shape[0], 1])
		X = np.zeros([A.shape[0], 1])
		U = input_dico

		S = simulation(A, B1, B2, C, X, U, nb_epochs)
		
		return S

	
	def write_csv(self, filepath="data"):
		"""
		Creates two csv files for the nodes and edges of the network;
		These csv files are designed for plotting with R (igraph).
		"""
		
		with open(os.path.join(filepath, 'nodes.csv'), 'w') as f:

			row_names = ["id", "ring_name"]
			writer = csv.DictWriter(f, fieldnames = row_names)
			writer.writeheader()
			
			for n in self.nodes:

				writer.writerow({"id": id(n), "ring_name": n.ring_name})
		
		with open(os.path.join(filepath, 'edges.csv'), 'w') as f:

			row_names = ["from", "to", "weight"]
			writer = csv.DictWriter(f, fieldnames = row_names)
			writer.writeheader()
			
			for e in self.edges:

				writer.writerow({"from": id(e[0][0]), "to": id(e[0][1]), "weight": e[1]})
			

# ******* #
# Example #
# ******* #

# R1 = Ring()
# print(R1.nodes)
# for e in R1.edges:
# 	print(e[0][0], e[0][1], e[1])
