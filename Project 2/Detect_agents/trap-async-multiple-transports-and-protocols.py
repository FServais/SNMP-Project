from pysnmp.entity.rfc3413.oneliner import ntforg
from pysnmp.proto import rfc1902

# List of targets in the followin format:
# ( ( authData, transportTarget ), ... )
targets = (
    # 1-st target (SNMPv1 over IPv4/UDP)
    ( ntforg.CommunityData('public', mpModel=0),
      ntforg.UdpTransportTarget(('run69Zork!', 161)) ),
    # 2-nd target (SNMPv2c over IPv4/UDP)
    ( ntforg.CommunityData('public'),
      ntforg.UdpTransportTarget(('run69Zork!', 161)) )
)

ntfOrg = ntforg.AsynNotificationOriginator()

for authData, transportTarget in targets:
    ntfOrg.sendNotification(
        authData,
        transportTarget,
        'trap',
        ntforg.MibVariable('SNMPv2-MIB', 'coldStart'),
        ( ( rfc1902.ObjectName('1.3.6.1.2.1.1.1.0'),
            rfc1902.OctetString('my name') ), )
    )

ntfOrg.snmpEngine.transportDispatcher.runDispatcher()
