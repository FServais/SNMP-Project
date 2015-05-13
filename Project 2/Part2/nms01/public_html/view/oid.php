<a href="index.php?page=agents"><- Back to agents</a>

<?php 

	echo '<h1> Oid tree for the agent '.$_GET['ip'].' </h1>';

	echo '<div id="refresh">';
	echo '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&refresh=true"> Refresh MIB list</a> </br>'; 
	echo '</div>';

	echo '<div id="tree">'; 

		
		if(isset($_GET['oid']))
		{
			$oid = $_GET['oid'];

			//split the oid in order to navigate through the tree
			$levels = explode('.', $oid);
		
			$oid_lvl = '';
			$space = 0;
			$oid_subtree = $oids;
			
			// displays the tree above the oid mentionned (all the parents are listed)
			foreach($levels as $level)
			{
				// $oid_lvl is used to reflect the current OID.
				if(strlen($oid_lvl != 0))
					$oid_lvl = $oid_lvl.'.'.$level;
				else
					$oid_lvl = $level;

				// we select the required son at each round
				$oid_subtree = $oid_subtree[$level];

				echo str_repeat(' -- ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&oid='.$oid_lvl.'"> '.$oid_lvl.' </a> </br>';
			 	$space++;
			}
			// displays the sons available for that OID
			foreach($oid_subtree as $key => $value)
			{
				// if the value is an empty array, then we know that the OID describes an object and we make a link to its value
				if(empty($value))
					echo str_repeat(' -- ', $space) . '<a href="index.php?page=oidvalue&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"]
			 			. '&secname=' . $_GET["secname"] . '&oid='.$oid.'.'.$key.'"> '.$oid.'.'.$key.' </a> </br>'; 
			 	else
			 		echo str_repeat(' -- ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"]
			 			. '&secname=' . $_GET["secname"] . '&oid='.$oid.'.'.$key.'"> '.$oid.'.'.$key.' </a> </br>'; 
				
			}
	
			
		}
		else 
		{
			// if there is no oid parameter, then we go to the root of the mib tree. 
			echo '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&oid=1"> 
			1</a> </br>'; 
		}
		echo '</div>';
?>

