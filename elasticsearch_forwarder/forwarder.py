# Copyright 2020, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#import ptvsd
#ptvsd.enable_attach(address=('192.168.170.200', 5678))
#ptvsd.wait_for_attach()

import os
import sys
import platform
import distro
import time
import logging
import argparse
import urllib3
import yaml

from elasticsearch import Elasticsearch, helpers
from datetime import datetime

def get_data(host_fields, extra_fields):
    for stdin_line in sys.stdin:
        line = stdin_line.strip()
        if line == '':
            continue

        logging.info('Message: %s', line)

        timestamp = int(time.time())
        timestamp_ms = timestamp * 1000

        doc = {
            '@timestamp': timestamp_ms,
            'message': line
        }
        doc.update(host_fields)
        doc.update(extra_fields)

        yield doc


def get_bulk_data(index, pipeline, host_fields, extra_fields):
    for doc in get_data(host_fields, extra_fields):
        data = {
            '_index': index,
            '_type': '_doc',
            '_source': doc,
            'pipeline': pipeline
        }

        logging.info('Document: %s', data)
        yield data


def main():
    # Certificate WARNING bug
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True,
                        help="Config file")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="Increase output verbosity")
    args = parser.parse_args()

    if args.verbosity == 2:
        loglevel = logging.DEBUG
    elif args.verbosity == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.ERROR

    logging.basicConfig(level=loglevel, 
                        filename='/var/log/elasticsearch-forwarder.log',
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    with open(args.config, 'r', encoding="utf-8") as config_file:
        config = yaml.load(config_file, Loader=yaml.Loader)

    es = Elasticsearch(
        config['elasticsearch']['hosts'],
        http_auth=(config['elasticsearch']['username'], config['elasticsearch']['password']),
        scheme=config['elasticsearch']['protocol'],
        port=config['elasticsearch']['port'],
        ca_certs=config['elasticsearch']['ssl']['certificate_authorities']
    )

    host_fields = {
        'host': {
            'name': platform.node(),
            'hostname': platform.node(),
            "os": {
                "kernel": platform.release(),
                "codename": distro.codename(),
                "name": distro.name(),
                'family': distro.like(),
                "version": distro.version(),
                "platform": distro.id()
            },
            "architecture": platform.machine()
        }
    }
    extra_fields = config['extra_fields']
    index = config['elasticsearch']['index']
    pipeline = config['elasticsearch']['pipeline']

    #helpers.bulk(es, get_bulk_data(index, pipeline, host_fields, extra_fields))
    for doc in get_data(host_fields, extra_fields):
        logging.info('Document: %s', data)
        res = es.index(index=index,  pipeline=pipeline, body=doc)
        logging.info("%s doc with id %s", res['result'], res['_id'])


if __name__ == '__main__':
    main()