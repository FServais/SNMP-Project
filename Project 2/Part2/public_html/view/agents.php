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
	<h1> Agents present in the network </h1>
		<div id="agents">
			<table>
				<tr>
					<th>IP</th>
					<th>Port</th>
					<th>Version</th>
					<th>Community name</th>
				</tr>
				
				<?php 
					foreach($agents_array as $key =>  $agent)
					{
						$ip = $agent["ip"];
						$port = $agent["port"];
						$version = $agent["version"];
						$secname = $agent["secname"];

						//echo '<a href="index.php?page=oid&ip=' . $ip . '&port=' . $port . '&version=' . $version . '&secname=' . $secname . '">' . $ip . ':' . $port . ' version: ' . $version . ' secname : ' . $secname . '  </a> </br>'; 
						

						echo "<tr class='clickable-row' data-href='index.php?page=oid&ip=" . $ip . "&port=" . $port . "&version=" . $version . "&secname=" . $secname . "'>";

							echo "<td>" . $ip . "</td>";
							echo "<td>" . $port . "</td>";
							echo "<td>" . $version . "</td>";
							echo "<td>" . $secname . "</td>";

						echo "</tr>";

					}
				?>
			</table>
		</div>

</body>
</html>
