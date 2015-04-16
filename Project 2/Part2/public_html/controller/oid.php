<?php
	
	include('model/sqlite_connection.php');
	include('model/agents.php');
	include('model/oids.php');


	if(isset($_GET['ip']) AND isset($_GET['port']) AND isset($_GET['version']) AND isset($_GET['secname']))
	{
		
		$refresh = false;
		if(isset($_GET['refresh']) && !strcmp($_GET['refresh'],'true'))
			$refresh = true;

		// if the agent is an snmpv3 one, we must retrieve the missing informations
		if(intval($_GET['version']) == 3)
		{
			$db = sqlite_connect();
			$agents = get_agents($db, false);
			$agent = findAgentV3($agents, $_GET['ip'], $_GET['port'], $_GET['secname'], $_GET['version']);
			
			$oids = get_mib_list($db, $refresh, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname'],
					$agent['auth_proto'], $agent['auth_pwd'], $agent['priv_proto'], $agent['priv_pwd']);
		}
		

		else
			$oids = get_mib_list($db,  $refresh, $_GET['ip'], intval($_GET['port']), intval($_GET['version']), $_GET['secname']);	

	}
	include_once('view/index.php');
	

	/**
	* Retrieve the good agent from the agent list
	*
	* @param array $agents 		the array containing all the agents
	* @param string $ip 		the ip address of the researched agent   
	* @param int $port 			the port number of the researched agent
	* @param int $version 		the snmp version of the researched agent
	* @param string $secname 	the community name of the researched agent
	* 
	* @return array 			the array containing all the informations about the corresponding agent
	**/
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