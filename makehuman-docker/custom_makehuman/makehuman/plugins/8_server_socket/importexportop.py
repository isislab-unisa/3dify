#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pprint
import math
import numpy as np
import time
import log
import events3d
import tempfile
import zipfile
import base64

from .abstractop import AbstractOp
from core import G

pp = pprint.PrettyPrinter(indent=4)

mhapi = G.app.mhapi
human = mhapi.internals.getHuman()

class ImportExportOps(AbstractOp):

    def __init__(self, sockettaskview):
        super().__init__(sockettaskview)

        # Sync operations
        self.functions["loadMhm"] = self.loadMhm
        self.functions["exportFbx"] = self.exportFbx
        self.functions["applyModifiers"] = self.applyModifiers

    def loadMhm(self,conn,jsonCall):
        human.load("D:\\Downloads\\output (1).mhm", True)
        jsonCall.setData("OK")

    def create_zip_file(self, directory, zip_filename):
        print("Creating zip file")
        print("DIRECTORY: ", directory)
        print("ZIP FILENAME: ", zip_filename)
        with zipfile.ZipFile(directory + "/" + zip_filename, "w") as zipf:
            rootzip = "myHuman/"
            for root, dirs, files in os.walk(directory):
                print("ROOT: ", root)
                print("DIRS: ", dirs)
                print("FILES: ", files)
                for directory in dirs:
                    zipf.write(os.path.join(root, directory), arcname=os.path.join(rootzip, directory) + "/")

                for file in files:
                    if ".zip" not in file:
                        if ".png" in file:
                            zipf.write(os.path.join(root, file), arcname=os.path.join(rootzip, os.path.join("textures", file)))
                        else:
                            zipf.write(os.path.join(root, file), arcname=os.path.join(rootzip, file))

        return
    
    def exportFbx(self,conn,jsonCall):
        tmpDirName = tempfile.mkdtemp()
        mhapi.exports.exportAsFBX(os.path.join(tmpDirName, 'myHuman.fbx'), False)
        #Cretae ZIP and return 
        self.create_zip_file(tmpDirName, 'myHuman.zip')
        print("Zip File Encoding Start")
        with open(tmpDirName + '/myHuman.zip', "rb") as zip_file:
            encoded_string = base64.b64encode(zip_file.read()).decode()
            jsonCall.setData(encoded_string)

    def applyModifiers(self, conn, jsonCall):
        for lh in list(G.app.loadHandlers.values()):
            lh(self, ['status', 'started'], True)

        event = events3d.HumanEvent(self, 'load')
        event.path = "./aaa.mhm"
        human.callEvent('onChanging', event)
        human.resetMeshValues()
        for key, value in jsonCall.params.items():
            linedata = key.strip().split() + value.strip().split()
            if linedata[0] == 'modifier':
                modifier = self.api.internals.getHuman().getModifier(linedata[1])
                if not modifier:
                    jsonCall.setError("No such modifier")
                    return
                self.api.modifiers.applyModifier(linedata[1], float(value), True)
            elif linedata[0] in G.app.loadHandlers:
                G.app.loadHandlers[linedata[0]](human, linedata, False)

        for lh in set(G.app.loadHandlers.values()):
            lh(self, ['status', 'finished'], True)
        human.blockEthnicUpdates = False        
        human._setEthnicVals()
        human.callEvent('onChanged', event)
        human.applyAllTargets()
        jsonCall.setData("OK")