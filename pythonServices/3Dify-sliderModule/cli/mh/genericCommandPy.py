#!/usr/bin/python

import sys
from cli.mh.mhrc.JsonCall import JsonCall

def sendCommand(command):
    jsc = JsonCall()
    jsc.setFunction(command)
    response = jsc.send()
    if not response:
        print("Command failed (returned null response)\n")
        sys.exit(1)
    if hasattr(response, "error") and getattr(response, "error"):
        print("ERROR: " + getattr(response, "error"))
        sys.exit(1)
    return response.getData()