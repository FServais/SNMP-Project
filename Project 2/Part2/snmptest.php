<?php 
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	$a = snmpwalk("hawk.run.montefiore.ulg.ac.be", "run69Zork!", "");

	foreach ($a as $val) {
	    echo "$val\n";
	}
 ?>