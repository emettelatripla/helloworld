'''
Created on 2016. 6. 15.

@author: UNIST
'''
from directed_hypergraph import DirectedHypergraph

def ACOAlgorithm(H: DirectedHypergraph, col_num, ant_num):
    #initialisation
    v_opt = 0.0
    hg = DirectedHypergraph()
    hg = H.copy()
    col = 0
    #Iterate on ant colonies
    while col < col_num:
        #iterate on ants within a colony
        ant = 0
        print("Processing new ant colony - number: "+str(col))
        # DO SOMETHING
        #list of nodes in the optimal path
        p = list()
        hg.g
        while ant < ant_num:
            print("--- Processing ant "+str(ant)+" in colony "+str(col))
            #DO SOMETHING
            ant++
        col++
    
def ACOSearch():
    
def calculateUtility(node_list):
    
    
    
    