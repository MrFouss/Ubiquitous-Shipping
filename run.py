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

if len(sys.argv) == 2:
    APP = Application(sys.argv[1])
else:
    print('Usage: {} data_file_name'.format(sys.argv[0]), file=sys.stderr)