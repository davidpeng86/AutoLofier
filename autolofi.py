#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
You can make more complicated longer tests to test other functionality
or to generate screenshots etc in other scripts.
Make sure Audacity is running first and that mod-script-pipe is enabled
before running this script.
Requires Python 2.7 or later. Python 3 is strongly recommended.
"""

"""
everything needs to be lowercase
0 space in filename is suggested
"""

import os
import re
import sys
import codecs

SOURCE = 'Jay'
OUTPUT = 'result'

AudacityPort = 31117

if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")

def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

def quick_test():
    """Example list of commands."""
    do_command('Help: Command=Help')
    do_command('Help: Command="GetInfo"')
    #do_command('SetPreference: Name=GUI/Theme Value=classic Reload=1')

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

for files in os.walk(SOURCE):
#    print(files[0])
    if files[0] != os.path.join(SOURCE,OUTPUT):
        output = os.path.join(OUTPUT,files[0])
        if not os.path.exists(output):
            os.makedirs(output)

    for folders in os.walk(files[0]):
        for foldername in folders[1]:
            filepath = os.path.join(SOURCE,foldername)
            outputdir = os.path.join('Jay',foldername)
            outputpath = os.path.join(OUTPUT,outputdir)
            if not os.path.exists(outputpath):
                os.makedirs(outputpath)
            for songs in os.walk(filepath):
                for songtitle in songs[2]:
                    isaudio = re.search("mp3|flac", songtitle)
                    if isaudio:
                        audiopath = os.path.abspath(os.path.join(filepath, songtitle))
                        exportpath = repr(os.path.abspath(os.path.join(outputpath, songtitle)))[1:-1]
                        if not os.path.exists(exportpath):
                            do_command('Import2:Filename=%s' % audiopath)
                            do_command('ChangeTempo:percentage=%d' % -15)
                            do_command('ChangePitch:percentage=%d' % -5)
                            do_command('Low-passFilter:frequency=%d' % 1400)
                            do_command('Reverb:RoomSize=%dReverberance=%dDamping=%d' % (100, 60,65))

                            do_command('Export2:Filename=%s' %  codecs.decode(exportpath.encode(), 'utf-8'))
                            do_command('TrackClose:')
            