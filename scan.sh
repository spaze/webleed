#!/bin/bash

scanport() {
	[ ! -f data/czip$1 ] && sudo masscan -p$1 --conf data/ripe.cz.conf --rate=10000 --output-format greppable --output-file data/massoutput$1 --excludefile exclude.txt --wait 30 \
	&& grep "Ports: $1" data/massoutput$1 | grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" > data/czip$1
	ssltest.py --input data/czip$1 --port $1 --json data$1.json --logfile data/results.txt --timeout 5 --threads 1000
}

mkdir -p data
cd data
[ ! -f ripe.db.inetnum ] && wget ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz && gunzip ripe.db.inetnum.gz
cd ..

[ ! -f data/ripe.cz.conf ] && ./parse-ripedb.py data/ripe.db.inetnum cz data/ripe.cz.conf

scanport 443 && scanport 465 && scanport 993 && scanport 995
