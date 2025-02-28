#!/usr/bin/python

import sys
from mhrc.JsonCall import JsonCall
import json
from dotenv import load_dotenv, dotenv_values
import os 

def usage():
    print("USAGE:\n")
    print("  applyModifiers.py <modifier json file name>\n")
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

if len(sys.argv) > 2:
    usage()

mods = sys.argv[1]
data = json.loads(mods)

jsc = JsonCall()

jsc.setFunction("applyModifiers")
# jsc.setParam("modifier",modname);
# jsc.setParam("power",modval);
# print(data)

for (key, value) in data.items():
    keySplit = key.split(' ')
    if keySplit[0] != "#":
        print(key + ' ' + value)
        jsc.setParam(key, value);

# loading variables from .env file
load_dotenv() 

ip = os.getenv("MAKEHUMAN_IP")
port = os.getenv("MAKEHUMAN_PORT")
if ip is None:
    up = "localhost"
if port is None:
    port = "12345"

response = jsc.send(ip, int(port))

if not response:
    print("Command failed (returned null response)\n")
    sys.exit(1)

if hasattr(response,"error") and getattr(response,"error"):
    print("ERROR: " + getattr(response,"error"))
    sys.exit(1)

print("OK")



