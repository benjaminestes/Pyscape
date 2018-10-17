#! /usr/bin/env/ python3

import argparse
import codecs
import csv
import json
import sys

from pyscape import Pyscape
from pyscape.fields import FIELDS

from time import time
from time import sleep
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from concurrent.futures import ThreadPoolExecutor

def batch_urls(urls, n):
    """n = size of batches. 10 is recommended."""
    for i in range(0, len(urls), n):
        yield urls[i:i+n]

def write_csv(outfile, data):
    "generate csv output"

    output = []
    headers = []
    keys = ["uu",
            "us",
            "upl",
            "ueid",
            "peid",
            "uipl",
            "pid",
            "pmrp",
            "ptrp",
            "upa",
            "pda",
            "ut",
            ]
        
    for k in keys:
        try:
            headers.append(FIELDS[k]['human'])
        except:
            headers.append(k)

    output.append(headers)

    for record in data:
        line = []
        try:
            for k in keys:
                if k in record:
                    line.append(record[k])
                else:
                    line.append('')
            output.append(line)
        except:
            output.append(['Error parsing line.'])

    writer = csv.writer(outfile, delimiter = ',',
                        quotechar = '"',
                        dialect = 'excel',
                        quoting = csv.QUOTE_ALL)
    writer.writerows(output)

def read_txt(textFile):
    fh = open(textFile, 'r')
    api_id = []
    api_key = []
    for line in fh.readlines():
        yh = line.strip().split('|')
        api_id.append(yh[0])
        api_key.append(yh[1])
    fh.close()
    return (api_id, api_key)

def get_url():
    args = parser.parse_args()
    # List URLs
    urls = []
    with open(args.src, 'r') as s:
        for line in s:
            urls.append(line.rstrip())
    return urls


def worker_API(worker_id, worker_key, urls):
    p = Pyscape(worker_id, worker_key)
    # Getting the datas (request)
    data = []
    for batch in batch_urls(urls, 10): # (ursl, n) : n urls at a time
        data.extend(p.batch_url_metrics(batch).json())
        print('%s URLs returned' % (len(data)))
        sleep(10) # Because every request needs 10 secs break
    return data

parser = argparse.ArgumentParser(description = 'Interface with the Mozscape API to provide link metrics')
parser.add_argument('src', help = 'specify a text file with URLs')
parser.add_argument('dest', help = 'specify an output file')

def main():
    ts = time() # starting timer
    urls = get_url() # get url from urls.txt to the list
    args = parser.parse_args()
    # -- Get the API from api.txt to the list
    # api.txt syntax : access_ID|secret_key. Each API separated by new line
    (api_id, api_key) = read_txt('api.txt')

    dataUrl = []
    urls_list = []
    # -- Define the maximum total domain per API
    # for example : 30 domains with 3 API
    # each API will process 10 domains
    urls_to_request = int(len(urls)/len(api_id))
    for i in range (1, len(api_id)+1):
        x = (i-1)*urls_to_request
        y = i*urls_to_request
        urls_list.append(urls[x:y])

    # -- Multi Threading Pool
    with ThreadPoolExecutor() as executor:
        for API, API_output in zip(api_id, executor.map(worker_API, api_id, api_key, urls_list)): # API variable should be ignored
            dataUrl = dataUrl + API_output # append the result every API done the work

    # Generate .csv
    with codecs.open(args.dest, 'w', encoding='utf-8') as outfile:
        write_csv(outfile, dataUrl)
    logging.info('Took %s', time() - ts)

if __name__ == '__main__':
    sys.exit(main())