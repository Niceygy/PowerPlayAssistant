# PowerPlay Assistant

Powerplay asistant is a web tool for Elite: Dangerous, to help cmdrs with their powerplay 2.0 weekly tasks.

## Updates

(See [elite.niceygy.net/changelog](https://elite.niceygy.net/changelog))

### Version 1.1.0 - Added notes!

Added system notes, which will now tell you if the system is permit-locked, a power's home system and if (it thinks, still gathering data on this one) there is a res site
Also added functionality to the "description" box when selecting task "Transport Power Commodities", to tell you what one you need
<i>Updated 11:15 On 20/01/3311 (2025)</i>
<br>

### Version 1.2.0 - Anarchy Warning!

Added a "this task is a crime!" warning. Users can choose to continue or find  nearby anarchy system instead
<i>Updated 09:40 On 24/01/3311 (2025)</i>
<br>

### Version 1.3.0 - Megaship Search!

Overhauled the megaship results page, to show the 10 nearest megaships to you!
System name can be copied by clicking on it.
<i>Updated 12:20 On 27/01/3311 (2025)</i>
<br>

### Version 1.3.1 - Megaship Search Filtering!

Updated the megaship search to filter for undermining or Reinforcing systems.
(Plus a bit of text to explain)
<i>Updated 09:00 on 29/01/3311 (2025)</i>

## Development

PowerPlay assistant requires two things:

- A python (3.9+) venv

- A MariaDB Database

All python requirements can be installed using `python3 -m pip3 install -r requirements.txt`
I would reccomend using a venv! `python3 -m venv .venv`
The MariaDB can be set up with the following sql commands.

Systems table: `CREATE TABLE IF NOT EXISTS star_systems (id BIGINT PRIMARY KEY AUTO_INCREMENT, system_name VARCHAR(255), latitude DOUBLE, longitude DOUBLE, height DOUBLE, state VARCHAR(255), shortcode VARCHAR(255), is_anarchy DOUBLE, has_res_sites DOUBLE);`
<br></br>
Megaships table: `CREATE TABLE IF NOT EXISTS megaships (name VARCHAR(255) PRIMARY KEY, SYSTEM1 VARCHAR(255), SYSTEM2 VARCHAR(255), SYSTEM3 VARCHAR(255), SYSTEM4 VARCHAR(255), SYSTEM5 VARCHAR(255), SYSTEM6 VARCHAR(255));`
<br></br>
Stations table: `CREATE TABLE IF NOT EXISTS stations (id BIGINT PRIMARY KEY AUTO_INCREMENT, station_name VARCHAR(255), star_system VARCHAR(255), station_type VARCHAR(255));`

## Help

If you need help with any part, feel free to contact me on [BlueSky](https://go.niceygy.net/bsky), or on the PowerPlay Assistant [fourm thread](https://forums.frontier.co.uk/threads/powerplay-2-0-activities.629227/).

## Deployment

PowerPlay Assistant uses the following docker-compose.yml.

``` yaml
# The docker compose file that runs powerplay assistant
services:
  powerplay_assistant:
    ports:
      - 5005:5005
    container_name: PowerPlayAssistant
    stdin_open: true
    tty: true
    image: ghcr.io/niceygy/powerplayassistant
    restart: unless-stopped
    networks:
      - intranet
    depends_on:
      - mariadb
    volumes:
      - powerplaycache:/home/cache/
  mariadb:
    image: mariadb:latest
    container_name: MariaDB
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: elite
      MYSQL_USER: assistant
      MYSQL_PASSWORD: 6548
      userstat: 1
    ports:
      - 3306:3306
    volumes:
      - mariadb_data:/var/lib/mysql
      - /root/code/ED/mysql.cnf:/etc/mysql/my.cnf
    restart: unless-stopped
  data_collector:
    container_name: EDDataCollector
    stdin_open: true
    tty: true
    image: ghcr.io/niceygy/eddatacollector
    restart: unless-stopped
    networks:
      - intranet
    depends_on:
      - mariadb
networks:
  intranet: {}
volumes:
  mariadb_data: null
  powerplaycache: null
x-dockge:
  urls:
    - https://elite.niceygy.net
```