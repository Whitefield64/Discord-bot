import sys
import json
import os

def print_help():
    print("--<HELP WINDOW>--")
    print("Run with: python ./yourscript.py -jsap path.jsap")


def get_configured_jsap():
    if len(sys.argv) == 1 :
        #QUI SIAMO IN DOCKER
        print("####################################################################")
        mySAP = open("./Resources/default.jsap", 'r')
        _JSAP = json.load(mySAP)
        print("- Jsap loaded, overriding configuration")
        # OVERRIDE VARIABLES
        try:
            _JSAP["host"]=os.environ['HOST_NAME']
            print("- Env variable 'HOST_NAME' set with value: "+str(_JSAP["host"]))
        except:
            print("- Env variable 'HOST_NAME' not set, using default: "+str(_JSAP["host"]))
        finally:
            pass
        try:
            _JSAP["sparql11protocol"]["port"]=os.environ['HTTP_PORT']
            print("- Env variable 'HTTP_PORT' set with value: "+str(_JSAP["sparql11protocol"]["port"]))
        except:
            print("- Env variable 'HTTP_PORT' not set, using default: "+str(_JSAP["sparql11protocol"]["port"]))
        finally:
            pass
        try:
            _JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]=os.environ['WS_PORT']
            print("- Env variable 'WS_PORT' set with value: "+str(_JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]))
        except:
            print("- Env variable 'WS_PORT' not set, using default: "+str(_JSAP["sparql11seprotocol"]["availableProtocols"]["ws"]["port"]))
        finally:
            pass
        print("####################################################################")
    else:
        if sys.argv[1] == "-jsap": # OVERRIDE WITH COMMAND LINE ARGUMENT
            #QUI SIAMO IN LOCALHOST
            print("####################################################################")
            print("Loading custom jsap from: "+sys.argv[2])
            mySAP = open(sys.argv[2], 'r')
            _JSAP = json.load(mySAP)
            print("- Custom Jsap loaded, skipping environment variables override")
            print("Host: "+str(_JSAP["host"]))
            print("####################################################################")
        else:
            print("WARNING: unknown parameter: "+str(sys.argv[1]))
            print_help()
    return _JSAP    