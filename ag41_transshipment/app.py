#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: app.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Main file for the transshipment solver project"""

from ag41_transshipment.parser import *


class Application(object):
    """Application class"""

    def __init__(self, file_name):
        self.parser = Parser(file_name)
        self.graph = self.parser.import_from_file()

        print('Name: {}'.format(self.graph.name))
        print('T: {}'.format(self.graph.max_t))

        print('\nNodes ({}):'.format(self.graph.nbr_nodes))
        for i in range(self.graph.nbr_nodes):
            if self.graph.nodes[i + 1].demand < 0:
                print('\tDepot #{}:'.format(self.graph.nodes[i + 1].id))
            elif self.graph.nodes[i + 1].demand > 0:
                print('\tClient #{}:'.format(self.graph.nodes[i + 1].id))
            else:
                print('\tPlatform #{}:'.format(self.graph.nodes[i + 1].id))
            print('\t\tCoordinates: ({},{})'.format(self.graph.nodes[i + 1].coord[0], self.graph.nodes[i + 1].coord[1]))
            print('\t\tDemand: {}'.format(self.graph.nodes[i + 1].demand))
            print('\t\tUnit cost: {}'.format(self.graph.nodes[i + 1].cost))
            print('\t\tTime: {}'.format(self.graph.nodes[i + 1].time))

        print('\nEdges ({}):'.format(self.graph.nbr_edges))
        for i in range(self.graph.nbr_edges):
            print('\tEdge #{}:'.format(self.graph.edges[i + 1].id))
            print('\t\tStarting node: {}'.format(self.graph.edges[i + 1].start))
            print('\t\tEnding node: {}'.format(self.graph.edges[i + 1].end))
            print('\t\tCapacity: {}'.format(self.graph.edges[i + 1].capacity))
            print('\t\tFixed cost: {}'.format(self.graph.edges[i + 1].fixed_cost))
            print('\t\tUnit cost: {}'.format(self.graph.edges[i + 1].unit_cost))
            print('\t\tTime: {}'.format(self.graph.edges[i + 1].time))
