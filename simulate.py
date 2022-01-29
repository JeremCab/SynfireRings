# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# ************************************************************* #
# Implementation of a neural network composed of synfire rings 	#
#																#
# that encodes a a TM recognizing \{a^n b^n a^n : n \geq 0 \}.	#
# This version uses 3 clock cells tic1, tic2 and tic3.			#
#																#
# The order of operations is the following:						#
# 0.  Set initial configuration and activate initial states		#
# 1.  Update cache (symbols read by the position heads)			#
# 2a. Update state (using current state and cache symbols)		#
# 2b. Write new symbol (accoroding to the current transition)	#
# 2c. Move head (accoroding to the current transition)			#
# 3.  GOTO 1 													#
# These operations are triggered by the 3 clock cells			#
# ************************************************************* #


# ******* #
# Imports #
# ******* #

import pickle
from os import sys
sys.path.insert(0, "./core")

from synfire_rings import *
from position_tape import *
from symbol_tape import *
from cache_tape import *


# ******* #
# Network #
# ******* #

N = Network()


# ****** #
# Inputs #
# ****** #

tic0 = Cell()
tic0.ring_name = "start"
tic1 = Cell()
tic1.ring_name = "tic"
tic2 = Cell()
tic2.ring_name = "tac"
tic3 = Cell()
tic3.ring_name = "toc"

# adding input cells
N.add_cell(tic0)
N.add_cell(tic1)
N.add_cell(tic2)
N.add_cell(tic3)


# ************************************** #
# Position tape, Symbol tape, Cache tape #
# ************************************** #

tape_length = 10

# 1st tapes (bottom)
PositionTape1 = PositionTape(N, length = tape_length, suffix = "1")
SymbolTape1 = SymbolTape(N, length = tape_length, suffix = "1")
CacheTape1 = CacheTape(N, length = tape_length, suffix = "1")
ConnectPositionSymbolCache(N, PositionTape1, SymbolTape1, CacheTape1,  exc2 = 0.3)
# names
[tape_L1, tape_R1] = PositionTape1
[tape_B1, tape_01, tape_11] = SymbolTape1
[tape_CB1, tape_C01, tape_C11] = CacheTape1

# 2nd tapes (middle)
PositionTape2 = PositionTape(N, length = tape_length, suffix = "2")
SymbolTape2 = SymbolTape(N, length = tape_length, suffix = "2")
CacheTape2 = CacheTape(N, length = tape_length, suffix = "2")
ConnectPositionSymbolCache(N, PositionTape2, SymbolTape2, CacheTape2, exc2 = 0.3)
# names
[tape_L2, tape_R2] = PositionTape2
[tape_B2, tape_02, tape_12] = SymbolTape2
[tape_CB2, tape_C02, tape_C12] = CacheTape2


# ********************* #
# Initial Configuration #
# ********************* #

# Initial configuration triggered by cells tic0.
# Write input 000111000B on tape 1.

k = 3
w_input2tape = 1.0

for i in range(tape_length - 3*k):
	N.cell2ring_connect(tic0, tape_B1[3*k + i], w_input2tape)

for i in range(k):
	N.cell2ring_connect(tic0, tape_01[i], w_input2tape)
	N.cell2ring_connect(tic0, tape_11[k + i], w_input2tape)
	N.cell2ring_connect(tic0, tape_01[2*k + i], w_input2tape)

# head at beginning of tape 1: activation of tape_R1[0]
N.cell2ring_connect(tic0, tape_R1[0], w_input2tape)

# write BBB... on tape 2
for i in range(tape_length):
	N.cell2ring_connect(tic0, tape_B2[i], w_input2tape)

# head at beginning of tape 2: activation of tape_R2[0]
N.cell2ring_connect(tic0, tape_R2[0], w_input2tape)


# ************* #
# Program rings #
# ************* #

# Create program rings.

# state i (initial state)
RiBB = Ring(name = "RiBB")
RiBB.make_triangle()
Ri0B = Ring(name = "Ri0B")
Ri0B.make_triangle()
Ri1B = Ring(name = "Ri1B")
Ri1B.make_triangle()

# states q0 and q0bis
Rq0BB = Ring(name = "Rq0BB")
Rq0BB.make_triangle()
Rq0bisBB = Ring(name = "Rq0bisBB")
Rq0bisBB.make_triangle()
Rq00B = Ring(name = "Rq00B")
Rq00B.make_triangle()
Rq0bis0B = Ring(name = "Rq0bis0B")
Rq0bis0B.make_triangle()
Rq01B = Ring(name = "Rq01B")
Rq01B.make_triangle()
Rq0bis1B = Ring(name = "Rq0bis1B")
Rq0bis1B.make_triangle()

# states q1 and q1bis
Rq1BB = Ring(name = "Rq1BB")
Rq1BB.make_triangle()
Rq1bisBB = Ring(name = "Rq1bisBB")
Rq1bisBB.make_triangle()

Rq1B0 = Ring(name = "Rq1B0")
Rq1B0.make_triangle()
Rq1bisB0 = Ring(name = "Rq1bisB0")
Rq1bisB0.make_triangle()

Rq1B1 = Ring(name = "Rq1B1")
Rq1B1.make_triangle()
Rq1bisB1 = Ring(name = "Rq1bisB1")
Rq1bisB1.make_triangle()

