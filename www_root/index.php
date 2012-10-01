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
<meta http-equiv="Content-Type" content="text/xhtml;charset=UTF-8"/>
<title>fgms-0: FlightGear MultiPlayer Server 0.x Production/Stable</title>
<link href="tabs.css" rel="stylesheet" type="text/css"/>
<link href="navtree.css" rel="stylesheet" type="text/css"/>
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript" src="resize.js"></script>
<script type="text/javascript" src="navtree.js"></script>
<script type="text/javascript">
  $(document).ready(initResizable);
</script>
<link href="search/search.css" rel="stylesheet" type="text/css"/>
<script type="text/javascript" src="search/search.js"></script>
<script type="text/javascript">
  $(document).ready(function() { searchBox.OnSelectItem(0); });
</script>

<link href="stylesheet.css" rel="stylesheet" type="text/css" />
</head>
<body>

<div id="top"><!-- do not remove this div! -->

<div id="titlearea">
<div id="fg_docx_header">
	<div id="fg_top_nav">
		<ul>
			<li><a href="#"><img src="logo-23.png"></a>
				<ul>
					<li><a href="http://flightgear.org" target="_blank">Home Page</a></li>
					<li><a href="http://wiki.flightgear.org/Portal:Developer"  target="_blank">Developer Wiki</a></li>
					<li><a href="https://code.google.com/p/flightgear-bugs/issues/list"  target="_blank">Issue Tracker</a></li>
					<li><a href="http://flightgear.simpits.org:8080/"  target="_blank">Build Server</a></li>
				</ul>
			</li>
		</ul>
	</div>
	<h1>FlightGear Documentation Project</h1>
	<ul id="menu">
		<li><a href="/">Home</a></li>
		<li><a  href=fgdata/'>FG Data</a></li>
		<li><a  href='flightgear/'>FlightGear</a></li>
		<li><a  href='fgms-0/'>FGMS-0</a></li>
		<li><a  href='fgms-1/'>FGMS-1</a></li>
		<li><a  href='plib/'>PLIB</a></li>
		<li><a  href='osg/'>OSG</a></li>
		<li><a  href='simgear/'>SimGear</a></li>
		<li><a  href='terragear/'>TerraGear</a></li>
	</ul>
</div>





</div>

<div class="fg_content">
<h1>Docs Index</h1>

<table>

<tr><th>Browse Html</th><th>Zip</th><th>Version</th><th>Updated</th><th>Repo</th><th>Checkout</th></tr>
<?php foreach($docs as $k => $v){ 
	echo '<tr><td><a class="lnk" href="'.$k.'/" style="border-left: 10px solid '.$v['color'].';">'.$v['title'].'</a></td>';
	echo '<td><a target="_blank" href="'.$k.'/'.$k.'.zip">'.$k.'.zip</a></td>';
	echo	'<td>'.$v['version'].'</td><td>'.nicetime($v['last_updated']).'</td>';
	echo '<td>'.$v['repo'].'</td><td>'.$v['checkout'].'</td></tr>';
} ?>
</table>


<!-- Put the following javascript before the closing </head> tag. -->
<script>
  (function() {
    var cx = '005020340521889986907:tdsrgbpk9s4';
    var gcse = document.createElement('script'); gcse.type = 'text/javascript'; gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(gcse, s);
  })();
</script>

<!-- Place this tag where you want both of the search box and the search results to render -->
<gcse:search></gcse:search>

<div class="info">
<ul>
<li>This project is an experiment to automatically generate docs from source files (ta Jenkins).</li>
<li>The goal is to automate the process completely, and make all the docs link together.</li>
<li>The code for this project is at gitorious <a 
	href="https://gitorious.org/fgx-xtras/flightgear-docs-project" target="_blank"><b>flightgear-docs-project</b></a></li>
<li>View the <a 
	href="README.txt" target="_blank"><b>README.txt</b></a> for more info</li>
<li>Feedback, bugs etc to <b>pete at freeflightsim dot org</b></li>
</ul>

</div>










</div>

</body>


</html>