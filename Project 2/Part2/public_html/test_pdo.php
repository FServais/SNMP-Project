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

	$agents = get_agents($db);
	echo "<pre>";
	print_r($agents);
	echo "</pre>";

 ?>