Rq10B = Ring(name = "Rq10B")
Rq10B.make_triangle()
Rq1bis0B = Ring(name = "Rq1bis0B")
Rq1bis0B.make_triangle()

Rq100 = Ring(name = "Rq100")
Rq100.make_triangle()
Rq1bis00 = Ring(name = "Rq1bis00")
Rq1bis00.make_triangle()

Rq101 = Ring(name = "Rq101")
Rq101.make_triangle()
Rq1bis01 = Ring(name = "Rq1bis01")
Rq1bis01.make_triangle()

Rq11B = Ring(name = "Rq11B")
Rq11B.make_triangle()
Rq1bis1B = Ring(name = "Rq1bis1B")
Rq1bis1B.make_triangle()

Rq110 = Ring(name = "Rq110")
Rq110.make_triangle()
Rq1bis10 = Ring(name = "Rq1bis10")
Rq1bis10.make_triangle()

Rq111 = Ring(name = "Rq111")
Rq111.make_triangle()
Rq1bis11 = Ring(name = "Rq1bis11")
Rq1bis11.make_triangle()

# states q2 and q2bis
Rq2BB = Ring(name = "Rq2BB")
Rq2BB.make_triangle()
Rq2bisBB = Ring(name = "Rq2bisBB")
Rq2bisBB.make_triangle()

Rq2B0 = Ring(name = "Rq2B0")
Rq2B0.make_triangle()
Rq2bisB0 = Ring(name = "Rq2bisB0")
Rq2bisB0.make_triangle()

Rq2B1 = Ring(name = "Rq2B1")
Rq2B1.make_triangle()
Rq2bisB1 = Ring(name = "Rq2bisB1")
Rq2bisB1.make_triangle()

Rq20B = Ring(name = "Rq20B")
Rq20B.make_triangle()
Rq2bis0B = Ring(name = "Rq2bis0B")
Rq2bis0B.make_triangle()

Rq200 = Ring(name = "Rq200")
Rq200.make_triangle()
Rq2bis00 = Ring(name = "Rq2bis00")
Rq2bis00.make_triangle()

Rq201 = Ring(name = "Rq201")
Rq201.make_triangle()
Rq2bis01 = Ring(name = "Rq2bis01")
Rq2bis01.make_triangle()

Rq21B = Ring(name = "Rq21B")
Rq21B.make_triangle()
Rq2bis1B = Ring(name = "Rq2bis1B")
Rq2bis1B.make_triangle()

Rq210 = Ring(name = "Rq210")
Rq210.make_triangle()
Rq2bis10 = Ring(name = "Rq2bis10")
Rq2bis10.make_triangle()

Rq211 = Ring(name = "Rq211")
Rq211.make_triangle()
Rq2bis11 = Ring(name = "Rq2bis11")
Rq2bis11.make_triangle()

# states accept and reject (final)
Raccept = Ring(name = "Raccept")
Raccept.make_triangle()
Rreject = Ring(name = "Rreject")
Rreject.make_triangle()


# Add program's rings.

# state i (initial)
N.add_ring(RiBB)
N.add_ring(Ri0B)
N.add_ring(Ri1B)

# state q0
N.add_ring(Rq0BB)
N.add_ring(Rq00B)
N.add_ring(Rq01B)
N.add_ring(Rq0bisBB)
N.add_ring(Rq0bis0B)
N.add_ring(Rq0bis1B)

# state q1
N.add_ring(Rq1BB)
N.add_ring(Rq1B0)
N.add_ring(Rq1B1)
N.add_ring(Rq10B)
N.add_ring(Rq100)
N.add_ring(Rq101)
N.add_ring(Rq11B)
N.add_ring(Rq110)
N.add_ring(Rq111)
N.add_ring(Rq1bisBB)
N.add_ring(Rq1bisB0)
N.add_ring(Rq1bisB1)
N.add_ring(Rq1bis0B)
N.add_ring(Rq1bis00)
N.add_ring(Rq1bis01)
N.add_ring(Rq1bis1B)
N.add_ring(Rq1bis10)
N.add_ring(Rq1bis11)

# state q2
N.add_ring(Rq2BB)
N.add_ring(Rq2B0)
N.add_ring(Rq2B1)
N.add_ring(Rq20B)
N.add_ring(Rq200)
N.add_ring(Rq201)
N.add_ring(Rq21B)
N.add_ring(Rq210)
N.add_ring(Rq211)
N.add_ring(Rq2bisBB)
N.add_ring(Rq2bisB0)
N.add_ring(Rq2bisB1)
N.add_ring(Rq2bis0B)
N.add_ring(Rq2bis00)
N.add_ring(Rq2bis01)
N.add_ring(Rq2bis1B)
N.add_ring(Rq2bis10)
N.add_ring(Rq2bis11)

# states accept and reject (final)
N.add_ring(Raccept)
N.add_ring(Rreject)


# **************************** #
# Input-to-Program connections #
# **************************** #

# Cell tic2 cmakes the computation start from initial state.

w_input2initial = 0.8
N.cell2ring_connect(tic2, RiBB, w_input2initial) # connection: start to initial state
N.cell2ring_connect(tic2, Ri0B, w_input2initial) # connection: start to initial state
N.cell2ring_connect(tic2, Ri1B, w_input2initial) # connection: start to initial state

