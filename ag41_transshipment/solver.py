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


def initialize(graph):
    """Defines an initial solution of maximum flow for the transshipment problem (Edmonds-Karp Algorithm)"""
    graph = expand(graph)
    old_graph = graph.copy()

    # initialization of source node
    graph.add_node('s', demand=0, time=0, flow=0)
    for depot in get_depot_list(graph):
        graph.add_edge('s', depot, capacity=-graph.node[depot]['demand'], time=0, flow=0)
        graph.node['s']['demand'] -= graph.node[depot]['demand']

    # initialization of target node
    graph.add_node('t', demand=0, time=0, flow=0)
    for client in get_client_list(graph):
        graph.add_edge(client, 't', capacity=graph.node[client]['demand'], time=0, flow=0)
        graph.node['t']['demand'] += graph.node[client]['demand']

    # initialization of reverse edges
    for (u, v) in graph.edges():
        graph.add_edge(v, u, capacity=0, time=0, flow=0)

    # body of the maximum flow

    while True:

        # run a breadth first traversal to find the shortest path from the source to the path
        queue = ['s']
        pred = dict()
        while queue != []:
            u = queue.pop(0)
            for v in graph.successors(u):
                if v not in pred and v != 's' and graph.edge[u][v]['capacity'] > graph.edge[u][v]['flow']:
                    pred[v] = (u, v)
                    queue.append(v)

        # if there is no path from the source to the target
        if 't' not in pred:
            break

        # look for the biggest flow that can fit in the path
        df = float('infinity')
        prev = 't'
        while prev != 's':
            (u, v) = pred[prev]
            df = min(df, graph.edge[u][v]['capacity'] - graph.edge[u][v]['flow'])
            prev = u

        # update the flow of the chosen path
        prev = 't'
        while prev != 's':
            (u, v) = pred[prev]
            graph.edge[u][v]['flow'] += df
            graph.edge[v][u]['flow'] -= df
            prev = u

    # removal of excess edges and nodes
    for (u, v) in old_graph.edges():
        graph.remove_edge(v, u)
    for depot in get_depot_list(graph):
        graph.remove_edge('s', depot)
    graph.remove_node('s')
    for client in get_client_list(graph):
        graph.remove_edge(client, 't')
    graph.remove_node('t')

    return graph


def solve(graph):
    """Main solving function"""

    try:
        u_time = time.time()
        s_time = time.clock()

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
            print('##############################\n')
            print_solution(graph)

            u_tmp = time.time() - u_time
            s_tmp = time.clock() - s_time

            u_hour = (u_tmp - (u_tmp % 3600.)) / 3600
            s_hour = (s_tmp - (s_tmp % 3600.)) / 3600

            u_tmp -= u_hour * 3600.
            s_tmp -= s_hour * 3600.

            u_min = (u_tmp - (u_tmp % 60.)) / 60
            s_min = (s_tmp - (s_tmp % 60.)) / 60

            u_tmp -= u_min * 60.
            s_tmp -= s_min * 60.

            print('\nTime since beginning:')
            print('\tUser time : {} hours, {} minutes and {} seconds'.format(u_hour, u_min, u_tmp))
            print('\tSystem time : {} hours, {} minutes and {} seconds\n'.format(s_hour, s_min, s_tmp))

        graph.graph['interrupted'] = False

    except KeyboardInterrupt:
        print('Optimization interrupted!', file=sys.stderr)
        graph.graph['interrupted'] = True
    finally:
        return graph


def get_depot_list(graph):
    """Lists all depot nodes"""

    depot_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] < 0 and i != 's' and i != 't':
            depot_list.append(i)

    return depot_list


def get_platform_list(graph):
    """"Lists all platform nodes"""

    platform_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] == 0 and i != 's' and i != 't':
            platform_list.append(i)

    return platform_list


def get_client_list(graph):
    """"Lists all client nodes"""

    client_list = []
    for i in graph.nodes():
        if graph.node[i]['demand'] > 0 and i != 's' and i != 't':
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

    # for i in get_platform_list(graph):
    #     if graph.node[i]['flow'] > 0:
    #         cost += graph.node[i]['unit_cost'] * graph.node[i]['flow']
    #         print('Platform node #{} used with flow={}'.format(i, graph.node[i]['flow']))

    print()
    for u, v in graph.edges_iter():
        if graph.edge[u][v]['flow'] > 0:
            cost += graph.edge[u][v]['flow'] * graph.edge[u][v]['unit_cost'] + graph.edge[u][v]['fixed_cost']
            print('Edge #{} from node #{} to node #{} used with flow={}'.format(graph.edge[u][v]['id'], u, v,
                                                                                graph.edge[u][v]['flow']))
    print('\nResult: {}'.format(cost))


def test_feasibility(graph):
    """Checks if a problem can or not be solved"""

    feasible = True

    for i in get_depot_list(graph):
        sum_flow = 0
        for j in graph.successors(i):
            sum_flow += graph.edge[i][j]['flow']
        if sum_flow != -graph.node[i]['demand']:
            feasible = False
            break

    graph.graph['feasible'] = feasible
    return feasible


def expand(graph):
    """Change the graph to take care of time constraints"""
    tmp_graph = nx.DiGraph()
    for depot in get_depot_list(graph):
        # for each depot we create a platform and its edge to it
        tmp_graph.add_node(depot, demand=graph.node[depot]['demand'])
        for platform in get_platform_list(graph):
            if graph.has_edge(depot, platform):
                tmp_graph.add_node('DP' + str(depot) + str(platform), demand=0)
                edge = graph.edge[depot][platform]
                tmp_graph.add_edge(depot, 'DP' + str(depot) + str(platform), id=edge['id'],
                                   capacity=edge['capacity'], fixed_cost=edge['fixed_cost'],
                                   unit_cost=edge['unit_cost'], flow=0)
    for client in get_client_list(graph):
        tmp_graph.add_node(client, demand=graph.node[client]['demand'])
        for platform in get_platform_list(graph):
            # like for the depots
            if graph.has_edge(platform, client):
                tmp_graph.add_node('CP' + str(client) + str(platform), demand=0)
                edge = graph.edge[platform][client]
                tmp_graph.add_edge('CP' + str(client) + str(platform), client, id=edge['id'],
                                   capacity=edge['capacity'], fixed_cost=edge['fixed_cost'],
                                   unit_cost=edge['unit_cost'], flow=0)
            for depot in get_depot_list(graph):
                # if we can go from a depot to a client through a platform, the edge is created
                if tmp_graph.has_node('DP' + str(depot) + str(platform)):
                    t = graph.edge[depot][platform]['time']
                    t += graph.node[platform]['time']
                    t += graph.edge[platform][client]['time']
                    if t <= graph.graph['time']:
                        tmp_graph.add_edge('DP' + str(depot) + str(platform),
                                           'CP' + str(client) + str(platform),
                                           id=str(depot) + str(platform) + str(client),
                                           capacity=min(graph.edge[depot][platform]['capacity'],
                                                        graph.edge[platform][client]['capacity']),
                                           fixed_cost=0, unit_cost=graph.node[platform]['unit_cost'], flow=0)
    tmp_graph.graph['interrupted'] = False
    graph = tmp_graph
    return graph
