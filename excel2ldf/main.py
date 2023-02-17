import os
import json
import sys
from curses.ascii import isdigit

import ldfparser
from dump import dumpp
import xlrd
from collections import OrderedDict
import json

if __name__ == "__main__":

    print("def : main - __main__")

    infile = ""
    outfile = ""
    infile = sys.argv[1]
    outfile = sys.argv[2]
    path = os.path.join(os.path.dirname(__file__), infile)
    wb = xlrd.open_workbook(path)
    path2 = os.path.join(os.path.dirname(__file__), outfile)
    dumpp(infile, outfile)
