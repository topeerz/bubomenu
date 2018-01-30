#!/usr/bin/python
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import bubomenu
from bubomenu.parsing import *

if __name__ == '__main__':
    print "Hello bubomenu"
    parser = bubomenu.parsing.MenuParser()

    with open('data.txt', 'r') as myfile:
        buffer = myfile.read()

    parser.parseBuffer(buffer)
    print parser.html()
