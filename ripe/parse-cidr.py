from netaddr import IPRange

fi = open('ripe.cz.ranges', 'r')
fo = open('ripe.cz.cidr', 'w')
for line in fi:
	ips = line.split('-')
	ip_range = IPRange(ips[0], ips[1])
	for cidr in ip_range.cidrs():
		fo.write("%s\n" % cidr)
fi.close()
fo.close()
