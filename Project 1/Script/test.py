import time
import logging
import datetime
import sys

from pysnmp.entity.rfc3413.oneliner import cmdgen

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


def getNumberPackets_if(oids):
    total = 0

    for oid in oids:
        for i in xrange(1,6):
            oid_to_send = oid + (i,)
            total += getValue(oid_to_send)

    return total



def getPacketsReceived_if():
    oid_in_prefix = [(1,3,6,1,2,1,2,2,1,11), (1,3,6,1,2,1,31,1,1,1,2), (1,3,6,1,2,1,31,1,1,1,3), (1,3,6,1,2,1,2,2,1,13), (1,3,6,1,2,1,2,2,1,14)]
    return getNumberPackets_if(oid_in_prefix)

def getPacketsSent_if():
    oid_out_prefix = [(1,3,6,1,2,1,2,2,1,17), (1,3,6,1,2,1,31,1,1,1,4), (1,3,6,1,2,1,31,1,1,1,5)]
    return getNumberPackets_if(oid_out_prefix)


def getPacketsReceived_ip():
    oid_in = (1,3,6,1,2,1,4,3,0)
    return getValue(oid_in)

def getPacketsSent_ip():
    oids_out = [(1,3,6,1,2,1,4,10,0), (1,3,6,1,2,1,4,6,0), (1,3,6,1,2,1,4,11,0), (1,3,6,1,2,1,4,12,0)]

    total = 0
    for oid in oids_out:
        total += getValue(oid)

    return total


def getDiffCounter32(prev_value, value):
    if value < prev_value:
        return (2**32 - 1 - prev_value) + value
    else:
        return value - prev_value

#########################################
logging.basicConfig(filename='data_packets.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# METHOD 1 (IF)
# num_of_ifs = getValue((1,3,6,1,2,1,2,1,0))


# For the script to have a duration of 24h
time_start = datetime.datetime.now()
num_min = 0

# Get first data
start_number_received_if = getPacketsReceived_if()
start_number_sent_if = getPacketsSent_if()
start_number_received_ip = getPacketsReceived_ip()
start_number_sent_ip = getPacketsSent_ip()

prev_packets_received_if = start_number_received_if
prev_packets_sent_if = start_number_sent_if
prev_packets_received_ip = start_number_received_ip
prev_packets_sent_ip = start_number_sent_ip

diff_received_if = 0
diff_sent_if = 0

diff_received_ip = 0
diff_sent_ip = 0

logging.info("| Number packets received [IF] (difference)    Number packets sent [IF] (difference)      Number packets received [IP] (difference)    Number packets sent [IP] (difference)")
logging.info("|              %d (+%d)                             %d (+%d)                                     %d (%d)                                  %d (%d)" % (prev_packets_received_if, diff_received_if, prev_packets_sent_if, diff_sent_if, prev_packets_received_ip, diff_received_ip, prev_packets_sent_ip, diff_sent_ip))

# To generate data file for Matlab
prev_matlab_received_if = prev_packets_received_if
prev_matlab_sent_if = prev_packets_sent_if

prev_matlab_received_ip = prev_packets_received_ip
prev_matlab_sent_ip = prev_packets_sent_ip

message = "%d %d %d %d %d %d %d %d %d\n" % (num_min, prev_matlab_received_if, prev_matlab_sent_if, diff_received_if, diff_sent_if, prev_matlab_received_ip, prev_matlab_sent_ip, diff_received_ip, diff_sent_ip)
sys.stderr.write(message)
while True:
    # Wait 5 minutes 
    time.sleep(300)
    num_min += 5

    packets_received_if = getPacketsReceived_if();
    packets_sent_if = getPacketsSent_if();
    packets_received_ip = getPacketsReceived_ip();
    packets_sent_ip = getPacketsSent_ip();

    # If the counter had wrapped
    diff_received_if = getDiffCounter32(prev_packets_received_if, packets_received_if);
    diff_sent_if = getDiffCounter32(prev_packets_sent_if, packets_sent_if);
    diff_received_ip = getDiffCounter32(prev_packets_received_ip, packets_received_ip);
    diff_sent_ip = getDiffCounter32(prev_packets_sent_ip, packets_sent_ip);

    # Log
    message = '|              %d (+%d)                             %d (+%d)                                     %d (%d)                                  %d (%d)' % (packets_received_if, diff_received_if, packets_sent_if, diff_sent_if, packets_received_ip, diff_received_ip, packets_sent_ip, diff_sent_ip)
    logging.info(message)

    prev_packets_received_if = packets_received_if
    prev_packets_sent_if = packets_sent_if
    prev_packets_received_ip = packets_received_ip
    prev_packets_sent_ip = packets_sent_ip


    # Matlab log
    prev_matlab_received_if += diff_received_if
    prev_matlab_sent_if += diff_sent_if
    prev_matlab_received_ip += diff_received_ip
    prev_matlab_sent_ip += diff_sent_ip
    message = "%d %d %d %d %d %d %d %d %d\n" % (num_min, prev_matlab_received_if, prev_matlab_sent_if, diff_received_if, diff_sent_if, prev_matlab_received_ip, prev_matlab_sent_ip, diff_received_ip, diff_sent_ip)
    sys.stderr.write(message)

    # Check duration of the executiin
    time_now = datetime.datetime.now()

    diff_time = time_now - time_start

    if diff_time.days > 0:
        break



    
