//mib structure
<?php
	
	include(model/sqlite_connection.php);

	if(isset($_GET['ip']) AND isset($_GET['port']) AND isset($_GET['version']) AND isset($_GET['secname']))
	{
		$db = sqlite_connect();
		$agents = get_agents($db, false);
		$agent = findAgentV3($agents, $_GET['ip'], $_GET['port'], $_GET['secname'], $_GET['version']);

		//$auth_proto = "", $auth_pwd = "", $priv_proto = "", $priv_pwd = ""
		if(in_array($agent, $agents))
		{
			$oids = get_mib_list($db, false, $_GET['ip'],  $_GET['port'], $_GET['secname'], $_GET['version'] ,
			 $agent['auth_proto'], $agent['auth_pwd'], $agent['priv_proto'], $agent['priv_pwd']);
			include_once('view/oids.php');
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
				AND !strcmp($agent['secname'], $secname))
				return $agent;
		}


	}


?>