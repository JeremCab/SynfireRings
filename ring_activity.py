# *********************** #
# Author: Jeremie Cabessa #
# Date: 26 December 2021  #
# *********************** #


# ********************************************************* #
# Implementation of one input cell and one synfire rings 	#
# ********************************************************* #


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

C = Cell()
N.add_cell(C)

R = Ring(width=3, length=5, name = "ring")
N.add_ring(R)

N.cell2ring_connect_no_inhibitory_system(C, R, weight=1.1)


# ********** #
# Simulation #
# ********** #

U = {0: np.array([[1]])} # C spikes at t=0
S = N.simulate(U, nb_epochs=25)
np.savetxt("data/raster_ring.csv", S, delimiter = ",")
