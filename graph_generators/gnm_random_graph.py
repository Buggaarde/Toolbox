import networkx as nx
import numpy as np

def gnm_random_graph(n, m, seed=None, directed=False):
    G = nx.gnm_random_graph(n, m, seed=seed, directed=directed)
    pos = dict(zip(G.nodes(),
                   zip(np.random.uniform(0, 1, n),
                       np.random.uniform(0, 1, n))))
    nx.set_node_attributes(G, 'pos', pos)
    return G
