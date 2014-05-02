<?php
// ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz
$country = 'CZ';
$fi = 'ripe.db.inetnum';
$fo = 'ripe.cz.ranges';

$fpi = fopen($fi, 'r');
$fpo = fopen($fo, 'w');
$ciders = array();
$countryLine = "country:        $country";
$assignedStatusLine = "status:         ASSIGNED";
$notSetStatusLine = "status:         NOT-SET";
$earlyStatusLine = "status:         EARLY-REGISTRATION";
$i = 0;
$lines = 0;
$notSetLines = 0;
$earlyLines = 0;
$inetnum = null;
$countryMatch = false;
$write = false;
while (($line = fgets($fpi)) !== false) {
	$lines++;
	if ($line === "\n") {
		$inetnum = null;
		$countryMatch = false;
	}
	if (strncmp($line, 'inetnum:', 8) === 0) {
		$inetnum = substr($line, 16, -1);
	}
	if (strncmp($line, $countryLine, 18) === 0) {
		if ($inetnum === null) {
			throw new RuntimeException("empty inetnum (line: {$lines})");
		}
		$countryMatch = true;
	}
	if (strncasecmp($line, $assignedStatusLine, 24) === 0 && $countryMatch) {
		$write = true;
	} elseif (strncasecmp($line, $notSetStatusLine, 23) === 0 && $countryMatch) {
		$notSetLines++;
		$write = true;
	} elseif (strncasecmp($line, $earlyStatusLine, 34) === 0 && $countryMatch) {
		$earlyLines++;
		$write = true;
	}
	if ($write) {
		list($ipMin, $ipMax) = explode(' - ', $inetnum);
		fwrite($fpo, "$ipMin-$ipMax\n");
		$i++;
		if ($i % 1000 === 0) {
			echo "$i\n";
		}
		$write = false;
	}
}
fclose($fpi);
fclose($fpo);
echo "Total: $i\n";
echo "Total not-set: $notSetLines\n";
echo "Total early-reg: $earlyLines\n";
