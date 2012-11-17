'''
Created on Jul 9, 2012

@author: bantosik
'''
import networkx as nx
import monte_carlo.utitities as utilities


class CycleDetectedError(ValueError):
    pass

def generate_path(G, source, sink):
    if not nx.is_directed_acyclic_graph(G):
        raise CycleDetectedError
    path = [source]
    while source != sink:
        source = pick_next_node(G, source)
        if source not in path:
            path.append(source)
    return path

def create_random_dag(size):
    G = nx.DiGraph()
    nodes = range(size) 
    G.add_nodes_from(nodes)
    for i in xrange(size):
        distribution = utilities.get_circular_distribution(size - i - 1)
        for j, probability in zip(xrange(i + 1, size), distribution):
            G.add_edge(nodes[i], nodes[j], prob = probability)
    return G

def pick_next_node(G, node):
    probs, edges = [], []
    for e in G.out_edges_iter(node):
        prob = G.get_edge_data(*e)["prob"]
        probs.append(prob)
        edges.append(e)
    return edges[utilities.pick_from_distr(probs)][1]

def get_sampled_distribution_of_collisions(G, source, sink, number):     
    count = utilities.get_longest_path_length(G, source, sink)   
    
    collision_dictionary = [0] * (count + 1)
    for collision in simulate_double_runs(G, source, sink, number):
        collision_dictionary[collision] = collision_dictionary[collision] + 1
    return collision_dictionary

def simulate_double_runs(G, source, sink, number):
        return [utilities.count_collisions(generate_path(G, source, sink), generate_path(G, source, sink)) for i in xrange(number)]
    
    
def full_dag(size):
    g = nx.DiGraph()
    for i in xrange(size):
        for j in xrange(i + 1, size):
            g.add_edge(i, j)
    
    utilities.add_uniform_distr_probs_to_out_edges(g)
    g.source = 0
    g.sink = size - 1
    return g
