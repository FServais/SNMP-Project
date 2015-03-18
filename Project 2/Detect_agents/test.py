from pysnmp.entity.rfc3413.oneliner import cmdgen

agents = {}

targets = [('hawk.run.montefiore.ulg.ac.be', 161, 1, 'run69Zork!'), 
('hawk.run.montefiore.ulg.ac.be', 161, 2, 'run69Zork!'),
('hawk.run.montefiore.ulg.ac.be', 161, 2, 'run69Zorky!')]

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

        cmdGen  = cmdgen.AsynCommandGenerator()

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

        agents[ret] = target

    cmdGen.snmpEngine.transportDispatcher.runDispatcher()    


# =========================================== #
#
# Beginning of the script
# 
# =========================================== #

discoverTargets(targets)

for k in agents:
    print k, ' -> ', agents[k]


