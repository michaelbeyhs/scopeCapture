#!/usr/bin/env python3

import visa
import sys
import argparse
from datetime import datetime

# setup arguments
parser = argparse.ArgumentParser(description='Agilent/Keysight InfiniiVision screendump tool')
parser.add_argument('filename', nargs='?', help = 'filename to write the output image to')
parser.add_argument('-l', '--list', help = 'display found devices', action='store_true')
parser.add_argument('-d', '--device', help = 'device ID to connect to')
parser.add_argument('-i', '--inksaver', help = 'enable inksaver', default = 0, type = int, choices = [0, 1])
parser.add_argument('-v', '--verbose', help = 'be verbose', action='store_true')
args = parser.parse_args()

fileName = ''

# init VISA
rm = visa.ResourceManager('')
resources = rm.list_resources()

if len(resources) == 0:
    print('no devices found')
    sys.exit(-1)

if args.list:
    for i in resources:
        print(i)
    sys.exit(0)

if args.filename == None:
    print('No filename specified. Generating filename:')
    dt = datetime.now()
    fileName = dt.strftime("Scope_%Y%m%d_%H%M%S.png")
    print(fileName)
else:
    fileName = args.filename

if args.device == None:
    args.device = resources[0]

if args.verbose:
    print('Using device %s.' % args.device)


scope = rm.open_resource(args.device, encoding = 'iso8859-1')
scope.timeout = 10000 # timeout in ms

if args.verbose:
    print('Device IDN is %s.' % scope.query("*IDN?").strip())

# configure ink saver (black background as seen on screen)
scope.write(':HARDcopy:INKSaver %u' % args.inksaver)

# get screen data
data = scope.query_binary_values(':DISPlay:DATA? PNG, COLOR', datatype='B')

# write it to file
newfile=open(fileName,'wb')
newfile.write(bytearray(data))