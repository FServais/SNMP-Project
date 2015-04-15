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

 ?>
