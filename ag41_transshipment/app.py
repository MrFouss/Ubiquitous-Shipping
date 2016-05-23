#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: app.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Main file for the transshipment solver project"""

from ag41_transshipment.parser import Parser
from ag41_transshipment.solver import *
import sys


class Application(object):
    """Application class"""

    def __init__(self, file_name):
        self.parser = Parser(file_name)

        self.graph = self.parser.import_from_file()

        # debug_graph(self.graph)

        solve(self.graph)

        # debug_graph(self.graph)

        self.parser.export_to_file()


def debug_graph(graph):
    """Displays all info about the graph (parser debugging only)"""

    print('Name: {}'.format(graph.graph['name']), file=sys.stderr)
    print('Time: {}'.format(graph.graph['time']), file=sys.stderr)

    print('\nNodes ({}):'.format(graph.graph['nbr_nodes']), file=sys.stderr)
    for i in graph.nodes():
        if graph.node[i]['demand'] < 0:
            print('\tDepot #{}:'.format(i), file=sys.stderr)
        elif graph.node[i]['demand'] > 0:
            print('\tClient #{}:'.format(i), file=sys.stderr)
        else:
            print('\tPlatform #{}:'.format(i), file=sys.stderr)
        print('\t\tCoordinates: ({}, {})'.format(graph.node[i]['x'], graph.node[i]['y']), file=sys.stderr)
        print('\t\tDemand: {}'.format(graph.node[i]['demand']), file=sys.stderr)
        print('\t\tUnit cost: {}'.format(graph.node[i]['unit_cost']), file=sys.stderr)
        print('\t\tTime: {}'.format(graph.node[i]['time']), file=sys.stderr)
        print('\t\tFlow: {}'.format(graph.node[i]['flow']), file=sys.stderr)

    print('\nEdges ({}):'.format(graph.graph['nbr_edges']), file=sys.stderr)
    for (u, v) in graph.edges():
        print('\tEdge #{}:'.format(graph.edge[u][v]['id']), file=sys.stderr)
        print('\t\tStarting node: {}'.format(u), file=sys.stderr)
        print('\t\tEnding node: {}'.format(v), file=sys.stderr)
        print('\t\tCapacity: {}'.format(graph.edge[u][v]['capacity']), file=sys.stderr)
        print('\t\tFixed cost: {}'.format(graph.edge[u][v]['fixed_cost']), file=sys.stderr)
        print('\t\tUnit cost: {}'.format(graph.edge[u][v]['unit_cost']), file=sys.stderr)
        print('\t\tTime: {}'.format(graph.edge[u][v]['time']), file=sys.stderr)
        print('\t\tFlow: {}'.format(graph.edge[u][v]['flow']), file=sys.stderr)
