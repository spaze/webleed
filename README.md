# We Bleed scanner tools
https://heartbleed.michalspacek.cz/

A bit about the project background: http://blog.testomato.com/michal-spacek-we-bleed/

The whole thing has two moving parts:

1. The scanner
2. The website (which is not moving much actually)

## The scanner
You can run the back-end part (called the scanner) using the `scan.sh` script.

This is what it does:

1. Download a list of IP ranges from RIPE
2. Parse the list for IP addresses for given country (CZ in my case)
3. For every port:
  1. Run `masscan` to scan for open ports
  2. Parse the result
  3. Feed the parsed result to `ssltest.py` to scan for the Heartbleed vulnerability
4. Parse the results
5. Import the results
6. Run a query to generate more queries
7. Run those queries on the website database

## The website
Displays just totals from the database, does not hold neither scan data nor list of vulnerable hosts.
Feel free to copy https://heartbleed.michalspacek.cz/ if you wish (including the `highcharts-webleed.js` code), that's fine.
I'll be happy for a link back to my site, but it's not required.

## Setting it up
1. Download and compile `masscan` from https://github.com/robertdavidgraham/masscan
2. Clone `ssltest.py` from https://github.com/musalbas/heartbleed-masstest
3. Copy `ip.template` to `ip`, edit it
4. Load `database/scanner.sql` into a PostgreSQL database used for scan data
5. Load `database/website.sql` into a MySQL database used for displaying the charts

## Run it
1. Run `scan.sh`
2. Wait
3. Run `parse.sh`
4. Grab `data<YYYY-MM-DD>.tar.bz2`
5. Extract it
6. Import `data<PORT>.sql` into a PostgreSQL database
7. Run `generate-query.py <table> <start> <end>`, where
  1. `table` is the name of the table where to insert the data for the website, I use `webleed`
  2. `start` is the date from `data<YYYY-MM-DD>.tar.bz2` archive
  3. `end` is when the scanner has finished the latest scan
8. Run the generated query on the PostgreSQL database
9. Run the resulting queries (one rather complicated `INSERT INTO`) on the website database
10. ...
11. Profit!

## List of files in the repository
- `database/scanner.sql` - `CREATE TABLE` queries for scanner, for a PostgreSQL server
- `database/website.sql` - `CREATE TABLE` for the website, for MySQL server
- `resources/*` - icons and such
- `cleanup.sh` - a cleanup script, deletes the logs and generated files, run after the data has been imported into the database
- `exclude.txt` - excludes IP addresses, these networks do not like me
- `generate-query.py` - generates a query which generates another query to be run on the MySQL database
- `ip.template` - copy this to file called `ip` and add the IP address of your scanner, will be just inserted into the database for information purposes does not serve any other purpose
- `parse.sh` - parse the scan results, generate `data*.sql` files
- `parse-data.py` - parses data for one specific port, used by `parse.sh`
- `parse-ripedb.py` - parser for RIPE data file
- `README.md` - this file
- `scan.sh` - downloads the RIPE data, parses it, runs the scanner, aka the glue
