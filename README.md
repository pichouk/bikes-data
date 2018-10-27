# Bikes data

Simple project that collect data about Velo'v station (from [JCDecaux API](https://developer.jcdecaux.com)) and push them to InfluxDB.

## Usage

You can simply run this script after installing requirements (`pipenv install`) and creating a configuration file with `pipenv run python main.py`. But the recommended way is to use Docker (see below).

### Configuration

This bot use a JSON file to get some different configuration variables it needs. An example of this file is provided under `config/config_example.json` and need to be copy (and modified) as `config/config.json`. This file contains InfluxDB connection information and configuration needed for JCDecaux API :
- `influxdb.url` : complete URL to connect to InfluxDB (eg. `https://my.influxinstance.tld`)
- `influxdb.user` : A user with write access to InfluxDB
- `influxdb.password` : Password for the user
- `influxdb.database` : Database to use
- `api.key`: API key

### Docker

A simple Docker image is provided in order to run this bot on a regular basis. It is a simple Python 3 (Alpine based) Docker image with all the requirements. The entrypoint is quite simple : a while loop that call the `main.py` script and sleep for some times. The interval to sleep between each calls can be configured with the environment variable `INTERVAL_SECONDS` (default to `10`).

Also, don't forget to mount your configuration file on `/code/config/config.json`

## Metrics

Following metrics are exported by this bot :
- `bike_stands` : Number of existing bike stands (with station's `id` and `name` tags)
- `available_bike_stands` : Number of available bike stands (with station's `id` and `name` tags)
- `available_bikes` : Number of available bikes (with station's `id` and `name` tags)
