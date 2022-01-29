# ******** #
# PACKAGES #
# ******** #

# install.packages("rstudioapi")
# install.packages("igraph")
# install.packages("network")
# install.packages("sna")
# install.packages("visNetwork")
# install.packages("threejs")
# install.packages("networkD3")
# install.packages("ndtv")
# install.packages('RColorBrewer')
# install.packages('extrafont')
# install.packages("animation")
# install.packages("pdf") # TO BE INSTALLED if exists and then loaded

library(rstudioapi)
library(igraph)
library(network)
library(sna)
library(visNetwork)
library(threejs)
library(networkD3)
library(ndtv)
library('RColorBrewer')
library('extrafont')
library(animation)

#colors()  # List all color names
#grep("blue", colors(), value = T) # Colors that have "blue" in the name
#display.brewer.all() # List all palettes

# removes variables
rm(list = ls())

# set correct path
current_path <- getActiveDocumentContext()$path
current_path <- paste(dirname(current_path), "data", sep = "/")
setwd(current_path)

# creating the network object
nodes <- read.csv("nodes.csv", header = T, as.is = T)
raster <- read.csv("raster.csv", header = F, as.is = T) # dynamics of the net (RNN_simulator.py)
nodes <- cbind(nodes, raster)
edges <- read.csv("edges.csv", header = T, as.is = T)
#head(nodes)
#head(edges)
net <- graph_from_data_frame(d = edges, vertices = nodes, directed = T)

# preliminaries
weights <- sort(unique(E(net)$weight)) # vector of all weights
weight_nb <- length(unique(E(net)$weight)) # number of different weights
weight_min <- min(E(net)$weight) # min weight
weight_max <- max(E(net)$weight) # max weight

# colors of vertices (black & red) and edges (blue: inhibitory, red: excitatory)
# Add an alpha value to a colour
add.alpha <- 
  function (hex.color.list,alpha) sprintf("%s%02X",hex.color.list,floor(alpha*256))
edge_colors <- brewer.pal(weight_nb, "OrRd") # weight colors
edge_colors <- add.alpha(edge_colors, 0.3) # add transparency
#plot(x = 1:weight_nb, y = 1:weight_nb, pch = 19, cex = 15, col = edge_colors)
node_colors <- c("black", "red")

# vertices in a loop at the end (to generate al graphs)
#V(net)$color <- node_colors[V(net)$V112 + 1] # V1 column ("+1" transforms 0 and 1 into 1 and 2)
#V(net)$frame.color <- node_colors[V(net)$V112 + 1]
# Note: V(net)$V1 is the same as nodes[,3]. Hence the above code can be rewritten as:
#V(net)$color <- node_colors[nodes[,114] + 1] # V1 column ("+1" transforms 0 and 1 into 1 and 2)
#V(net)$frame.color <- node_colors[nodes[,114] + 1]
#V(net)$size <- 1
V(net)$label <- NA


# edges
#E(net)$edge.color <- edge_colors[E(net)$weight]
E(net)$color[E(net)$weight == weights[1]] <- adjustcolor("dodgerblue", alpha.f = 0.3) # inhibitory connections (same alpha)
for(i in 2:weight_nb){
  E(net)$color[E(net)$weight == weights[i]] <- edge_colors[i] # excitatory connections
}
E(net)$width <- 0.3
E(net)$arrow.size <- 0.01

# construction of the layout
# pentagone coordinates
#15 o  o  o  o  o  x  o  o  o  o  o  o  o
#14 o  o  o  o  o  o  o  o  o  o  o  o  o
#13 o  o  o  o  o  o  o  o  o  o  o  o  o
#12 o  o  x  o  o  o  o  o  x  o  o  o  o
#11 o  o  o  x  o  x  o  x  o  o  o  o  o
#10 o  o  o  o  o  o  o  o  o  o  o  o  o
#9  o  o  o  o  o  =  o  o  o  o  o  o  o
#8  o  o  o  o  o  o  o  o  o  o  o  o  o
#7  o  o  o  o  x  o  x  o  o  o  o  o  o
#6  o  o  o  o  o  o  o  o  o  o  o  o  o
#5  o  o  o  x  o  o  o  x  o  o  o  o  o
#4  o  o  o  o  o  o  o  o  o  o  o  o  o
#3  o  o  o  o  o  o  o  o  o  o  o  o  o
#2  o  o  o  o  o  o  o  o  o  o  o  o  o
#1  o  o  o  o  o  T  o  o  o  o  o  o  o
#   1  2  3  4  5  6  7  8  9  10 11 12 13
# coordinates of the pentagone
# x,y+2
# x,y+6
# x+2,y+2
# x+3,y+3
# x+1,y-2
# x+2,y-4
# x-1,y-2
# x-2,y-4
# x-2,y+1
# x-4,y+2

