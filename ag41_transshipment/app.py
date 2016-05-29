#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: app.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Main file for the transshipment solver project"""

from ag41_transshipment.parser import Parser
from ag41_transshipment.solver import initialize, solve, print_solution, test_feasability
import sys
import time


class Application(object):
    """Application class"""

    def __init__(self, file_name, max_time):

        self.parser = Parser(file_name)

        self.graph = self.parser.import_from_file()
        # debug_graph(self.graph)

        u_time = time.time()
        s_time = time.clock()

        initialize(self.graph)
        self.init_graph = self.graph.copy()
        if test_feasability(self.graph):

            print('\n#####################')
            print('# Initial solution! #')
            print('#####################')
            print_solution(self.init_graph)

            self.graph = solve(self.graph, max_time)

            u_time = time.time() - u_time
            s_time = time.clock() - s_time

            self.parser.export_to_file(self.init_graph, self.graph, u_time, s_time)

            u_hour = (u_time - (u_time % 3600.)) / 3600
            s_hour = (s_time - (s_time % 3600.)) / 3600

            u_time -= u_hour * 3600.
            s_time -= s_hour * 3600.

            u_min = (u_time - (u_time % 60.)) / 60
            s_min = (s_time - (s_time % 60.)) / 60

            u_time -= u_min * 60.
            s_time -= s_min * 60.

            print('\nExecution time:')
            print('\tUser time : {} hours, {} minutes and {} seconds'.format(u_hour, u_min, u_time))
            print('\tSystem time : {} hours, {} minutes and {} seconds\n'.format(s_hour, s_min, s_time))

        else:
            print('The problem can\'t be solved!')
            self.parser.export_to_file(self.init_graph, self.graph, u_time, s_time)

        # debug_graph(self.graph)


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
