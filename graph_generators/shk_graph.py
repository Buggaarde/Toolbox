#! /usr/bin/env python
from __future__ import print_function
import numpy as np
import networkx as nx
import random


def shk_graph(N, p, q, r, s,
              N0 = 10,
              distribution='uniform',
              dist_func='euclidean'):
    '''
    An implementation of the random growth model proposed by
    Paul Schultz, Jobst Heitzig and Jurgen Kurths.
    DOI: 10.1140/epjst/e2014-02279-6.
    
    Parameters
    ----------
    N : int or list
      If int, N is the number of nodes in the network. If list, N is
      a list of touples containing the node positions in the network.
      Furthermore, if N0 is int, N0 becomes the first N0 positions in N,
      and if N0 is list the N0 gets overwritten with the first len(N0)
      positions in N.
    p : float
      The probability of constructing an additional redundancy line
      attached at each new node
    q : float
      The probability of constructing a further redundancy line
      between existing nodes in each growth step
    r : float
      The exponent for the cost-vs-redundancy trade-off
    s : float
      The probability of splitting an existing line in each growth
      step
    N0 : int or list, optional
      If int, N0 is the number of initial nodes with which to 
      initialize the graph, with positions drawn from 'distribution'.
      If list, N0 is a list of touples of the positions of the initial
      nodes with which to initilize the graph (default=10)
    distribution : string, optional
      Keyword indicating which distribution the remaining node
      positions must be drawn from (default='uniform')
    dist_func : string, optional
      Keyword indicating which distance function is used to determine
      distance (default='euclidean')
    '''
    if dist_func == 'euclidean':
        def length(G, m, n):
            m_x = G.node[m]['pos'][0]
            m_y = G.node[m]['pos'][1]
            n_x = G.node[n]['pos'][0]
            n_y = G.node[n]['pos'][1]
            return np.sqrt((m_x - n_x)**2 + (m_y - n_y)**2)


    def target_function(G, m, n):
        shortest_path = nx.shortest_path(G, source=m, target=n)
        path_length = len(shortest_path) - 1
        if m==n:
            print(m)
        return (path_length + 1)**r/length(G, m, n)

    # print(type(N))
    if type(N) is list:
        M = list(N) # Takes a copy of N, so what we can use it in the future.
    elif type(N) is int:
        M = N
    # Initializing the network
    if type(M) is list:
        if type(N0) is int:
            N0 = M[:N0]
        elif type(N0) is list:
            N0 = M[:len(N0)]
            
    if type(N0) is int:
        G = nx.complete_graph(N0)
        pos = dict(zip(G.nodes(),
                       zip(np.random.uniform(0, 1, N0),
                           np.random.uniform(0, 1, N0))))
        nx.set_node_attributes(G, 'pos', pos)
        # Assigning lengths to the edges
        for m,n in G.edges_iter():
            G[m][n]['length'] = length(G, m, n)

        G = nx.minimum_spanning_tree(G, weight='length')
    elif type(N0) is list:
        G = nx.complete_graph(len(N0))
        pos = dict(zip(G.nodes(), N0))
        nx.set_node_attributes(G, 'pos', pos)
        # Assigning lengths to the edges
        for m,n in G.edges_iter():
            G[m][n]['length'] = length(G, m, n)

        G = nx.minimum_spanning_tree(G, weight='length')
        
            
    else:
        raise nx.NetworkXError('NetworkXError N0 must be integer')

    if type(N0) is int:
        m = int(np.round(N0*(1 - s)*(p + q)))
    elif type(N0) is list:
        m = int(np.round(len(N0)*(1 - s)*(p + q)))
    # print(m)
    for a in xrange(m):
        target_value = 0
        connected_nodes = (0, 0)
        for node1 in G.nodes():
            for node2 in G.nodes():
                if node1 is not node2:
                    if node2 not in G.neighbors(node1):
                        t_val = target_function(G, node1, node2)
                        if t_val > target_value:
                            target_value = t_val
                            connected_nodes = (node1, node2)
        G.add_edge(*connected_nodes)
    if type(M) is int:
        G.name = 'SHK_graph({}, {}, {}, {}, {})'.format(M, p, q, r, s)
    elif type(M) is list:
        G.name = 'SHK_graph({}, {}, {}, {}, {})'.format(len(M), p, q, r, s)

    if type(M) is int:
        lenN = M
    elif type(M) is list:
        lenN = len(M)
            
    # Growing the network
    while len(G.nodes()) < lenN:
        # print(len(G.nodes()))
        P = random.uniform(0, 1)
        nodes = len(G.nodes())
        # print(p)
        if P <= s: # if we split an existing line
            r_edge = random.choice(G.edges())
            G.remove_edge(*r_edge)
            node1_pos = G.node[r_edge[0]]['pos']
            node2_pos = G.node[r_edge[1]]['pos']
            new_pos = ((node1_pos[0] + node2_pos[0])/2.,
                       (node1_pos[1] + node2_pos[1])/2.)
            G.add_node(nodes, pos=new_pos)
            G.add_edges_from([(nodes, r_edge[0]),
                              (nodes, r_edge[1])])
        else: # place a new node according to distribution,
              # and attach to spatially closest neighbor
            
            if type(M) is int:
                new_pos = (random.uniform(0, 1), random.uniform(0, 1))
            elif type(M) is list:
                new_pos = M.pop()
            G.add_node(nodes, pos=new_pos)
            min_dist = 2
            min_dist_node = -1
            for node in G.nodes():
                if node is not nodes:
                    dist = length(G, node, nodes)
                    if dist < min_dist:
                        min_dist = dist
                        min_dist_node = node
            G.add_edge(nodes, min_dist_node)
            P = random.uniform(0, 1)
            if P <= p: # if we need to construct a redundancy line
                       # to the new node
                target_value = 0
                target_node = 0
                for node in G.nodes():
                    if node is not nodes:
                        t_val = target_function(G, nodes, node)
                        if node == nodes:
                            print('p')
                        if t_val > target_value:
                            target_value = t_val
                            target_node = node
                G.add_edge(nodes, target_node)
            Q = random.uniform(0, 1)
            if Q <= q: # if we need to construct a redundancy line
                       # between existing lines in the network
                node1 = random.choice(range(len(G)))
                target_value = 0
                node2 = 0
                for node in G.nodes():
                    if node != node1:
                        if node == node1:
                            print('q')
                        if node not in G.neighbors(node1):
                            t_val = target_function(G, node1, node)
                            if t_val > target_value:
                                target_value = t_val
                                node2 = node
                G.add_edge(node1, node2)
    return G


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    N = zip(np.random.uniform(0, 1, 50), np.random.uniform(0, 1, 50))
    params = (N, 0.2, 0.4, 1, 0)
    N0 = 10
    G = shk_graph(*params, N0=N0)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos=pos)
    plt.show()
    plt.savefig('minimal_spanning_tree.pdf')
    plt.clf()
    plt.close()
