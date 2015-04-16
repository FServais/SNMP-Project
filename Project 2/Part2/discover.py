#!/usr/bin/env python3.4

from __future__ import print_function
from collections import deque
from ipaddress import ip_network
from sys import argv, stderr
from threading import Lock, Thread
from time import strftime

from pysnmp.error import PySnmpError
from pysnmp.entity.rfc3413.oneliner import cmdgen

import xml.etree.cElementTree as ET

agents = []
config_file_name = ""; # Global to export

usage = """\
Usage: %s CONFIG

where CONFIG is the name of a configuration file in the following format:
    IP/PREFIX
    PORT VERSION SEC_NAME [AUTH_PROTO AUTH_PWD [PRIV_PROTO PRIV_PWD]]
    PORT VERSION SEC_NAME [AUTH_PROTO AUTH_PWD [PRIV_PROTO PRIV_PWD]]
    ...
where
    IP is an IP address.
    PREFIX is the prefix length.
    PORT is a port number.
    VERSION is the SNMP version to use, either 1, 2 or 3.
    SEC_NAME is the community name for SNMPv1 and SNMPv2, and the user name for
             SNMPv3.
    AUTH_PROTO is the authentication protocol, either MD5 or SHA.
    AUTH_PWD is the authentication password.
    PRIV_PROTO is the encryption cipher, either DES or AES.
    PRIV_PWD is the encryption password.""" % argv[0]

def fatal(msg):
    """Exit with an error message."""
    print("Error: %s\n" % msg, file=stderr)
    print(usage, file=stderr)
    exit(1)

class Config:
    """ Read configuration from file and remember it.

    The parsing is not resilient at all to errors, but the wording says you can
    assume the configuration file is well-formatted.
    """
    def __init__(self, file_name):
        with open(file_name, "r") as f:
            # Network/prefix
            self.network = ip_network(f.readline().rstrip())
            # Credentials
            self.credentials = [] # (port, version, sec_name, auth_data)
            for line in f.readlines():
                self.add_credentials(line.rstrip())

    def add_credentials(self, line):
        parts = line.split();
        port, version, sec_name = int(parts[0]), int(parts[1]), parts[2]
        if version == 1:
            # mpModel needs to be set to 0 for SNMPv1 (defaults to 1)
            auth_data = cmdgen.CommunityData(sec_name, mpModel=0)
            self.credentials.append((port, 1, sec_name, auth_data))
        elif version == 2:
            auth_data = cmdgen.CommunityData(sec_name, mpModel=1)
            self.credentials.append((port, 2, sec_name, auth_data))
        else:
            auth_proto = cmdgen.usmNoAuthProtocol
            auth_pwd = ""
            priv_proto = cmdgen.usmNoPrivProtocol
            priv_pwd = ""
            if len(parts) > 3:
                if parts[3] == "SHA":
                    auth_proto = cmdgen.usmHMACSHAAuthProtocol
                else:
                    auth_proto = cmdgen.usmHMACMD5AuthProtocol
                auth_pwd = parts[4]
            if len(parts) > 5:
                if parts[5] == "AES":
                    priv_proto = cmdgen.usmAesCfb128Protocol
                else:
                    priv_proto = cmdgen.usmDESPrivProtocol
                priv_pwd = parts[6]
            auth_data = cmdgen.UsmUserData(sec_name, auth_pwd, priv_pwd,
                                           auth_proto, priv_proto)
            self.credentials.append((port, 3, sec_name, auth_data))

def add_agent(version, sec_name, ip, cred_index):
    """Add a detected agent to the agents list.

    version -- SNMP version
    sec_name -- security name, i.e. community for v1-2, and user for v3
    ip -- IP address of the agent
    cred_index -- index of the credentials to use

    The credentials index is 0-based, and their order is the same as in the
    configuration file. This allows to recover authentication/encryption
    parameters for SNMPv3.
    """
    # TODO Modify this function to write agent information in a place and form
    #      suitable for your web application
    date_time = strftime('%d/%m/%Y %H:%M:%S')
    #print("%s: v%d agent with sec_name %s on %s (%d)" % (date_time, version, sec_name, ip, cred_index))
    fp = open(config_file_name, 'r')
    for i,line in enumerate(fp):
        if i == cred_index+1:
            if version == 3:
                port, _, _, auth_proto, auth_pwd, priv_proto, priv_pwd = line.split(' ')
                agent = (ip, port, str(version), sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd)
            else:
                port, _, _ = line.split(' ')
                agent = (ip, port, str(version), sec_name, None, None, None, None)
    fp.close()

    agents.append(agent)


def process_response(sendRequestHandle, errorIndication, errorStatus,
                     errorIndex, varBinds, args):
    """Callback for asynchronous requests.

    If there is no error, add the agent which responded to the list of detected
    agents.
    """
    if errorIndication is None and not errorStatus:
        (version, sec_name, ip, cred_index) = args
        add_agent(version, sec_name, ip, cred_index)

