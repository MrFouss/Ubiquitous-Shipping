#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: parser.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Parser for the transshipment solver project"""

import networkx as nx


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
            if line[0] == 'NODE:':
                new_graph.add_node(int(line[1]), x=float(line[2]), y=float(line[3]), demand=int(line[4]),
                                   unit_cost=float(line[5]), time=float(line[6]), flow=0)
            elif line[0] == 'EDGE:':
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
            elif '#' in line[0]:
                pass
            elif line[0] == 'EOF':
                break
            else:
                raise SyntaxError('File {} has syntax error at line {}'.format(self.file_path, i))

        file.close()

        return new_graph

    def export_to_file(self):
        """Exports the solution of the problem"""

        file = open(self.file_path+'.sol', 'w+')

        pass

        file.close()
