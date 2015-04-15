<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Oid value</title>
  <link rel="stylesheet" href="view/style.css" />
</head>

<body>
	<h1> Oid Value </h1>

	<?php 
		echo 'Agent informations : '. $_GET['ip']. ' : '. $_GET['port'].'</br> version : ' .$_GET['version'].'</br> secname : '. $_GET['secname']. '</br>';
		echo $oid.' : '. $value .'</br>';

		echo '<a href="index.php?"> Agent page  </a> </br>'; 
	?>

</body>
</html>
