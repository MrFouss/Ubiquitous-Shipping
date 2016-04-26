#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: run.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 17/04/2016 by Fouss

"""Running file for the transshipment solver project"""

from ag41_transshipment.app import Application
import sys
import time


if len(sys.argv) == 2:
    u_time = time.time()
    s_time = time.clock()

    APP = Application(sys.argv[1])

    print('\nExecution time (in seconds):')
    print('\tuser time: {}'.format(time.time() - u_time))
    print('\tsystem time: {}\n'.format(time.clock() - s_time))
else:
    print('Usage: {} data_file_name'.format(sys.argv[0]), file=sys.stderr)