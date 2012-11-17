'''
Created on Jul 9, 2012

@author: bantosik
'''
import networkx as nx
from monte_carlo.utitities import get_longest_path_length

class CollisionCounter(object):
    '''
    classdocs
    '''


    def __init__(self,graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        
        self.double_passage_graph = nx.DiGraph()
        for n in self.graph.nodes():
            for m in self.graph.nodes():
                self.double_passage_graph.add_node((n, m))
                
        for v in self.double_passage_graph.nodes_iter():
            for w in self.double_passage_graph.nodes_iter():
                if self.graph.has_edge(v[0], w[0]) and self.graph.has_edge(v[1], w[1]): 
                    self.double_passage_graph.add_edge(v, w)
                    self.double_passage_graph[v][w]['prob'] = self.graph[v[0]][w[0]]['prob'] * self.graph[v[1]][w[1]]['prob']
        
        self.probability = {}
        self.distributions = {}
        
        self.maximum_collisions = get_longest_path_length(self.graph, self.source, self.sink)
        
        for n in self.double_passage_graph.nodes_iter():
            self.distributions[n] = {}
            self.probability[n] = 0.0
            if self.double_passage_graph.in_degree(n) == 0:
                for i in xrange(self.maximum_collisions + 1):
                    self.distributions[n][i] = 0.0
        
        self.distributions[(self.source, self.source)][1] = 1.0
        self.probability[(self.source, self.source)] = 1.0

    
    
    
    
    def get_collision_distribution(self):
        
                  
        for node in nx.topological_sort(self.double_passage_graph, [(self.source, self.source)]):
            if not node == (self.source, self.source):
                for k in xrange(self.maximum_collisions + 1):
                    if node[0] == node[1]:
                        if k > 0:
                            self.distributions[node][k] = sum(
                                             [self.distributions[parent][k-1]*self.double_passage_graph[parent][node]['prob']*
                                              self.probability[parent] 
                                              for parent in self.double_passage_graph.predecessors_iter(node)]
                                             )
                        else:
                            self.distributions[node][k] = 0.0
                    else:
                        self.distributions[node][k] = sum(
                                             [self.distributions[parent][k]*self.double_passage_graph[parent][node]['prob']*
                                              self.probability[parent] 
                                              for parent in self.double_passage_graph.predecessors_iter(node)]
                                             )
                self.probability[node] = sum([self.probability[parent]*self.double_passage_graph[parent][node]['prob'] 
                                         for parent in self.double_passage_graph.predecessors_iter(node)])
                
                for k,v in self.distributions[node].iteritems():
                    self.distributions[node][k] = v/self.probability[node]
                
        return self.distributions[(self.sink, self.sink)]
                                        
                    
                            
                
        
        
        

        


                