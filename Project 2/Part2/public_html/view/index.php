<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Agents present in the network</title>
  <link rel="stylesheet" href="view/style.css" />
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>

  <script>
	jQuery(document).ready(function($) {
		$(".clickable-row").click(function() {
			$("#agents .clickable-row tr td").toggleClass('clicked');
		    window.document.location = $(this).data("href");
		});
	});
  </script>

</head>

<body>

	<?php

		$pages = array('index', 'agents', 'oid', 'oidvalue');

		/* Launch the corresponding view (variable 'page' in URL)*/
		if(isset($_GET['page']) && in_array($_GET['page'], $pages) AND isset($_GET['ip']) AND
			 isset($_GET['port']) AND isset($_GET['version']) AND isset($_GET['secname']))
			include_once('view/' . $_GET['page'] . '.php');
		else
			include_once('view/agents.php');

	?>

<body>
	
</body>
</html>
