<?php
	
	include('model/sqlite_connection.php');
	include('model/agents.php');
	include('model/oids.php');


	if(isset($_GET['ip']) AND isset($_GET['port']) AND isset($_GET['version']) AND isset($_GET['secname']))
	{
		$db = sqlite_connect();
		$agents = get_agents($db, false);
		$agent = findAgentV3($agents, $_GET['ip'], $_GET['port'], $_GET['secname'], $_GET['version']);

		if(in_array($agent, $agents))
		{
			echo $agent['ip'].':'.$agent['port'].'<br>';
			if($agent['version'] == 3)
				$oids = get_mib_list($db, false, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname'],
				 $agent['auth_proto'], $agent['auth_pwd'], $agent['priv_proto'], $agent['priv_pwd']);

			else
				$oids = get_mib_list($db, false, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname']);
			
			include_once('view/oid.php');
			echo 'coucou je viens de la vue';
		}

	}
	else{
		include_once('view/agents.php');
	}


	function findAgentV3($agents, $ip, $port, $secname, $version)
	{
		
		foreach ($agents as $key => $agent)
		{
			if( !strcmp($agent['ip'], $ip) AND $port == $agent['port'] AND $version == $agent['version']
				AND !strcmp($agent['secname'], $secname)){
				return $agent;

			}
				
		}

	}


?>