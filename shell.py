#!/usr/bin/env python

# shell.py allows for console in Flask environment
import os
import readline
from pprint import pprint

from flask import *
from app import *

os.environ['PYTHONINSPECT'] = 'True'