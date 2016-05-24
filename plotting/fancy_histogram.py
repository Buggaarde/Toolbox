#! /usr/bin/env python3
import numpy as np

def fancy_histogram(array, bins=10, density=False, range=None):
    '''
    Outputs the bin edges of np.histogram as well as the y-values
    corresponding to the edges, instead of the y-values in 
    between the edges.

    Example
    -------
    hist, bin_edges = fancy_histogram(array)
    plt.plot(bin_edges, hist, 'b-')
    '''
    hist, bin_edges = np.histogram(array, bins=bins, range=range,
                                   density=density)
    left, right = bin_edges[:-1], bin_edges[1:]
    X = np.array([left, right]).T.flatten()
    Y = np.array([hist, hist]).T.flatten()

    return Y, X
    













    
