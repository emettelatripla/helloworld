'''
Created on 2016. 6. 14.

@author: UNIST
'''
from directed_hypergraph import DirectedHypergraph
import random

print("something")

# Initialize an empty hypergraph
H = DirectedHypergraph()

# Add nodes 's' and 't' individually with arbitrary attributes
H.add_node('A', sink=False, source=True, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('B', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('C', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('D', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('E', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('G', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('H', sink=False, source=False, cost=0.245, avail=0.99, qual=0.7, time=0.78)
H.add_node('F', source=False, sink=True, cost=0.1, avail=0.98, qual=0.4, time=0.45)
# Add several nodes simultaneously, having the same arbitrary attributes 
#H.add_nodes(['B', 'D', 'E', 'G', 'H', 'C'], label='grey')

# Add hyperedge from {'s'} to {'x'} with a weight of 1
#H.add_hyperedge(set(['s']), set(['x']), weight=1)
# Add hyperedge from {'s'} to {'x', 'y'} with some arbitrary attributes and weight of 2
#H.add_hyperedge(set(['s']), set(['x', 'y']), {'color': 'red', 'active': True}, weight=2)
# Add several hyperedges simultaneously, having individual weights
hyperedges = [(['A'], ['B'], {'weight': 2}),
              (['A'], ['D','E'], {'weight': 100}),
              (['A'], ['G'], {'weight': 1}),
              (['B'], ['C'], {'weight': 3}),
              (['D','E'], ['F'], {'weight': 3}),
              (['E','H'], ['F'], {'weight': 3}),
              (['G'], ['H'], {'weight': 3}),
              (['H'], ['F'], {'weight': 3}),
              (['C'], ['F'], {'weight': 3})  
        ]
H.add_hyperedges(hyperedges)

H.write("hyp_file.txt", ',','\t')

source_weight = H.get_node_attribute('A', 'cost')
print(str(source_weight))
sink_weight = H.get_node_attribute('F','avail')
print(sink_weight)
#let's explore the hypergraph
print("Travelling randomly through the hypergraph....")
source_edges = H.get_successors('A')
print("One randomly chosen hyperedge: "+str(random.sample(source_edges, 1)))
for hyperedge in source_edges:
    print(H.get_hyperedge_attributes(hyperedge))
source_head = H.get_hyperedge_head('e1')
next_source_edge = random.sample(source_edges, 1)[0]
print("Weight of this random is "+str(H.get_hyperedge_attribute(next_source_edge, 'weight')))
print(next_source_edge)
source_head = H.get_hyperedge_head(next_source_edge)
for head_node in source_head:
    print("!!!! Found new node from source: "+str(head_node))    
# print(str(H.get_forward_star('E')))
# print(str(H.get_forward_star('D')))
# print(str(H.get_backward_star('E')))
# print(str(H.get_backward_star('D')))
# print(str(H.get_backward_star('A')))
# print(str(H.get_backward_star('F')))

bD = H.get_backward_star('D')
bE = H.get_backward_star('E')
bF = H.get_backward_star('F')
b = set().union(bD, bE, bF)
# print("D is: "+str(bD));
# print("E is: "+str(bE));
# print("F is: "+str(bF));
# print("Merge is: "+str(b));

def hgRandomWalk(node_set, hg:DirectedHypergraph):
    #check if current node set is sink TBC TBC
    print("--- Visiting (hyper)node: "+str(node_set))
    isSink = False
    for node in node_set:
        if hg.get_node_attribute(node,'sink'):
            isSink = True
            print("!!! STOP: SINK NODE FOUND !!!!")
    #find all hyperdges (unique set) in the forward star of the currently visited node_set
    if isSink == False: 
        hedge_set = set()
        for node in node_set:
            hedge_set = set.union(hedge_set,hg.get_forward_star(node))
        #choose randomly one of the hyperdges
        next_edge = random.sample(hedge_set, 1)[0]
        print("++ Exploring edge: "+str(next_edge))
        #call recursively the head of the chosen hyperdge (node_set)
        next_node_set = H.get_hyperedge_head(next_edge)
        hgRandomWalk(next_node_set,hg)
        
       
#This utility function simply makes the sum of the costs of all nodes 
def calculateUtility(hg:DirectedHypergraph):
    utility = 0.0
    node_set = hg.get_node_set()
    for node in node_set:
        print(str(node))
        utility = utility + hg.get_node_attribute(node,'cost')
    return utility
        
#this choice function simply picks the edge with highest weight
def pheroChoice(edge_set, hg:DirectedHypergraph):
    max = 0
    max_edge = ()
    for edge in edge_set:
        if hg.get_hyperedge_attribute(edge,'weight') > max:
            max = hg.get_hyperedge_attribute(edge,'weight')
            max_edge = edge
    return max_edge
    

def acoSearch(p:DirectedHypergraph, hg:DirectedHypergraph, node_set):
    #select next hypeedge from node according to pheromone distribution
    edge_set = set()
    for node in node_set:
        edge_set = set.union(edge_set,hg.get_forward_star(node))
    #select edge based on value of pheromone attribute
    next_edge = pheroChoice(edge_set, hg)
    tail = hg.get_hyperedge_head(next_edge)
    head = hg.get_hyperedge_tail(next_edge)
    attrs = hg.get_hyperedge_attributes(next_edge)
    #add selected hyperedge/node to p
    print(str(next_edge))
    print(str(tail))
    print(str(head))
    print(str(attrs))
    p.add_hyperedge(tail, head, attrs)
    next_head = hg.get_hyperedge_head(next_edge)
    for node in next_head:
        p.add_node(node, hg.get_node_attributes(node))
    #if new node added is sink, then return p
    isSink = False
    for node in next_head:
        if hg.get_node_attribute(node,'sink') == True:
            isSink = True
    if isSink == False:
        acoSearch(p, hg, next_head)
    #else recursive call
    return p


def acoAlgorithm(node_set, hg:DirectedHypergraph, ANT_NUM, COL_NUM):
    #ANT_NUM number of ants in one colony
    #COL_NUM number of colonies
    p_opt = DirectedHypergraph()
    utility_opt = 0.0
    ant = 0
    col = 0
    while col < COL_NUM:
        print("Processing colony n. "+str(col))
        #do something
        p = DirectedHypergraph()
        for node in node_set:
            p.add_node(node, hg.get_node_attributes(node))
        while ant < ANT_NUM:
            print("--- Porcessing ant n. "+str(ant))
            #call acoSearch on p
            p = acoSearch(p, hg, node_set)
            #calculate utility of p
            utility = calculateUtility(p)
            #check if p is better than current optimal solution
            #update if p is optimal
            if utility > utility_opt:
                utility_opt = utility
                p_opt = p
            ant = ant + 1
        col = col + 1
    #do something else
    

        
print("RANDOMW WALK EXECUTING......")
hgRandomWalk(['A'],H)


print("ACO SEARCH EXECUTING...")
acoAlgorithm(['A'], H, 10, 10)






