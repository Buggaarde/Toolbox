import numpy as np
import networkx as nx
import random
import toolbox.decorators as dec

def minimum_distance_graph(N, m, c=0):
    '''
    From The Topological Electrical Structure of Power Grids.
    '''
    def length(G, m, n):
        m_x = G.node[m]['pos'][0]
        m_y = G.node[m]['pos'][1]
        n_x = G.node[n]['pos'][0]
        n_y = G.node[n]['pos'][1]
        d = np.sqrt((m_x - n_x)**2 + (m_y - n_y)**2)
        # print(d)
        return d
    

    def distance_from_node_to_line(G, node, m, n):
        node_x = G.node[node]['pos'][0]
        node_y = G.node[node]['pos'][1]
        m_x = G.node[m]['pos'][0]
        m_y = G.node[m]['pos'][1]
        n_x = G.node[n]['pos'][0]
        n_y = G.node[n]['pos'][1]
        return abs((n_y - m_y)*node_x
                   - (n_x - m_x)*node_y
                   + n_x*m_y - n_y*m_x)/length(G, m, n)

    def dist_from_line_segment(G, node, m, n):
        d_m = length(G, node, m)
        d_n = length(G, node, n)
        d_l = distance_from_node_to_line(G, node, m, n)
        return min(d_m, d_n, d_l)

    @dec.embed_in_unit_cube
    def no_edge_graph(N):
        G = nx.Graph()
        G.add_nodes_from(range(N))
        return G

    G = no_edge_graph(N)

    P = float(m)/N - np.round(float(m)/N)
    for node in G.nodes_iter():
        target_node = 0
        target_edge = (-1, -1)
        target_node_dist = 2
        target_edge_dist = 2
        for t_node in G.nodes_iter():
            if t_node != node:
                if t_node not in G.neighbors(node):
                    d = length(G, node, t_node)
                    if d < target_node_dist:
                        target_node = t_node
                        target_node_dist = d
        for t_edge in G.edges_iter():
            if node not in t_edge:
                d = dist_from_line_segment(G, node, *t_edge)
                print d
                if d < target_edge_dist:
                    target_edge = t_edge
                    target_edge_dist = d

        if target_node_dist <= target_edge_dist + c:
            G.add_edge(node, target_node)        
        else:
            G.remove_edge(*target_edge)
            G.add_edges_from([(target_node, target_edge[0]),
                              (target_node, target_edge[1])])

    return G

if __name__ == '__main__':
    G = minimum_distance_graph(100, 150)

            
        
