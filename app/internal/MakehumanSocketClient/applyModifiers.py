#!/usr/bin/python

import os
import sys
from mhrc.JsonCall import JsonCall
import json
from dotenv import load_dotenv

def usage():
    print("USAGE:\n")
    print("  applyModifiers.py <modifier json file name>\n")
    sys.exit(1)

for arg in sys.argv:
    print(arg + "\n")

if len(sys.argv) != 2:
    usage()

mods = sys.argv[1].replace("'", '"')
print(mods)
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

load_dotenv() 
ip = os.environ["MAKEHUMAN_IP"]
port = os.environ["MAKEHUMAN_PORT"]

if ip is None:
    ip = "172.16.15.156"
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