# coordinate matrix (i.e., layout)
ring_coord <- function(xy, width = 2, length = 5){
  x <- xy[1]
  y <- xy[2]
  coords <- matrix(nrow = 0, ncol = 2)
  coords <- rbind(coords, c(x,y+4))
  coords <- rbind(coords, c(x,y+8))
  coords <- rbind(coords, c(x+2,y+2))
  coords <- rbind(coords, c(x+4,y+3))
  coords <- rbind(coords, c(x+1,y-2))
  coords <- rbind(coords, c(x+3,y-4))
  coords <- rbind(coords, c(x-1,y-2))
  coords <- rbind(coords, c(x-3,y-4))
  coords <- rbind(coords, c(x-2,y+2))
  coords <- rbind(coords, c(x-4,y+3))
  coords <- rbind(coords, c(x,y-8)) # inhibitory cell
  return(coords)
}

# rings' names in the way they appear in the network's construction
ring_names1 <- unique(V(net)$ring_name) # ring names

# desired net's architecture
# "start"    "tic1"  "tic2"   "tic3"
# "RiBB"      "Ri0B"    "Ri1B"
# "Rq0BB"   "Rq0bisBB"  "Rq00B"   "Rq0bis0B"  "Rq01B" "Rq0bis1B"
# "Rq1BB"   "Rq1bisBB"  "Rq1B0"   "Rq1bisB0"  "Rq1B1" "Rq1bisB1" "Rq10B"  "Rq1bis0B"  "Rq100" "Rq1bis00"  "Rq101" "Rq1bis01"  "Rq11B" "Rq1bis1B"  "Rq110" "Rq1bis10"  "Rq111" "Rq1bis11"
# "Rq2BB"   "Rq2bisBB"  "Rq2B0"   "Rq2bisB0"  "Rq2B1" "Rq2bisB1" "Rq20B"  "Rq2bis0B"  "Rq200" "Rq2bis00"  "Rq201" "Rq2bis01"  "Rq21B" "Rq2bis1B"  "Rq210" "Rq2bis10"  "Rq211" "Rq2bis11"
# "Raccept" "Rreject

# tape_C110 -> tape_C118
# tape_C010 -> tape_C018
# tape_CB10 -> tape_CB18

# tape_110 -> tape_118
# tape_010 -> tape_018
# tape_B10 -> tape_B18

# tape_R10 -> tape_R18
# tape_L10 -> tape_L18

# tape_C120 -> tape_C128
# tape_C020 -> tape_C028
# tape_CB20 -> tape_CB28

# tape_120 -> tape_128
# tape_020 -> tape_028
# tape_B20 -> tape_B28

# tape_R20 -> tape_R28
# tape_L20 -> tape_L28

# rings' names in the "right" order
ring_names2 = c(
list("start", "tic1", "tic2", "tic3"),
list("RiBB", "Ri0B", "Ri1B"),
list("Rq0BB", "Rq0bisBB", "Rq00B", "Rq0bis0B", "Rq01B", "Rq0bis1B"),
list("Rq1BB", "Rq1bisBB", "Rq1B0", "Rq1bisB0", "Rq1B1", "Rq1bisB1", "Rq10B", "Rq1bis0B", "Rq100", "Rq1bis00", "Rq101", "Rq1bis01", "Rq11B", "Rq1bis1B", "Rq110", "Rq1bis10", "Rq111", "Rq1bis11"),
list("Rq2BB", "Rq2bisBB", "Rq2B0", "Rq2bisB0", "Rq2B1", "Rq2bisB1", "Rq20B", "Rq2bis0B", "Rq200", "Rq2bis00", "Rq201", "Rq2bis01", "Rq21B", "Rq2bis1B", "Rq210", "Rq2bis10", "Rq211", "Rq2bis11"),
list("Raccept", "Rreject"),
as.list(paste("tape_C11", 0:9, sep="")),
as.list(paste("tape_C01", 0:9, sep="")),
as.list(paste("tape_CB1", 0:9, sep="")),
as.list(paste("tape_11", 0:9, sep="")),
as.list(paste("tape_01", 0:9, sep="")),
as.list(paste("tape_B1", 0:9, sep="")),
as.list(paste("tape_R1", 0:9, sep="")),
as.list(paste("tape_L1", 0:9, sep="")),
as.list(paste("tape_C12", 0:9, sep="")),
as.list(paste("tape_C02", 0:9, sep="")),
as.list(paste("tape_CB2", 0:9, sep="")),
as.list(paste("tape_12", 0:9, sep="")),
as.list(paste("tape_02", 0:9, sep="")),
as.list(paste("tape_B2", 0:9, sep="")),
as.list(paste("tape_R2", 0:9, sep="")),
as.list(paste("tape_L2", 0:9, sep=""))
)

