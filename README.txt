SELECT SUM(len) - 5600 FROM (SELECT power(2, 32 - masklen(network)) AS len FROM networks WHERE scan_id = 98) f

SELECT CONCAT(
'INSERT INTO cz_michalspacek.webleed (date, port, vulnerable, total) VALUES
(''2014-06-20'', null, ',
(SELECT COUNT(*) FROM (SELECT DISTINCT h.host FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND h.vulnerable) v2),
', ',
(SELECT COUNT(*) FROM (SELECT DISTINCT h.host FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20') t2),
'),
(''2014-06-20'', 443, ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 443 AND h.vulnerable),
', ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 443),
'),
(''2014-06-20'', 465, ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 465 AND h.vulnerable),
', ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 465),
'),
(''2014-06-20'', 993, ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 993 AND h.vulnerable),
', ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 993),
'),
(''2014-06-20'', 995, ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 995 AND h.vulnerable),
', ',
(SELECT COUNT(*) FROM hosts h JOIN scans s on h.scan_id = s.id WHERE s.end_time::date = '2014-06-20' AND s.port = 995),
');'
);
