#!/usr/bin/python3
# -*- coding: utf8 -*-

# File: run_all.py
#
# By Maxime Brodat <maxime.brodat@fouss.fr>
#
# Created: 24/05/2016 by Fouss

"""Runs run.py for each file in the data folder"""

import os


for file in os.listdir('../data'):
    os.system('/usr/bin/python3 run.py {}'.format(file))
