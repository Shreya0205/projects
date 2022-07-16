i,
Here is the format of each of the two files:
first line: num_of_nodes, num_of_edges
for lines = num_of_nodes
  nodeid,lat,lon,<list of edges connected with this node>
for lines = num_of_edges
  edgeid,source node,destination node,flag_if_the_edge_directed(1 means
directed from source to desti, 0 means undirected so there is no
source/destination)

The beijing_adj.txt is the original road network of beijing.
Beijing_adj_large.txt is not only road, but also includes water paths,
suburbs roads.

Hope this helps. Please feel free to ask if you have further queries.

best regards,
Prithu Banerjee.