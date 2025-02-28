#!/usr/bin/python

import sys
from mhrc.JsonCall import JsonCall
from dotenv import load_dotenv, dotenv_values
import os 

def usage():
    print("USAGE:\n")
    print("  genericCommand.py <command> [parameter name] [parameter value]\n")
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

if len(sys.argv) == 3:
    usage()

if len(sys.argv) > 4:
    usage()

function = sys.argv[1]
argname = None
argval = None

if len(sys.argv) > 2:
    argname = sys.argv[2]
    argval = sys.argv[3]

jsc = JsonCall()
jsc.setFunction(function)
if argname:
    jsc.setParam(argname,argval)

# loading variables from .env file
load_dotenv() 

ip = os.getenv("MAKEHUMAN_IP")
port = os.getenv("MAKEHUMAN_PORT")
if ip is None:
    up = "localhost"
if port is None:
    port = "12345"

response = jsc.send(ip, port)

if not response:
    print("Command failed (returned null response)\n")
    sys.exit(1)

if hasattr(response,"error") and getattr(response,"error"):
    print("ERROR: " + getattr(response,"error"))
    sys.exit(1)

print(response.getData())


