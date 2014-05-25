#!/usr/bin/env python

from netaddr import IPRange
from optparse import OptionParser

class Parser:

	total_networks = 0

	total_ips = 0

	country = None

	input_file = None

	output_file = None

	def __init__(self, input_file, country, output_file):
		self.input_file = input_file
		self.country = country.lower()
		self.output_file = output_file

	def process(self, record, output_file):
		status = record['status'].split(' ', 1)[0]
		if record['country'] == self.country and status in ['assigned', 'not-set', 'early-registration']:
			ips = record['inetnum'].split(' - ')
			ip_range = IPRange(ips[0], ips[1])
			for cidr in ip_range.cidrs():
				self.total_networks += 1
				self.total_ips += cidr.size
				output_file.write('range = %s\n' % cidr)

	def parse_line(self, line):
		return line.split(':', 1)[1].strip().lower()

	def parse(self):
		empty = {
			'inetnum': '',
			'country': '',
			'status': '',
		}
		record = empty.copy()
		with open(self.input_file, 'r') as fi:
			with open(self.output_file, 'w') as fo:
				for line in fi:
					if (line.find('inetnum') == 0):
						record['inetnum'] = self.parse_line(line)
					if (line.find('country') == 0):
						record['country'] = self.parse_line(line)
					if (line.find('status') == 0):
						record['status'] = self.parse_line(line)
					if line in ['\r\n', '\n']:
						self.process(record, fo)
						record = empty.copy()

if __name__ == '__main__':
	options = OptionParser(usage='%prog <inputfile> <country> <outputfile>', description='Parse RIPE whois data and return records in masscan format')
	(opts, args) = options.parse_args()
	if len(args) == 3:
		parser = Parser(args[0], args[1], args[2])
		parser.parse()
		print 'Total networks: %d' % parser.total_networks
		print 'Total IPs: %d' % parser.total_ips
	else:
		options.print_help()
