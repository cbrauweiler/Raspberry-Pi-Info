--
-- Tabellenstruktur für Tabelle `data`
--

CREATE TABLE `data` (
  `id` int(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `hostname` varchar(255) NOT NULL,
  `ipaddress` varchar(25) NOT NULL,
  `os` varchar(200) NOT NULL,
  `board` varchar(25) NOT NULL,
  `cpu_clock` smallint(6) NOT NULL DEFAULT 0,
  `cpu_temp` float NOT NULL DEFAULT 0,
  `cpu_usage` float NOT NULL DEFAULT 0,
  `cpu_voltage` float NOT NULL DEFAULT 0,
  `ram_total` float NOT NULL DEFAULT 0,
  `ram_usage` float NOT NULL DEFAULT 0,
  `ram_free` float NOT NULL DEFAULT 0,
  `disk_total` varchar(50) NOT NULL DEFAULT '0',
  `disk_usage` varchar(50) NOT NULL DEFAULT '0',
  `disk_perc` varchar(50) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `data`
--
ALTER TABLE `data`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT;
COMMIT;
