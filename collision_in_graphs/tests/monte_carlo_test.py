'''
Created on 05-07-2012

@author: bartek
'''
import unittest
import random
import networkx as nx
import monte_carlo.utitities as mc
import monte_carlo.simulation as s
import dynamic_programming.possible_collision_counter as dp

epsilon = 2e-16





class Test(unittest.TestCase):
    def setUp(self):
        self.path_graph = nx.path_graph(5, nx.DiGraph())
        mc.add_uniform_distr_probs_to_out_edges(self.path_graph)
        self.path_graph_sources = mc.select_sources_list(self.path_graph)
        self.path_graph_sinks = mc.select_sinks_list(self.path_graph)
        

    def test_get_circular_distribution(self):
        distribution = mc.get_circular_distribution(5)
        self.assertEqual(len(distribution), 5)
        self.assertAlmostEqual(sum(distribution), 1.0)
        self.assertTrue(all([x > 0.0 for x in distribution]), "All elements from distribution should be greater than 0.0")
    
    def test_pick_from_distr(self):
        d = mc.pick_from_distr(mc.get_circular_distribution(5))
        self.assertGreaterEqual(d, 0)
        self.assertLess(d, 5)
        
    def test_create_random_dag(self):
        g = s.create_random_dag(13)
        for node in g:
            probs = []
            for edge in g.edges_iter([node]):
                probs.append(g.get_edge_data(*edge)["prob"])
            if g.out_degree(node) != 0:
                self.assertAlmostEqual(sum(probs), 1.0)
    
    def test_generate_path(self):
        p = s.generate_path(self.path_graph, self.path_graph_sources[0], self.path_graph_sinks[0])
        self.assertEqual(p, self.path_graph.nodes(), "in a graph with a single path it should be returned by generate_path with probability 1")
        
    def test_generate_path_should_raise_when_find_cycle(self):
        g = nx.cycle_graph(5, nx.DiGraph())
        
        mc.add_uniform_distr_probs_to_out_edges(g)
        [source, sink] = random.sample(g.nodes(), 2)
        self.assertRaises(s.CycleDetectedError, lambda : s.generate_path(g, source, sink))
    
    def test_count_collisions(self):
        self.assertEqual(mc.count_collisions([1,2,3], [3,2,1]), 3, "permutation of n should have collision count 3")
        self.assertEqual(mc.count_collisions([1,2,3], [3,4,2,1]), 3, "permutation of n and one additional element should have collision count 3")
    
    
    def test_get_sampled_distribution_of_collisions(self):
        collisions = s.get_sampled_distribution_of_collisions(self.path_graph, self.path_graph_sources[0], self.path_graph_sinks[0], 1000)
        self.assertEqual(collisions, [0,0,0,0,0,1000], "path graph of size n should have always collision of count n")
        
    def test_get_longest_path_length(self):
        self.assertEqual(5, mc.get_longest_path_length(self.path_graph, self.path_graph_sources[0], self.path_graph_sinks[0]), "should return 5 for a path graph with")   
        self.assertEqual(15, mc.get_longest_path_length(s.create_random_dag(15), 0, 14))
        
    def test_get_collision_distribution(self):
        collisions = dp.CollisionCounter(self.path_graph, self.path_graph_sources[0], 
                                                                         self.path_graph_sinks[0])
        self.assertAlmostEqual(
                               sum(collisions.get_collision_distribution().itervalues()),
                               1.0
                               )
    def test_get_collision_distribution2(self):
        dag = s.full_dag(6) 
        collisions = dp.CollisionCounter(dag, dag.source, dag.sink)
        probs = collisions.get_collision_distribution()
        print probs
        self.assertAlmostEqual(
                               sum(probs.itervalues()),
                               1.0
                               )
        
        
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_circular_distribution']
    unittest.main()