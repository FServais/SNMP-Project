<?php 
	include('model/agents.php');
	include('model/sqlite_connection.php');

	$db = sqlite_connect();
	echo 'Ok connection';
	$agents_array = get_agents($db, false);
	echo 'Ok get agents ';
	include_once('view/agents.php');
	echo 'Oki controller';

?>
