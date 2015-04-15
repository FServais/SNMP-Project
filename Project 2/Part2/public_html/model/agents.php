<?php 

	/**
	 * Get the SNMP agents. 
	 * @param  SQLite3 $db Database connection
	 * @return Array       List of the agents
	 */
	function get_agents($db)
	{
		$agents = array();

		// Check timeout of the cache
		$timeout_result = $db->query('SELECT 1 FROM agentstimeout WHERE strftime("%s", "now") - strftime("%s", agents_last_refresh) >= ' . 2 * 60 * 60);
		$timeout = $timeout_result->fetchArray();

		if ($timeout[0] == 1) 
		{
			echo "Refreshing...";
			$agents_file = load_agents('agents.xml');
			refresh_agents($agents_file, $db);
			update_agents_timeout($db);
		}
		else
			echo "Not refreshing.";

		$results = $db->query('SELECT ip, port, version, secname FROM agent WHERE version=1 OR version=2');
		
		while ($row = $results->fetchArray()) 
			array_push($agents, array('ip' => $row['ip'],
									  'port' => $row['port'],
									  'version' => $row['version'],
									  'secname' => $row['secname']));
		
		$results = $db->query('SELECT * FROM agentv3');
		while ($row = $results->fetchArray()) 
		{
			$agent = array('ip' => $row['ip'],
						   'port' => $row['port'],
						   'version' => $row['version'],
						   'secname' => $row['secname']);

			if(isset($row['auth_proto']))
				$agent["auth_proto"] = $row['auth_proto'];
			if(isset($row['auth_pwd']))
				$agent["auth_pwd"] = $row['auth_pwd'];
			if(isset($row['priv_proto']))
				$agent["priv_proto"] = $row['priv_proto'];
			if(isset($row['priv_pwd']))
				$agent["priv_pwd"] = $row['priv_pwd'];

			array_push($agents, $agent);
		}

		return $agents;
	}

	/**
	 * Read the list of agents in $agent_file, and return them as en array.
	 * @param  string $agent_file File where are located the agents
	 * @return array              Array containing the agents.
	 */
	function load_agents($agent_file)
	{
		$agents_xml = array();

		// Loading agents
		if(file_exists($agent_file))
			$agents_xml = simplexml_load_file($agent_file);
		else
			echo "File does not exist.";

		// Transform the XML file into an array of arrays
		$agents = array();

		foreach ($agents_xml as $agent_xml)
		{
			$agent["ip"] = (string) $agent_xml->ip;
			$agent["port"] = (int) $agent_xml->port;
			$agent["version"] = (int) $agent_xml->version;
			$agent["sec_name"] = (string) $agent_xml->sec_name;

			if($agent["version"] == 3)
			{
				if(isset($agent_xml->auth_proto))
					$agent["auth_proto"] = (string) $agent_xml->auth_proto;
				if(isset($agent_xml->auth_pwd))
					$agent["auth_pwd"] = (string) $agent_xml->auth_pwd;
				if(isset($agent_xml->priv_proto))
					$agent["priv_proto"] = (string) $agent_xml->priv_proto;
				if(isset($agent_xml->priv_pwd))
					$agent["priv_pwd"] = (string) $agent_xml->priv_pwd;
			}

			array_push($agents, $agent);
		}

		return $agents;
	}

	/**
	 * Re-populate the database with the list of agents.
	 * @param  Array   $agents  List of agents.
	 * @param  SQLite3 $db      Connection to the database.
	 */
	function refresh_agents($agents, $db)
	{
		$query = 'BEGIN TRANSACTION; ';
		$queryv3 = 'BEGIN TRANSACTION; ';
		foreach ($agents as $agent)
		{
			$query .= 'INSERT INTO agent (ip, port, version, secname) VALUES ("' . SQLite3::escapeString($agent['ip']) . '", ' . $agent['port'] . ', ' . $agent['version'] . ', "' . SQLite3::escapeString($agent['sec_name']) . '");';
			
			if ($agent['version'] == 3)
				$queryv3 .= 'INSERT INTO agentv3 (ip, port, version, secname, auth_proto, auth_pwd, priv_proto, priv_pwd) VALUES ("' . SQLite3::escapeString($agent['ip']) . '", ' . $agent['port'] . ', ' . $agent['version'] . ', "' . SQLite3::escapeString($agent['sec_name']) . '", "' . SQLite3::escapeString($agent['auth_proto']) . '", "' . SQLite3::escapeString($agent['auth_pwd']) . '", "' . SQLite3::escapeString($agent['priv_proto']) . '", "' . SQLite3::escapeString($agent['priv_pwd']) . '");';			
			
		}

		$query .= 'COMMIT;';
		$queryv3 .= 'COMMIT;';

		$db->query($query);
		$db->query($queryv3);
	}

	/**
	 * Change the value for the timeout of the list of agents.
	 * @param  SQLite3 $db Connection to the database.
	 */
	function update_agents_timeout($db)
	{
		$db->query('UPDATE agentstimeout SET agents_last_refresh = datetime("now")');
	}

 ?>