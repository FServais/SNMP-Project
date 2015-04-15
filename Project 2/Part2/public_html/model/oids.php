<?php 
	
	function get_mib_list($ip, $port, $community, $version, $db)
	{
		$oids = array();

		// Check timeout of the cache
		$timeout_result = $db->query('SELECT 1 FROM oidstimeout WHERE strftime("%s", "now") - strftime("%s", oids_last_refresh) < ' . 2 * 60 * 60);
		$timeout = $timeout_result->fetchArray();

		if ($timeout[0] == 1) 
		{
			echo "Refreshing...";
			$oids_raw = get_oids($ip, $port, $community, $version);

			refresh_oids($oids_raw, $ip, $port, $community, $version, $db);
			update_oids_timeout($ip, $port, $community, $version, $db);			
		}
		else
		{
			echo "Not refreshing.";
			get_oids_db($ip, $port, $community, $version, $db);
		}
		
		$oids = explodeTree($oids_raw, '.', false);
		
		return $oids;
	}


	function get_oids($ip, $port, $version, $community, $auth_proto = "", $auth_pwd = "", $priv_proto = "", $priv_pwd = "")
	{
		$oids = array();
		snmp_set_quick_print( 1 );
		snmp_set_enum_print( 0 );
		snmp_set_oid_output_format( SNMP_OID_OUTPUT_NUMERIC );

		if($version == 1)
		{
			$oid = @snmpgetnext($ip, $community, [".1"]);		
			while($oid)
			{
				$oids[substr(key($oid),1)] = "";
				$oid = snmpgetnext($ip, $community, [key($oid)]);
			}
		}
		elseif($version == 2)
		{
			$oid = @snmp2_getnext($ip, $community, [".1"]);
			
			while($oid)
			{
				$oids[substr(key($oid),1)] = "";
				$oid = snmp2_getnext($ip, $community, [key($oid)]);
			}
		}
		elseif($version == 3)
		{
			$oid = @snmp3_getnext($ip, $community, [".1"]);
			
			while($oid)
			{
				$oids[substr(key($oid),1)] = "";
				$oid = snmp3_getnext($ip, $community, $auth_proto, $auth_pwd, $priv_proto, $priv_pwd, [key($oid)]);
			}
		}
		
		return $oids;
	}


	function refresh_oids($oids, $ip, $port, $version, $secname, $db)
	{
		$query = 'BEGIN TRANSACTION; ';
		foreach ($oids as $oid => $value)
			$query .= 'INSERT INTO oidnode (ip, port, version, secname, oid) VALUES ("' . SQLite3::escapeString($ip) . '", ' . $port . ', ' . $version . ', "' . SQLite3::escapeString($secname) . ', "' . SQLite3::escapeString($oid) . '");';

		$query .= 'COMMIT;';

		echo $query;

		$db->query($query);
	}


	function update_oids_timeout($ip, $port, $version, $secname, $db)
	{
		$db->query('INSERT OR REPLACE INTO oidstimeout (ip, port, version, secname, oids_last_refresh) VALUES ("' . SQLite3::escapeString($ip) . '", ' . $port . ', ' . $version . ', "' . SQLite3::escapeString($secname) . '", datetime("now"))');
	}


	function get_oids_db($ip, $port, $version, $secname, $db)
	{
		$oids = array();
		$result = $db->query('SELECT oid FROM oidnode WHERE ip=' . SQLite3::escapeString($ip) . ' AND port=' . $port . ' AND version=' . $version . ' AND secname=' . SQLite3::escapeString($secname));
		while ($row = $results->fetchArray())
			$oids[substr($row['oid'],1)];
		
		return $oids;
	}

	/**
	 * (This function has been taken from the Internet, source above.)
	 * Explode any single-dimensional array into a full blown tree structure,
	 * based on the delimiters found in it's keys.
	 *
	 * The following code block can be utilized by PEAR's Testing_DocTest
	 * <code>
	 * // Input //
	 * $key_files = array(
	 *   "/etc/php5" => "/etc/php5",
	 *   "/etc/php5/cli" => "/etc/php5/cli",
	 *   "/etc/php5/cli/conf.d" => "/etc/php5/cli/conf.d",
	 *   "/etc/php5/cli/php.ini" => "/etc/php5/cli/php.ini",
	 *   "/etc/php5/conf.d" => "/etc/php5/conf.d",
	 *   "/etc/php5/conf.d/mysqli.ini" => "/etc/php5/conf.d/mysqli.ini",
	 *   "/etc/php5/conf.d/curl.ini" => "/etc/php5/conf.d/curl.ini",
	 *   "/etc/php5/conf.d/snmp.ini" => "/etc/php5/conf.d/snmp.ini",
	 *   "/etc/php5/conf.d/gd.ini" => "/etc/php5/conf.d/gd.ini",
	 *   "/etc/php5/apache2" => "/etc/php5/apache2",
	 *   "/etc/php5/apache2/conf.d" => "/etc/php5/apache2/conf.d",
	 *   "/etc/php5/apache2/php.ini" => "/etc/php5/apache2/php.ini"
	 * );
	 *
	 * // Execute //
	 * $tree = explodeTree($key_files, "/", true);
	 *
	 * // Show //
	 * print_r($tree);
	 *
	 * // expects:
	 * // Array
	 * // (
	 * //    [etc] => Array
	 * //        (
	 * //            [php5] => Array
	 * //                (
	 * //                    [__base_val] => /etc/php5
	 * //                    [cli] => Array
	 * //                        (
	 * //                            [__base_val] => /etc/php5/cli
	 * //                            [conf.d] => /etc/php5/cli/conf.d
	 * //                            [php.ini] => /etc/php5/cli/php.ini
	 * //                        )
	 * //
	 * //                    [conf.d] => Array
	 * //                        (
	 * //                            [__base_val] => /etc/php5/conf.d
	 * //                            [mysqli.ini] => /etc/php5/conf.d/mysqli.ini
	 * //                            [curl.ini] => /etc/php5/conf.d/curl.ini
	 * //                            [snmp.ini] => /etc/php5/conf.d/snmp.ini
	 * //                            [gd.ini] => /etc/php5/conf.d/gd.ini
	 * //                        )
	 * //
	 * //                    [apache2] => Array
	 * //                        (
	 * //                            [__base_val] => /etc/php5/apache2
	 * //                            [conf.d] => /etc/php5/apache2/conf.d
	 * //                            [php.ini] => /etc/php5/apache2/php.ini
	 * //                        )
	 * //
	 * //                )
	 * //
	 * //        )
	 * //
	 * // )
	 * </code>
	 *
	 * @author  Kevin van Zonneveld &lt;kevin@vanzonneveld.net>
	 * @author  Lachlan Donald
	 * @author  Takkie
	 * @copyright 2008 Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	 * @license   http://www.opensource.org/licenses/bsd-license.php New BSD Licence
	 * @version   SVN: Release: $Id: explodeTree.inc.php 89 2008-09-05 20:52:48Z kevin $
	 * @link      http://kevin.vanzonneveld.net/
	 *
	 * @param array   $array
	 * @param string  $delimiter
	 * @param boolean $baseval
	 *
	 * @return array
	 */
	function explodeTree($array, $delimiter = '.', $baseval = false)
	{
	    if(!is_array($array)) return false;
	    $splitRE   = '/' . preg_quote($delimiter, '/') . '/';
	    $returnArr = array();
	    foreach ($array as $key => $val) {
	        // Get parent parts and the current leaf
	        $parts  = preg_split($splitRE, $key, -1, PREG_SPLIT_NO_EMPTY);
	        $leafPart = array_pop($parts);

	        // Build parent structure
	        // Might be slow for really deep and large structures
	        $parentArr = &$returnArr;
	        foreach ($parts as $part) {
	            if (!isset($parentArr[$part])) {
	                $parentArr[$part] = array();
	            } elseif (!is_array($parentArr[$part])) {
	                if ($baseval) {
	                    $parentArr[$part] = array('__base_val' => $parentArr[$part]);
	                } else {
	                    $parentArr[$part] = array();
	                }
	            }
	            $parentArr = &$parentArr[$part];
	        }

	        // Add the final part to the structure
	        if (empty($parentArr[$leafPart])) {
	            $parentArr[$leafPart] = $val;
	        } elseif ($baseval && is_array($parentArr[$leafPart])) {
	            $parentArr[$leafPart]['__base_val'] = $val;
	        }
	    }
	    return $returnArr;
	}

 ?>