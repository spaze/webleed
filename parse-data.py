#!/usr/bin/env python

import json
import time
from optparse import OptionParser

def import_json(filename):
	host_status = {}
	with open(filename) as f:
		json_data = f.read()
	data = json.loads(json_data)
	for k, v in data.items():
		host_status[k] = v
	return host_status

options = OptionParser(usage='%prog', description='Generate SQL queries from ssltest.py output')
options.add_option('--scanid', '-i', dest='scan_id', help='Scan id to insert into queries')
options.add_option('--ip', dest='ip', help='Outgoing IP address of the scan')
options.add_option('--port', dest='port', help='Target port of the scan')
options.add_option('--start', dest='start', help='Start time of the scan')
options.add_option('--total', dest='total', help='Total hosts scanned')
options.add_option('--json', '-j', dest='json_file', help='Load data from this json file')
options.add_option('--networks', '-n', dest='networks_file', help='Load networks from this file')
opts, args = options.parse_args()

def main():
	if not opts.scan_id or not opts.json_file or not opts.networks_file:
		options.print_help()
		return

	end_time = 0
	host_status = import_json(opts.json_file)
	print "INSERT INTO scans (id, total, total_open_port, ip, port) VALUES (%s, %s, %s, '%s', %s);" % (opts.scan_id, opts.total, len(host_status), opts.ip, opts.port)
	print "BEGIN;"
	for host_name, data in host_status.items():
		status = data.get('status')
		last_scan = data.get('last_scan')
		if (end_time < last_scan):
			end_time = last_scan
		if status is not None:
			print "INSERT INTO hosts (scan_id, host, vulnerable, scanned) VALUES (%s, '%s', %s, TIMESTAMP WITH TIME ZONE 'epoch' + %s * INTERVAL '1 second');" \
				% (opts.scan_id, host_name, status, last_scan)
	print "COMMIT;"

	del host_status
	print "UPDATE scans SET start_time = '%s', end_time = TIMESTAMP WITH TIME ZONE 'epoch' + %s * INTERVAL '1 second' WHERE id = %s;" \
		% (opts.start, end_time, opts.scan_id)

	with open(opts.networks_file) as f:
		networks = f.readlines()
	print "BEGIN;"
	for network in networks:
		print "INSERT INTO networks (scan_id, network) VALUES (%s, '%s');" % (opts.scan_id, network.strip())
	print "COMMIT;"

if __name__ == '__main__':
	main()