# computes list of center coordinates of a "horizontal layer"
h_layer_coord <- function(xy, h_step, n = 9){
  x <- xy[1]
  y <- xy[2]
  coords <- list()
  for (i in 0:(n-1)){
    coords <- c(coords, list(c(x + i*h_step, y)))
  }
  return(coords)
}
# then use c with the lists

# small and big vertical spaces are +23 and +25 resp., from initial value of 8
net_architecture <- c(
  list(c(1,388)), list(c(2,388)), list(c(3,388)), list(c(4,388)), # 3 input cells
  h_layer_coord(c(6,467), 13, 3), # programm (add space)
  h_layer_coord(c(6,445), 13, 6),
  h_layer_coord(c(6,423), 13, 18),
  h_layer_coord(c(6,401), 13, 18),
  h_layer_coord(c(6,379), 13, 2), 
  h_layer_coord(c(6,354), 13, 10), # cache 1 (add space)
  h_layer_coord(c(6,332), 13, 10),
  h_layer_coord(c(6,310), 13, 10), 
  h_layer_coord(c(6,285), 13, 10), # symbols 1 (add space)
  h_layer_coord(c(6,263), 13, 10),
  h_layer_coord(c(6,241), 13, 10), 
  h_layer_coord(c(6,216), 13, 10), # positions 1 (add space)
  h_layer_coord(c(6,194), 13, 10), 
  h_layer_coord(c(6,169), 13, 10), # cache 2 (add space)
  h_layer_coord(c(6,147), 13, 10),
  h_layer_coord(c(6,125), 13, 10), 
  h_layer_coord(c(6,100), 13, 10), # symbols 2 (add space)
  h_layer_coord(c(6,78), 13, 10),
  h_layer_coord(c(6,56), 13, 10), 
  h_layer_coord(c(6,31), 13, 10), # positions 2 (add space)
  h_layer_coord(c(6,8), 13, 10)   
  )
 
names(net_architecture) <- ring_names2
net_architecture <- net_architecture[ring_names1] # we reorder the list according to ring_names1

# we now create the layout by assigning the rings' coordinates
layout <- matrix(nrow = 0, ncol = 2)
layout <- rbind(layout, c(-5,80)) # start
layout <- rbind(layout, c(-5,160)) # tic1
layout <- rbind(layout, c(-5,320)) # tic2
layout <- rbind(layout, c(-5,240)) # tic3
for (x in net_architecture[4:length(net_architecture)]){
  layout <- rbind(layout, ring_coord(x))
}

# controling dimensions
dim(nodes)[1] == dim(layout)[1]

# plotting the network
#dev.off()

for (i in 1:(dim(nodes)[2] - 2)){
#for (i in 1:1){ # just for test
  # nodes' colours (according to the current time step)
  j <- i + 2
  V(net)$color <- node_colors[nodes[,j] + 1] # V1 column ("+1" transforms 0 and 1 into 1 and 2)
  V(net)$frame.color <- node_colors[nodes[,j] + 1] # colours black and red for non-spiking and spiking, resp.
  V(net)$size <- nodes[,j]/2 + 1 # sizes 1 and 1.5 for non-spiking and spiking, resp.
  # file (generated in png)
  file_name <- paste(paste("snapshots/plot", i, sep=""), ".png", sep="")
  png(file_name, width = 18, height = 18, units = 'in', res = 600)
  #pdf(file_name, width = 10, height = 10)
  # plot
  plot(net, layout = layout)
  # legend
#  legend(x = 0.8, y = 1.05, c("program", "t1: caches", "t1: symbols", "t1: position", "t2: caches", "t2: symbols", "t2: positions"),
#        y.intersp = c(5), col = "black", pt.cex = 2, cex = 1.3, bty = "n", ncol = 1)
  dev.off()
  }


# plot 1 graph
# file
#dev.off()
#file_name <- paste(paste("plots/plot", 1, sep=""), ".pdf", sep="")
#pdf(file_name)
# plot
#plot(net, layout = layout)
#dev.off()
