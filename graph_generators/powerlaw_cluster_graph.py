import networkx as nx

def powerlaw_cluster_graph(n, m, p, seed=None, scale=1.0):
    '''
    Creates a NetworkX powerlaw cluster graph with positions
    given by the spring layout. The positions are stored
    in the 'pos' node attribute.
    
    Will position the nodes in a unit square unless scale!=0,
    in which case the square is scaled accordingly.
    '''
    Network = nx.powerlaw_cluster_graph(n, m, p, seed=seed)
    pos = nx.spring_layout(Network, scale=scale)
    nx.set_node_attributes(Network, 'pos', pos)

    return Network
