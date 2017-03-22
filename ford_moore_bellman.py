import os

# see documentation at : https://networkx.github.io/
import networkx as nx
# see documentation at: https://docs.python.org/2/library/timeit.html
import timeit
# see documentation at: https://docs.python.org/2/library/sys.html
import sys
#relax the edge
def relax_edge(prev,dist,edge):
	global qty_of_relaxations

	u = edge[0]
	v = edge[1]
	weight = edge[2]

	if (dist[v] > dist[u] + weight):
		dist[v] = dist[u] + weight
		prev[v] = u

	qty_of_relaxations = qty_of_relaxations + 1

#build list to show the path to reach the end node
def get_minimum_path(prev,end_node):
	min_path = []

	u = end_node
	while prev[u] is not None:
		min_path = [u] + min_path
		u = prev[u]

	min_path = [u] + min_path
	return min_path

# ford_moore_bellman algorithm
def ford_moore_bellman(G,prev,dist):
	global time_consumed
	global qty_of_iterations

	for edge in G.edges(data='weight'):
		relax_edge(prev,dist,edge)
		qty_of_iterations = qty_of_iterations + 1



# dictionary containing the necessary information
data = [
	{
		'algorithm' : "ford_moore_bellman",
		'graph_name' : "rede_italiana",
		'file' : 'redeitaliana.ncol',
		'start_node' : [1],
		'end_node' : [7,14,21]
	},
	{
		'algorithm' : "ford_moore_bellman",
		'graph_name' : "rede_usa",
		'file' : 'redeusa.ncol',
		'start_node' : [1],
		'end_node' : [10,20,30,40,50,60,70]
	}
]

pasta = "output/"
if not os.path.exists(pasta):
	os.makedirs(pasta)


#main loop through data dictionary defined above
for d in data:
	G = nx.read_weighted_edgelist(d['file'],nodetype=int)

	#start node
	start_node = d['start_node']

	#ending nodes
	end_node = d['end_node']

	for s in start_node:
		for e in end_node:
			f = file( pasta + d['algorithm'] + "_" + d['graph_name'] + "_" +
			str(s) + "_" + str(e) + ".txt", 'w' )
			sys.stdout = f

			print "************************************"
			print "Ford-Moore-Bellman's Algorithm"

			#global variables
			qty_of_relaxations = 0
			qty_of_iterations = 0
			time_consumed = 0

			prev = {}
			dist = {}
			for i in G.nodes():
				#stores the last node between s and v
				prev[i] = None
				#stores the minimun path length between s and v.
				dist[i] = float('inf')

			# initial node distance is zero
			dist[s] = 0

			print "************************************"
			print "Graph Name: ",d['graph_name']
			print "Start Node: ",s
			print "End Node: ",e
			print ""

			#run the algorithm
			time_consumed = 0
			start_time = 0
			start_time = timeit.default_timer()
			ford_moore_bellman(G,prev,dist)
			time_consumed = timeit.default_timer() - start_time

			print "|Original Algorithm|"
			print "Shortest Path from ",s," to ",e," is: ",get_minimum_path(prev,e)
			print "Previous Node before ",e," is : ",prev[e]
			print "Shortest Path Length from ",s," to ",e," is:  ",dist[e]
			print "Time Elapsed (in seconds): ", time_consumed
			print "Number of Iterations: ",qty_of_iterations
			print "Number of Relaxations: ",qty_of_relaxations
			print ""

			#run networkx algorithm
			time_consumed = 0
			start_time = 0
			start_time = timeit.default_timer()
			predecessor, distance = nx.bellman_ford(G, s)
			time_consumed = timeit.default_timer() - start_time

			print "|Networkx Algorithm|"
			print "Shortest Path from ",s," to ",e," is : ",get_minimum_path(predecessor,e)
			print "Previous Node before ",e," is : ",predecessor[e]
			print "Shortest Path Length from ",s," to ",e," is : ",distance[e]
			print "Time Elapsed (in seconds): ", time_consumed
			print ""

			f.close()