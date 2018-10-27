# coding=utf-8

"""Driver for JCDecaux API."""

# Libs
import json
import requests

# Constants
BASE_URL = 'https://api.jcdecaux.com/vls'


class JCDecauxDriver(object):
    """
    JCDecauxDriver.
    Get data from JCDecaux API.
    """

    def __init__(self, key, version=1):
        """
        Initialize a connector.
        :param key: API key
        :param version: API version to use (default is 1)
        """
        # Set some variables
        self.url = BASE_URL + '/v' + str(version)
        self.key = key

    def __send(self, path, params=None):
        """
        Send an API request.
        :param path: API path to query.
        :param params: Parameters for this request.
        :returns: API answer.
        """
        # Add API key to parameters
        if params:
            params['apiKey'] = self.key
        else:
            params = {'apiKey': self.key}

        # Send the request
        try:
            res = requests.get(self.url + path, params=params)
        except requests.RequestException as e:
            print(e)
            return None

        # Catch error code
        if res.status_code == 404 or res.status_code == 400:
            return None

        # Extract data
        try:
            data = res.json()
        except json.decoder.JSONDecodeError as e:
            print(e)
            return None
        return data

    def get_contracts(self):
        """
        Get all contracts.
        :returns: List of contracts objects from API.
        """
        # Get contracts from API
        contracts = self.__send('/contracts')

        # Check errors
        if contracts is None:
            print('Not able to get contracts from API.')
            return []

        return contracts

    def get_stations(self, contract=None):
        """
        Get all stations. Allow to filter by contract.
        :param contract: Contract name to filter on. Get all if not set.
        :returns: List of stations objects from API.
        """
        # Get stations from API
        if contract:
            stations = self.__send('/stations', {'contract': contract})
        else:
            stations = self.__send('/stations')

        # Check errors
        if stations is None:
            print('Not able to get stations from API.')
            return []

        return stations

    def get_station(self, station_id, contract):
        """
        Get information for a specific station.
        :param station_id: API ID for this station (field 'number').
        :param contract: Contract name of this station.
        :returns: Station object from API.
        """
        station = self.__send('/stations/' + str(station_id), {'contract': contract})

        # Check errors
        if station is None:
            print('Not able to get station from API.')
            return []

        return station
