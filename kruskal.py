import os

# see documentation at : https://networkx.github.io/
import networkx as nx

# see documentation at: https://docs.python.org/2/library/timeit.html
import timeit

# see documentation at: https://docs.python.org/2/library/sys.html
import sys

def isCyclicUtil(G, v, visited, parent):

    # Mark the current node as visited
    visited[v] = True

    # Search for all the vertices adjacent to this vertex    
    for edge in G.edges(v):
        i = edge[1]

        # If the node is not visited then recurse on it
        if visited[i] == False:
            if (isCyclicUtil(G, i, visited, v)):
                return True
        # If an adjacent vertex is visited and not parent of current vertex, is a cycle!
        elif parent != i:
            return True

    return False


def isCyclic(G):

    # Mark all the vertices as not visited
    visited = {}
    for i in G.nodes():
        visited[i] = False

    # Call the recursive helper function to detect cycle in different DFS trees    
    for i in G.nodes():
        if visited[i] == False:  # Don't recur for u if it is already visited
            if (isCyclicUtil(G, i, visited, -1)) == True:
                return True

    return False


def build_ordered_edges(g):
    return sorted(G.edges(data=True), key=lambda (a, b, data): data['weight'])

def kruskal(G,s):

    global qty_of_iterations

    mst = nx.Graph()

    ordered_edges = build_ordered_edges(G)

    total_cost = 0

    for candidate in ordered_edges:

        u = candidate[0]
        v = candidate[1]
        weight = candidate[2]['weight']

        mst.add_edge(u, v, weight=weight)      

        if (isCyclic(mst)):
            mst.remove_edge(u,v)
            total_cost -= weight
        
        total_cost += weight

        qty_of_iterations += 1
            

    return total_cost,mst

def print_edges(G):    
    print ""
    for i in G.edges(data='weight'):
        print "(From,To,Weight) = ",i

# dictionary containing the necessary information
data = [
    {
        'algorithm' : "kruskal",
        'graph_name' : "rede_italiana",
        'file' : 'redeitaliana.ncol',
        'start_node' : [1]
    },
    {
        'algorithm' : "kruskal",
        'graph_name' : "rede_usa",
        'file' : 'redeusa.ncol',
        'start_node' : [1]
    }
]


pasta = "output/"
if not os.path.exists(pasta):
    os.makedirs(pasta)

#main loop through data dictionary defined above
for d in data:   

    G = nx.read_weighted_edgelist(d['file'],nodetype=int)

    f = file( pasta + d['algorithm'] + "_" + d['graph_name'] + '.txt', 'w')
    sys.stdout = f

    for s in d['start_node']:

        #global variables
        time_consumed = 0
        qty_of_iterations = 0

        print "************************************"
        print "Kruskal's Algorithm"
        print "************************************"
        print "Graph Name: ",d['graph_name']
        print "Start Node: ",s        
        print ""

        #run the algorithm
        time_consumed = 0
        start_time = 0
        start_time = timeit.default_timer()
        total_cost,mst = kruskal(G,s)
        time_consumed = timeit.default_timer() - start_time

        print "|Original Algorithm|"
        
        print "Nodes of MST is: ",mst.nodes()
        print "Edges of MST is: "
        print_edges(mst)
        print "Total Cost is: ",total_cost
        print "Time Elapsed (in seconds): ", time_consumed
        print "Number of Iterations: ",qty_of_iterations
        print ""


        #run the networkx algorithm
        time_consumed = 0
        start_time = 0
        start_time = timeit.default_timer()
        #it's kruskal algorithm
        T = nx.minimum_spanning_tree(G)
        time_consumed = timeit.default_timer() - start_time        
        
        print "|Networkx Algorithm|"

        print "Nodes of MST is: ",T.nodes()
        print "Edges of MST is: "
        print_edges(T)

        total_cost = 0
        for edge in T.edges(data='weight'):
            total_cost += edge[2]
        
        print "Total Cost is: ",total_cost
        print "Time Elapsed (in seconds): ", time_consumed        
        print "" 

    f.close()