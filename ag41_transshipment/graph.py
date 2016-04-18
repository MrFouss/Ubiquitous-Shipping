#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: graph.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Graph class file for the transshipment solver project"""


class Graph(object):
    """Graph class"""

    def __init__(self, name, max_t, nbr_nodes, nbr_edges, nodes, edges):
        """Creates the Graph object"""

        self.name = name
        self.max_t = max_t
        self.nbr_nodes = nbr_nodes
        self.nbr_edges = nbr_edges
        self.nodes = nodes
        self.edges = edges
