import re
from pysnmp.entity.rfc3413.oneliner import cmdgen
from Queue import Queue
from threading import Thread

# Read file
config_file = open('config.txt', 'r')

ip = config_file.readline()
configs = []

for line in config_file:
    configs.append(line)

# Matching the IP
match_ip = re.match('([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/([0-9]{1,2})', ip)
#print "IP:     ", match_ip.group(1)
#print "PREFIX: ", match_ip.group(2)

ip = match_ip.group(1)
prefix = match_ip.group(2)

# tuple containing the IP line
t_ip = (ip, prefix)

# list of tuple containing the fields of the configurations
t_configs = []

# Matching the configurations
for config in configs:
    comp_config = re.compile('([0-9]+) ([123]) (\S+)')
    match_config = re.match(comp_config, config)
    
    if match_config.group(1) is None or match_config.group(2) is None or match_config.group(3) is None:
        continue

    port = match_config.group(1)
    version = match_config.group(2)
    sec_name = match_config.group(3)
    auth_proto = None
    auth_pwd = None
    priv_proto = None
    priv_pwd = None

    if version is "3":
        comp_config = re.compile('([0-9]+) ([123]) (\S+)( (MD5|SHA) (\S*)( (DES|AES) (\S*))?)?')
        match_config = re.match(comp_config, config)
        
        if match_config.group(5) is None or match_config.group(6) is None:
            continue

        auth_proto = match_config.group(5)
        auth_pwd = match_config.group(6)

        if match_config.group(8) is None or match_config.group(9) is None:
            continue

        priv_proto = match_config.group(8)
        priv_pwd = match_config.group(9)

    
#   print port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd

    t_configs.append((port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd))


list_ip = ip.split(".", 4)
list_int_ip = [0, 0, 0, 0]

for i in range(0,4):
    list_int_ip[i] = int(list_ip[i]);

suffix = 32 - int(prefix)
left = suffix%8
nb_full_loops = suffix/8
nb_loops = nb_full_loops

if left != 0 :
    nb_loops = nb_full_loops + 1
    
max_nb_loop = [1, 1, 1, 1]
for i in range(0,4):
    
    if i < nb_full_loops:
        max_nb_loop[i] = 256
        
    elif i < nb_loops:
        max_nb_loop[i] = pow(2,left)
        
list_ips = []

oct = [list_int_ip[0], 0, 0, 0]
for i in range(0, max_nb_loop[3]):
    
    oct[1] = list_int_ip[1]
    for j in range(0, max_nb_loop[2]):
        
        oct[2] = list_int_ip[2]
        for k in range(0, max_nb_loop[1]):
            
            oct[3] = list_int_ip[3]
            for l in range(0, max_nb_loop[0]):
                
                list_ips.append(str(oct[0])+"."+str(oct[1])+"."+str(oct[2])+"."+str(oct[3]))
                oct[3] += 1
                 
            oct[2] += 1
            
        oct[1] +=1
   
    oct[0] += 1

targets = []
for ip in list_ips:
    
    for config in t_configs:
        port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = config
        targets.append((ip, port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd))




agentsV1V2 = {}
agents = []


class Worker(Thread):
    def __init__(self, requests, responses):
        Thread.__init__(self)
        self.requests = requests
        self.responses = responses
        self.cmdGen = cmdgen.CommandGenerator()
        self.setDaemon(True)
        self.start()
    
    def run(self):
        while True:
            target = self.requests.get()
            ip, port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = target
            
            authProtocol = None
            if auth_proto == "SHA":
                authProtocol=cmdgen.usmHMACSHAAuthProtocol
            elif auth_proto == "MD5":
                authProtocol=cmdgen.usmHMACMD5AuthProtocol
            else:
                authProtocol=cmdgen.usmNoAuthProtocol

            privProtocol = None
            if priv_proto == "DES":
                privProtocol=cmdgen.usmDESPrivProtocol
            elif priv_proto == "AES":
                privProtocol=cmdgen.usmAesCfb128Protocol
            else:
                privProtocol=cmdgen.usmNoPrivProtocol

            try:
                errorIndication, errorStatus, errorIndex, varBinds = self.cmdGen.getCmd(
                        cmdgen.UsmUserData(sec_name, auth_pwd, priv_pwd,
                                           authProtocol,
                                           privProtocol),
                        cmdgen.UdpTransportTarget((ip, int(port))),
                        '1.3.6.1.2.1.1.1.0'
                    )
                if errorIndication:
                    print target, " ??? -> ", errorIndication
                else : 
                    if errorStatus:
                        print target, " ??? -> "
                        print('%s at %s' % (
                            errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                            )
                        )
                    else:
                       agents.append(target)

                self.requests.task_done()

            except:
                print "PySnmpError"
                self.requests.task_done()

            

