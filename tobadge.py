#!/usr/bin/env python

# tobadge.py
# author:   Christian Sullivan
#           hanzo@freezerpants.com
#           http://freezerpants.com/toledo/
#
# About:    Script to control Amplus LED e-Badge
#
# Bugs:     None known so far
#
# ToDo:
#           
#
# License:
#           This software is licensed under a Creative Commons
#           Attribution-Noncommercial-Share Alike 3.0 United States License
#           Please see http://creativecommons.org/licenses/by-nc-sa/3.0/us/
#
#           If you find this software useful, have problems or suggestions,
#           Please email me at hanzo@freezerpants.com
#           If you wish to host this software elsewhere, please provide a link to
#           http://freezerpants.com and credit to Christian Sullivan
#
# Notes:    Requiring the -o flag is a little annoying, and really only useful for
##              the initial progressive code. Eventually we will just assume that the 
##              -o flag has been called.

import sys
import getopt
import serial
import time

def main(argv):
    # let's create the defaults
    # probably shouldn't be global
    global _port
    global _message
    global _raw
    global _speed
    global _debug
    global _version
    global _output
    global _loop
    global _count

    _port       = "COM7"
    _message    = "snicklfritz982342"
    _raw        = "0"
    _speed      = "3"
    _debug      = "0"
    _version    = "0.1"
    _output     = "0"
    _loop       = "0"
    _count      =  0
    
    try:
        opts, args = getopt.getopt(argv, "hrvom:p:s:l:d", ["help", "raw=", "version", "output", "message=", "port=", "speed=", "loop=", "debug"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-r", "--raw"):
            _raw = arg
            toraw()
            sys.exit()
        if opt in ("-v", "--version"):
            print "tobadge version", _version
        if opt == '--debug':
            _debug = 1
            print "set debugging ON"
        if opt in ("-p", "--port"):
            _port = arg
        if opt in ("-l", "--loop"):
            _loop = arg
        if opt in ("-m", "--message"):
            _message = arg
            toled()
        if opt in ("-o", "--output"):
            if (_message != "snicklfritz982342"):
                _output = 1
                toled()
            else:
                print "Message must be specified"
                sys.exit()
            
    source = "".join(args)
    
def speedFlag():
    global _speed
    if (_speed == "4"):
        _speed = '04' # slowest
    elif (_speed == "3"):
        _speed = '03'
    elif (_speed == "2"):
        _speed = '02'
    elif (_speed == "1"):
        _speed = '01'
    elif (_speed == "0"):
        _speed = '00' # fastest

def loopFlag():
    global _loop
    _loop = "%X" % int(_loop)

def count():
    # doesn't use a checksum like other amplus boards, this just counts characters
    global _count
    _count = len(_message)
    _count = "%X" % int(_count)
    
def toled():
    #run various functions to get tags
    speedFlag()
    loopFlag()
    count()

    finalMessage = "01%s%s10%s%s" % (_loop,_speed,_count,_message)
    if (_debug == 1):
        print finalMessage
    
    if (_output ==1):
        serout(finalMessage)
        
def toraw():
    # this is for sending straight up commands using protocol syntax to the LED sign
    ## basically all we do is create the checksum and send it off
    count()
    inMessage ="%s" % (_raw)
    finalMessage = "01%s%s" % (inMessage,_count)
    if (_debug == 1):
        print finalMessage
    serout(finalMessage)
    
def usage():
    print ""
    print "tobadge version", _version
    print "-------------------------------------------------------------------------"
    print " Always use flags --message and --output last"
    print "-------------------------------------------------------------------------"
    print ""
    print "-h (--help)       This screen"
    print "-v (--version)    Show tobadge version"
    print "-p (--port)       Set the port for use (default /dev/tty.usbserial)"
    print "-d (--debug)      Enable debug mode (same as verbose)"
    print "-s (--speed)      Set the movement speed, 0 is fastest (0-4)"
    print "-l (--loop)       Loop set amount of times, 0 is forever (0-255)"
    print "-r  --raw         Send protocol specific commands"
    print "                    Include the FULL string to send, between 01 and checksum"
    print "-m (--message)    Set the desired message (Up to 150 chars)"
    print "-o (--output)     Output to badge"
    print ""
    print "-------------------------------------------------------------------------"
    print 'example: ./tobadge.py --speed="0" --message="Holy Tobadge" --output'
    print 'example: ./toledo.py --port=/dev/tty.usbserial --message="Holy Tobadge" -o'
    print 'example: ./toledo.py -d -s="2" -l="243" -m="Holy Tobadge" -o'
    print ""

def serout(finalMessage):
   # set up serial port
    ser = serial.Serial(_port, 1200, timeout=3)
    # clear out the buffer 
    ser.flushInput()
    ser.flushOutput()
    ser.write (finalMessage)   
    # e-Badge doesn't produce a response, so just close and hope
    ser.close

if __name__ == "__main__":
    main(sys.argv[1:])
