<?php
error_reporting(E_ALL);

define('HEIGHT', '86');

define('ROOT_DIR', dirname(__FILE__));
define('DOCS_DIR', ROOT_DIR.'/docs');

## Get list of dirs
$dirs = scandir(DOCS_DIR, 1);
#echo DOCS_DIR;
#print_r($dirs);

$docs = array();

foreach($dirs aS $d){
	#print_r($d);
	if($d == '.' or $d == '..' or $d == '.gitignore' or substr($d, - 4) === '.zip'){
		// do nothing
	}else{
		$fn = DOCS_DIR."/$d/info.json";
		
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
ksort($docs)
#print_r($docs);
?>
<!DOCTYPE html>
<html>
<head>
<title>FlightGear Documentation Project (Experimental)</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>

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
		echo "<li><a target='doc_iframe' href='docs/$k/html/'>".$v['title']."</a></li>";
	} ?>
	</ul>
</header>


<iframe src="info.php"  id="doc_iframe" name="doc_iframe"></iframe>


<script>
$(document).ready(function() {
	$('#doc_iframe').height(window.innerHeight - <?php echo HEIGHT ?> - 10);
});
</script>


</body>


</html>