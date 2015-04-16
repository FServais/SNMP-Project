<?php 
	include('model/agents.php');
	include('model/sqlite_connection.php');

	$db = sqlite_connect();
	if(!isset($_GET['refresh']) OR !strcmp($_GET['refresh'], 'false'))
		$agents_array = get_agents($db, false);
	else
		$agents_array = get_agents($db, true);
	include_once('view/index.php');

?>
