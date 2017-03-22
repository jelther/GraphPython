# see documentation at : https://networkx.github.io/
import networkx as nx

# see documentation at: https://docs.python.org/2/library/timeit.html
import timeit

# see documentation at: https://docs.python.org/2/library/itertools.html
import itertools

# see documentation at: https://docs.python.org/2/library/sys.html
import sys

def getWeight(k):
	return k[2]

def return_minimum_edge_fringe(fringe):
	ordered_edges_by_weight = sorted(fringe.edges(data='weight'),key=getWeight)
	return ordered_edges_by_weight[0]

def build_fringe(g,mst):

	fringe = nx.Graph()

	fringe_nodes = set(nx.nodes(g)).difference(set(nx.nodes(mst)))

	fringe.add_nodes_from(set(nx.nodes(g)).difference(set(nx.nodes(mst))))
	
	for node in itertools.product(nx.nodes(mst),nx.nodes(fringe)):        
		if g.has_edge(*node) or g.has_edge(*tuple(reversed(node))):
			fringe.add_edge(*node,weight=g.get_edge_data(*node)['weight'])            

	for i in nx.nodes(fringe):
		if fringe.degree(i) == 0:
			fringe.remove_node(i)
		  
	return fringe


def prim(G,start_node):

	global qty_of_iterations

	total_cost = 0

	mst = nx.Graph()
	mst.add_node(start_node)

	while (nx.number_of_nodes(mst) < nx.number_of_nodes(G)):

		fringe = build_fringe(G,mst)
		min_edge = return_minimum_edge_fringe(fringe)

		mst.add_edge(min_edge[0],min_edge[1],weight=getWeight(min_edge))

		total_cost += getWeight(min_edge)
		qty_of_iterations += 1

	return total_cost,mst

def print_edges(G):    
	print ""
	for i in G.edges(data='weight'):
		print "(From,To,Weight) = ",i

# dictionary containing the necessary information
data = [
	{
		'algorithm' : "prim",
		'graph_name' : "rede_italiana",
		'file' : 'redeitaliana.ncol',
		'start_node' : [1]
	},
	{
		'algorithm' : "prim",
		'graph_name' : "rede_usa",
		'file' : 'redeusa.ncol',
		'start_node' : [1]
	}
]


#main loop through data dictionary defined above
for d in data:   

	G = nx.read_weighted_edgelist(d['file'],nodetype=int)

	f = file( d['algorithm'] + "_" + d['graph_name'] + '.txt', 'w')
	sys.stdout = f

	for s in d['start_node']:

		#global variables        
		time_consumed = 0
		qty_of_iterations = 0
		
		print "************************************"
		print "Prim's Algorithm"
		print "************************************"
		print "Graph Name: ",d['graph_name']
		print "Start Node: ",s        
		print ""

		#run the algorithm
		time_consumed = 0
		start_time = 0
		start_time = timeit.default_timer()
		total_cost,mst = prim(G,s)
		time_consumed = timeit.default_timer() - start_time

		print "|Original Algorithm|"
		
		print "Nodes of MST is: ",mst.nodes()
		print "Edges of MST is: ",
		print_edges(mst)

		print "Total Cost is: ",total_cost
		print "Time Elapsed (in seconds): ", time_consumed
		print "Number of Iterations: ",qty_of_iterations
		print ""

		#run the networkx algorithm
		time_consumed = 0
		start_time = 0
		start_time = timeit.default_timer()
		T = nx.prim_mst(G)        
		time_consumed = timeit.default_timer() - start_time        
		
		print "|Networkx Algorithm|"

		print "Nodes of MST is: ",T.nodes()
		print "Edges of MST is: "
		print_edges(T)

		total_cost = 0
		for edge in T.edges(data='weight'):
			total_cost += getWeight(edge)

		print "Total Cost is: ",total_cost
		print "Time Elapsed (in seconds): ", time_consumed        
		print ""

	f.close()