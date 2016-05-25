#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: parser.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Parser for the transshipment solver project"""

from ag41_transshipment.solver import get_platform_list
import networkx as nx
import math


class Parser(object):
    """Parser class"""

    def __init__(self, file_path):
        """Creates the Parser object"""
        try:
            tmp = open(file_path, 'r')
            tmp.close()
            self.file_path = file_path
        except IOError:
            raise IOError('File {} doesn\'t exist'.format(file_path))

    def import_from_file(self):
        """Imports all informations about the problem"""

        file = open(self.file_path, 'r')

        new_graph = nx.DiGraph()

        i = 0

        for line in file.readlines():
            i += 1

            line = line.split()
            if '#' in line[0]:
                pass
            elif line[0] == 'NODE:':
                new_graph.add_node(int(line[1]), x=float(line[2]), y=float(line[3]), demand=int(line[4]),
                                   unit_cost=float(line[5]), time=float(line[6]), flow=0)
            elif line[0] == 'EDGE:':
                if float(line[4]) != 0:
                    new_graph.add_edge(int(line[2]), int(line[3]), id=int(line[1]), capacity=int(line[4]),
                                       fixed_cost=float(line[5]), unit_cost=float(line[6]), time=float(line[7]), flow=0)
            elif line[0] == 'NAME':
                new_graph.graph['name'] = line[2]
            elif line[0] == 'NBR_NODES':
                new_graph.graph['nbr_nodes'] = int(line[2])
            elif line[0] == 'NBR_EDGES':
                new_graph.graph['nbr_edges'] = int(line[2])
            elif line[0] == 'T':
                new_graph.graph['time'] = float(line[2])
            elif line[0] == 'EOF':
                break
            else:
                raise SyntaxError('File {} has syntax error at line {}'.format(self.file_path, i))

        file.close()

        return new_graph

    def export_to_file(self, init_graph, graph, u_time, s_time):
        """Exports the solution of the problem"""

        file = open(self.file_path + '.sol', 'w+')

        file.write('###############\n')
        file.write('# FILE LOADED #\n')
        file.write('###############\n\n')

        file.write('Problem file: {}\n'.format(self.file_path))
        file.write('Solution file: {}\n'.format(self.file_path + '.sol'))

        if graph.graph['feasible']:

            file.write('\n####################\n')
            file.write('# INITIAL SOLUTION #\n')
            file.write('####################\n\n')

            cost = 0
            for i in get_platform_list(init_graph):
                if init_graph.node[i]['flow'] > 0:
                    cost += init_graph.node[i]['unit_cost'] * init_graph.node[i]['flow']
                    file.write('Platform node #{} used with flow={}\n'.format(i, init_graph.node[i]['flow']))
            file.write('\n')
            for u, v in init_graph.edges_iter():
                if init_graph.edge[u][v]['flow'] > 0:
                    cost += init_graph.edge[u][v]['flow'] * init_graph.edge[u][v]['unit_cost'] + init_graph.edge[u][v]['fixed_cost']
                    file.write('Edge #{} from node #{} to node #{} used with flow={}\n'.format(init_graph.edge[u][v]['id'], u, v, init_graph.edge[u][v]['flow']))

            file.write('\nResult: {}\n'.format(cost))

            if graph.graph['interrupted']:
                file.write('\n#####################################\n')
                file.write('#        BEST SOLUTION FOUND        #\n')
                file.write('# The program has been interrupted! #\n')
                file.write('#####################################\n\n')
            else:
                file.write('\n####################\n')
                file.write('# OPTIMAL SOLUTION #\n')
                file.write('####################\n\n')

            cost = 0
            for i in get_platform_list(graph):
                if graph.node[i]['flow'] > 0:
                    cost += graph.node[i]['unit_cost'] * graph.node[i]['flow']
                    file.write('Platform node #{} used with flow={}\n'.format(i, graph.node[i]['flow']))
            file.write('\n')
            for u, v in graph.edges_iter():
                if graph.edge[u][v]['flow'] > 0:
                    cost += graph.edge[u][v]['flow'] * graph.edge[u][v]['unit_cost'] + graph.edge[u][v]['fixed_cost']
                    file.write('Edge #{} from node #{} to node #{} used with flow={}\n'.format(graph.edge[u][v]['id'], u, v,
                                                                                               graph.edge[u][v]['flow']))
            file.write('\nResult: {}\n'.format(cost))

            file.write('\n###################\n')
            file.write('# RESOLUTION TIME #\n')
            file.write('###################\n\n')

            u_hour = (u_time - (u_time % 3600.))/3600
            s_hour = (s_time - (s_time % 3600.))/3600

            u_time -= u_hour * 3600.
            s_time -= s_hour * 3600.

            u_min = (u_time - (u_time % 60.))/60
            s_min = (s_time - (s_time % 60.))/60

            u_time -= u_min * 60.
            s_time -= s_min * 60.

            file.write('Execution time:\n')
            file.write('\tUser time : {} hours, {} minutes and {} seconds\n'.format(u_hour, u_min, u_time))
            file.write('\tSystem time : {} hours, {} minutes and {} seconds\n'.format(s_hour, s_min, s_time))

        else:
            file.write('\nThe problem can\'t be solved!\n')

        file.close()
