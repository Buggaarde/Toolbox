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

def make_connected(attempts=10000, connect_subgraphs=False):
    def ensure_connected(Graph):
        @wraps(Graph)
        def func_wrapper(*args, **kwargs):
            connected_flag = 0
            for attempt in xrange(attempts):
                G = Graph(*args, **kwargs)
                if nx.is_connected(G):
                    connected_flag = 1
                    break
            if not connected_flag:
                print('Timeout; maximum attempts reached: {}'.format(attempts))
            if connect_subgraphs:
                print('Connecting subgraphs')
            
            return G
        return func_wrapper
    return ensure_connected

def return_largest_connected_subgraph(silent=True):
    def outer_wrapper(Graph):
        @wraps(Graph)
        def func_wrapper(*args, **kwargs):
            G = Graph(*args, **kwargs)
            name = G.name # resetting the indicies changes the name
                          # so we save it here, for later retrieval.
            subgraphs = list(nx.connected_component_subgraphs(G))
            sizes = [len(g) for g in subgraphs]
            i_max = sizes.index(max(sizes))
            G = subgraphs[i_max]
            G = nx.convert_node_labels_to_integers(G) # changes name
            G.name = name # give back old name
            if not silent:
                print('Largest connected subgraph: {}'.format(len(G)))
            return G
        return func_wrapper
    return outer_wrapper
