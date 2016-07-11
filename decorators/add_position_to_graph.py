import numpy as np
import networkx as nx
from functools import wraps

def embed_in_unit_cube(Graph):
    @wraps(Graph)
    def func_wrapper(*args, **kwargs):
        G = Graph(*args, **kwargs)
        nodes = len(G.nodes())
        pos = dict(zip(G.nodes(),
                       zip(np.random.uniform(0, 1, nodes),
                           np.random.uniform(0, 1, nodes))))
        nx.set_node_attributes(G, 'pos', pos)
        return G
    return func_wrapper
