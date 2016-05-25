#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: run_all.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 24/05/2016 by Fouss

"""Runs run.py for each file in the data folder"""

import os
import sys


if len(sys.argv) == 2:
    files = os.listdir(sys.argv[1])
    files.sort()
    for file in files:
        os.system('/usr/bin/python3 run.py {}'.format(sys.argv[1] + '/' + file))
else:
    print('Usage: {} data_directory'.format(sys.argv[0]), file=sys.stderr)

