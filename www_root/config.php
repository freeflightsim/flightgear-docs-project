<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);

define('HEIGHT', '86');

define('ROOT_DIR', dirname(__FILE__));
define('DOCS_DIR', ROOT_DIR.'');
define('IDX_FILE', ROOT_DIR.'/index.json');


function get_index(){
	return json_decode(file_get_contents(IDX_FILE), true);
}
?>