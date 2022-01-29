# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# ******* #
# Imports #
# ******* #

from synfire_rings import *
from position_tape import *
from symbol_tape import *


# ********** #
# Cache Tape #
# ********** #

def CacheTape(N, length=9, inh=-10.0, suffix=""):
	"""
	Creates a cache tape of length "length" and using inhibitory weights "inh".
	The tape is composed of 3 layers of synfire rings whose activations encode the
	symbol currently read by the TM's head, blank, 0 or 1.
	The 3 layers are called tape_CB+suffix, tape_C0+suffix and tape_C1+suffix, resp.
	The symbol tape is added to the network N.
	"""

	# 3 layers of synfire rings composing the cache tape
	tape_CB, tape_C0, tape_C1 = [], [], []

	for i in range(length):
		R1 = Ring(name = "tape_CB" + suffix + str(i))
		R2 = Ring(name = "tape_C0" + suffix + str(i))
		R3 = Ring(name = "tape_C1" + suffix + str(i))
		R1.make_triangle()
		R2.make_triangle()
		R3.make_triangle()
		tape_CB.append(R1)
		tape_C0.append(R2)
		tape_C1.append(R3)
		
	# add tape_CB to the network
	for ring in tape_CB:
		N.add_ring(ring)

	# add tape_C0 to the network
	for ring in tape_C0:
		N.add_ring(ring)

	# add tape_C1 to the network
	for ring in tape_C1:
		N.add_ring(ring)
		
	# add inhibitory connections throughout columns of layers CB, C0, C1
	# ensures that one symbol is read at a time
	for i in range(length):
		N.ring2ring_connectI(tape_CB[i], tape_C0[i], inh)
		N.ring2ring_connectI(tape_CB[i], tape_C1[i], inh)
		if i < length - 1:
			N.ring2ring_connectI(tape_CB[i], tape_CB[i+1], inh)
			N.ring2ring_connectI(tape_CB[i], tape_C0[i+1], inh)
			N.ring2ring_connectI(tape_CB[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI(tape_CB[i], tape_CB[i-1], inh)
			N.ring2ring_connectI(tape_CB[i], tape_C0[i-1], inh)
			N.ring2ring_connectI(tape_CB[i], tape_C1[i-1], inh)
		N.ring2ring_connectI(tape_C0[i], tape_CB[i], inh)
		N.ring2ring_connectI(tape_C0[i], tape_C1[i], inh)
		if i < length - 1:
			N.ring2ring_connectI(tape_C0[i], tape_CB[i+1], inh)
			N.ring2ring_connectI(tape_C0[i], tape_C0[i+1], inh)
			N.ring2ring_connectI(tape_C0[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI(tape_C0[i], tape_CB[i-1], inh)
			N.ring2ring_connectI(tape_C0[i], tape_C0[i-1], inh)
			N.ring2ring_connectI(tape_C0[i], tape_C1[i-1], inh)
		N.ring2ring_connectI(tape_C1[i], tape_CB[i], inh)
		N.ring2ring_connectI(tape_C1[i], tape_C0[i], inh)
		if i < length - 1:
			N.ring2ring_connectI(tape_C1[i], tape_CB[i+1], inh)
			N.ring2ring_connectI(tape_C1[i], tape_C0[i+1], inh)
			N.ring2ring_connectI(tape_C1[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI(tape_C1[i], tape_CB[i-1], inh)
			N.ring2ring_connectI(tape_C1[i], tape_C0[i-1], inh)
			N.ring2ring_connectI(tape_C1[i], tape_C1[i-1], inh)
			
	return [tape_CB, tape_C0, tape_C1]


def ConnectPositionSymbolCache(N, PositionTape, SymbolTape, CacheTape, exc1=0.5, exc2=0.5):
	"""
	Creates connections between a position tape, a symbol tape and a cache tape.
	Uses 2 excitatory weights exc1 and exc1.
	Original setting: exc1=exc2=0.5 and connections of types E, E2, E.
	Current setting: no more need of E2 connections.
	"""
	
	[tape_L, tape_R] = PositionTape
	[tape_B, tape_0, tape_1] = SymbolTape
	[tape_CB, tape_C0, tape_C1] = CacheTape
	length = len(PositionTape[0])
	
	for i in range(length):

		# excitatory connections throughout columns of tapes L, R and B, 0, 1
		# ensures the possibility to write a symbol at current position
		N.ring2ring_connectE(tape_L[i], tape_B[i], exc1)
		N.ring2ring_connectE(tape_L[i], tape_0[i], exc1)
		N.ring2ring_connectE(tape_L[i], tape_1[i], exc1)
		N.ring2ring_connectE(tape_R[i], tape_B[i], exc1)
		N.ring2ring_connectE(tape_R[i], tape_0[i], exc1)
		N.ring2ring_connectE(tape_R[i], tape_1[i], exc1)
		
		# excitatory connections throughout columns of tapes L, R and CB, C0, C1
		# copying current symbol into the cache, part 1
		# (current setting: this is no more relevant)
		# (ring2ring_connectE2 means that the activation happens only once, 
		# otherwise cache over-activated)
		N.ring2ring_connectE(tape_L[i], tape_CB[i], exc2)
		N.ring2ring_connectE(tape_L[i], tape_C0[i], exc2)
		N.ring2ring_connectE(tape_L[i], tape_C1[i], exc2)
		N.ring2ring_connectE(tape_R[i], tape_CB[i], exc2)
		N.ring2ring_connectE(tape_R[i], tape_C0[i], exc2)
		N.ring2ring_connectE(tape_R[i], tape_C1[i], exc2)
		
		# excitatory connections throughout columns of tapes B, 0, 1 and CB, C0, C1
		# copying current symbol into the cache, part 2
		N.ring2ring_connectE(tape_B[i], tape_CB[i], exc2)
		N.ring2ring_connectE(tape_0[i], tape_C0[i], exc2)
		N.ring2ring_connectE(tape_1[i], tape_C1[i], exc2)
	

def CacheTapeNew(N, length=9, inh=-10.0, suffix=""):
	"""
	Creates a cache tape of length "length" and using inhibitory weights "inh".
	The tape is composed of 3 layers of synfire rings whose activations encode the
	symbol currently read by the TM's head, blank, 0 or 1.
	The 3 layers are called tape_CB+suffix, tape_C0+suffix and tape_C1+suffix, resp.
	The symbol tape is added to the network N.
	"""

	# 3 layers of synfire rings composing the cache tape
	tape_CB, tape_C0, tape_C1 = [], [], []
	for i in range(length):
		R1, R2, R3 = Ring(name = "tape_CB" + suffix + str(i)), Ring(name = "tape_C0" + suffix + str(i)), Ring(name = "tape_C1" + suffix + str(i))
		R1.add_satellite()
		R2.add_satellite()
		R3.add_satellite()
		tape_CB.append(R1)
		tape_C0.append(R2)
		tape_C1.append(R3)
		
	# add tape_CB to the network
	for ring in tape_CB:
		N.add_ring(ring)

	# add tape_C0 to the network
	for ring in tape_C0:
		N.add_ring(ring)

	# add tape_C1 to the network
	for ring in tape_C1:
		N.add_ring(ring)
		
	# add inhibitory connections throughout columns of layers CB, C0, C1
	# ensures that one symbol is read at a time
	for i in range(length):
		N.ring2ring_connectI_new(tape_CB[i], tape_C0[i], inh)
		N.ring2ring_connectI_new(tape_CB[i], tape_C1[i], inh)
		if i < length - 1:
			N.ring2ring_connectI_new(tape_CB[i], tape_CB[i+1], inh)
			N.ring2ring_connectI_new(tape_CB[i], tape_C0[i+1], inh)
			N.ring2ring_connectI_new(tape_CB[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI_new(tape_CB[i], tape_CB[i-1], inh)
			N.ring2ring_connectI_new(tape_CB[i], tape_C0[i-1], inh)
			N.ring2ring_connectI_new(tape_CB[i], tape_C1[i-1], inh)
		N.ring2ring_connectI_new(tape_C0[i], tape_CB[i], inh)
		N.ring2ring_connectI_new(tape_C0[i], tape_C1[i], inh)
		if i < length - 1:
			N.ring2ring_connectI_new(tape_C0[i], tape_CB[i+1], inh)
			N.ring2ring_connectI_new(tape_C0[i], tape_C0[i+1], inh)
			N.ring2ring_connectI_new(tape_C0[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI_new(tape_C0[i], tape_CB[i-1], inh)
			N.ring2ring_connectI_new(tape_C0[i], tape_C0[i-1], inh)
			N.ring2ring_connectI_new(tape_C0[i], tape_C1[i-1], inh)
		N.ring2ring_connectI_new(tape_C1[i], tape_CB[i], inh)
		N.ring2ring_connectI_new(tape_C1[i], tape_C0[i], inh)
		if i < length - 1:
			N.ring2ring_connectI_new(tape_C1[i], tape_CB[i+1], inh)
			N.ring2ring_connectI_new(tape_C1[i], tape_C0[i+1], inh)
			N.ring2ring_connectI_new(tape_C1[i], tape_C1[i+1], inh)
		if i > 0:
			N.ring2ring_connectI_new(tape_C1[i], tape_CB[i-1], inh)
			N.ring2ring_connectI_new(tape_C1[i], tape_C0[i-1], inh)
			N.ring2ring_connectI_new(tape_C1[i], tape_C1[i-1], inh)
			
	return [tape_CB, tape_C0, tape_C1]


def ConnectPositionSymbolCacheNew(N, PositionTape, SymbolTape, CacheTape, exc1=0.5, exc2=0.5):
	"""
	Creates connections between a position tape, a symbol tape and a cache tape.
	Uses 2 excitatory weights exc1 and exc1.
	Original setting: exc1=exc2=0.5 and connections of types E, E2, E.
	Current setting: no more need of E2 connections.
	"""
	
	[tape_L, tape_R] = PositionTape
	[tape_B, tape_0, tape_1] = SymbolTape
	[tape_CB, tape_C0, tape_C1] = CacheTape
	length = len(PositionTape[0])
	
	for i in range(length):

		# excitatory connections throughout columns of tapes L, R and B, 0, 1
		# ensures the possibility to write a symbol at current position
		N.ring2ring_connectE_new(tape_L[i], tape_B[i], exc1)
		N.ring2ring_connectE_new(tape_L[i], tape_0[i], exc1)
		N.ring2ring_connectE_new(tape_L[i], tape_1[i], exc1)
		N.ring2ring_connectE_new(tape_R[i], tape_B[i], exc1)
		N.ring2ring_connectE_new(tape_R[i], tape_0[i], exc1)
		N.ring2ring_connectE_new(tape_R[i], tape_1[i], exc1)
		
		# excitatory connections throughout columns of tapes L, R and CB, C0, C1
		# copying current symbol into the cache, part 1
		# (current setting: this is no more relevant)
		# (ring2ring_connectE2 means that the activation happens only once, 
		# otherwise cache over-activated)
		N.ring2ring_connectE_new(tape_L[i], tape_CB[i], exc2)
		N.ring2ring_connectE_new(tape_L[i], tape_C0[i], exc2)
		N.ring2ring_connectE_new(tape_L[i], tape_C1[i], exc2)
		N.ring2ring_connectE_new(tape_R[i], tape_CB[i], exc2)
		N.ring2ring_connectE_new(tape_R[i], tape_C0[i], exc2)
		N.ring2ring_connectE_new(tape_R[i], tape_C1[i], exc2)
		
		# excitatory connections throughout columns of tapes B, 0, 1 and CB, C0, C1
		# copying current symbol into the cache, part 2
		N.ring2ring_connectE_new(tape_B[i], tape_CB[i], exc2)
		N.ring2ring_connectE_new(tape_0[i], tape_C0[i], exc2)
		N.ring2ring_connectE_new(tape_1[i], tape_C1[i], exc2)


# # ******* #
# # Example #
# # ******* #

# # Network
# N = Network()

# # inputs
# # position cells
# start = Cell()
# start.ring_name = "start"
# cell_l = Cell()
# cell_l.ring_name = "cell_left"
# cell_r = Cell()
# cell_r.ring_name = "cell_right"
# # writing cells
# write_B = Cell()
# write_B.ring_name = "cell_B"
# write_0 = Cell()
# write_0.ring_name = "cell_0"
# write_1 = Cell()
# write_1.ring_name = "cell_1"

# # adding cells to the network
# N.add_cell(start)
# N.add_cell(cell_l)
# N.add_cell(cell_r)
# N.add_cell(write_B)
# N.add_cell(write_0)
# N.add_cell(write_1)

# # creation of the position, symbol and cache tapes and adding them to the net
# PositionTape = PositionTapeNew(N)
# SymbolTape = SymbolTapeNew(N)
# CacheTape = CacheTapeNew(N)
# ConnectPositionSymbolCacheNew(N, PositionTape, SymbolTape, CacheTape)

# # other connections
# # positions
# exc2 = 0.6
# # start cell activates leftmost ring
# N.cell2ring_connect_new(start, PositionTape[1][0], 1.0)
# # connect cell_l to the "left" rings
# for i in range(len(PositionTape[0])):
# 	N.cell2ring_connect_new(cell_l, PositionTape[0][i], exc2)
# # connect cell_r to the "right" rings
# for i in range(len(PositionTape[1])):
# 	N.cell2ring_connect_new(cell_r, PositionTape[1][i], exc2)
# # symbols
# exc = 1.0
# # writing the pattern BB010011B
# N.cell2ring_connect_new(write_B, SymbolTape[0][0], exc)
# N.cell2ring_connect_new(write_B, SymbolTape[0][1], exc)
# N.cell2ring_connect_new(write_0, SymbolTape[1][2], exc)
# N.cell2ring_connect_new(write_1, SymbolTape[2][3], exc)
# N.cell2ring_connect_new(write_0, SymbolTape[1][4], exc)
# N.cell2ring_connect_new(write_0, SymbolTape[1][5], exc)
# N.cell2ring_connect_new(write_1, SymbolTape[2][6], exc)
# N.cell2ring_connect_new(write_1, SymbolTape[2][7], exc)
# N.cell2ring_connect_new(write_B, SymbolTape[0][8], exc)


# # print indices
# print "Tape L"
# print N.nodes.index(PositionTape[0][0].nodes[0])
# print N.nodes.index(PositionTape[0][-1].nodes[-1])
# print "Tape R"
# print N.nodes.index(PositionTape[1][0].nodes[0])
# print N.nodes.index(PositionTape[1][-1].nodes[-1])
# print "Tape B"
# print N.nodes.index(SymbolTape[0][0].nodes[0])
# print N.nodes.index(SymbolTape[0][-1].nodes[-1])
# print "Tape 0"
# print N.nodes.index(SymbolTape[1][0].nodes[0])
# print N.nodes.index(SymbolTape[1][-1].nodes[-1])
# print "Tape 1"
# print N.nodes.index(SymbolTape[2][0].nodes[0])
# print N.nodes.index(SymbolTape[2][-1].nodes[-1])
# print "Tape CB"
# print N.nodes.index(CacheTape[0][0].nodes[0])
# print N.nodes.index(CacheTape[0][-1].nodes[-1])
# print "Tape C0"
# print N.nodes.index(CacheTape[1][0].nodes[0])
# print N.nodes.index(CacheTape[1][-1].nodes[-1])
# print "Tape C1"
# print N.nodes.index(CacheTape[2][0].nodes[0])
# print N.nodes.index(CacheTape[2][-1].nodes[-1])


# # input dico U (write_B, write_0, write_1)
# # after test, all transitions are working
# U = {
# 	# position on leftmost ring + writing symbols
# 	0: np.array([[1], [0], [0], [1], [1], [1]]), \
# 	# move right
# 	20: np.array([[0], [0], [1], [0], [0], [0]]), \
# 	40: np.array([[0], [0], [1], [0], [0], [0]]), \
# 	# move left
# 	60: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	80: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	100: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	# oscillate
# 	120: np.array([[0], [0], [1], [0], [0], [0]]), \
# 	140: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	160: np.array([[0], [0], [1], [0], [0], [0]]), \
# 	180: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	200: np.array([[0], [0], [1], [0], [0], [0]]), \
# 	220: np.array([[0], [1], [0], [0], [0], [0]]), \
# 	}


# # simulation
# path = "/Users/jeremie.cabessau-paris2.fr/Desktop/MAIN/Programmation/Python/My_programs/synfire_rings/"
# N.write_csv()
# S = N.simulate(U, epoch = 300)
# np.savetxt(path + "data/raster2.csv", S, delimiter = ",")
