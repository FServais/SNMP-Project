<?php 
	error_reporting(E_ALL);

	include_once('model/sqlite_connection.php');
	include_once('model/agents.php');

	$db = sqlite_connect();
	$agents = get_agents($db, false);

	echo "<pre>";
	print_r($agents);
	echo "</pre>";

 ?>
