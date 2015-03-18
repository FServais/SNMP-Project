from pysnmp.entity.rfc3413.oneliner import cmdgen

agents = []

agentsV1V2 = {}

targets = [('hawk.run.montefiore.ulg.ac.be', 161, 3, 'run69Zork!', None, None, None, None), 
('hawk.run.montefiore.ulg.ac.be', 161, 3, 'run69Zork!', None, None, None, None),
('hawk.run.montefiore.ulg.ac.be', 161, 3, 'run69Zorky!', None, None, None, None)]


"""
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
        ip, port, version, secName = target

        cmdGen = cmdgen.AsynCommandGenerator()

        # authData depending on the version
        if version == 1:
            authData = cmdgen.CommunityData(secName, mpModel=0)
        elif version == 2:
            authData = cmdgen.CommunityData(secName)
        else:
            return
        
        transportTarget = cmdgen.UdpTransportTarget((ip, port))
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

    cmdGen.snmpEngine.transportDispatcher.runDispatcher()    


# =========================================== #
#
# Beginning of the script
# 
# =========================================== #

discoverTargets(targets)

for k in agentsV1V2:
    print k, ' -> ', agentsV1V2[k]
    agents.append(agentsV1V2[k])

"""

def discoverTargetsV3(targets):
    for target in targets:
        ip, port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = target

        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.UsmUserData('JohnSmith', 'Fei)bu7re', 'Kaeph-ah9',
                               authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                               privProtocol=cmdgen.usmAesCfb128Protocol),
            cmdgen.UdpTransportTarget(('hawk.run.montefiore.ulg.ac.be', 161)),
            ( '1.3.6.1.2.1' )
        )

        if not errorIndication and not errorStatus:
            agents.append(target)

discoverTargetsV3(targets)

for agent in agents:
    print agent,
