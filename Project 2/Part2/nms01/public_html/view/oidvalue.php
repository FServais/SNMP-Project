<a href="javascript:history.back()"><- Back to OID's</a>

<?php 
	echo '<h1> Oid Value </h1>';
?>

<div id="oidvalue">
<table align="center">
	<?php
		$secname = (intval($_GET['version']) == 3) ? 'User name' : 'Community name';
		echo '<tr><td>Address</td><td>' . $_GET['ip']. ' : '. $_GET['port'] . '</td></tr>';
		echo '<tr><td>Version</td><td>' . $_GET['version'] . '</td></tr>';
		echo '<tr><td>' . $secname . '</td><td>' . $_GET['secname'] . '</td></tr>';
		echo '<tr><td>Value of <class style="color:black;">' . $oid . '</class></td><td>' . $value . '</td></tr>';
	?>
</table>
</div>
