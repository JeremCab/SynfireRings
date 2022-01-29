# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# **************** #
# GLOBAL NOTATIONS #
# **************** #

# Every (vertical) vector is of the form:
# np.array([[x1],
#			[X2],
#			[X3],
#			...
#				])
# A: weight matrix		internal connections
#						A[i,j] = w iff x_i --w--> x_j

# B1: weight matrix		input connections (from input to internal cells)
# 						B1[i,j] = w iff u_i --w--> x_j

# B2: weight matrix		interactive connections (from internal to input cells)
#						B2[i,j] = w iff x_i--w--> u_j

# C: weight vector		bias connections (from env. to internal cells)
#						C[i] = w iff env.--w--> x_i

# X: state vector		initial activation values of internal cells
#						X[i] = a iff x_i(0) = a

# U: input dictionary	keys: time steps; values: input vectors
#						U[t] = input vector at time step t
#						if time step not specified, then input vector = [0,...,0]



# ******************* #
# DYNAMICAL EQUATIONS #
# ******************* #

# u'_j(t) = \sigma ( u_j(t) + \sum b2_jk.x_k(t) )
# x_i(t+1) = \sigma ( \sum a_ij.x_j(t) + \sum b1_ij.u'_j(t) + c_i )


# ******* #
# IMPORTS #
# ******* #

import numpy as np


# ******************** #
# ACTIVATION FUNCTIONS #
# ******************** #

def theta(x, threshold=1):
	"""Hard-threshold activation function."""
	if x < threshold:
		return 0
	else:
		return 1

theta = np.vectorize(theta)	# in order to apply theta componentwise

def sigma(x):
	"""Linear-sigmoidal activation function."""
	if x < 0:
		return 0
	elif (x >= 0 and x <= 1):
		return x
	else:
		return 1

sigma = np.vectorize(sigma)	# in order to sigma sigma componentwise


# ************ #
# STDP (basic) #
# ************ #

def push(value, n):
	"""Increses a value by 1/(2^(n+1)) and the counter by 1."""
	new_value = value + 1.0/(2**(n+1))
	return (new_value, n+1)
# NOTE: we push according to the "next" level n+1, i.e., 1/(2^(n+1))


def pop(value, n):
	"""Decreses a value by 1/(2^n) until 0 and the counter by 1."""
	if value - 1.0/(2**n) > 0:
		new_value = value - 1.0/(2**n)
	else:
		new_value = 0
	return (new_value, max(0,n-1))
# NOTE: we pop according to the "current" level n, i.e., 1/(2^n)


def STDP(pre_t0, post_t0, pre_t1, post_t1, synapse, counter):
	"""Implements the following basic STDP rule:
			pre		post
		t0	1		0 
		t1	0		1
		=> synaptic weight increased by 1/(2^n)
			pre		post
		t0	0		1 
		t1	1		0
		=> synaptic weight decreased by 1/(2^n) if > 0
		Tis STDP could be generalized to other patterns 
		where the pre-synaptic neuron remains active at t1 (case1)
		or the post-synaptic remains active at t1 (case2)
	"""
	if pre_t0 == 1 and post_t0 == 0 and pre_t1 == 0 and post_t1 == 1:
		(new_synapse, counter) = push(synapse, counter)
	elif pre_t0 == 0 and post_t0 == 1 and pre_t1 == 1 and post_t1 == 0:
		(new_synapse, counter) = pop(synapse, counter)
	else:
		(new_synapse, counter) = (synapse, counter)
	return (new_synapse, counter)


# ********* #
# SIMULATOR #
# ********* #

def simulation(A, B1, B2, C, X, U, nb_epochs, STDP_rule = "off"):
	"""
	Implements the simulation of a neural network characrterized by 
	the weight matrices A, B1, B2, C, X and U, during nb_epochs, 
	and using a possible STDP rule.
	If the STDP in not off, it has to be given as a list of tuples of the form 
	[(i1, j1), (i2, j2),...,(ik, jk)]
	Each tuple represents a synaptic connection for which STDP is applied.
	The cells' numbering begins at 1, not at 0 (example: [(1,2), (1.3), ...]).
"""
	counter = 0									# counter for the STDP
	dim = U[0].shape[0]+ X.shape[0]							# state space dimension
	#dim = U[U.keys()[0]].shape[0]+ X.shape[0]				# state space dimension
	history = np.zeros([dim, 1])							# initialize history (dummy first state)

	for i in range(nb_epochs):

		# input signal at time step i
		u = U[i] if i in U.keys() else np.zeros([B1.shape[0], 1])
		# input at time step i after the interactive signal is received
		u = theta(np.dot(B2.T, X) + u)
		# append (input u, state X) to history
		history = np.hstack([history, np.vstack([u, X])])
		# compute new state	
		X_plus = theta(np.dot(A.T, X) + np.dot(B1.T, u) + C)
		# apply STDP
		if STDP_rule != "off":
			for synapse in STDP_rule:
				(A[synapse[0]-1][synapse[1]-1], counter) = STDP(X[synapse[0]-1],
															X[synapse[1]-1],
															X_plus[synapse[0]-1],
															X_plus[synapse[1]-1],
															A[synapse[0]-1][synapse[1]-1],
															counter)
		# update states
		X = X_plus
	
	history = history[:, 1:nb_epochs]						# remove 1st dummy state of history

	return history											# history (x axis: time; y axis: #cells)

# NOTE:
# - The last state of the history is not appended.
# - history:	first rows	:	inputs' spikes trains
#				next rows	:	internal cells' spike trains


# ******* #
# Example #
# ******* #

# A = np.array([[0, 0.5, 0.5],[0, 0, 0],[0, 0, 0]])
# B1 = np.array([[0.5, 0, 0],[0, 0, 0.5]])
# B2 = np.array([[0, 0],[1, 0],[0, 0]])
# C = np.array([[0.5], [0.5], [0]])
# X = np.zeros([3, 1])
# U = {0: np.array([[1], [0]]), 1: np.array([[0], [1]])}
# 
# print simulation(A, B1, B2, C, X, U, nb_epochs = 10, STDP_rule = [(1,2)])