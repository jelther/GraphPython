# see documentation at : https://networkx.github.io/
import networkx as nx

# see documentation at: https://docs.python.org/2/library/timeit.html
import timeit

class Element:
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank
        self.size = size


class UnionFind:
    def __init__(self, size):
        self.el = [Element(i) for i in range(size)]
        self.size = size

    def find(self, x):
        cur = x
        while cur != self.el[cur].parent:
            cur = self.el[cur].parent
        self.el[x].parent = cur
        return cur

    def union(self, x, y):
        if self.el[x].parent != x:
            x = self.find(x)
        if self.el[y].parent != y:
            y = self.find(y)
        if self.el[x].rank > self.el[y].rank:
            self.el[y].parent = x
            self.el[x].size += self.el[y].size
        else:
            self.el[x].parent = y
            self.el[y].size += self.el[x].size
            if self.el[x].rank == self.el[y].rank:
                self.el[y].rank += 1
        self.size -= 1


    def __len__(self):
        return self.size

    def size(self, x):
        return self.el[x].size

    def __iter__(self):
        for i, el in enumerate(self.el):
            if el.parent == i:
                yield i

    def __str__(self):
        return " ".join(map(str, self))

def getWeight(k):
    return k[2]

def build_ordered_edges(g):
    return sorted(G.edges(data=True), key=lambda (a, b, data): data['weight'])

def kruskal(G,s):

    global qty_of_iterations

    mst = nx.Graph()

    ordered_edges = build_ordered_edges(G)

    tracking_cycle = UnionFind(G.number_of_nodes())

    total_cost = 0

    for candidate in ordered_edges:

        u = candidate[0]
        v = candidate[1]
        weight = candidate[2]['weight']

        if (tracking_cycle.find(u - 1) != tracking_cycle.find(v - 1)):
            mst.add_edge(u, v, weight=weight)
            total_cost += weight
            qty_of_iterations += 1
            tracking_cycle.union(u - 1,v - 1)

    return total_cost,mst


# dictionary containing the necessary information
data = [
    {
        'graph_name' : "Rede Italiana",
        'file' : 'redeitaliana.ncol',
        'start_node' : [1]
    },
    {
        'graph_name' : "Rede USA",
        'file' : 'redeusa.ncol',
        'start_node' : [1]
    }
]

#main loop through data dictionary defined above
for d in data:   

    G = nx.read_weighted_edgelist(d['file'],nodetype=int)

    for s in d['start_node']:

        #global variables
        time_consumed = 0
        qty_of_iterations = 0

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
        print "Edges of MST is: ",mst.edges(data='weight')        
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
        print "Edges of MST is: ",T.edges(data='weight')    

        total_cost = 0
        for edge in T.edges(data='weight'):
            total_cost += getWeight(edge)

        print "Total Cost is: ",total_cost
        print "Time Elapsed (in seconds): ", time_consumed        
        print ""       
        

print "************************************"