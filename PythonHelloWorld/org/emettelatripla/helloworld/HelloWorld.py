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

def HgRandomWalk(node_set, hg:DirectedHypergraph):
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
        HgRandomWalk(next_node_set,hg)
        
print("RANDOMW WALK EXECUTING......")
HgRandomWalk(['A'],H)
    




