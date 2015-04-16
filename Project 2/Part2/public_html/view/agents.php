
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
				echo '<a href="index.php?page=agents&refresh=true"> Refresh agents </a> </br>'; 
				foreach($agents_array as $key =>  $agent)
				{
					$ip = $agent["ip"];
					$port = $agent["port"];
					$version = $agent["version"];
					$secname = $agent["secname"];

					

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


