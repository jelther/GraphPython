import os

# see documentation at : https://networkx.github.io/
import networkx as nx

# see documentation at: https://docs.python.org/2/library/timeit.html
import timeit

# see documentation at: https://docs.python.org/2/library/sys.html
import sys

#gets the minimum node based on the visited nodes
def select_minimum_node(dist,visited_nodes):
	minimum_value = float("inf")

	minimum_node = 0

	for i in visited_nodes:
		if (visited_nodes[i] == 0):
			if (dist[i] < minimum_value):
				minimum_node = i
				minimum_value = dist[i]

	return minimum_node

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


#check if unvisited nodes still exist
def unvisited_nodes_exist(visited_nodes):
	for i in visited_nodes:
		if (visited_nodes[i] == 0):
			return True
	return False

#build list to show the path to reach the end node
def get_minimum_path(prev,end_node):
	min_path = []

	u = end_node
	while prev[u] is not None:
		min_path = [u] + min_path
		u = prev[u]

	min_path = [u] + min_path
	return min_path

# dijkstra algorithm
def dijkstra(G,prev,dist,visited_nodes,start_node,end_node):

	global time_consumed
	global qty_of_iterations

	#the minimum node is the start node
	minimum_node = start_node

	start_time = timeit.default_timer()

	while (unvisited_nodes_exist(visited_nodes)):
		minimum_node = select_minimum_node(dist,visited_nodes)

		if minimum_node == end_node:
			break

		for edge in G.edges(minimum_node,data='weight'):
			relax_edge(prev,dist,edge)

		visited_nodes[minimum_node] = 1
		qty_of_iterations = qty_of_iterations + 1
	time_consumed = timeit.default_timer() - start_time

# dictionary containing the necessary information
data = [
	{
		'algorithm' : "dijkstra",
		'graph_name' : "rede_italiana",
		'file' : 'redeitaliana.ncol',
		'start_node' : [1],
		'end_node' : [7,14,21]
	},
	{
		'algorithm' : "dijkstra",
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
			f = file( pasta + d['algorithm'] + "_" + d['graph_name'] + "_" + str(s) + "_" + str(e) + ".txt", 'w' )
			sys.stdout = f

			print "************************************"
			print "Dijkstra's Algorithm"

			#global variables
			qty_of_relaxations = 0
			qty_of_iterations = 0
			time_consumed = 0

			prev = {}
			dist = {}
			visited_nodes = {}
			for i in G.nodes():
				#stores the last node between s and v
				prev[i] = None
				#stores the minimun path length between s and v.
				dist[i] = float('inf')
				#visited nodes : 1 is visited and 0 is unvisited
				visited_nodes[i] = 0

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
			dijkstra(G,prev,dist,visited_nodes,s,e)
			time_consumed = timeit.default_timer() - start_time

			print "|Original Algorithm|"
			print "Shortest Path from ",s," to ",e," is: ",get_minimum_path(prev,e)
			print "Previous Node before ",e," is : ",prev[e]
			print "Shortest Path Length from ",s," to ",e," is: ",dist[e]
			print "Time Elapsed (in seconds): ", time_consumed
			print "Number of Iterations: ",qty_of_iterations
			print "Number of Relaxations: ",qty_of_relaxations
			print ""

			#run networkx algorithm
			time_consumed = 0
			start_time = 0
			start_time = timeit.default_timer()
			distance,path = nx.single_source_dijkstra(G, s)
			time_consumed = timeit.default_timer() - start_time

			print "|Networkx Algorithm|"
			print "Shortest Path from ",s," to ",e," is : ",path[e]
			print "Previous Node before ",e," is : ",path[e][len(path[e]) - 2]
			print "Shortest Path Length from ",s," to ",e," is : ",distance[e]
			print "Time Elapsed (in seconds): ", time_consumed
			print ""

			f.close()
