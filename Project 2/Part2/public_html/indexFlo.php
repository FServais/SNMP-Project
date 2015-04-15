<?php
	error_reporting(E_ALL); 
	session_start();

	echo 'coucou y a quand même un truc marche';
	// Contains the accessible pages
	$pages = array('index', 'agents');

	/* Launch the corresponding controller (variable 'page' in URL)*/
	if(isset($_GET['page']) && in_array($_GET['page'], $pages))
		include_once('controller/' . $_GET['page'] . '.php');
	else
		include_once('controller/agents.php');
 ?>
