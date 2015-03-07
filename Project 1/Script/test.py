from pysnmp.entity.rfc3413.oneliner import cmdgen

def getNumberOfPackets(oid):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('run69Zork!'),
        cmdgen.UdpTransportTarget(('hawk.run.montefiore.ulg.ac.be', 161)),
        oid,
        lookupNames=True, lookupValues=True
    )

    if errorIndication:
        print(errorIndication)
        return
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
            return
        else:
            for name, val in varBinds:
                return val
            return


oid_received = (1,3,6,1,2,1,11,1,0)
oid_sent = (1,3,6,1,2,1,11,2,0)

packets_received = getNumberOfPackets(oid_received)
packets_sent = getNumberOfPackets(oid_sent)


