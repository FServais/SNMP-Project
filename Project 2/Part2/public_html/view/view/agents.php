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
		foreach($agents_array as $key =>  $agent)
		{
			$ip = $agent["ip"];
			$port = $agent["port"];
			$version = $agent["version"];
			$secname = $agent["secname"];

			echo '<a href="index.php?page=oid&ip=' . $ip . '&port=' . $port . '&version=' . $version . '&secname=' . $secname . '">' . $ip . ':' . $port . ' version: ' . $version . ' secname : ' . $secname . '  </a> </br>'; 
			
		}

	?>

</body>
</html>
