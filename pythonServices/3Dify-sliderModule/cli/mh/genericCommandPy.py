#!/usr/bin/python

import os
import sys
from cli.mh.mhrc.JsonCall import JsonCall
from dotenv import load_dotenv 

def sendCommand(command):
    jsc = JsonCall()
    jsc.setFunction(command)

    load_dotenv()
    ip = None
    port = None
    
    parent_dir = os.path.join(os.getcwd(), "..")
    up_dir = os.listdir(parent_dir)
    if ".dockerenv" in up_dir:
        print("Running in Docker")
        try: 
            ip = os.environ["MAKEHUMAN_IP"]
            port = os.environ["MAKEHUMAN_PORT"]
        except KeyError:
            ip = None
            port = None
    else:
        print("Running locally")
        
        
    if ip is None:
        ip = "localhost"
    if port is None:
        port = "12345"
        
    print("ip " + ip)
    print("port " + port)

    try:
        response = jsc.send(ip, int(port))
    except Exception as e:
        raise RuntimeError("Could not connect to Makehuman Daemon")

    if not response:
        print("Command failed (returned null response)\n")
        sys.exit(1)
    if hasattr(response, "error") and getattr(response, "error"):
        print("ERROR: " + getattr(response, "error"))
        sys.exit(1)
    return response.getData()


def sendCommandParameters(command, parameters):
    jsc = JsonCall()
    jsc.setFunction(command)

    load_dotenv()
    ip = None
    port = None
    
    parent_dir = os.path.join(os.getcwd(), "..")
    up_dir = os.listdir(parent_dir)
    if ".dockerenv" in up_dir:
        print("Running in Docker")
        try: 
            ip = os.environ["MAKEHUMAN_IP"]
            port = os.environ["MAKEHUMAN_PORT"]
        except KeyError:
            ip = None
            port = None
    else:
        print("Running locally")

    if ip is None:
        ip = "localhost"
    if port is None:
        port = "12345"
        
    print("ip " + ip)
    print("port " + port)
        
    for (key, value) in parameters.items():
        keySplit = key.split(' ')
        if keySplit[0] != "#":
            print(key + ' ' + value)
            jsc.setParam(key, value)
    try:
        response = jsc.send(ip, int(port))
    except Exception as e:
        raise RuntimeError("Could not connect to Makehuman Daemon")
    
    if not response:
        print("Command failed (returned null response)\n")
        sys.exit(1)
    if hasattr(response, "error") and getattr(response, "error"):
        print("ERROR: " + getattr(response, "error"))
        sys.exit(1)
    return response.getData()