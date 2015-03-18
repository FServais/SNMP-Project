from pysnmp.entity.rfc3413.oneliner import cmdgen

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


def send(ip, port, version, community, auth_pwd=None, priv_pwd=None, auth_proto=usmNoAuthProtocol, priv_proto=usmNoPrivProtocol):
	cmdGen  = cmdgen.AsynCommandGenerator()
	if version == 1 or version == 2:
		sec_name = cmdgen.CommunityData(community)
	elif version == 3:
		if auth_proto == "MD5":
			auth_proto = usmHMACMD5AuthProtocol
		elif auth_proto == "SHA":
			auth_proto = usmHMACSHAAuthProtocol

		if auth_proto == "AES":
			auth_proto = usmAesCfb128Protocol
		elif auth_proto == "DES":
			auth_proto = usmDESPrivProtocol

		if auth_proto is not None and auth_pwd is not None:
			if priv_proto is not None and priv_pwd is not None:
				cmdgen.UsmUserData(community, auth_key, priv_key)#...
			else:
				cmdgen.UsmUserData(community, auth_proto, auth_pwd)
		else:
			sec_name = cmdgen.CommunityData(community)
	else:
		return


	cmdGen.getCmd(
	    sec_name,
	    cmdgen.UdpTransportTarget((ip, port)),
	    (cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0),),
	    (cbFun, None)
	)

	cmdGen.snmpEngine.transportDispatcher.runDispatcher()

send('hawk.run.montefiore.ulg.ac.be', 161, 3, 'run69Zork!')