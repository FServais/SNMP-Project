<?php 
	// Loading agents
	$agents_xml = simplexml_load_file('agents.xml');

	// Transform the XML file into an array of arrays
	$agents = array();

	foreach ($agents_xml as $agent_xml) {
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
	
	print_tree($agents);

	

	/**
	 * Pretty print an array.
	 * @param  array $xml Array to print.
	 */
	function print_tree($xml)
	{
		print "<pre>";
		print_r($xml);
		print "</pre>";
	}

 ?>
