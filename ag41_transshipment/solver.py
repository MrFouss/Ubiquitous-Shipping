#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: solver.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 20/04/2016 by Fouss

"""Solver file for the transshipment solver project"""


def solve(graph):
    """Main solving function"""

    initialize(graph)


def initialize(graph):
    """Defines an initial solution for the transshipment problem"""

    for i in get_depot_list(graph):
        for j in graph.neighbors(i):
            if graph.node[i]['flow'] == -1 * graph.node[i]['demand']:
                break
            else:
                for k in graph.neighbors(j):
                    if graph.node[i]['flow'] == -1 * graph.node[i]['demand']:
                        break
                    elif graph.edge[i][j]['time'] + graph.node[j]['time'] + graph.edge[j][k]['time'] < \
                            graph.graph['time']:
                        diff = min(-1 * graph.node[i]['demand'] - graph.node[i]['flow'], graph.node[k]['demand'] -
                                   graph.node[k]['flow'], graph.edge[i][j]['capacity'] - graph.edge[i][j]['flow'],
                                   graph.edge[j][k]['capacity'] - graph.edge[j][k]['flow'])
                        graph.node[i]['flow'] += diff
                        graph.node[j]['flow'] += diff
                        graph.node[k]['flow'] += diff
                        graph.edge[i][j]['flow'] += diff
                        graph.edge[j][k]['flow'] += diff


def get_depot_list(graph):
    """Lists all depot nodes"""

    depot_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] < 0:
            depot_list.append(i)

    return depot_list
