import numpy as np
import networkx as nx

def save_graph(savefile, G):
    adjacency_matrix = nx.adjacency_matrix(G).todense()
    nodes = G.nodes(data=True)
    edges = G.edges(data=True)
    name = G.name
    np.savez_compressed(savefile + '.npz',
                        adjacency_matrix=adjacency_matrix,
                        nodes=nodes,
                        edges=edges,
                        name=name)

def load_graph(loadfile):
    adjacency_matrix = np.load(loadfile + '.npz')['adjacency_matrix']
    nodes = np.load(loadfile + '.npz')['nodes']
    edges = np.load(loadfile + '.npz')['edges']
    name = np.load(loadfile + '.npz')['name']

    G = nx.from_numpy_matrix(adjacency_matrix)
    G.name = name
    for node, data_dict in nodes:
        G.node[node].update(data_dict)
    for node1, node2, data_dict in edges:
        del G[node1][node2]['weight']
        G[node1][node2].update(data_dict)

    return G

