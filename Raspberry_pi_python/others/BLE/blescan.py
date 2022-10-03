#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import time
import os
import sys
from bluepy import btle


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            if self.opts.new:
                return
            status = "update"
        else:
            if not self.opts.all:
                return
            status = "old"

        if dev.rssi < self.opts.sensitivity:
            return

        print ('    Device (%s): %s (%s), %d dBm %s' %
               (status,
                   dev.addr,
                   dev.addrType,
                   dev.rssi,
                   ('' if dev.connectable else '(not connectable)'))
               )
        
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                print ('\t' + desc + ': \'' + val + '\'')
            else:
                print ('\t' + desc + ': <' + val + '>')
        if not dev.scanData:
            print ('\t(no data)')
        print


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

    print ("Scanning for devices..." )
    devices = scanner.scan(arg.timeout)

    if arg.discover:
        print ("Discovering services...")

        for d in devices:
            if not d.connectable:

                continue

            print ("Connecting to" + d.addr + ":")

            dev = btle.Peripheral(d)
            dump_services(dev)
            dev.disconnect()
            print

if __name__ == "__main__":
    main()
