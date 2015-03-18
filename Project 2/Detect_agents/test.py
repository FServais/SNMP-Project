from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

agents = {}

targets = [('hawk.run.montefiore.ulg.ac.be', 161, 1, 'run69Zork!'), ('hawk.run.montefiore.ulg.ac.be', 161, 2, 'run69Zork!')]

# Wait for responses or errors, submit GETNEXT requests for further OIDs
def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
        del agents[sendRequestHandle]
        return 1
    if errorStatus:
        print(errorStatus.prettyPrint())
        del agents[sendRequestHandle]
        return 1

# Send asynchronous requests to a list of devices ('targets') following the form :
# (ip, port, version, communityName).
# This function will populate the hashtable 'agents' with the targets
# that contains an agent.
# Note: Only for SNMPv1 and SNMPv2.
def discoverTargets(targets):
    for target in targets:
        ip, port, version, secName = target

        cmdGen  = cmdgen.AsynCommandGenerator()

        if version == 1:
            authData = cmdgen.CommunityData(secName, mpModel=0)
        elif version == 2:
            authData = cmdgen.CommunityData(secName)
        else:
            return
        
        transportTarget = cmdgen.UdpTransportTarget((ip, port))
        var = ( '1.3.6.1.2.1', )

        ret = cmdGen.nextCmd(
            authData,
            transportTarget,
            var,
            (cbFun, None),
            lookupNames=True, lookupValues=True
        )

        agents[ret] = target

    cmdGen.snmpEngine.transportDispatcher.runDispatcher()    

# =========================================== #


discoverTargets(targets)

for k in agents:
    print k, ' -> ', agents[k]
