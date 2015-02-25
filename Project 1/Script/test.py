from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

#oid = cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0), \
 #     cmdgen.MibVariable('SNMPv2-MIB', 'ipForwarding', 0), \
  #    cmdgen.MibVariable('SNMPv2-MIB', 'ifNumber', 0)

oid = (1,3,6,1,2,1,1,1,0), \
      (1,3,6,1,2,1,4,1,0), \
      (1,3,6,1,2,1,2,1,0);
#oid = sysDescr, ipForwarding, ifNumber

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('run69Zork!'),
    cmdgen.UdpTransportTarget(('hawk.run.montefiore.ulg.ac.be', 161)),
    *oid,
    lookupNames=True, lookupValues=True
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s\n' % (name.prettyPrint(), val.prettyPrint()))


