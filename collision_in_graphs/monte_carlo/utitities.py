from random import random
from numpy import cumsum
import networkx as nx


def get_circular_distribution(n):
    initial = sorted( [random() for i in xrange(n)])
    initial = [x + 1 - initial[-1] for x in initial ]
    result = []
    last = 0.0
    for i in initial:
        result.append(i - last)
        last = i
    return result

def pick_from_distr(distr):
    p = random()
    cumulant = cumsum(distr)
    for i, c in enumerate(cumulant):
        if c >= p:
            return i

def add_uniform_distr_probs_to_out_edges(g):
    for e in g.edges_iter():
        g[e[0]][e[1]]['prob'] = 1.0 / g.out_degree(e[0])
        
def select_sources_list(G):
    return [n for n in G.nodes_iter() if G.in_degree(n) == 0]

def select_sinks_list(G):
    return [n for n in G.nodes_iter() if G.out_degree(n) == 0]

def count_collisions(path1, path2):
    return len(set.intersection(set(path1), set(path2)))
#TODO: compare
def get_longest_path_length(G, source, sink):
    for edge in G.edges_iter():
        G[edge[0]][edge[1]]['weight'] = -1.0
    return len(nx.single_source_dijkstra_path(G, source)[sink])
        
    
    
    
    
    
            
    
    

