<?php
	
	include('model/sqlite_connection.php');
	include('model/agents.php');
	include('model/oids.php');


	if(isset($_GET['ip']) AND isset($_GET['port']) AND isset($_GET['version']) AND isset($_GET['secname']))
	{
		$db = sqlite_connect();
		$agents = get_agents($db, false);
		$agent = findAgentV3($agents, $_GET['ip'], $_GET['port'], $_GET['secname'], $_GET['version']);
		$refresh = false;

		if(isset($_GET['refresh']) && !strcmp($_GET['refresh'],'true'))
			$refresh = true;
		

		if($agent['version'] == 3)
			$oids = get_mib_list($db, $refresh, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname'],
				$agent['auth_proto'], $agent['auth_pwd'], $agent['priv_proto'], $agent['priv_pwd']);

		else
			$oids = get_mib_list($db,  $refresh, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname']);	

	}
	include_once('view/index.php');
	


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