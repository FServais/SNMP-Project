import re
from pysnmp.entity.rfc3413.oneliner import cmdgen

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

prefix = "24"
ip = "132.165.0.0"
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

targets1 = []
targets2 = []

for ip in list_ips:
    
    for config in t_configs:
        port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = config
        if(version == 3):        
            targets2.append((ip, port, version, sec_name))
        else :
            targets1.append((ip, port, version, sec_name))

print targets1
print targets2
agents = {}

# Callback function that removes the entry in the hashtable 'agent' if an
# error has occured (typically timeout)
def callbackFunction(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication or errorStatus:
        del agents[sendRequestHandle]
        return 1


# Send asynchronous requests to a list of devices ('targets') following the form :
# (ip, port, version, communityName).
# This function will populate the hashtable 'agents' with the targets
# that contains an agent.
# Note: Only for SNMPv1 and SNMPv2.
def discoverTargets(targets):
    

    # Iterate through all targets
    for target in targets:
        # Get the differents values of the tuple
        ip, port, version, secName = target

        # authData depending on the version
        if version == "3":
            continue

        cmdGen = cmdgen.AsynCommandGenerator()

        authData = None
        if version == "1":
            authData = cmdgen.CommunityData(secName, mpModel=0)
        elif version == "2":
            authData = cmdgen.CommunityData(secName)

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

        agents[ret] = target

    if cmdGen.snmpEngine.transportDispatcher is None:
        print "WTF?"
    cmdGen.snmpEngine.transportDispatcher.runDispatcher()
    
# Given a list of agents, write a XML file.
def XMLWriter(agentsList):
    
    targets = ET.Element("targets")
    
    for i in agentsList:
        
        target = ET.SubElement(targets, "target")
        
        ip,port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = i
        ET.SubElement(target, "ip", ).text = ip
        ET.SubElement(target, "port",).text = port
        ET.SubElement(target, "version", ).text = version
        ET.SubElement(target, "sec_name", ).text = sec_name
        if auth_proto != None:
            ET.SubElement(target, "auth_proto", ).text = auth_proto
        if auth_pwd != None:    
            ET.SubElement(target, "auth_pwd", ).text = auth_pwd
        if priv_proto != None:        
            ET.SubElement(target, "priv_proto", ).text = priv_proto
        if priv_pwd != None:
            ET.SubElement(target, "priv_pwd", ).text = priv_pwd
    
    
    
    
    tree = ET.ElementTree(targets)
    tree.write("filename.xml")

# =========================================== #
#
# Beginning of the detection part
# 
# =========================================== #

# discoverTargets(targets)

for k in agents:
    print k, ' -> ', agents[k]