class V3Searcher(Thread):
    """Thread to send synchronous SNMPv3 requests."""

    def __init__(self, lock, queue):
        Thread.__init__(self)
        self.lock = lock
        self.queue = queue

    def run(self):
        while True:
            self.lock.acquire()
            if len(self.queue) > 0:
                (cred_index, auth_data, target, sec_name, ip) =\
                        self.queue.popleft()
                self.lock.release()
                # Create a new command generator to avoid caching issues
                cmdGen = cmdgen.CommandGenerator()
                # We use a GETNEXT request rather than a GET request because we
                # don't know any OID which would be guaranteed to be there.
                #
                # It would have been simpler to use OID 1, but this is
                # not possible with pysnmp. We obtain the same result by
                # starting from 1.1 and enabling lexicographic mode (see pysnmp
                # documentation for details).
                errorIndication, errorStatus, errorIndex, varBinds =\
                        cmdGen.nextCmd(auth_data, target, '1.1',
                                       lexicographicMode=True, maxRows=1)
                if errorIndication is None and not errorStatus:
                    add_agent(3, sec_name, ip, cred_index)
            else:
                self.lock.release()
                break


# Given a list of agents, write a XML file.
def xmlWriter(agentsList):
    
    targets = ET.Element("targets")
    
    for i in agentsList:
        
        target = ET.SubElement(targets, "target")
        
        ip,port, version, sec_name, auth_proto, auth_pwd, priv_proto, priv_pwd = i
        ET.SubElement(target, "ip", ).text = ip
        ET.SubElement(target, "port",).text = port
        ET.SubElement(target, "version", ).text = version
        ET.SubElement(target, "sec_name", ).text = sec_name

        if auth_proto != None:
            ET.SubElement(target, "auth_proto", ).text = auth_proto
        if auth_pwd != None:    
            ET.SubElement(target, "auth_pwd", ).text = auth_pwd
        if priv_proto != None:        
            ET.SubElement(target, "priv_proto", ).text = priv_proto
        if priv_pwd != None:
            ET.SubElement(target, "priv_pwd", ).text = priv_pwd

    tree = ET.ElementTree(targets)
    tree.write("/home/nfs/nms01/public_html/model/agents.xml")



if __name__ == "__main__":
    if len(argv) != 2:
        fatal("wrong number of arguments")

    if argv[1] in ["-h", "-help", "--help"]:
        print(usage)
        exit(0)

    try:
        config = Config(argv[1])
        config_file_name = argv[1]
    except FileNotFoundError:
        fatal("could not open \"%s\"" % argv[1])

    # Prepare the (#Credentials x #IPs) requests to be attempted
    v3Queue = deque([])
    asynCmdGen = cmdgen.AsynCommandGenerator()
    for i, cred in enumerate(config.credentials):
        (port, version, sec_name, auth_data) = cred
        for ip in config.network.hosts():
            ip = str(ip)
            # We use a rather long timeout because lab network is slow, and can
            # be overloaded by other groups. 4 attempts should be OK.
            target = cmdgen.UdpTransportTarget((ip, port), timeout=5, retries=3)
            if version == 3:
                # No asynch requests for SNMPv3, see below
                v3Queue.append((i, auth_data, target, sec_name, ip))
            else:
                # We use a GETNEXT request rather than a GET request because we
                # don't know any OID which would be guaranteed to be there.
                #
                # It would have been simpler to use OID 1, but this is
                # not possible with pysnmp. In asynchronous mode, there is no
                # lexicographic mode, so we instead try all possible level-2
                # targets (i.e. 1.1 to 1.3 which are defined by the standard).
                asynCmdGen.nextCmd(auth_data, target, ('1.1', '1.2', '1.3'),
                                   (process_response,
                                    (version, sec_name, ip, i)))

    # There are bugs with SNMPv3 requests in asynchronous mode. So, we do it
    # manually by creating a thread pool to serve the collected SNMPv3
    # requests synchronously.
    #
    # Since we are speaking about *lightweight* Python threads, and not
    # something heavier like full-blown processes, we use a rather high count
    # of 64 threads to speed up detection.
    #
    # We use a simple lock to protect queue access. It should be fast enough,
    # since the threads will very likely pass most of their time waiting for
    # answers, rather than competing for the lock.
    lock = Lock()
    threads = []
    for i in range(0, 64):
        threads.append(V3Searcher(lock, v3Queue))
        threads[i].start()

    # Execute asynchronously the SNMPv1 and SNMPv2 requests in the main thread
    try:
        asynCmdGen.snmpEngine.transportDispatcher.runDispatcher()
    except PySnmpError as e:
        print("Error: ", e)

    # Wait for all the children to finish
    for t in threads:
        t.join()

    xmlWriter(agents)
