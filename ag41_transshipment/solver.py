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
import time


def solve(graph):
    """Main solving function"""

    try:
        u_time = time.time()

        continual = True
        while continual:
            # while there is at least one negative cycle
            continual = False
            gap_graph = get_gap_graph(graph)
            tmp_graph = graph.copy()
            cycles = nx.simple_cycles(gap_graph)
            for cycle in cycles:
                # to end the optimization before the end, after a certain time
                if (time.time() - u_time) / 60. >= 30.:
                    raise KeyboardInterrupt

                # for each cycle in the gap graph
                if len(cycle) > 2:
                    # if the cycle is not only between two nodes
                    cycle = cycle + [cycle[0]]
                    # adding the first node of the cycle at the end
                    maxi = gap_graph.edge[cycle[0]][cycle[1]]['capacity']
                    for i in range(1, len(cycle)):
                        # computing the maximum flow we can change in the cycle
                        maxi = min(maxi, gap_graph.edge[cycle[i - 1]][cycle[i]]['capacity'])

                    cost = 0
                    for i in range(1, len(cycle)):
                        cost += gap_graph.edge[cycle[i - 1]][cycle[i]]['unit_cost'] * maxi
                        # adding the unit cost of the edge
                        if gap_graph[cycle[i - 1]][cycle[i]]['fixed_cost'] > 0:
                            # if we increase the flow in a graph edge
                            if tmp_graph[cycle[i - 1]][cycle[i]]['flow'] == 0:
                                # if the edge was unused, we add the fixed cost
                                cost += gap_graph.edge[cycle[i - 1]][cycle[i]]['fixed_cost']
                        else:
                            # if we decrease the flow in a graph edge
                            if gap_graph.edge[cycle[i - 1]][cycle[i]]['capacity'] == maxi:
                                # if we empty the edge in the base graph, we deduce the fixed cost
                                cost += gap_graph.edge[cycle[i - 1]][cycle[i]]['fixed_cost']
                        if tmp_graph.node[cycle[i]]['demand'] == 0:
                            # if it is a platform
                            if i < len(cycle) - 1:
                                if tmp_graph.node[cycle[i - 1]]['demand'] < 0 < \
                                        tmp_graph.node[cycle[i + 1]]['demand']:
                                    # if the in node of the edge is a depot and the out is a client
                                    cost += tmp_graph.node[cycle[i]]['unit_cost'] * maxi
                                    # we add the unit cost of the platform
                                elif tmp_graph.node[cycle[i - 1]]['demand'] > 0 > \
                                        tmp_graph.node[cycle[i + 1]]['demand']:
                                    # if the in node of the edge is a client and the out is a depot
                                    cost -= tmp_graph.node[cycle[i]]['unit_cost'] * maxi
                                    # we deduce the unit cost of the platform
                            else:
                                if tmp_graph.node[cycle[i - 1]]['demand'] < 0 < tmp_graph.node[cycle[1]]['demand']:
                                    cost += tmp_graph.node[cycle[i]]['unit_cost'] * maxi
                                elif tmp_graph.node[cycle[i - 1]]['demand'] > 0 > tmp_graph.node[cycle[1]]['demand']:
                                    cost -= tmp_graph.node[cycle[i]]['unit_cost'] * maxi

                    if cost < 0:
                        continual = True
                        # there is a negative cycle so we continue
                        for i in range(1, len(cycle)):

                            if tmp_graph.has_edge(cycle[i - 1], cycle[i]):
                                # if the edge is in the same orientation in the graph and the gap graph
                                tmp_graph.edge[cycle[i - 1]][cycle[i]]['flow'] += maxi
                                # we add the flow
                            else:
                                # if the edge is in the opposite orientation in the graph and the gap graph
                                tmp_graph.edge[cycle[i]][cycle[i - 1]]['flow'] -= maxi
                                # we deduce the flow
                            if tmp_graph.node[cycle[i]]['demand'] == 0:
                                # if it is a platform
                                if i < len(cycle) - 1:
                                    if tmp_graph.node[cycle[i - 1]]['demand'] < 0 < \
                                            tmp_graph.node[cycle[i + 1]]['demand']:
                                        # if the in node of the edge is a depot and the out is a client
                                        tmp_graph.node[cycle[i]]['flow'] += maxi
                                        # we add the unit cost of the platform
                                    elif tmp_graph.node[cycle[i - 1]]['demand'] > 0 > \
                                            tmp_graph.node[cycle[i + 1]]['demand']:
                                        # if the in node of the edge is a client and the out is a depot
                                        tmp_graph.node[cycle[i]]['flow'] -= maxi
                                        # we deduce the unit cost of the platform
                                else:
                                    if tmp_graph.node[cycle[i - 1]]['demand'] < 0 < \
                                            tmp_graph.node[cycle[1]]['demand']:
                                        tmp_graph.node[cycle[i]]['flow'] += maxi
                                    elif tmp_graph.node[cycle[i - 1]]['demand'] > 0 > \
                                            tmp_graph.node[cycle[1]]['demand']:
                                        tmp_graph.node[cycle[i]]['flow'] -= maxi

                        break
            graph = tmp_graph
            print('\n##############################')
            print('# New better solution found! #')
            print('##############################')
            print_solution(graph)
        graph.graph['interrupted'] = False

    except KeyboardInterrupt:
        print('Optimization interrupted!', file=sys.stderr)
        graph.graph['interrupted'] = True
    finally:
        return graph


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
        if u != v:
            if graph.edge[u][v]['flow'] < graph.edge[u][v]['capacity']:
                gap_graph.add_edge(u, v,
                                   capacity=graph.edge[u][v]['capacity'] - graph.edge[u][v]['flow'],
                                   fixed_cost=graph.edge[u][v]['fixed_cost'], unit_cost=graph.edge[u][v]['unit_cost'],
                                   time=graph.edge[u][v]['time'])

            if graph.edge[u][v]['flow'] > 0:
                gap_graph.add_edge(v, u, capacity=graph.edge[u][v]['flow'],
                                   fixed_cost=-graph.edge[u][v]['fixed_cost'], unit_cost=-graph.edge[u][v]['unit_cost'],
                                   time=graph.edge[u][v]['time'])

    return gap_graph


def print_solution(graph):
    """Displays all info about the solution of the problem"""

    cost = 0

    for i in get_platform_list(graph):
        if graph.node[i]['flow'] > 0:
            cost += graph.node[i]['unit_cost'] * graph.node[i]['flow']
            print('Platform node #{} used with flow={}'.format(i, graph.node[i]['flow']))

    for u, v in graph.edges_iter():
        if graph.edge[u][v]['flow'] > 0:
            cost += graph.edge[u][v]['flow'] * graph.edge[u][v]['unit_cost'] + graph.edge[u][v]['fixed_cost']
            print('Edge #{} from node #{} to node #{} used with flow={}'.format(graph.edge[u][v]['id'], u, v,
                                                                                graph.edge[u][v]['flow']))
    print('Result: {}'.format(cost))


def test_feasability(graph):
    """Checks if a problem can or not be solved"""

    feasable = True

    for i in get_depot_list(graph):
        sum_flow = 0
        for j in graph.successors(i):
            sum_flow += graph.edge[i][j]['flow']
        if sum_flow != -graph.node[i]['demand']:
            feasable = False
            break

    graph.graph['feasable'] = feasable
    return feasable
