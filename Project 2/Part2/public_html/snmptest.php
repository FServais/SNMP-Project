<?php 
	error_reporting(E_ALL);

	
	ini_set('display_errors', 1);
	//snmp_set_oid_output_format(SNMP_OID_OUTPUT_NUMERIC);
	$a = snmp2_get("hawk.run.montefiore.ulg.ac.be", "run69Zork!", "1.2.1");

	if(empty($a))
		echo "Null";

	echo "<pre>";
	print_r($a);
	echo "</pre>";
	
	/*
	foreach ($a as $val) {
	    echo "$val\n";
	}
	*/
	/*
	$a = snmpwalkoid("hawk.run.montefiore.ulg.ac.be", "run69Zork!", "", 5000000);
	for (reset($a); $i = key($a); next($a)) {
	    echo "$i: $a[$i]<br />\n";
	}
	*/
	/*
	ini_set('display_errors', 1);
	snmp_set_valueretrieval( SNMP_VALUE_OBJECT | SNMP_VALUE_PLAIN );
	
	snmp_set_quick_print( 1 );
	snmp_set_enum_print( 0 );
	snmp_set_oid_output_format( SNMP_OID_OUTPUT_NUMERIC );
	$oid = snmp2_getnext("139.165.222.253", "public!", [".1"]);
	
	while($oid)
	{
		print_r($oid);
		echo '<br>';
		$oid = snmp2_getnext("139.165.222.253", "public!", [key($oid)]);
	}
	*/
	
	/*
	include_once('model/sqlite_connection.php');
	include_once('model/oids.php');
	$db = sqlite_connect();
	$oids = get_oids("hawk.run.montefiore.ulg.ac.be", 161, 1, "run69Zork!");
	echo "<PRE>";
	print_r($oids);
	echo "<PRE>";
	*/
	/*
	$oids = array("1.1.1.1.1" => "a",
				  "1.1.1.1.1.3" => "b",
				  "1.1.1.2.1" => "c",
				  "1.1.1.2.1.1" => "d",
				  "1.1.1.2.2" => "e",
				  "1.1.1.2.3.4" => "f",
				  "1.1.1.1.1.1" => "g",
				  "1.1.1.1.2" => "h",
				  "1.1.1.1.2.3" => "i",
				  "1.1.1.1.1.3.5" => "j");

	$tree = explodeTree($oids, '.', true);
	echo "<pre>";
	print_r($tree);
	echo "</pre>"
	*/
	/*
	include_once("model/sqlite_connection.php");
	include_once("model/agents.php");
	include_once("model/oids.php");

	$db = sqlite_connect();

	echo "test : <br>";
	*/
	/*
	$agents = get_agents($db, false);
	echo "<pre>";
	print_r($agents);
	echo "</pre>";
	*/
	/*
	$oids = get_mib_list($db, true, "hawk.run.montefiore.ulg.ac.be", 161, 1, "run69Zork!");
	echo "<pre>";
	print_r($oids);
	echo "</pre>"
	*/
	//$agents = get_agents($db,false);
	/*
	$oid = get_oid_value("1.3.6.1.2.1.1.1.0", "hawk.run.montefiore.ulg.ac.be", 161, 1, "run69Zork!");
	echo $oid . "<br>";

	$test = "";
	if(is_null($test))
		echo "ISSET";
	else
		echo "NOT ISSET";
	*/


 ?>