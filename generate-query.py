#!/usr/bin/env python

from optparse import OptionParser

def build_total_queries(start, end):
	query = '''(''%s'', null, ',
		(SELECT COUNT(*) FROM (SELECT DISTINCT h.host FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date > '%s' AND h.vulnerable) v2),
		', ',
		(SELECT COUNT(*) FROM (SELECT DISTINCT h.host FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date > '%s') t2),
		')''' % (end, start, start)
	return query

def build_port_queries(port, start, end):
	query = '''(''%s'', %d, ',
		(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date > '%s' AND s.port = %d AND h.vulnerable),
		', ',
		(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date > '%s' AND s.port = %d),
		')''' % (end, port, start, port, start, port)
	return query

if __name__ == '__main__':
	options = OptionParser(usage='%prog <table> <start> <end>', description='Generate SQL query which generates another SQL query with vulnerable and total hosts')
	(opts, args) = options.parse_args()
	if len(args) == 3:
		print '-----8<-----'
		print '''SELECT CONCAT('INSERT INTO %s (date, port, vulnerable, total) VALUES''' % (args[0])
		print build_total_queries(args[1], args[2])
		print ','
		print build_port_queries(443, args[1], args[2])
		print ','
		print build_port_queries(465, args[1], args[2])
		print ','
		print build_port_queries(993, args[1], args[2])
		print ','
		print build_port_queries(995, args[1], args[2])
		print ''';');'''
		print '-----8<-----'
		print 'Now run this on the scan results database and then run the result on the "charts" database'
	else:
		options.print_help()