# Cells tic2 initiates every computational state.

# Uses smaller weights, since these rings also receive connections from other program rings.
w_input2noninitial = 0.5
w_input2final = 0.7

# Excitatory connections from cell tic2 to state rings ("one shot" by definition)

# to q0 and q0bis
N.cell2ring_connect(tic2, Rq0BB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq0bisBB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq00B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq0bis0B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq01B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq0bis1B, w_input2noninitial)

# to q1 and q1bis
N.cell2ring_connect(tic2, Rq1BB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bisBB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1B0, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bisB0, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1B1, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bisB1, w_input2noninitial)
N.cell2ring_connect(tic2, Rq10B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis0B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq100, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis00, w_input2noninitial)
N.cell2ring_connect(tic2, Rq101, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis01, w_input2noninitial)
N.cell2ring_connect(tic2, Rq11B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis1B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq110, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis10, w_input2noninitial)
N.cell2ring_connect(tic2, Rq111, w_input2noninitial)
N.cell2ring_connect(tic2, Rq1bis11, w_input2noninitial)

# to q2 and q2bis
N.cell2ring_connect(tic2, Rq2BB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bisBB, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2B0, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bisB0, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2B1, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bisB1, w_input2noninitial)
N.cell2ring_connect(tic2, Rq20B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis0B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq200, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis00, w_input2noninitial)
N.cell2ring_connect(tic2, Rq201, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis01, w_input2noninitial)
N.cell2ring_connect(tic2, Rq21B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis1B, w_input2noninitial)
N.cell2ring_connect(tic2, Rq210, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis10, w_input2noninitial)
N.cell2ring_connect(tic2, Rq211, w_input2noninitial)
N.cell2ring_connect(tic2, Rq2bis11, w_input2noninitial)

# to q_accept and q_reject
N.cell2ring_connect(tic2, Raccept, w_input2final)
N.cell2ring_connect(tic2, Rreject, w_input2final)


# ************************** #
# Input-to-Cache connections #
# ************************** #

# Excitatory connections from cell tic1 to symbol cache rings ("one shot" by definition).
# Cell tic1 updates the cache, i.e., copies current read symbols into the cache.
# Note that the cache rings receive:
# 	- w_input2cache
#	- excitatory connections from position rings
# 	- excitatory connections from symbol rings

# RULE 0
# (i)  w_input2cache + excitatory connections from position rings and symbol rings > theta
# (ii) every combination where one of this weight is missing < theta
# Here, one  has: exc2 + exc2 + w_input2cache = 0.3 + 0.3 + 0.4 = 1

w_input2cache = 0.4 

for i in range(tape_length):

	# tic1 to cache1
	N.cell2ring_connect(tic1, tape_CB1[i], w_input2cache)
	N.cell2ring_connect(tic1, tape_C01[i], w_input2cache)
	N.cell2ring_connect(tic1, tape_C11[i], w_input2cache)

	# tic1 to cache2
	N.cell2ring_connect(tic1, tape_CB2[i], w_input2cache)
	N.cell2ring_connect(tic1, tape_C02[i], w_input2cache)
	N.cell2ring_connect(tic1, tape_C12[i], w_input2cache)


# ************************************************* #
# Input-to-Symbols & Input-to-Positions connections #
# ************************************************* #

# Excitatory connections from cell tic3 to symbol and position rings ("one shot" by definition).

w_input2symbpos = 0.4

