
import os
import platform
import socket
import re
import json

def safelower(s):
	if isinstance(s, str):
		return s.lower()
	else:
		return ''

def getpcname_raw():
    n1 = platform.node()
    n2 = socket.gethostname()
    n3 = os.environ["COMPUTERNAME"] if "COMPUTERNAME" in os.environ else ''
    if n1 == n2 == n3:
        return n1
    elif n1 == n2:
        return n1
    elif n1 == n3:
        return n1
    elif n2 == n3:
        return n2
    else:
        raise Exception("Computernames are not equal to each other")

def getpcname():
    x = getpcname_raw()
    x = safelower(x)
    x = re.sub(r'[^\d\w]+', "_", x)
    return x

config = None

def getconfig():
    global config
    if config:
    	return config
    fname = 'config_'+getpcname()+'.json'
    configforpc = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), fname)
    if os.path.exists(configforpc):
        with open(configforpc) as outfile:
            config = json.load(outfile)
            return config
    else:
        raise Exception('No config for computer. Expected: '+fname)


if __name__ == "__main__":
	print(getpcname())
else:
    getconfig()
