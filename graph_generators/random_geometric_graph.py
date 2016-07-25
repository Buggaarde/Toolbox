import networkx as nx
import numpy as np
import toolbox.decorators as dec

@dec.return_largest_connected_subgraph(silent=False)
def random_geometric_graph(*args, **kwargs):
    return nx.random_geometric_graph(*args, **kwargs)
