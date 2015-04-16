<a href="javascript:history.back()"><- Back to OID's</a>
<?php 
	echo '<h1> Oid Value </h1>';
	echo 'Agent informations : '. $_GET['ip']. ' : '. $_GET['port'].'</br> version : ' .$_GET['version'].'</br> secname : '. $_GET['secname']. '</br>';
	echo $oid.' : '. $value .'</br>';

	echo '<a href="index.php?"> Agent page  </a> </br>'; 
?>
