<?php
error_reporting(E_ALL);

define('ROOT_DIR', dirname(__FILE__));
define('DOCS_DIR', ROOT_DIR.'/docs');

## Get list of dirs
$dirs = scandir(DOCS_DIR, 1);
#echo DOCS_DIR;
#print_r($dirs);

$docs = array();

foreach($dirs as $d){
	#print_r($d);
	if($d == '.' or $d == '..' or $d == '.gitignore'){
		// do nothing
	}else{
		## Read the info.json in each folder
		$info_str = file_get_contents(DOCS_DIR."/$d/info.json");
		$data = json_decode($info_str, true);
		#print_r($data);
		$docs[$d] = $data;
	}
}

#print_r($docs);
?>

<html>
<head>
<title>FlightGear Documentation Project (experimental)</title>

<link rel="stylesheet" href="style.css">
</head>

<body>

<header>
	<img src="http://wiki.flightgear.org/skins/common/images/icons-fg-135.png">
	<h1>FlightGear Docs Project (experimental)</h1>
</header>
<p class="top">This project is an experiment to automatically generate docs from source files.</p>


<table>
<caption>Docs Index</caption>
<tr><th>Browse Html</th><th>Zip</th><th>Version</th><th>Updated</th><th>Repo</th><th>Checkout</th></tr>
<?php foreach($docs as $k => $v){ 
	echo '<tr><td><a href="/docs/'.$k.'/html/">'.$v['title'].'</a></td>';
	echo '<td><a href="/docs/'.$k.'/'.$k.'.zip">'.$k.'.zip</a></td>';
	echo	'<td>'.$v['version'].'</td><td>'.$v['last_updated'].'</td>';
	echo '<td>'.$v['repo'].'</td><td>'.$v['checkout'].'</td></tr>';


} ?>
</table>

<ul>
	<li>All the projects are spooled out to the <a href="/docs/"><b>docs/</b></a> directory.</li>
	<li>A project's directory have the html/ directory (but proobably not others).</li>

</ul>



<div class="info">
<ul>
<li>This project is work in progress, being developed by irc #peteffs (pete morgan atmo)</li>
<li>The code for this project is at gitorious <a 
	href="https://gitorious.org/fgx-xtras/flightgear-docs-build" target="_blank">flightgear-docs-build</a></li>
<li>View the <a 
	href="README.txt" target="_blank">README.txt</a> fro more info.</li>
</ul>

</div>
</body>


</html>