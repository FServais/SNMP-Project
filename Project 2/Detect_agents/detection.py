
from pysnmp.entity.rfc3413.oneliner import cmdgen

"""
# Function that get the value of the object with the oid 'oid' on "ip":"port".
# id        : ip address of the targeted router
# port      : port on the targeted router
# version   : SNMP version to use
# community : community name
# oid       : OID from which we want to get the value. (tuple)
def getValue(ip, port, version, community, oid):
    cmdGen = cmdgen.AsynCommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((ip, port)),
        oid,
        lookupNames=True, lookupValues=True
    )

    if errorIndication or errorStatus:
        return
    else:
    	for name, val in varBinds:
    		return val
	return

# Function that check if the device at "ip":"port" has an agent.
# id        : ip address of the targeted router
# port      : port on the targeted router
# version   : SNMP version to use
# community : community name
def isAgent(ip, port, version, community):
	return getValue(ip, port, version, community, (1,3,6,1,2,1,1,1)) is None

print isAgent("hawk.run.montefiore.ulg.ac.be", 161, 2, "run69Zork!")
"""

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
        return
    if errorStatus:
        print('%s at %s' % \
            (errorStatus.prettyPrint(),
             errorIndex and varBinds[int(errorIndex)-1] or '?')
        )
        return
    
    for oid, val in varBinds:
        if val is None:
            print(oid.prettyPrint())
        else:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

cmdGen  = cmdgen.AsynCommandGenerator()

for varName in ( cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0),
                 cmdgen.MibVariable('SNMPv2-SMI', 'directory', 0),
                 cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0) ):
    cmdGen.getCmd(
        cmdgen.CommunityData('run69Zork!'),
        cmdgen.UdpTransportTarget(('hawk.run.montefiore.ulg.ac.be', 161)),
        (varName,),
        (cbFun, None)
    )

cmdGen.snmpEngine.transportDispatcher.runDispatcher()

"""
def cbFun(sendRequestHandle, errorIndication, \
          errorStatus, errorIndex, varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
        return
    if errorStatus:
        print('%s at %s' % \
           (errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
        )
        return
    
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            if val is None:
                return    # stop table retrieval
            else:
                print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

    return True  # continue table retrieval

cmdGen  = cmdgen.AsynCommandGenerator()

for transportTarget in ( cmdgen.UdpTransportTarget(('hawk.run.montefiore.ulg.ac.be', 161)),
                         cmdgen.UdpTransportTarget(('192.168.1.1', 161)),
                         cmdgen.UdpTransportTarget(('10.40.1.1', 161)) ):
    cmdGen.nextCmd(

        #cmdgen.UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
        cmdgen.CommunityData('run69Zork!'),
        transportTarget,
        ( cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr'), ),
        (cbFun, None)
    )

cmdGen.snmpEngine.transportDispatcher.runDispatcher()
"""



