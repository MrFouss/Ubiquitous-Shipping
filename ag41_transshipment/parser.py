#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: parser.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Parser for the transshipment solver project"""

from edge import Edge
from graph import Graph
from node import Node


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

        name = ''
        nbr_nodes = -1
        nbr_edges = -1
        max_t = -1
        nodes = dict()
        edges = dict()

        i = 0

        for line in file.readlines():
            i += 1

            line = line.split()
            if line[0] == 'NODE:':
                nodes[int(line[1])] = Node(int(line[1]), float(line[2]), float(line[3]), int(line[4]), float(line[5]),
                                           float(line[6]))
            elif line[0] == 'EDGE:':
                edges[int(line[1])] = Edge(int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]),
                                           float(line[6]), float(line[7]))
            elif line[0] == 'NAME':
                name = line[2]
            elif line[0] == 'NBR_NODES':
                nbr_nodes = int(line[2])
            elif line[0] == 'NBR_EDGES':
                nbr_edges = int(line[2])
            elif line[0] == 'T':
                max_t = float(line[2])
            elif '#' in line[0]:
                pass
            elif line[0] == 'EOF':
                break
            else:
                raise SyntaxError('File {} has syntax error at line {}'.format(self.file_path, i))

        graph = Graph(name, max_t, nbr_nodes, nbr_edges, nodes, edges)

        file.close()
        return graph
