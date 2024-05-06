#!/usr/bin/python

import sys
from mhrc.JsonCall import JsonCall
import json

def usage():
    print("USAGE:\n")
    print("  applyModifiers.py <modifier json file name>\n")
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

if len(sys.argv) > 2:
    usage()

modsFileName = sys.argv[1]
f = open(modsFileName)
data = json.load(f)

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

# TODO replace with ip and port got from env
response = jsc.send("localhost", "12345")

if not response:
    print("Command failed (returned null response)\n")
    sys.exit(1)

if hasattr(response,"error") and getattr(response,"error"):
    print("ERROR: " + getattr(response,"error"))
    sys.exit(1)

print("OK")



