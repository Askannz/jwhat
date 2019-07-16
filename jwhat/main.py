import sys
import argparse
import json
from .data_collapse import collapse_data
from .print import print_data

VERSION = 0.1

def main():

    parser = argparse.ArgumentParser(description="A tool to summarize JSON files")

    parser.add_argument('file', metavar="FILE", nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='Input file name containing a valid JSON.')
    parser.add_argument('-v', '--version', action='store_true', help='Print version and exit.')
    parser.add_argument('-d', '--max-depth', action="store", type=int, default=-1, help="Maximum tree depth")
    parser.add_argument('--no-color', action="store_true", help="Disable colored output")
    args = parser.parse_args()

    try:
        data = json.loads(args.file.read())
    except json.decoder.JSONDecodeError as e:
        print("JSON parsing error : %s\n" % str(e))
        sys.exit(1)

    collapsed_data = collapse_data(data)

    print_data(collapsed_data, max_depth=args.max_depth, no_color=args.no_color)


if __name__ == "__main__":
    main()
