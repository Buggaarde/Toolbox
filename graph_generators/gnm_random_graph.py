import networkx as nx
import numpy as np
import toolbox.decorators as dec

@dec.embed_in_unit_cube
@dec.return_largest_connected_subgraph(silent=False)
def gnm_random_graph(*args, **kwargs):
    return nx.gnm_random_graph(*args, **kwargs)
