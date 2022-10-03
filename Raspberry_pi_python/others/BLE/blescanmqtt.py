#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import time
import os
import sys
import json
from bluepy import btle
Cloud_host = 'XXXXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXX'
###########################################
#insert the mqtt library here
import paho.mqtt.client as mqtt
time.sleep(1)

#######################################################

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
        :#######################################################
        if(dev.addr=='c5:85'):
			dbm = str(dev.rssi)
			adress = dev.addr#+','+dbm
			ble_data = {'name': 0 , 'tagId':0,'readerId':0 , 'rssi':0 , 'ls':0}
			#ble_data = {'Name': 0,'Tag':0,'Reader':0,'LastSeen':0}
			client = mqtt.Client()
			client.username_pw_set(ACCESS_TOKEN)
			client.connect(Cloud_host,1883,60)
			client.loop_start()
			ble_data['name'] = "Team_name"
			ble_data['tagId'] = adress
			ble_data['readerId'] = "RPi"
			ble_data['rssi'] = dbm
			ble_data['ls'] = time.asctime(time.localtime(time.time()))             
			client.publish('v1/devices/me/telemetry', json.dumps(ble_data),1)
			print (json.dumps(ble_data))
			client.loop_stop()
		###########################################################
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
