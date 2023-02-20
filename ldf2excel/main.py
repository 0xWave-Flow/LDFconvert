import os
import json
import sys
import ldfparser
import LDFstruct
from dump import dumpp

if __name__ == "__main__":

    print("def : main - __main__")

    infile = ""
    outfile = ""
    infile = sys.argv[1]
    outfile = sys.argv[2]
    path = os.path.join(os.path.dirname(__file__), infile)
    ldf = ldfparser.parse_ldf_to_dict(path)
    print("def : main - LDF PARSER : {}".format(ldf))
    # dumpp(json.dumps(ldf), outfile)
    dumpp(ldf, outfile)
