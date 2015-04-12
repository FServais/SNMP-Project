<?php 
	error_reporting(E_ALL);
	try {
		$pdo = new PDO('mysql:host=localhost;dbname=OIDTREE', 'root', 'root');
		$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	} catch (Exception $e) {
		echo 'Connection to database failed: ' . $e->getMessage() . '<br/>';
		exit();
	}

	/*
	//$test_insert = $pdo->prepare("INSERT INTO agent (ip, version, port, secname) VALUES (?,?,?,?)");
	//$test_insert->execute(array('192.161.1.1', 1, 161, 'secname'));

	$select = $pdo->prepare('SELECT * FROM agent');

	$select->execute();

	$agents = $select->fetchAll();
	echo "<pre>";
	print_r($agents);
	echo "</pre>";
 	*/
 
	// OIDS



 ?>
