<?php 
	error_reporting(E_ALL);
	/*
	$db = new SQLite3('mibviewer');


	$results = $db->query('SELECT * FROM agentstimeout');
	while ($row = $results->fetchArray()) {
		echo "<pre>";
		print_r($row);
		echo "</pre>";
	}*/

	include_once('model/sqlite_connection.php');
	$db = sqlite_connect();

	$oids = get_mib_list("hawk.run.montefiore.ulg.ac.be", "run69Zork!", 1, $db);
	echo "<pre>";
	print_r($oids);
	echo "</pre>";

 ?>
