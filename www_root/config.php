<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);

define('HEIGHT', '86');

define('ROOT_DIR', dirname(__FILE__));
define('DOCS_DIR', ROOT_DIR.'');
define('IDX_FILE', ROOT_DIR.'/index.json');


function get_index(){
	return json_decode(file_get_contents(IDX_FILE), true);
}

function nicetime($date) {
    if(empty($date)) {
        return "ERROR: No date provided";
    }
    $periods = array("second", "minute", "hour", "day", "week", "month", "year", "decade");
    $lengths = array("60","60","24","7","4.35","12","10");
    $now = time();
    $unix_date = strtotime($date);
    // check validity of date
    if(empty($unix_date)) {
        return "ERROR: Invalid date";
    }
    // is it future date or past date
    if($now > $unix_date) {
        $difference = $now - $unix_date;
        $tense = "ago";
    }
    else {
        $difference = $unix_date - $now;
        $tense = "from now";
    }
    for($j = 0; $difference >= $lengths[$j] && $j < count($lengths)-1; $j++) {
        $difference /= $lengths[$j];
    }
    $difference = round($difference);
    if($difference != 1) {
//      $periods[$j] .= "s"; // plural for English language
        $periods = array("seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades"); // plural for international words
    }
    return "$difference $periods[$j] {$tense}";
}
?>