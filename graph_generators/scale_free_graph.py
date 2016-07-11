import networkx as nx
from toolbox.decorators import embed_in_unit_cube

@embed_in_unit_cube
def scale_free_graph(n, alpha=0.41, beta=0.54, gamma=0.05,
                     delta_in=0.2, delta_out=0,
                     create_using=None, seed=None):
    G = nx.scale_free_graph(n, alpha=alpha, beta=beta, gamma=gamma,
                            delta_in=delta_in, delta_out=delta_out,
                            create_using=create_using, seed=seed)
    return G
    
