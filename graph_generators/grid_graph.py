import networkx as nx

def grid_graph(dim, scale=1.0, periodic=False):
    '''
    Creates a NetworkX grid graph with the original
    node labels as positions in the 'pos' node attribute.
    
    Will position the nodes in a unit square unless scale!=0,
    in which case the square is scaled accordingly.
    '''
    Network = nx.grid_graph(dim=dim, periodic=periodic)
    n = len(Network.nodes())
    positions = Network.nodes()
    positions = [(scale*i/float(n-1), scale*j/float(n-1))
                 for (i, j) in positions]
    Network = nx.convert_node_labels_to_integers(Network)
    pos = dict(zip(Network.nodes(), positions))
    nx.set_node_attributes(Network, 'pos', pos)
    
    return Network
