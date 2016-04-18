#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: edge.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Edge class file for the transshipment solver project"""


class Edge(object):
    """Edge class"""

    def __init__(self, id_edge, start, end, capacity, fixed_cost, unit_cost, time):
        """Creates the Edge object"""

        self.id = id_edge  # id of the edge
        self.start = start  # starting node
        self.end = end  # ending node
        self.capacity = capacity  # capacity of the edge
        self.fixed_cost = fixed_cost  # fixed cost of the edge
        self.unit_cost = unit_cost  # unit cost of the edge
        self.time = time  # transportation time on the edge
