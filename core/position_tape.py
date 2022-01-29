# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# ******* #
# Imports #
# ******* #

from synfire_rings import *


# ************* #
# Position Tape #
# ************* #

def PositionTape(N, length=9, exc=0.4, inh=-10.0, suffix=""):
	"""
	Create a position tape of length "length" using excitatory 
	and inhibitory weights "exc" and "inh".
	The tape is composed of 2 layers of synfire rings that encodes 
	the left and right movements of the TM's head, respecively.
	The position tape is added to the network N.
	"""

	# 2 layers of synfire rings composing the symbol tape
	tape_L, tape_R = [], []

	for i in range(length):
		R1 = Ring(name = "tape_L" + suffix + str(i))
		R2 = Ring(name = "tape_R" + suffix + str(i))
		R1.make_triangle()
		R2.make_triangle()
		tape_L.append(R1)
		tape_R.append(R2)
		
	# add tape_L to the network
	for ring in tape_L:
		N.add_ring(ring)

	# add tape_R to the network
	for ring in tape_R:
		N.add_ring(ring)
		
	# add excitatory and inhibitory connections throughout layers R and L.
	# ensures that one position is activated at a time
	for i in range(length - 1):
		# add excitatory and inhibitory connections along layers L and R
		# (ensures the possibility to move left or right, part 1)
		N.ring2ring_connectE(tape_L[i+1], tape_L[i], exc)
		N.ring2ring_connectI(tape_L[i], tape_L[i+1], inh)
		N.ring2ring_connectE(tape_R[i], tape_R[i+1], exc)
		N.ring2ring_connectI(tape_R[i+1], tape_R[i], inh)
		# add excitatory and inhibitory connections throughout diagonals of layers L and R
		# (ensures the possibility to move left or right, part 2)
		N.ring2ring_connectE(tape_L[i], tape_R[i+1], exc)
		N.ring2ring_connectI(tape_R[i+1], tape_L[i], inh)
		N.ring2ring_connectE(tape_R[i+1], tape_L[i], exc)
		N.ring2ring_connectI(tape_L[i], tape_R[i+1], inh)
	
	return [tape_L, tape_R]


def PositionTapeNew(N, length=9, exc=0.4, inh=-10.0, suffix=""):
	"""
	Create a position tape of length "length" using excitatory 
	and inhibitory weights "exc" and "inh".
	The tape is composed of 2 layers of synfire rings that encodes 
	the left and right movements of the TM's head, respecively.
	The position tape is added to the network N.
	"""

	# 2 layers of synfire rings composing the symbol tape
	tape_L, tape_R = [], []

	for i in range(length):
		R1 = Ring(name = "tape_L" + suffix + str(i))
		R2 = Ring(name = "tape_R" + suffix + str(i))
		R1.add_satellite()
		R2.add_satellite()
		tape_L.append(R1)
		tape_R.append(R2)
		
	# add tape_L to the network
	for ring in tape_L:
		N.add_ring(ring)

	# add tape_R to the network
	for ring in tape_R:
		N.add_ring(ring)
		
	# add excitatory and inhibitory connections throughout layers R and L.
	# ensures that one position is activated at a time
	for i in range(length - 1):
		# add excitatory and inhibitory connections along tape L and R
		# (ensures the possibility to move left or right, part 1)
		N.ring2ring_connectE_new(tape_L[i+1], tape_L[i], exc)
		N.ring2ring_connectI_new(tape_L[i], tape_L[i+1], inh)
		N.ring2ring_connectE_new(tape_R[i], tape_R[i+1], exc)
		N.ring2ring_connectI_new(tape_R[i+1], tape_R[i], inh)
		# add excitatory and inhibitory connections throughout diagonals of tapes L and R
		# (ensures the possibility to move left or right, part 2)
		N.ring2ring_connectE_new(tape_L[i], tape_R[i+1], exc)
		N.ring2ring_connectI_new(tape_R[i+1], tape_L[i], inh)
		N.ring2ring_connectE_new(tape_R[i+1], tape_L[i], exc)
		N.ring2ring_connectI_new(tape_L[i], tape_R[i+1], inh)
	
	return [tape_L, tape_R]


# # ******* #
# # Example #
# # ******* #

# # Network
# N = Network()

# # inputs
# start = Cell()
# start.ring_name = "start"
# cell_l = Cell()
# cell_l.ring_name = "cell_left"
# cell_r = Cell()
# cell_r.ring_name = "cell_right"

# # adding cells to the network
# N.add_cell(start)
# N.add_cell(cell_l)
# N.add_cell(cell_r)

# # creation of the tape and adding it to the net
# PositionTape = PositionTapeNew(N)

# # other connections
# exc2 = 0.6
# # start cell activates leftmost ring
# N.cell2ring_connect_new(start, PositionTape[1][0], 1.0)
# # connect cell_l to the "left" rings
# for i in range(len(PositionTape[0])):
# 	N.cell2ring_connect_new(cell_l, PositionTape[0][i], exc2)
# # connect cell_r to the "right" rings
# for i in range(len(PositionTape[1])):
# 	N.cell2ring_connect_new(cell_r, PositionTape[1][i], exc2)

# # input dico U (start1, start2, tic)
# # after test, all transitions are working
# U = {
# 	# start1 only (to set the initial configuration)
# 	0: np.array([[1], [0], [0]]), \
# 	21: np.array([[0], [0], [1]]), \
# 	42: np.array([[0], [0], [1]]), \
# 	63: np.array([[0], [1], [0]]), \
# 	84: np.array([[0], [1], [0]]), \
# 	105: np.array([[0], [1], [0]]), \
# 	126: np.array([[0], [0], [1]]), \
# 	147: np.array([[0], [1], [0]]), \
# 	168: np.array([[0], [0], [1]]), \
# 	189: np.array([[0], [0], [1]]), \
# 	210: np.array([[0], [1], [0]]), \
# 	231: np.array([[0], [0], [1]])
# 	}

# # simulation
# path = "/Users/jeremie.cabessau-paris2.fr/Desktop/MAIN/Programmation/Python/My_programs/synfire_rings/"
# N.write_csv()
# S = N.simulate(U, epoch = 240)
# np.savetxt(path + "data/raster2.csv", S, delimiter = ",")
