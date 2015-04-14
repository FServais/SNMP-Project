<?php 
	/**
	 * Connect to the database.
	 * @return SQLite3 Connection to the database.
	 */
	function sqlite_connect()
	{
		$db = new SQLite3('mibviewer');
		return $db;
	}

	/**
	 * Get the SNMP agents. 
	 * @param  SQLite3 $db Database connection
	 * @return Array       List of the agents
	 */
	function get_agents($db)
	{
		$agents = array();

		// Check timeout of the cache
		$timeout_result = $db->query('SELECT 1 FROM agentstimeout WHERE datetime("now")-agents_last_refresh >= 2');
		$timeout = $timeout_result->fetchArray();

		if ($timeout[0] == 1) 
		{
			echo "Refreshing...";
			$agents_file = load_agents('agents.xml');
			refresh_agents($agents_file, $db);
			update_agents_timeout($db);
		}

		$results = $db->query('SELECT ip, port, version, secname FROM agent WHERE version=1 OR version=2');
		
		while ($row = $results->fetchArray()) 
		{
			array_push($agents, array('ip' => $row['ip'],
									  'port' => $row['port'],
									  'version' => $row['version'],
									  'secname' => $row['secname']));
		}

		$results = $db->query('SELECT * FROM agent JOIN agentv3 ON agent.id = agentv3.id');
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
		foreach ($agents as $agent)
		{
			$db->query('INSERT INTO agent (ip, port, version, secname) VALUES ("' . SQLite3::escapeString($agent['ip']) . '", ' . $agent['port'] . ', ' . $agent['version'] . ', "' . SQLite3::escapeString($agent['sec_name']) . '")');
			
			if ($agent['version'] == 3){
				$_id = $db->query('SELECT MAX(id) FROM agent');
				$id = $_id->fetchArray();
				echo "IDs : <br>";
				print_r($id);
				echo "<br>";
				$id = $id[0];
				$db->query('INSERT INTO agentv3 (id, auth_proto, auth_pwd, priv_proto, priv_pwd) VALUES ("' . $id . '", "' . SQLite3::escapeString($agent['auth_proto']) . '", "' . SQLite3::escapeString($agent['auth_pwd']) . '", "' . SQLite3::escapeString($agent['priv_proto']) . '", "' . SQLite3::escapeString($agent['priv_pwd']) . '")');			
			}
		}
	}

	/**
	 * Change the value for the timeout of the list of agents.
	 * @param  SQLite3 $db Connection to the database.
	 */
	function update_agents_timeout($db)
	{
		$db->query('UPDATE agentstimeout SET agents_last_refresh = datetime("now", "+2 hours")'); // "+2 hours" due to configuration problem on sqlite
	}


	function get_mib_list($db)
	{
		$oids = get_oids("hawk.run.montefiore.ulg.ac.be", "run69Zork!", 1);

		return $oids;
	}


	function get_oids($ip, $community, $version)
	{
		snmp_set_oid_output_format(SNMP_OID_OUTPUT_NUMERIC);
		if($version == 1)
			$walk = snmprealwalk($ip, $community, "");
		if($version == 2)
			$walk = snmp2_real_walk($ip, $community, "");
		if($version == 3)
			$walk = snmp3_real_walk($ip, $community, "");

		$oids = array();
		foreach ($walk as $oid => $value) 
		{
			$oid = substr($oid, 1);
			$oids[$oid] = "";
		}
		
		return $oids;
	}

 ?>
