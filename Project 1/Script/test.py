import time
import logging
import datetime
import sys

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

#########################################
logging.basicConfig(filename='data_packets.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Objects to consult (snmpInPkts and snmpOutPkts)
oid_received = (1,3,6,1,2,1,11,1,0)
oid_sent = (1,3,6,1,2,1,11,2,0)

# For the script to have a duration of 24h
time_start = datetime.datetime.now()
num_min = 0

# Get first data
start_number_received = getNumberOfPackets(oid_received)
start_number_sent = getNumberOfPackets(oid_sent)

prev_packets_received = start_number_received
prev_packets_sent = start_number_sent

diff_received = 0
diff_sent = 0

logging.info("| Number packets received (difference)    Number packets sent (difference)")
logging.info("|              %d (+%d)                             %d (+%d)" % (prev_packets_received, diff_received, prev_packets_sent, diff_sent))

# To generate data file for Matlab
prev_matlab_received = prev_packets_received
prev_matlab_sent = prev_packets_sent

#matlab_data = open('matlab_data.dat', 'a')
message = "%d %d %d %d %d\n" % (num_min, prev_matlab_received, prev_matlab_sent, diff_received, diff_sent)
sys.stderr.write(message)
while True:
    # Wait 5 minutes 
    time.sleep(300)
    num_min += 5

    packets_received = getNumberOfPackets(oid_received)
    packets_sent = getNumberOfPackets(oid_sent)

    # If the counter had wrapped
    if(packets_received < prev_packets_received):
        diff_received = (2**32 - 1 - prev_packets_received) + packets_received
    else: 
        diff_received = packets_received - prev_packets_received

    if(packets_sent < prev_packets_sent):
        diff_sent = (2**32 - 1 - prev_packets_sent) + packets_sent
    else: 
        diff_sent = packets_sent - prev_packets_sent

    # Log
    message = '|              %d (+%d)                             %d (+%d)' % (packets_received, diff_received, packets_sent, diff_sent)
    logging.info(message)

    prev_packets_received = packets_received
    prev_packets_sent = packets_sent

    # Matlab log
    prev_matlab_received += diff_received
    prev_matlab_sent += diff_sent
    message = "%d %d %d %d %d\n" % (num_min, prev_matlab_received, prev_matlab_sent, diff_received, diff_sent)
    sys.stderr.write(message)

    # Check duration of the executiin
    time_now = datetime.datetime.now()

    diff_time = time_now - time_start

    if diff_time.days > 0:
        break



    
