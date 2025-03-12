# PowerPlay Assistant

Powerplay asistant is a web tool for Elite: Dangerous, to help cmdrs with their powerplay 2.0 weekly tasks.

## Updates

(See [elite.niceygy.net/changelog](https://elite.niceygy.net/changelog))


## Development

PowerPlay assistant requires two things:

- A python (3.9+) venv

- A MariaDB Database

And works best with [EDDataCollector](github.com/niceygy/eddatacollector) to input data to the database.

All python requirements can be installed using `python3 -m pip3 install -r requirements.txt`
I would reccomend using a venv! `python3 -m venv .venv`
The MariaDB can be set up with the following sql commands.

Systems table: `CREATE TABLE IF NOT EXISTS star_systems (system_name VARCHAR(255) PRIMARY KEY, latitude DOUBLE, longitude DOUBLE, height DOUBLE, state VARCHAR(255), shortcode VARCHAR(255), is_anarchy TINTYINT(1), has_res_sites TINTYINT(1));`
<br></br>
Megaships table: `CREATE TABLE IF NOT EXISTS megaships (name VARCHAR(255) PRIMARY KEY, SYSTEM1 VARCHAR(255), SYSTEM2 VARCHAR(255), SYSTEM3 VARCHAR(255), SYSTEM4 VARCHAR(255), SYSTEM5 VARCHAR(255), SYSTEM6 VARCHAR(255));`
<br></br>
Stations table: `CREATE TABLE IF NOT EXISTS stations (id BIGINT PRIMARY KEY AUTO_INCREMENT, station_name VARCHAR(255), star_system VARCHAR(255), station_type VARCHAR(255), economy VARCHAR(255));`
<br></br>
You also need to run the 

## Help

If you need help with any part, feel free to contact me on [BlueSky](https://go.niceygy.net/bsky), or on the PowerPlay Assistant [fourm thread](https://forums.frontier.co.uk/threads/powerplay-2-0-activities.629227/).

## Deployment

You need a .env with the following:
`
DATABASE_CONNECTION_STRING=mysql+pymysql://<username>:<password>@<ip>/<database name>
`

PowerPlay Assistant uses the following docker-compose.yml.

``` yaml
# The docker compose file that runs powerplay assistant
services:
  powerplay_assistant:
    ports:
      - 5005:5005
    container_name: PowerPlayAssistant
    image: ghcr.io/niceygy/powerplayassistant
    restart: unless-stopped
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
    image: ghcr.io/niceygy/eddatacollector
    restart: unless-stopped
    depends_on:
      - mariadb
networks:
    {}
volumes:
  mariadb_data: null
  powerplaycache: null
x-dockge:
  urls:
    - https://elite.niceygy.net
```