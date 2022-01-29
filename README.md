# SynfireRings

**Turing computation with neural networks composed of synfire rings**

This little GiHub repository contains the code to reproduce the results of the paper submitted to IJCNN 2022.

The program that implements neural networks composed of synfire rings is located in the ``/core/`` folder.  This program can be executed with ``python 3.7``or higher.

In oder to reproduce the results and figures of the paper, execute the following steps:

1. Compile the file ``simulate.py`` (with python 3.7 or higher). This will simulate a boolean neural network composed of synfire rings that mimics the behavior of a 2-tape Turing machine recognizing the language ${ 0^n1^n0^n : n \geq 0 }$. This step generates the following files:
	- ``data/node.csv``
	- ``data/edges.csv``
	- ``data/raster.csv``

2. Execute the notebook ``raster_plot.ipynb`` to create the pdf figure ``raster.pdf`` that corresponds to the raster plot of the whole network.

3. Compile the file ``simulate_ring.py`` (with python 3.7 or higher). This will generate the following file:
	- ``data/raster_ring.csv``

4. Execute the notebook ``raster_plot.ipynb`` to create the pdf figure ``raster_ring.pdf`` that corresponds to the raster plot of a single ring.

5. Run ``movie_snapshot.R`` to create the set of images that constitute the movie. This process takes a long time. It will generate 300 png files in the folder ``/data/snapshots/``

6. Go to the folder ``/data/snapshots/`` and execute the command below to create the movie. Here the movie ``movie.m4v``has already been created.

        ffmpeg -r 3 -start_number 1 -i plot%d.png -s 1080x1080 -ar 44100 -async 44100 -r 29.970 -ac 2 movie.m4v
