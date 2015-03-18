from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

agents = {}

target = ('hawk.run.montefiore.ulg.ac.be', 161, 1, 'run69Zork!')

# List of targets in the followin format:
# ( ( authData, transportTarget, varNames ), ... )
targets = (
    # 1-st target (SNMPv1 over IPv4/UDP)
    ( cmdgen.CommunityData(target[3], mpModel=0),
      cmdgen.UdpTransportTarget((target[0], target[1])),
      ( '1.3.6.1.2.1',) ),
    ( cmdgen.CommunityData(target[3]),
      cmdgen.UdpTransportTarget((target[0], target[1])),
      ( '1.3.6.1.2.1',) ),
    ( cmdgen.CommunityData('falseCumm'),
      cmdgen.UdpTransportTarget((target[0], target[1])),
      ( '1.3.6.1.2.1',) )
)

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


cmdGen  = cmdgen.AsynCommandGenerator()

# Submit initial GETNEXT requests and wait for responses
for authData, transportTarget, varNames in targets:

    #varBindHead = [ x[0] for x in cmdGen.makeReadVarBinds(varNames) ]

    ret = cmdGen.nextCmd(
        authData, transportTarget, varNames,
        # User-space callback function and its context
        (cbFun, None),
        lookupNames=True, lookupValues=True
    )
    agents[ret] = target

cmdGen.snmpEngine.transportDispatcher.runDispatcher()

for k in agents:
    print k, ' -> ', agents[k]
