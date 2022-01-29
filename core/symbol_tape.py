# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# ******* #
# Imports #
# ******* #

from synfire_rings import *


# *********** #
# Symbol Tape #
# *********** #

def SymbolTape(N, length=9, inh=-10.0, suffix=""):
	"""
	Creates a symbol tape of length "length" and using inhibitory weights "inh".
	The tape is composed of 3 layers of synfire rings whose activations encode the
	presence of symbols "blank", 0 and 1 written on the TM's tape, respectively.
	The 3 layers are called tape_B+suffix, tape_0+suffix and tape_1+suffix, resp.
	The symbol tape is added to the network N.
	"""

	# 3 layers of synfire rings composing the symbol tape
	tape_B, tape_0, tape_1 = [], [], []

	for i in range(length):
		R1 = Ring(name = "tape_B" + suffix + str(i))
		R2 = Ring(name = "tape_0" + suffix + str(i))
		R3 = Ring(name = "tape_1" + suffix + str(i))
		R1.make_triangle()
		R2.make_triangle()
		R3.make_triangle()
		tape_B.append(R1)
		tape_0.append(R2)
		tape_1.append(R3)
		
	# add tape_B to the network
	for ring in tape_B:
		N.add_ring(ring)

	# add tape_0 to the network
	for ring in tape_0:
		N.add_ring(ring)

	# add tape_1 to the network
	for ring in tape_1:
		N.add_ring(ring)
		
	# add inhibitory connections throughout columns of layers B, 0, 1
	# ensures that one symbol is activated at a time
	for i in range(length):
		N.ring2ring_connectI(tape_B[i], tape_0[i], inh)
		N.ring2ring_connectI(tape_B[i], tape_1[i], inh)
		N.ring2ring_connectI(tape_0[i], tape_B[i], inh)
		N.ring2ring_connectI(tape_0[i], tape_1[i], inh)
		N.ring2ring_connectI(tape_1[i], tape_B[i], inh)
		N.ring2ring_connectI(tape_1[i], tape_0[i], inh)
	
	return [tape_B, tape_0, tape_1]


def SymbolTapeNew(N, length=9, inh=-10.0, suffix=""):
	"""
	Compared to the previous function, we try to remove the 
	"triangular" or "single cell" inhibitory systems.
	
	Creates a symbol tape of length "length" and using inhibitory weights "inh".
	The tape is composed of 3 layers of synfire rings whose activations encode the
	presence of symbols "blank", 0 and 1 written on the tape, respectively.
	The 3 layers are called tape_B+suffix, tape_0+suffix and tape_1+suffix, resp.
	The symbol tape is added to the network N.
	"""

	# 3 layers of synfire rings composing the symbol tape
	tape_B, tape_0, tape_1 = [], [], []
	for i in range(length):
		R1 = Ring(name = "tape_B" + suffix + str(i))
		R2 = Ring(name = "tape_0" + suffix + str(i))
		R3 = Ring(name = "tape_1" + suffix + str(i))
		R1.add_satellite()
		R2.add_satellite()
		R3.add_satellite()
		tape_B.append(R1)
		tape_0.append(R2)
		tape_1.append(R3)
		
	# add tape_B to the network
	for ring in tape_B:
		N.add_ring(ring)

	# add tape_0 to the network
	for ring in tape_0:
		N.add_ring(ring)

	# add tape_1 to the network
	for ring in tape_1:
		N.add_ring(ring)
		
	# add inhibitory connections throughout columns of layers B, 0, 1
	# ensures that one symbol is activated at a time
	for i in range(length):
		N.ring2ring_connectI_new(tape_B[i], tape_0[i], inh)
		N.ring2ring_connectI_new(tape_B[i], tape_1[i], inh)
		N.ring2ring_connectI_new(tape_0[i], tape_B[i], inh)
		N.ring2ring_connectI_new(tape_0[i], tape_1[i], inh)
		N.ring2ring_connectI_new(tape_1[i], tape_B[i], inh)
		N.ring2ring_connectI_new(tape_1[i], tape_0[i], inh)
	
	return [tape_B, tape_0, tape_1]


# # ******* #
# # Example #
# # ******* #

# # Network
# N = Network()

# # inputs
# write_B = Cell()
# write_B.ring_name = "cell_B"
# write_0 = Cell()
# write_0.ring_name = "cell_0"
# write_1 = Cell()
# write_1.ring_name = "cell_1"
# # inputs for overwriting
# write_B_overwrite = Cell()
# write_B_overwrite.ring_name = "cell_B_overwrite"
# write_0_overwrite = Cell()
# write_0_overwrite.ring_name = "cell_0_overwrite"
# write_1_overwrite = Cell()
# write_1_overwrite.ring_name = "cell_1_overwrite"

# # adding cells to the network
# N.add_cell(write_B)
# N.add_cell(write_0)
# N.add_cell(write_1)
# N.add_cell(write_B_overwrite)
# N.add_cell(write_0_overwrite)
# N.add_cell(write_1_overwrite)

# # creation of the tape and adding it to the net
# SymbolTape = SymbolTapeNew(N)

# # other connections
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
# # overwriting the pattern 10B0110B0
# N.cell2ring_connect_new(write_1_overwrite, SymbolTape[2][0], exc)
# N.cell2ring_connect_new(write_0_overwrite, SymbolTape[1][1], exc)
# N.cell2ring_connect_new(write_B_overwrite, SymbolTape[0][2], exc)
# N.cell2ring_connect_new(write_0_overwrite, SymbolTape[1][3], exc)
# N.cell2ring_connect_new(write_1_overwrite, SymbolTape[2][4], exc)
# N.cell2ring_connect_new(write_1_overwrite, SymbolTape[2][5], exc)
# N.cell2ring_connect_new(write_0_overwrite, SymbolTape[1][6], exc)
# N.cell2ring_connect_new(write_B_overwrite, SymbolTape[0][7], exc)
# N.cell2ring_connect_new(write_0_overwrite, SymbolTape[1][8], exc)

# # print indices
# print "Tape B"
# print N.nodes.index(SymbolTape[0][0].nodes[0])
# print N.nodes.index(SymbolTape[0][-1].nodes[-1])
# print "Tape 0"
# print N.nodes.index(SymbolTape[1][0].nodes[0])
# print N.nodes.index(SymbolTape[1][-1].nodes[-1])
# print "Tape 1"
# print N.nodes.index(SymbolTape[2][0].nodes[0])
# print N.nodes.index(SymbolTape[2][-1].nodes[-1])


# # input dico U (write_B, write_0, write_1)
# # after test, all transitions are working
# U = {
# 	# writing symbols
# 	0: np.array([[1], [1], [1], [0], [0], [0]]), \
# 	# overwriting symbols
# 	50: np.array([[0], [0], [0], [1], [1], [1]]) 
# 	}

# # simulation
# path = "/Users/jeremie.cabessau-paris2.fr/Desktop/MAIN/Programmation/Python/My_programs/synfire_rings/"
# N.write_csv()
# S = N.simulate(U, epoch = 200)
# np.savetxt(path + "data/raster2.csv", S, delimiter = ",")
