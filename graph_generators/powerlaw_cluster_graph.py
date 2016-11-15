import networkx as nx
import toolbox.decorators as dec

@dec.embed_in_unit_cube
def powerlaw_cluster_graph(*args, **kwargs):
    return nx.powerlaw_cluster_graph(*args, **kwargs)
