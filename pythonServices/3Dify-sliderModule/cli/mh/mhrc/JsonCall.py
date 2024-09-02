#!/usr/bin/python

import re
import json
import socket
import numpy

# Why is the encoding routine even necessary? Why not simply use the 
# json.dumps function already available in the imported json library?
#
# Largely, this is because we want to format the floats with eight
# decimals no matter where in the hierarchy they appear, including
# converting strings containing numbers into real numbers. 
#
# Also, this way we can avoid accidentally including internal 
# makehuman data types (the encoding routine will croak on anything
# that isn't scalar, array or dict)

class JsonCall():


    def __init__(self,jsonData = None):        
        self.params = {}
        self.data = None
        self.function = "generic"
        self.error = ""

        if jsonData:
            self.initializeFromJson(jsonData)


    def initializeFromJson(self,jsonData):

        j = json.loads(jsonData)
        if not j:
            return
        self.function = j["function"]
        self.error = j["error"]
        if j["params"]:
            for key in j["params"]:
                self.params[key] = j["params"][key]
        if j["data"]:
            self.data = j["data"]


    def setData(self,data = ""):
        self.data = data


    def getData(self):
        return self.data


    def setParam(self,name,value):
        self.params[name] = value


    def getParam(self,name):
        if not name in self.params:
            return None        
        return self.params[name]


    def setFunction(self,func):
        self.function = func


    def getFunction(self):
        return self.function


    def setError(self,error):
        self.error = error


    def getError(self):
        return self.error


    def _guessValueType(self,val):

        if isinstance(val,bytes):
            return "string"

        if isinstance(val,str):
            return "string"

        if val == None:
            return "none"

        if self._isDict(val):
            return "dict"

        if self._isArray(val):
            return "array"

        if self._isNumeric(val):
            return "numeric"

        return "string"


    def _isArray(self,val):
        return (hasattr(val, '__len__') and (not isinstance(val, str)))


    def _isDict(self,val):
        return type(val) is dict


    def _isNumeric(self,val):
        if val == None:
            return False
        if isinstance(val,int):
            return True
        if isinstance(val,float):
            return True
        if isinstance(val,numpy.float32):
            return True
        if isinstance(val,numpy.float64):
            return True
        num_format = re.compile("^[\-]?[0-9][0-9]*\.?[0-9]+$")
        isnumber = re.match(num_format,str(val))
        return isnumber


    def _numberAsString(self,val):
        if isinstance(val,float):
            return "{0:.8f}".format(val)
        else:
            return str(val)


    def _dictAsString(self,val):
        ret = "{ "

        first = True

        for key in val.keys():
            if first:
                first = False
            else:
                ret = ret + ", "
            ret = ret + self.pythonValueToJsonValue(val[key],key)

        return ret + " }"


    def _arrayAsString(self,array):
        ret = "[ "
        n = len(array)
        for i in range(n):
            val = array[i]
            ret = ret + self.pythonValueToJsonValue(val)
            if i + 1 < n:
                ret += ","
        return ret + " ]"


    def pythonValueToJsonValue(self,val,keyName = None):

        out = ""

        if keyName:
            out = "\"" + keyName + "\": "

        vType = self._guessValueType(val)

        if val == None:
            return out + "null"

        if vType == "string":
            return out + "\"" + val.replace("\"","\\\"") + "\""

        if vType == "dict":
            return out + self._dictAsString(val)

        if vType == "array":
            return out + self._arrayAsString(val)

        if vType == "numeric":
            return out + self._numberAsString(val)

        return out + "\"" + str(val) + "\""


    def serialize(self):
        ret = "{\n";
        ret = ret + "  \"function\": \"" + self.function + "\",\n"
        ret = ret + "  \"error\": \"" + self.error + "\",\n"
        ret = ret + "  \"params\": {\n"

        first = True

        for key in self.params.keys():
            if not first:
                ret = ret + ",\n"
            else:
                first = False
            ret = ret + "    " + self.pythonValueToJsonValue(self.params[key],key) 

        ret = ret + "\n  },\n"

        ret = ret + "  " + self.pythonValueToJsonValue(self.data,"data") + "\n}\n"

        return ret


    def send(self, host="127.0.0.1", port=12345):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))   
        client.send(bytes(self.serialize(), 'utf-8'))
     
        data = ""
    
        while True:
            buf = client.recv(1024)
            if len(buf) > 0:
                data += buf.strip().decode('utf-8')
            else:
                break
    
        if data:
            return JsonCall(data)
        else:            
            return None


