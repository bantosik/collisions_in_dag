'''
Created on Jul 11, 2012

@author: bantosik
'''

import monte_carlo.utitities as utilities
import monte_carlo.simulation as sim
import networkx as nx
import dynamic_programming.possible_collision_counter as dp
from monte_carlo.simulation import get_sampled_distribution_of_collisions

from pylab import *

if __name__ == '__main__':
    g = sim.create_random_dag(15)
    s = []
    for i in xrange(1000):
        s.append(get_sampled_distribution_of_collisions(g, 0, 14, 1000))
    theoretic = dp.CollisionCounter(g, 0, 14).get_collision_distribution()
    empirical = zip(*s)
    means = [float(sum(x))/len(x) for x in empirical]
    summ = sum(means)
    means = [x / summ for x in means]
        
      