for i in range(tape_length):

	# tic3 to symbol_tape1
	N.cell2ring_connect(tic3, tape_B1[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_01[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_11[i], w_input2symbpos)

	# tic3 to position_tape1
	N.cell2ring_connect(tic3, tape_L1[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_R1[i], w_input2symbpos)
	
	# tic3 to symbol_tape2
	N.cell2ring_connect(tic3, tape_B2[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_02[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_12[i], w_input2symbpos)
	
	# tic3 to position_tape2
	N.cell2ring_connect(tic3, tape_L2[i], w_input2symbpos)
	N.cell2ring_connect(tic3, tape_R2[i], w_input2symbpos)


# **************************** #
# Cache-to-Program connections #
# **************************** #

# Permanent excitatory connections.

# 1. TO INITIAL STATES
# Note that the initial states' rings receive:
# 	- w_input2initial
#	- w_cache2program (tape 1)
# 	- w_cache2program (tape 2)
# RULE 1
# (i)  w_input2initial + w_cache2program (tape 1) + w_cache2program (tape 2) > theta
# (ii) every combination where one of this weight is missing < theta

w_cache2program1 = 0.1

# CB1 to RiBB
N.ring2ring_connectE(tape_CB1[0], RiBB, w_cache2program1)
# CB2 to RiBB
N.ring2ring_connectE(tape_CB2[0], RiBB, w_cache2program1)

# C01 to Ri0B
N.ring2ring_connectE(tape_C01[0], Ri0B, w_cache2program1)
# CB2 to Ri0B
N.ring2ring_connectE(tape_CB2[0], Ri0B, w_cache2program1)

# C11 to Ri1B
N.ring2ring_connectE(tape_C11[0], Ri1B, w_cache2program1)
# CB2 to Ri1B
N.ring2ring_connectE(tape_CB2[0], Ri1B, w_cache2program1)

# 2. TO NON-INITIAL STATES
# Note that non-initial states' rings receive:
# 	- w_input2noninitial
#	- w_cache2program (tape 1)
# 	- w_cache2program (tape 2)
# 	- w_program2program (cf. next sections)
# RULE 2 
# (i)  w_input2noninitial + w_cache2program (tape 1) + 
# 	   w_cache2program (tape 2) + w_program2program > theta
# (ii) every combination where one of this weight is missing < theta

w_cache2program2 = 0.1

for i in range(tape_length):

	# cache 1 to q0 and q0bis
	N.ring2ring_connectE(tape_CB1[i], Rq0BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq0bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq00B, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq0bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq01B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq0bis1B, w_cache2program2)

	# cache 2 to q0 and q0bis
	N.ring2ring_connectE(tape_CB2[i], Rq0BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq0bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq00B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq0bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq01B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq0bis1B, w_cache2program2)

	# cache 1 to q1 and q1bis
	N.ring2ring_connectE(tape_CB1[i], Rq1BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq1bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq1B0, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq1bisB0, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq1B1, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq1bisB1, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq10B, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq1bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq100, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq1bis00, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq101, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq1bis01, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq11B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq1bis1B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq110, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq1bis10, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq111, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq1bis11, w_cache2program2)

	# cache 2 to q1 and q1bis
	N.ring2ring_connectE(tape_CB2[i], Rq1BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq1bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq1B0, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq1bisB0, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq1B1, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq1bisB1, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq10B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq1bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq100, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq1bis00, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq101, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq1bis01, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq11B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq1bis1B, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq110, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq1bis10, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq111, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq1bis11, w_cache2program2)

	# cache 1 to q2 and q2bis
	N.ring2ring_connectE(tape_CB1[i], Rq2BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq2bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq2B0, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq2bisB0, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq2B1, w_cache2program2)
	N.ring2ring_connectE(tape_CB1[i], Rq2bisB1, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq20B, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq2bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq200, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq2bis00, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq201, w_cache2program2)
	N.ring2ring_connectE(tape_C01[i], Rq2bis01, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq21B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq2bis1B, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq210, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq2bis10, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq211, w_cache2program2)
	N.ring2ring_connectE(tape_C11[i], Rq2bis11, w_cache2program2)

	# cache 2 to q2 and q2bis
	N.ring2ring_connectE(tape_CB2[i], Rq2BB, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq2bisBB, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq2B0, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq2bisB0, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq2B1, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq2bisB1, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq20B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq2bis0B, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq200, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq2bis00, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq201, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq2bis01, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq21B, w_cache2program2)
	N.ring2ring_connectE(tape_CB2[i], Rq2bis1B, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq210, w_cache2program2)
	N.ring2ring_connectE(tape_C02[i], Rq2bis10, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq211, w_cache2program2)
	N.ring2ring_connectE(tape_C12[i], Rq2bis11, w_cache2program2)


# ******************* #
# Program connections #
# ******************* #

# Instructions of the Turing machines (cf. 0n1n0n.py)
# instructions =[
# (("initial", ("B", "B")), ("accept", ("B", "B"), ("S", "S"))),
# (("initial", ("0", "B")), ("q0", ("0", "B"), ("S", "S"))),
# (("initial", ("1", "B")), ("reject", ("1", "B"), ("S", "S"))),
# #
# #
# (("q0", ("B", "B")), ("reject", ("B", "B"), ("S", "S"))),
# (("q0bis", ("B", "B")), ("reject", ("B", "B"), ("S", "S"))),
# #
# (("q0", ("0", "B")), ("q0bis", ("0", "0"), ("R", "R"))),
# (("q0bis", ("0", "B")), ("q0", ("0", "0"), ("R", "R"))),
# #
# (("q0", ("1", "B")), ("q1", ("1", "B"), ("S", "L"))),
# (("q0bis", ("1", "B")), ("q1", ("1", "B"), ("S", "L"))),
# #
# #
# (("q1", ("B", "B")), ("reject", ("B", "B"), ("S", "S"))),
# (("q1bis", ("B", "B")), ("reject", ("B", "B"), ("S", "S"))),
# #
# (("q1", ("B", "0")), ("reject", ("B", "0"), ("S", "S"))),
# (("q1bis", ("B", "0")), ("reject", ("B", "0"), ("S", "S"))),
# #
# (("q1", ("B", "1")), ("reject", ("B", "1"), ("S", "S"))),
# (("q1bis", ("B", "1")), ("reject", ("B", "1"), ("S", "S"))),
# #
# (("q1", ("0", "B")), ("reject", ("0", "B"), ("S", "S"))),
# (("q1bis", ("0", "B")), ("reject", ("0", "B"), ("S", "S"))),
# #
# (("q1", ("0", "0")), ("reject", ("0", "0"), ("S", "S"))),
# (("q1bis", ("0", "0")), ("reject", ("0", "0"), ("S", "S"))),
# #
# (("q1", ("0", "1")), ("q2", ("0", "0"), ("R", "R"))),
# (("q1bis", ("0", "1")), ("q2", ("0", "0"), ("R", "R"))),
# #
# (("q1", ("1", "B")), ("reject", ("1", "B"), ("S", "S"))),
# (("q1bis", ("1", "B")), ("reject", ("1", "B"), ("S", "S"))),
# #
# (("q1", ("1", "0")), ("q1bis", ("1", "1"), ("R", "L"))),
# (("q1bis", ("1", "0")), ("q1", ("1", "1"), ("R", "L"))),
# #
# (("q1", ("1", "1")), ("reject", ("1", "1"), ("S", "S"))),
# (("q1bis", ("1", "1")), ("reject", ("1", "1"), ("S", "S"))),
# #
# #
# (("q2", ("B", "B")), ("accept", ("B", "B"), ("S", "S"))),
# (("q2bis", ("B", "B")), ("accept", ("B", "B"), ("S", "S"))),
# #
# (("q2", ("B", "0")), ("reject", ("B", "0"), ("S", "S"))),
# (("q2bis", ("B", "0")), ("reject", ("B", "0"), ("S", "S"))),
# #
# (("q2", ("B", "1")), ("reject", ("B", "1"), ("S", "S"))),
# (("q2bis", ("B", "1")), ("reject", ("B", "1"), ("S", "S"))),
# #
# (("q2", ("0", "B")), ("reject", ("0", "B"), ("S", "S"))),
# (("q2bis", ("0", "B")), ("reject", ("0", "B"), ("S", "S"))),
# #
# (("q2", ("0", "0")), ("reject", ("0", "0"), ("S", "S"))),
# (("q2bis", ("0", "0")), ("reject", ("0", "0"), ("S", "S"))),
# #
# (("q2", ("0", "1")), ("q2bis", ("0", "0"), ("R", "R"))),
# (("q2bis", ("0", "1")), ("q2", ("0", "0"), ("R", "R"))),
# #
# (("q2", ("1", "B")), ("reject", ("1", "B"), ("S", "S"))),
# (("q2bis", ("1", "B")), ("reject", ("1", "B"), ("S", "S"))),
# #
# (("q2", ("1", "0")), ("reject", ("1", "0"), ("S", "S"))),
# (("q2bis", ("1", "0")), ("reject", ("1", "0"), ("S", "S"))),
# #
# (("q2", ("1", "1")), ("reject", ("1", "1"), ("S", "S"))),
# (("q2bis", ("1", "1")), ("reject", ("1", "1"), ("S", "S"))),
# #
# ]

w_program2program = 0.3		# cf. RULE 2 for the setting of this weight
w_program2symbol = 0.2	 	# program ring is activated => write symbols
w_program2position = 0.25 	# program ring is activated => move heads
w_inh = -10.0 				# inhibitory weights

# transition
N.ring2ring_connectE(RiBB, Raccept, w_program2program)
N.ring2ring_connectI(Raccept, RiBB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Ri0B, Rq0BB, w_program2program)
N.ring2ring_connectI(Rq0BB, Ri0B, w_inh)
N.ring2ring_connectE(Ri0B, Rq00B, w_program2program)
N.ring2ring_connectI(Rq00B, Ri0B, w_inh)
N.ring2ring_connectE(Ri0B, Rq01B, w_program2program)
N.ring2ring_connectI(Rq01B, Ri0B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Ri1B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Ri1B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq0BB, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq0BB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq0bisBB, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq0bisBB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq00B, Rq0bisBB, w_program2program)
N.ring2ring_connectI(Rq0bisBB, Rq00B, w_inh)
N.ring2ring_connectE(Rq00B, Rq0bis0B, w_program2program)
N.ring2ring_connectI(Rq0bis0B, Rq00B, w_inh)
N.ring2ring_connectE(Rq00B, Rq0bis1B, w_program2program)
N.ring2ring_connectI(Rq0bis1B, Rq00B, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq00B, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq00B, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq00B, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq00B, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq0bis0B, Rq0BB, w_program2program)
N.ring2ring_connectI(Rq0BB, Rq0bis0B, w_inh)
N.ring2ring_connectE(Rq0bis0B, Rq00B, w_program2program)
N.ring2ring_connectI(Rq00B, Rq0bis0B, w_inh)
N.ring2ring_connectE(Rq0bis0B, Rq01B, w_program2program)
N.ring2ring_connectI(Rq01B, Rq0bis0B, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq0bis0B, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq0bis0B, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq0bis0B, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq0bis0B, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq01B, Rq1BB, w_program2program)
N.ring2ring_connectI(Rq1BB, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq1B0, w_program2program)
N.ring2ring_connectI(Rq1B0, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq1B1, w_program2program)
N.ring2ring_connectI(Rq1B1, Rq01B, w_inh)

N.ring2ring_connectE(Rq01B, Rq10B, w_program2program)
N.ring2ring_connectI(Rq10B, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq100, w_program2program)
N.ring2ring_connectI(Rq100, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq101, w_program2program)
N.ring2ring_connectI(Rq101, Rq01B, w_inh)

N.ring2ring_connectE(Rq01B, Rq11B, w_program2program)
N.ring2ring_connectI(Rq11B, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq110, w_program2program)
N.ring2ring_connectI(Rq110, Rq01B, w_inh)
N.ring2ring_connectE(Rq01B, Rq111, w_program2program)
N.ring2ring_connectI(Rq111, Rq01B, w_inh)
# no writing
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq01B, tape_L2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq0bis1B, Rq1BB, w_program2program)
N.ring2ring_connectI(Rq1BB, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq1B0, w_program2program)
N.ring2ring_connectI(Rq1B0, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq1B1, w_program2program)
N.ring2ring_connectI(Rq1B1, Rq0bis1B, w_inh)

N.ring2ring_connectE(Rq0bis1B, Rq10B, w_program2program)
N.ring2ring_connectI(Rq10B, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq100, w_program2program)
N.ring2ring_connectI(Rq100, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq101, w_program2program)
N.ring2ring_connectI(Rq101, Rq0bis1B, w_inh)

N.ring2ring_connectE(Rq0bis1B, Rq11B, w_program2program)
N.ring2ring_connectI(Rq11B, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq110, w_program2program)
N.ring2ring_connectI(Rq110, Rq0bis1B, w_inh)
N.ring2ring_connectE(Rq0bis1B, Rq111, w_program2program)
N.ring2ring_connectI(Rq111, Rq0bis1B, w_inh)
# no writing
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq0bis1B, tape_L2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq1BB, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1BB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bisBB, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bisBB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1B0, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1B0, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bisB0, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bisB0, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1B1, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1B1, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bisB1, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bisB1, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq10B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq10B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bis0B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bis0B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq100, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq100, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bis00, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bis00, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq101, Rq2BB, w_program2program)
N.ring2ring_connectI(Rq2BB, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq2B0, w_program2program)
N.ring2ring_connectI(Rq2B0, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq2B1, w_program2program)
N.ring2ring_connectI(Rq2B1, Rq101, w_inh)

N.ring2ring_connectE(Rq101, Rq20B, w_program2program)
N.ring2ring_connectI(Rq20B, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq200, w_program2program)
N.ring2ring_connectI(Rq200, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq201, w_program2program)
N.ring2ring_connectI(Rq201, Rq101, w_inh)

N.ring2ring_connectE(Rq101, Rq21B, w_program2program)
N.ring2ring_connectI(Rq21B, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq210, w_program2program)
N.ring2ring_connectI(Rq210, Rq101, w_inh)
N.ring2ring_connectE(Rq101, Rq211, w_program2program)
N.ring2ring_connectI(Rq211, Rq101, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq101, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq101, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq101, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq101, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq1bis01, Rq2BB, w_program2program)
N.ring2ring_connectI(Rq2BB, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq2B0, w_program2program)
N.ring2ring_connectI(Rq2B0, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq2B1, w_program2program)
N.ring2ring_connectI(Rq2B1, Rq1bis01, w_inh)

N.ring2ring_connectE(Rq1bis01, Rq20B, w_program2program)
N.ring2ring_connectI(Rq20B, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq200, w_program2program)
N.ring2ring_connectI(Rq200, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq201, w_program2program)
N.ring2ring_connectI(Rq201, Rq1bis01, w_inh)

N.ring2ring_connectE(Rq1bis01, Rq21B, w_program2program)
N.ring2ring_connectI(Rq21B, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq210, w_program2program)
N.ring2ring_connectI(Rq210, Rq1bis01, w_inh)
N.ring2ring_connectE(Rq1bis01, Rq211, w_program2program)
N.ring2ring_connectI(Rq211, Rq1bis01, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq1bis01, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq1bis01, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq1bis01, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq1bis01, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq11B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq11B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bis1B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bis1B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq110, Rq1bisBB, w_program2program)
N.ring2ring_connectI(Rq1bisBB, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bisB0, w_program2program)
N.ring2ring_connectI(Rq1bisB0, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bisB1, w_program2program)
N.ring2ring_connectI(Rq1bisB1, Rq110, w_inh)

N.ring2ring_connectE(Rq110, Rq1bis0B, w_program2program)
N.ring2ring_connectI(Rq1bis0B, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bis00, w_program2program)
N.ring2ring_connectI(Rq1bis00, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bis01, w_program2program)
N.ring2ring_connectI(Rq1bis01, Rq110, w_inh)

N.ring2ring_connectE(Rq110, Rq1bis1B, w_program2program)
N.ring2ring_connectI(Rq1bis1B, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bis10, w_program2program)
N.ring2ring_connectI(Rq1bis10, Rq110, w_inh)
N.ring2ring_connectE(Rq110, Rq1bis11, w_program2program)
N.ring2ring_connectI(Rq1bis11, Rq110, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq110, tape_11[i], w_program2symbol)
	N.ring2ring_connectE(Rq110, tape_12[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq110, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq110, tape_L2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq1bis10, Rq1BB, w_program2program)
N.ring2ring_connectI(Rq1BB, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq1B0, w_program2program)
N.ring2ring_connectI(Rq1B0, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq1B1, w_program2program)
N.ring2ring_connectI(Rq1B1, Rq1bis10, w_inh)

N.ring2ring_connectE(Rq1bis10, Rq10B, w_program2program)
N.ring2ring_connectI(Rq10B, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq100, w_program2program)
N.ring2ring_connectI(Rq100, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq101, w_program2program)
N.ring2ring_connectI(Rq101, Rq1bis10, w_inh)

N.ring2ring_connectE(Rq1bis10, Rq11B, w_program2program)
N.ring2ring_connectI(Rq11B, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq110, w_program2program)
N.ring2ring_connectI(Rq110, Rq1bis10, w_inh)
N.ring2ring_connectE(Rq1bis10, Rq111, w_program2program)
N.ring2ring_connectI(Rq111, Rq1bis10, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq110, tape_11[i], w_program2symbol)
	N.ring2ring_connectE(Rq1bis10, tape_12[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq1bis10, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq1bis10, tape_L2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq111, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq111, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq1bis11, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq1bis11, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2BB, Raccept, w_program2program)
N.ring2ring_connectI(Raccept, Rq2BB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bisBB, Raccept, w_program2program)
N.ring2ring_connectI(Raccept, Rq2bisBB, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2B0, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2B0, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bisB0, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bisB0, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2B1, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2B1, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bisB1, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bisB1, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq20B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq20B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bis0B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bis0B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq200, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq200, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bis00, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bis00, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq201, Rq2bisBB, w_program2program)
N.ring2ring_connectI(Rq2bisBB, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bisB0, w_program2program)
N.ring2ring_connectI(Rq2bisB0, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bisB1, w_program2program)
N.ring2ring_connectI(Rq2bisB1, Rq201, w_inh)

N.ring2ring_connectE(Rq201, Rq2bis0B, w_program2program)
N.ring2ring_connectI(Rq2bis0B, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bis00, w_program2program)
N.ring2ring_connectI(Rq2bis00, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bis01, w_program2program)
N.ring2ring_connectI(Rq2bis01, Rq201, w_inh)

N.ring2ring_connectE(Rq201, Rq2bis1B, w_program2program)
N.ring2ring_connectI(Rq2bis1B, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bis10, w_program2program)
N.ring2ring_connectI(Rq2bis10, Rq201, w_inh)
N.ring2ring_connectE(Rq201, Rq2bis11, w_program2program)
N.ring2ring_connectI(Rq2bis11, Rq201, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq201, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq201, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq201, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq201, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq2bis01, Rq2BB, w_program2program)
N.ring2ring_connectI(Rq2BB, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq2B0, w_program2program)
N.ring2ring_connectI(Rq2B0, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq2B1, w_program2program)
N.ring2ring_connectI(Rq2B1, Rq2bis01, w_inh)

N.ring2ring_connectE(Rq2bis01, Rq20B, w_program2program)
N.ring2ring_connectI(Rq20B, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq200, w_program2program)
N.ring2ring_connectI(Rq200, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq201, w_program2program)
N.ring2ring_connectI(Rq201, Rq2bis01, w_inh)

N.ring2ring_connectE(Rq2bis01, Rq21B, w_program2program)
N.ring2ring_connectI(Rq21B, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq210, w_program2program)
N.ring2ring_connectI(Rq210, Rq2bis01, w_inh)
N.ring2ring_connectE(Rq2bis01, Rq211, w_program2program)
N.ring2ring_connectI(Rq211, Rq2bis01, w_inh)
# writing: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(0, tape_length):
#	N.ring2ring_connectE(Rq2bis01, tape_01[i], w_program2symbol)
	N.ring2ring_connectE(Rq2bis01, tape_02[i], w_program2symbol)
# moving: "one shot excitation (i.e., ring2ring_connectE)"
for i in range(tape_length):
	N.ring2ring_connectE(Rq2bis01, tape_R1[i], w_program2position)
	N.ring2ring_connectE(Rq2bis01, tape_R2[i], w_program2position)

# transition
N.ring2ring_connectE(Rq21B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq21B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bis1B, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bis1B, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq210, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq210, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bis10, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bis10, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq211, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq211, w_inh)
# no writing
# no moving

# transition
N.ring2ring_connectE(Rq2bis11, Rreject, w_program2program)
N.ring2ring_connectI(Rreject, Rq2bis11, w_inh)
# no writing
# no moving


# ********** #
# Simulation #
# ********** #

print("indices *position* tape L1")
print(N.nodes.index(tape_L1[0].nodes[0]))
print(N.nodes.index(tape_L1[-1].nodes[-1]))
print("indices *position* tape R1")
print(N.nodes.index(tape_R1[0].nodes[0]))
print(N.nodes.index(tape_R1[-1].nodes[-1]))
print("indices *symbol* tape B1")
print(N.nodes.index(tape_B1[0].nodes[0]))
print(N.nodes.index(tape_B1[-1].nodes[-1]))
print("indices *symbol* tape 01")
print(N.nodes.index(tape_01[0].nodes[0]))
print(N.nodes.index(tape_01[-1].nodes[-1]))
print("indices *symbol* tape 11")
print(N.nodes.index(tape_11[0].nodes[0]))
print(N.nodes.index(tape_11[-1].nodes[-1]))
print("indices *cache* tape CB1")
print(N.nodes.index(tape_CB1[0].nodes[0]))
print(N.nodes.index(tape_CB1[-1].nodes[-1]))
print("indices *cache* tape C01")
print(N.nodes.index(tape_C01[0].nodes[0]))
print(N.nodes.index(tape_C01[-1].nodes[-1]))
print("indices *cache* tape C11")
print(N.nodes.index(tape_C11[0].nodes[0]))
print(N.nodes.index(tape_C11[-1].nodes[-1]))

print("indices *position* tape L2")
print(N.nodes.index(tape_L2[0].nodes[0]))
print(N.nodes.index(tape_L2[-1].nodes[-1]))
print("indices *position* tape R2")
print(N.nodes.index(tape_R2[0].nodes[0]))
print(N.nodes.index(tape_R2[-1].nodes[-1]))
print("indices *symbol* tape B2")
print(N.nodes.index(tape_B2[0].nodes[0]))
print(N.nodes.index(tape_B2[-1].nodes[-1]))
print("indices *symbol* tape 02")
print(N.nodes.index(tape_02[0].nodes[0]))
print(N.nodes.index(tape_02[-1].nodes[-1]))
print("indices *symbol* tape 12")
print(N.nodes.index(tape_12[0].nodes[0]))
print(N.nodes.index(tape_12[-1].nodes[-1]))
print("indices *cache* tape CB2")
print(N.nodes.index(tape_CB2[0].nodes[0]))
print(N.nodes.index(tape_CB2[-1].nodes[-1]))
print("indices *cache* tape C02")
print(N.nodes.index(tape_C02[0].nodes[0]))
print(N.nodes.index(tape_C02[-1].nodes[-1]))
print("indices *cache* tape C12")
print(N.nodes.index(tape_C12[0].nodes[0]))
print(N.nodes.index(tape_C12[-1].nodes[-1]))

print("\nindices programm ring RiBB")
print(N.nodes.index(RiBB.nodes[0]))
print(N.nodes.index(RiBB.nodes[-1]))
print("indices programm ring Ri0B")
print(N.nodes.index(Ri0B.nodes[0]))
print(N.nodes.index(Ri0B.nodes[-1]))
print("indices programm ring Ri1B")
print(N.nodes.index(Ri1B.nodes[0]))
print(N.nodes.index(Ri1B.nodes[-1]))

print("\nindices programm ring Raccept")
print(N.nodes.index(Raccept.nodes[0]))
print(N.nodes.index(Raccept.nodes[-1]))
print("indices programm ring Rreject")
print(N.nodes.index(Rreject.nodes[0]))
print(N.nodes.index(Rreject.nodes[-1]))

print("NODES & CONNECTIONS")
print("number of nodes")
print(len(N.nodes))
print("number of connections")
print(len(N.edges))

# After test, all transitions are working

# Input dict U (start1, start2, tic)
U = {
	# tic0 sets the initial configuration
	0: np.array([[1], [0], [0], [0]]), \
	# alternations of tic1's, tic2's and tic3's
	10: np.array([[0], [1], [0], [0]]), \
	20: np.array([[0], [0], [1], [0]]), \
	23: np.array([[0], [0], [0], [1]]), \
	#
	30: np.array([[0], [1], [0], [0]]), \
	40: np.array([[0], [0], [1], [0]]), \
	43: np.array([[0], [0], [0], [1]]), \
	#
	50: np.array([[0], [1], [0], [0]]), \
	60: np.array([[0], [0], [1], [0]]), \
	63: np.array([[0], [0], [0], [1]]), \
	#
	70: np.array([[0], [1], [0], [0]]), \
	80: np.array([[0], [0], [1], [0]]), \
	83: np.array([[0], [0], [0], [1]]), \
	#
	90: np.array([[0], [1], [0], [0]]), \
	100: np.array([[0], [0], [1], [0]]), \
	103: np.array([[0], [0], [0], [1]]), \
	#
	110: np.array([[0], [1], [0], [0]]), \
	120: np.array([[0], [0], [1], [0]]), \
	123: np.array([[0], [0], [0], [1]]), \
	#
	130: np.array([[0], [1], [0], [0]]), \
	140: np.array([[0], [0], [1], [0]]), \
	143: np.array([[0], [0], [0], [1]]), \
	#
	150: np.array([[0], [1], [0], [0]]), \
	160: np.array([[0], [0], [1], [0]]), \
	163: np.array([[0], [0], [0], [1]]), \
	#
	170: np.array([[0], [1], [0], [0]]), \
	180: np.array([[0], [0], [1], [0]]), \
	183: np.array([[0], [0], [0], [1]]), \
	#
	190: np.array([[0], [1], [0], [0]]), \
	200: np.array([[0], [0], [1], [0]]), \
	203: np.array([[0], [0], [0], [1]]), \
	#
	210: np.array([[0], [1], [0], [0]]), \
	220: np.array([[0], [0], [1], [0]]), \
	223: np.array([[0], [0], [0], [1]]), \
	#
	230: np.array([[0], [1], [0], [0]]), \
	240: np.array([[0], [0], [1], [0]]), \
	243: np.array([[0], [0], [0], [1]]), \
	#
	250: np.array([[0], [1], [0], [0]]), \
	260: np.array([[0], [0], [1], [0]]), \
	263: np.array([[0], [0], [0], [1]]), \
	#
	270: np.array([[0], [1], [0], [0]]), \
	280: np.array([[0], [0], [1], [0]]), \
	283: np.array([[0], [0], [0], [1]]), \
	#
	290: np.array([[0], [1], [0], [0]]), \
	300: np.array([[0], [0], [1], [0]]), \
	303: np.array([[0], [0], [0], [1]]), \
	}

cwd = os.getcwd()

N.write_csv(filepath = os.path.join(cwd, 'data'))

S = N.simulate(U, nb_epochs=300)

np.savetxt("data/raster.csv", S, delimiter = ",")
# pickle.dump( S, open( os.path.join(cwd, "simulation_dumped.p"), "wb" ) )
