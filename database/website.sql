CREATE TABLE webleed (
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    date date NOT NULL,
    port int(10) unsigned DEFAULT NULL,
    vulnerable int(10) unsigned DEFAULT NULL,
    total int(10) unsigned DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY date_port_UNIQUE (date,port)
);
