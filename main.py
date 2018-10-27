#!/usr/bin/python3
# coding=utf-8

"""Collect Velo'v data and push to InfluxDB."""

# Libraries
import sys
import os
import json
from urllib.parse import urlparse
from influxdb import InfluxDBClient
from jcdecaux import JCDecauxDriver

# Some constants
DIR_NAME = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(DIR_NAME, 'config/config.json')
CONTRACT_NAME = 'Lyon'


def influxb_connect(config):
    """
    Instanciate a client for InfluxDB.
    :param config: Configuration for InfluxDB
    :returns: InfluxDBClient object
    """
    # Check configuration file
    if 'url' not in config and 'user' not in config and 'password' not in config and 'database' not in config:
        print('You need to add influxdb URL, user, password and database to configuration file.')
        sys.exit(1)

    # Parse influx connection string
    o = urlparse(config['url'])
    if o.port is None:
        if o.scheme == 'https':
            port = 443
            ssl = True
        elif o.scheme == 'http':
            port = 80
            ssl = False
        else:
            port = 8086
            ssl = False
    else:
        port = o.port
        ssl = bool(o.scheme == 'https')
    if ssl:
        verify = True

    # Connect to influx db
    return InfluxDBClient(
        host=o.hostname,
        port=port,
        username=config['user'],
        password=config['password'],
        database=config['database'],
        ssl=ssl,
        verify_ssl=verify
    )


def main():
    """Run main function."""
    # Load configuration file
    try:
        with open(CONFIG_FILE, 'r') as fd:
            config = json.load(fd)
    except IOError as e:
        print('Error when reading configuration file.')
        print(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print('Invalid JSON for configuration file.')
        print(e)
        sys.exit(1)

    # Get connector for InfluxDB
    if 'influxdb' not in config:
        print('You need to add InfluxDB configuration on your config file.')
        sys.exit(1)
    influx_client = influxb_connect(config['influxdb'])

    # Get connector to JCDecaux API
    api = JCDecauxDriver(config['api']['key'])

    # Collect all metrics on an array
    metrics = []

    # Get all Velo'v stations
    stations = api.get_stations(CONTRACT_NAME)
    for station in stations:
        # Extract some data about the station
        station_id = station['number']
        station_name = station['name']
        timestamp = station['last_update']

        # Number of bike stands
        metrics.append(
            {
                'measurement': 'bike_stands',
                'tags': {
                    'name': station_name,
                    'id': station_id
                },
                'time': timestamp,
                'fields': {
                    'value': station['bike_stands']
                }
            }
        )
        # Number of stands available
        metrics.append(
            {
                'measurement': 'available_bike_stands',
                'tags': {
                    'name': station_name,
                    'id': station_id
                },
                'time': timestamp,
                'fields': {
                    'value': station['available_bike_stands']
                }
            }
        )
        # Number of available bikes
        metrics.append(
            {
                'measurement': 'available_bikes',
                'tags': {
                    'name': station_name,
                    'id': station_id
                },
                'time': timestamp,
                'fields': {
                    'value': station['available_bikes']
                }
            }
        )

    # Write points to InfluxDB
    influx_client.write_points(metrics, 'ms')


if __name__ == "__main__":
    main()
