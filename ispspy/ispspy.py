#!/usr/bin/python3
import os
import sys
import os.path
import argparse
import traceback
import logging
import speedtest
from time import sleep
import time

__author__ = 'Mark Valdez'

"""
ISP Spy
Reports upload/download speeds using speedtest library.

Options:
    interval: wait time in minutes between tests
"""

SPEED_MARGIN_OF_ERROR = 3  # the margin in which your internet can be slower than you pay for
EXPECTED_UP = 180  # expected upload speed in Mbps
EXPECTED_DOWN = 180  # expected download speed in Mbps
LOG_FILE = 'isp-spy.csv'


def print_sys_info():
    print('-------------------')
    print('ISP Spy')
    print('Python Version Info: ' + sys.version)
    print('Author: ' + __author__)
    print('Current Working Directory: ' + os.getcwd())
    print('-------------------')
    print('')


def main(args):
    if args.header:
        logging.info("timestamp,id,sponsor,host,city,state,latency,ping,"
                     "download,upload,bytes_sent,bytes_received")
    while True:
        print('Testing speeds...')
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()

        print('Parsing results...')
        results = s.results.dict()
        logging.info("%s, %s, %s, %s, %s, %s, %s, %5.2f, %5.2f, %s, %s", results['timestamp'], results['server']['id'],
                     results['server']['sponsor'], results['server']['host'], results['server']['name'],
                     results['server']['latency'], results['ping'], (results['download'] / 1000.0 / 1000.0),
                     (results['upload'] / 1000.0 / 1000.0), results['bytes_sent'], results['bytes_received'])

        print("Download : {0:.3f} MB/s".format(results['download'] / 1000.0 / 1000.0))
        print("Upload   : {0:.3f} MB/s".format(results['upload'] / 1000.0 / 1000.0))

        if args.interval > 0:
            print("Next test in {delay} minute(s)...".format(delay=args.interval))
            countdown(args.interval)
            print("")
        else:
            break


def countdown(t):  # in minutes
    for remaining in range(t, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} minutes remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(60)


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(message)s"
    )


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval',
                        dest='interval',
                        type=int,
                        default=0,
                        help='Time interval between tests in minutes')
    parser.add_argument('--header',
                        dest='header',
                        default=False,
                        action='store_true',
                        help='Print headers to log file')
    return parser


if __name__ == '__main__':
    print_sys_info()
    print('Warming up...')
    setup_logging()
    op = configure_options()
    try:
        args = op.parse_args()
        main(args)
    except Exception as e:
        traceback.print_exc()
        op.print_help()
        sys.exit(1)
