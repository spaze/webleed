CREATE TABLE scans (
    id SERIAL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    total integer NOT NULL,
    total_open_port integer NOT NULL,
    note text,
    ip inet NOT NULL,
    port integer NOT NULL
);
COMMENT ON COLUMN scans.total_open_port IS 'Number of IP addresses with given port open';
COMMENT ON COLUMN scans.ip IS 'Outgoing IP address of the scan';
COMMENT ON COLUMN scans.port IS 'Target port of the scan';
ALTER TABLE ONLY scans
    ADD CONSTRAINT scans_pkey PRIMARY KEY (id);


CREATE TABLE networks (
    id SERIAL,
    scan_id integer,
    network cidr
);
ALTER TABLE ONLY networks
    ADD CONSTRAINT networks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY networks
    ADD CONSTRAINT networks_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES scans(id) ON UPDATE CASCADE ON DELETE CASCADE;


CREATE TABLE hosts (
    id SERIAL,
    scan_id integer NOT NULL,
    host inet NOT NULL,
    vulnerable boolean NOT NULL,
    scanned timestamp with time zone
);
COMMENT ON TABLE hosts IS 'Only hosts that respond on given port are added here';
CREATE INDEX hosts_vulnerable_idx ON hosts (vulnerable);
ALTER TABLE ONLY hosts
    ADD CONSTRAINT hosts_scan_id_fkey FOREIGN KEY (scan_id) REFERENCES scans(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY hosts
    ADD CONSTRAINT hosts_pkey PRIMARY KEY (id);
