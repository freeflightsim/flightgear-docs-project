<?php

require_once('config.php');



$docs = get_index();

?>

<html>
<head>
<title>FlightGear Documentation Project (experimental)</title>





<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="content">



<h1>Docs Index</h1>

<table>

<tr><th>Browse Html</th><th>Zip</th><th>Version</th><th>Updated</th><th>Repo</th><th>Checkout</th></tr>
<?php foreach($docs as $k => $v){ 
	echo '<tr><td><a class="lnk" href="'.$k.'/html/" style="border-left: 10px solid '.$v['color'].';">'.$v['title'].'</a></td>';
	echo '<td><a target="_blank" href="'.$k.'/'.$k.'.zip">'.$k.'.zip</a></td>';
	echo	'<td>'.$v['version'].'</td><td>'.$v['last_updated'].'</td>';
	echo '<td>'.$v['repo'].'</td><td>'.$v['checkout'].'</td></tr>';
} ?>
</table>

<!-- Put the following javascript before the closing </head> tag. -->
<script>
  (function() {
    var cx = '014455812952330413319:oiztngtmppy';
    var gcse = document.createElement('script'); gcse.type = 'text/javascript'; gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.co.uk/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(gcse, s);
  })();
</script>

<!-- Place this tag where you want both of the search box and the search results to render -->
<gcse:search></gcse:search>

<div class="info">
<ul>
<li>This project is an experiment to automatically generate docs from source files (ta Jenkins).</li>
<li>The goal is to automate the process completely, and make all the docs link together. eg FlightGear docs currently link to Simgear docs. TODO is osg, plib, OpenAL, etc.</li>
<li>The code for this project is at gitorious <a 
	href="https://gitorious.org/fgx-xtras/flightgear-docs-build" target="_blank"><b>flightgear-docs-build</b></a></li>
<li>View the <a 
	href="README.txt" target="_blank"><b>README.txt</b></a> for more info</li>
</ul>

</div>

</div>

</body>


</html>