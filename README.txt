cd ripe \
&& wget ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz \
&& gunzip ripe.db.inetnum.gz \
&& php parse.php \
&& python parse-cidr.py \
&& cd .. \
&& awk '{print "range = " $0}' ripe/ripe.cz.cidr > ripe.cz.cidr \
&& sudo ../masscan/bin/masscan -p443 --conf ripe.cz.cidr --rate=1000 --output-format greppable --output-file massoutput \
&& grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" massoutput > czip443 \
&& time ./ssltest.py --input czip443 --json data.json --timeout 1 --threads 1000 \



time ./ssltest.py --input ripe/ripe.cz.cidr --json data.json --timeout 1 --threads 1000

sudo ~/masscan/bin/masscan -p443 --conf ripe/ripe.cz.cidr --rate=1000 --output-format greppable --output-file massoutput
grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" massoutput > czip443
time ./ssltest.py --input czip443 --json data.json --timeout 1 --threads 1000


cd ripe \
&& wget ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz \
&& gunzip ripe.db.inetnum.gz \
&& php parse.php \
&& python parse-cidr.py \
&& cd .. \
&& awk '{print "range = " $0}' ripe/ripe.cz.cidr > ripe.cz.cidr \
&& sudo ../masscan/bin/masscan -p465,993,995 --conf ripe.cz.cidr --rate=1000 --output-format greppable --output-file massoutput \
&& grep "Ports: 465" massoutput | grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" massoutput > czip465 \
&& grep "Ports: 993" massoutput | grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" massoutput > czip993 \
&& grep "Ports: 995" massoutput | grep -oP "(?<=Host: )\d+\.\d+.\d+.\d+" massoutput > czip995 \
&& time ./ssltest.py --input czip465 --port 465 --json data465.json --timeout 1 --threads 1000 \
&& time ./ssltest.py --input czip993 --port 993 --json data993.json --timeout 1 --threads 1000 \
&& time ./ssltest.py --input czip995 --port 995 --json data995.json --timeout 1 --threads 1000 \
