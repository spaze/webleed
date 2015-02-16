#!/bin/sh

IP=`head -1 ./ip`
I=`head -1 ./scanid`
for P in 443 465 993 995; do
	INITIATED=`head -1 ./data/massoutput$P | grep -oP "(?<= initiated ).*"`
	START=`date -d "$INITIATED" +"%Y-%m-%d %H:%M:%S+00"`
	./parse-data.py --scanid $I --json data$P.json --masscan-conf data/ripe.cz.conf --port $P --ip $IP --start "$START" --total `head -1 ./data/total` > data$I.sql
	echo "$P parsed"
	I=$((I+1))
done;
echo $I > ./scanid

START=`date -d "$INITIATED" +"%Y-%m-%d"`
tar cjf data$START.tar.bz2 data*.sql
