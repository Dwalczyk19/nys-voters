import argparse
import csv
import json
import sys
from collections import OrderedDict


# Clean each field in a parsed CSV row:
# - Remove bad unicode character codes
# - Remove newlines and quotes
# - Empty strings are treated as None (for safety with INTEGER fields)
def clean(s):
    c = ''.join(c for c in str(s) if c not in ('"', "\n", "\r", "'"))
    return c if len(c) > 0 else None


def transform(infile, schemafile):
    schema = json.load(schemafile)
    print("Found " + str(len(schema)) + " fields", file=sys.stderr)
    print(schema, file=sys.stderr)
    reader = csv.reader(infile)
    for line in reader:
        if len(line) == len(schema):
            obj = OrderedDict(zip([f.get("name") for f in schema], [clean(elem) for elem in line]))
            print(json.dumps(obj))
        else:
            print("Error: only {} fields.".format(len(line)), file=sys.stderr)
            print("Line: ", line, file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('schemafile', type=argparse.FileType('r'))
    args = parser.parse_args()
    transform(args.infile, args.schemafile)
