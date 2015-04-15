<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Agents present in the network</title>
  <link rel="stylesheet" href="view/style.css" />
</head>

<body>
	
	<?php 

		echo '<h1> Oid tree for the agent '.$_GET['ip'].' </h1>';

	

		echo '<div id="tree">'; 

			if(isset($_GET['oid']))
			{
				$oid = $_GET['oid'];

				$levels = explode('.', $oid);

			
				$oid_lvl = '';
				$space = 0;
				$oid_subtree = $oids;
				
				foreach($levels as $level)
				{
					if(strlen($oid_lvl != 0))
						$oid_lvl = $oid_lvl.'.'.$level;
					else
						$oid_lvl = $level;

					$oid_subtree = $oid_subtree[$level];
					echo str_repeat(' -- ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&oid='.$oid_lvl.'"> '.$oid_lvl.' </a> </br>';
				 	$space++;
				}
				foreach($oid_subtree as $key => $value)
				{
					echo str_repeat(' -- ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"]
				 	. '&secname=' . $_GET["secname"] . '&oid='.$oid.'.'.$key.'"> '.$oid.'.'.$key.' </a> </br>'; 
				}
		
				
			}
			else 
			{
				echo '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET["port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&oid=1"> 
				1 </a> </br>'; 
			}
			echo '</div>';
	?>

</body>
</html>