class ThreadPool:
    def __init__(self, num_threads):
        self.requests = Queue(num_threads)
        self.responses = []
        for _ in range(num_threads):
            Worker(self.requests, self.responses)

    def addRequest(self, target):
        self.requests.put(target)

    def getResponses(self): return self.responses

    def waitCompletion(self): self.requests.join()


# Callback function that removes the entry in the hashtable 'agent' if an
# error has occured (typically timeout)
def callbackFunction(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication or errorStatus:
        del agentsV1V2[sendRequestHandle]
        return 1


# Send asynchronous requests to a list of devices ('targets') following the form :
# (ip, port, version, communityName).
# This function will populate the hashtable 'agentsV1V2' with the targets
# that contains an agent.
# Note: Only for SNMPv1 and SNMPv2.
def discoverTargets(targets):
    

    # Iterate through all targets
    for target in targets:
        # Get the differents values of the tuple
        ip, port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = target

        # authData depending on the version
        if version == "3":
            continue

        cmdGen = cmdgen.AsynCommandGenerator()

        authData = None
        if version == "1":
            authData = cmdgen.CommunityData(sec_name, mpModel=0)
        elif version == "2":
            authData = cmdgen.CommunityData(sec_name)

        transportTarget = cmdgen.UdpTransportTarget((ip, int(port)))
        var = ( '1.3.6.1.2.1', )

        # Make and send request
        ret = cmdGen.nextCmd(
            authData,
            transportTarget,
            var,
            (callbackFunction, None),
            lookupNames=True, lookupValues=True
        )

        agentsV1V2[ret] = target

    try:
        cmdGen.snmpEngine.transportDispatcher.runDispatcher()
    except:
        del agentsV1V2[ret]



def discoverTargetsV3(targets):
    pool = ThreadPool(10)

    for target in targets:
        ip, port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = target

        if version != "3":
            continue

        """
        cmdGen = cmdgen.CommandGenerator()

        authProtocol = None
        if auth_proto == "SHA":
            authProtocol=cmdgen.usmHMACSHAAuthProtocol
        elif auth_proto == "MD5":
            authProtocol=cmdgen.usmHMACMD5AuthProtocol
        else:
            authProtocol=cmdgen.usmNoAuthProtocol

        privProtocol = None
        if priv_proto == "DES":
            privProtocol=cmdgen.usmDESPrivProtocol
        elif priv_proto == "AES":
            privProtocol=cmdgen.usmAesCfb128Protocol
        else:
            privProtocol=cmdgen.usmNoPrivProtocol

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.UsmUserData(sec_name, auth_pwd, priv_pwd,
                               authProtocol,
                               privProtocol),
            cmdgen.UdpTransportTarget((ip, int(port))),
            ( '1.3.6.1.2.1' )
        )

        if not errorIndication and not errorStatus:
            agents.append(target)
        """
        pool.addRequest(target)
        print target, " added to queue\n"

    pool.waitCompletion()
    print "Completed\n"
    """
    # Walk through responses
    for errorIndication, errorStatus, errorIndex, varBinds in pool.getResponses():
        if errorIndication:
            print(errorIndication)
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )
            )
        else:
           agents.append(target)
    """




# =========================================== #
#
# Beginning of the detection part
# 
# =========================================== #

#discoverTargets(targets)

#for k in agentsV1V2:
 #   agents.append(agentsV1V2[k])

discoverTargetsV3(targets)

for agent in agents:
    print agent, " -> OK!\n"

