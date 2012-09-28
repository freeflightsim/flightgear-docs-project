<?php

require_once('config.php');

if(isset($_GET['update'])){
	echo "UPDATE<br>";
	## Get list of dirs
	$dirs = scandir(DOCS_DIR, 1);
	#echo DOCS_DIR;
	#print_r($dirs);

	$docs = array();

	foreach($dirs aS $d){
		#print_r($d);
		
		$fp = DOCS_DIR."/$d";
		#echo "d=$d  ====== $fp<br>";
		if(is_dir($fp)){
			if($d == '.' or $d == '..' or $d == '.gitignore' or substr($d, - 4) === '.zip'){
				// do nothing
			}else{
				$fn = DOCS_DIR."/$d/info.json";
				#echo "fn=$fn";
				## Read the info.json in each folder
				if( file_exists($fn) ){
					$info_str = file_get_contents($fn);
					$data = json_decode($info_str, true);
				#print_r($data);
				}else{
					$data = array('title' => $d, 'version' => '-', 'last_updated'=> '', 'checkout'=>'', 'repo'=>'');
				}
				$docs[$d] = $data;
			}
		}
	}
	ksort($docs);
	$json_data = json_encode($docs);
	echo ROOT_DIR.'/index.json';
	file_put_contents(IDX_FILE, $json_data, LOCK_EX);
}else{
	$docs = get_index();
}


?>
<!DOCTYPE html>
<html>
<head>
<title>FlightGear Documentation Project (Experimental)</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
<link rel="shortcut icon" href="favicon.ico" />
<link rel="stylesheet" href="style.css">
<style>
header {
	height: <?php echo HEIGHT.'px' ?>;
}
</style>


</head>

<body>

<header>
		<h1>FlightGear Docs Project (experimental)</h1>
	
	<ul id="menu">
	<li><a href="info.php" target='doc_iframe'>Home</a></li>
	<?php foreach($docs as $k => $v){ 
		echo "<li><a target='doc_iframe' href='$k/html/'>".$v['title']."</a></li>";
	} ?>
	</ul>
</header>


<iframe src="info.php?frame=1"  id="doc_iframe" name="doc_iframe"></iframe>


<script>
$(document).ready(function() {
	$('#doc_iframe').height(window.innerHeight - <?php echo HEIGHT ?> - 10);
});
</script>


</body>


</html>