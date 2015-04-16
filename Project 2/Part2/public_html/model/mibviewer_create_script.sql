----
-- phpLiteAdmin database dump (http://phpliteadmin.googlecode.com)
-- phpLiteAdmin version: 1.9.5
-- Exported: 3:40pm on April 16, 2015 (CEST)
-- database file: ./mibviewer
----
BEGIN TRANSACTION;

----
-- Table structure for agentstimeout
----
CREATE TABLE "agentstimeout" ('agents_last_refresh' DATETIME NOT NULL);

----
-- Table structure for agent
----
CREATE TABLE 'agent' ('ip' TEXT NOT NULL, 'port' INTEGER NOT NULL, 'version' INTEGER NOT NULL, 'secname' TEXT NOT NULL, PRIMARY KEY ("ip", "port", "version", "secname") );

----
-- Table structure for agentv3
----
CREATE TABLE 'agentv3' ('ip' TEXT NOT NULL, 'port' INTEGER NOT NULL, 'version' INTEGER NOT NULL, 'secname' TEXT NOT NULL, 'auth_proto' TEXT, 'auth_pwd' TEXT, 'priv_proto' TEXT, 'priv_pwd' TEXT, PRIMARY KEY ('ip', 'port', 'version', 'secname'));

----
-- Table structure for oidnode
----
CREATE TABLE 'oidnode' ('ip' TEXT NOT NULL, 'port' INTEGER NOT NULL, 'version' INTEGER NOT NULL, 'secname' TEXT NOT NULL, 'oid' TEXT NOT NULL, PRIMARY KEY ('ip', 'port', 'version', 'secname', 'oid'));

----
-- Table structure for oidstimeout
----
CREATE TABLE 'oidstimeout' ('ip' TEXT NOT NULL, 'port' INTEGER NOT NULL, 'version' INTEGER NOT NULL, 'secname' TEXT NOT NULL, 'oids_last_refresh' DATETIME, PRIMARY KEY ('ip', 'port', 'version', 'secname'));

----
-- structure for index sqlite_autoindex_agent_1 on table agent
----
;

----
-- structure for index sqlite_autoindex_agentv3_1 on table agentv3
----
;

----
-- structure for index sqlite_autoindex_oidnode_1 on table oidnode
----
;

----
-- structure for index sqlite_autoindex_oidstimeout_1 on table oidstimeout
----
;
COMMIT;
