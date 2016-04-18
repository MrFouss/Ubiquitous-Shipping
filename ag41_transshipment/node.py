#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: node.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Node class file for the transshipment solver project"""


class Node(object):
    """Node class"""

    def __init__(self, id_node, x, y, demand, cost, time):
        """Creates the Node object"""

        self.id = id_node  # id of the node
        self.coord = x, y  # display coordinates of the node
        self.demand = demand  # < 0 for depots, > 0 for clients, = 0 for platforms
        self.cost = cost  # unit cost of the node, platforms only
        self.time = time  # transportation time on the node, platforms only
