//mib display
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Agents present in the network</title>
  <link rel="stylesheet" href="view/style.css" />
</head>

<body>
	<h1> Agents present in the network </h1>

	<?php 

		if(isset($_GET['oid']))
		{
			$oid = $_GET['oid'];
			$levels = explode('.', $oid);

			if(is_leaf($oid))
			{
				include_once(controller/oidvalue);
				//echo '<a href="index.php?page=oidvalue&ip=' . $_GET["ip"] . '&port=' . $_GET[^"port"] . '&version=' . $_GET["version"]
				 //. '&secname=' . $_GET["secname"] . '&oid='.$oid.'"> '.$oid.' </a> </br>'; 
			}

			
			
			else
			{
				$oid_lvl = '';
				$space = 0;
				foreach($levels as $level)
				{
					$oid_lvl = $oid_lvl.'.'.$level;
					$oid_subtree = $oid_subtree[$level];
					echo str_repeat('  ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET[^"port"] . '&version=' . $_GET["version"]
				 	. '&secname=' . $_GET["secname"] . '&oid='.$oid_lvl.'"> '.$oid_lvl.' </a> </br>';
				 	$space++;
				}

				foreach($oid_subtree as $key => $value)
				{
					echo str_repeat('  ', $space) . '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET[^"port"] . '&version=' . $_GET["version"]
				 	. '&secname=' . $_GET["secname"] . '&oid='.$oid.'.'.$key.'"> '.$oid.'.'.$key.' </a> </br>'; 
				}
			}	
			
		}
		else 
		{
			echo '<a href="index.php?page=oid&ip=' . $_GET["ip"] . '&port=' . $_GET[^"port"] . '&version=' . $_GET["version"] . '&secname=' . $_GET["secname"] . '&oid=1"> 
			1 </a> </br>'; 
		}

	?>

</body>
</html>