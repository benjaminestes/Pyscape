#! /usr/bin/env/ python3

import sys
import codecs

from pyscape.core import Pyscape
from pyscape.util.flagindex import FlagIndex
from pyscape.util.preset_handler import PresetHandler
from pyscape.util import custom
from pyscape.util import credentials
from pyscape.util import output

from pyscape.util.clean import *
from src.cli import *

def main():

    parser = build_parser()
    args = parser.parse_args()
    preset = get_preset(args)

    # load API credentials
    with open('keys.json', 'r') as k:
        creds = credentials.load(k)

    with open('data/bitflags.json') as b:
        flag_index = FlagIndex(b)

    with open('data/defaults.json') as d:
        ph = PresetHandler(d, flag_index)

    # Make sure URL is safe
    # This is OK for bulk-metrics since that uses
    # args.source directly
    url = clean_url(args.source)

    pys = Pyscape(*creds)
    pys.set_reporting(True)
    ph.set_preset(preset)

    if args.command != 'bulk-metrics' and \
       args.command != 'ose-style':
        data = pys.query(url, ph.get_args())
    elif args.command == 'bulk-metrics':
        # replace this call with custom.py 
        urls = []
        with open(args.source, 'r') as s:
            for line in s:
                # Make sure each line is clean
                urls.append(clean_url(line.rstrip()))
        data = custom.get_bulk_metrics(pys, urls, ph.get_args())
    elif args.command == 'ose-style':
        data = pys.query(url, ph.get_args())
        print("Writing OSE-style CSV.")
        with codecs.open(args.dest, 'w', encoding='utf-8') as outfile:
            output.ose_style(outfile, data)
        sys.exit()

    # write output
    print('Writing file.')
    with codecs.open(args.dest, 'w', encoding='utf-8') as outfile:
        if args.json:
            output.to_json(outfile, data)
        elif args.csv:
            output.to_csv(outfile, ph, preset, data)

if __name__ == '__main__':
    sys.exit(main())
