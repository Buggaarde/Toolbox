import networkx as nx
from toolbox.decorators import embed_in_unit_cube

@embed_in_unit_cube
def connected_watts_strogatz_graph(*args, **kwargs):
    return nx.connected_watts_strogatz_graph(*args, **kwargs)
