#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: solver.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 20/04/2016 by Fouss

"""Solver file for the transshipment solver project"""

import networkx as nx
import sys


def solve(graph):
    """Main solving function"""

    initialize(graph)
    print('\n#####################', file=sys.stderr)
    print('# Initial solution! #', file=sys.stderr)
    print('#####################', file=sys.stderr)
    print_solution(graph)

    try:
        continual = True
        while continual:
            # while there is at least one negative cycle
            continual = False
            gap_graph = get_gap_graph(graph)
            tmp_graph = graph.copy()
            for cycle in nx.simple_cycles(gap_graph):
                # for each cycle in the gap graph
                if len(cycle) > 2:
                    # if the cycle is not only between two nodes
                    cycle = cycle + [cycle[0]]
                    # adding the first node of the cycle at the end
                    maxi = gap_graph.edge[cycle[0]][cycle[1]]['capacity']
                    first = True
                    for i in range(0, len(cycle)):
                        # computing the maximum flow we can change in the cycle
                        if not first:
                            maxi = min(maxi, gap_graph.edge[cycle[i - 1]][cycle[i]]['capacity'])
                        else:
                            first = False

                    first = True
                    cost = 0
                    for i in range(0, len(cycle)):
                        if not first:
                            cost += gap_graph.edge[cycle[i - 1]][cycle[i]]['unit_cost'] * maxi
                            if gap_graph.edge[cycle[i - 1]][cycle[i]]['capacity'] == maxi:
                                cost -= gap_graph.edge[cycle[i - 1]][cycle[i]]['fixed_cost']
                            if tmp_graph.node[cycle[i]]['demand'] == 0:
                                if tmp_graph.node[cycle[i - 1]]['demand'] < 0:
                                    cost += tmp_graph.node[cycle[i]]['unit_cost'] * maxi
                                else:
                                    cost -= tmp_graph.node[cycle[i]]['unit_cost'] * maxi
                        else:
                            first = False

                    if cost < 0:
                        continual = True
                        first = True
                        for i in range(0, len(cycle)):
                            if not first:
                                if tmp_graph.has_edge(cycle[i - 1], cycle[i]):
                                    tmp_graph.edge[cycle[i - 1]][cycle[i]]['flow'] += maxi
                                else:
                                    tmp_graph.edge[cycle[i]][cycle[i - 1]]['flow'] += maxi

                                if tmp_graph.node[cycle[i]]['demand'] == 0:
                                    if tmp_graph.node[cycle[i - 1]]['demand'] > 0:
                                        tmp_graph.node[cycle[i]]['flow'] += maxi
                                    else:
                                        tmp_graph.node[cycle[i]]['flow'] -= maxi
                            else:
                                first = False
                        break
            graph = tmp_graph
            print('\n##############################', file=sys.stderr)
            print('# New better solution found! #', file=sys.stderr)
            print('##############################', file=sys.stderr)
            print_solution(graph)

    except KeyboardInterrupt:
        print('Optimization interrupted!')


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


def get_platform_list(graph):
    """"Lists all platform nodes"""

    platform_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] == 0:
            platform_list.append(i)

    return platform_list


def get_client_list(graph):
    """"Lists all client nodes"""

    client_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] > 0:
            client_list.append(i)

    return client_list


def get_gap_graph(graph):
    """Details platforms with new nodes and edges"""

    gap_graph = nx.DiGraph()
    gap_graph.add_nodes_from(graph)
    for u, v in graph.edges_iter():
        if graph.edge[u][v]['flow'] < graph.edge[u][v]['capacity']:
            gap_graph.add_edge(u, v, id=graph.edge[u][v]['id'],
                               capacity=graph.edge[u][v]['capacity'] - graph.edge[u][v]['flow'],
                               fixed_cost=graph.edge[u][v]['fixed_cost'], unit_cost=graph.edge[u][v]['unit_cost'],
                               time=graph.edge[u][v]['time'])

        if graph.edge[u][v]['flow'] > 0:
            gap_graph.add_edge(v, u, id=graph.edge[u][v]['id'], capacity=graph.edge[u][v]['flow'],
                               fixed_cost=-graph.edge[u][v]['fixed_cost'], unit_cost=-graph.edge[u][v]['unit_cost'],
                               time=graph.edge[u][v]['time'])

    return gap_graph


def print_solution(graph):
    """Displays all info about the solution of the problem"""

    cost = 0

    for i in get_platform_list(graph):
        if graph.node[i]['flow'] > 0:
            cost += graph.node[i]['unit_cost'] * graph.node[i]['flow']
            print('Platform node #{} used with flow={}'.format(i, graph.node[i]['flow']), file=sys.stderr)

    for u, v in graph.edges_iter():
        if graph.edge[u][v]['flow'] > 0:
            cost += graph.edge[u][v]['flow'] * graph.edge[u][v]['unit_cost'] + graph.edge[u][v]['fixed_cost']
            print('Edge #{} from node #{} to node #{} used with flow={}'.format(graph.edge[u][v]['id'], u, v,
                                                                                graph.edge[u][v]['flow']),
                  file=sys.stderr)

    print('Result: {}'.format(cost), file=sys.stderr)
