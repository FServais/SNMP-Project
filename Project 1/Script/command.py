import time
import logging
import datetime
import sys

from pysnmp.entity.rfc3413.oneliner import cmdgen

# Function that get the value of the object with the oid 'oid' on "hawk".
# oid : Oid from which we want to get the value. (tuple)
def getValue(oid):
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


# Function that gets the number the number of packets received on hawk.
def getPacketsReceived():
    oid_in = (1,3,6,1,2,1,4,3,0) #ipInReceives
    return getValue(oid_in)


# Function that gets the number the number of packets sent on hawk.
def getPacketsSent():
    oids_out = [(1,3,6,1,2,1,4,10,0), (1,3,6,1,2,1,4,6,0), (1,3,6,1,2,1,4,11,0), (1,3,6,1,2,1,4,12,0)] #[ipOutRequests, ipForwDatagrams, ipOutDiscards, ipOutNoRoutes]

    total = 0
    for oid in oids_out:
        total += getValue(oid)

    return total


# Return the value of the difference of to values contained in a Counter32.
# prev_value, value : values from which we want the difference (value - prev_value)
def getDiffCounter32(prev_value, value):
    if value < prev_value:
        return (2**32 - 1 - prev_value) + value
    else:
        return value - prev_value

#########################################
logging.basicConfig(filename='data_packets.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# For the script to have a duration of 24h
time_start = datetime.datetime.now()
num_min = 0

# Get first data
start_number_received = getPacketsReceived()
start_number_sent = getPacketsSent()

prev_packets_received = start_number_received
prev_packets_sent = start_number_sent


diff_received = 0
diff_sent = 0

logging.info("|     Difference number packets received    Difference number packets sent")
logging.info("|                     %d                                  %d" % (diff_received, diff_sent))

# To generate data file to plot
prev_data_received = prev_packets_received
prev_data_sent = prev_packets_sent

message = "%d %d %d\n" % (num_min, diff_received, diff_sent)
sys.stderr.write(message)
while True:
    # Wait 5 minutes 
    time.sleep(5)
    num_min += 5

    packets_received = getPacketsReceived();
    packets_sent = getPacketsSent();

    # If the counter had wrapped
    diff_received = getDiffCounter32(prev_packets_received, packets_received);
    diff_sent = getDiffCounter32(prev_packets_sent, packets_sent);

    # Log
    message = '|                     %d                                  %d' % (diff_received, diff_sent)
    logging.info(message)

    prev_packets_received = packets_received
    prev_packets_sent = packets_sent


    # Data log
    prev_data_received += diff_received
    prev_data_sent += diff_sent
    message = "%d %d %d\n" % (num_min, diff_received, diff_sent)
    sys.stderr.write(message)

    # Check duration of the executiin
    time_now = datetime.datetime.now()

    diff_time = time_now - time_start

    if diff_time.days > 0:
        break



    
