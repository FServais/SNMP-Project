<?php 
	session_start();

	// Contains the accessible pages
	$pages = array('index', 'agents', 'oid', 'oidvalue');

	/* Launch the corresponding controller (variable 'page' in URL)*/
	if(isset($_GET['page']) && in_array($_GET['page'], $pages))
		include_once('controller/' . $_GET['page'] . '.php');
	else
		include_once('controller/agents.php');
 ?>