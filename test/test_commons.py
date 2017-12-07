# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

import json

class MockResponse(object):
    """
    Wrapper for response in mocks
    """

    text = None

    def __init__(self, text):
        self.text = text

    def json(self):
        """
        Mocking retrieving as JSON
        """

        return self.text

def get_mock_data(data_json_path):
    """
    Gets data from JSON mock file.

        :param data_json_path: path to data in json file
        :type data_json_path: string
        :raises IOError on nonexisting JSON file
        :raises KeyError on nonexisting data in JSON
        :returns: data from json file
        :rtype: dict
    """

    return _get_mock_data(data_json_path)

def get_mock_dataV4(data_json_path):
    """
    Gets data from JSON mock file.

        :param data_json_path: path to data in json file
        :type data_json_path: string
        :raises IOError on nonexisting JSON file
        :raises KeyError on nonexisting data in JSON
        :returns: data from json file
        :rtype: dict
    """
    
    return _get_mock_data(data_json_path, 'V4')
        
def _get_mock_data(data_json_path, version = ''):
    """
    Gets data from JSON mock file.

        :param data_json_path: path to data in json file
        :type data_json_path: string
        :raises IOError on nonexisting JSON file
        :raises KeyError on nonexisting data in JSON
        :returns: data from json file
        :rtype: dict
    """
    
    with open('./client-commons/mockData'+version+'.json') as mock_data:
        mock_data = json.load(mock_data)
        path_array = data_json_path.split('/')

        for p in path_array:
            mock_data = mock_data[p]

        http_code = mock_data['httpCode'] if 'httpCode' in mock_data else 0
        http_body = mock_data['httpBody'] if 'httpBody' in mock_data else ''
        conn_errno = mock_data['connErrno'] if 'connErrno' in mock_data else 0
        conn_error = mock_data['connError'] if 'connError' in mock_data else ''

        return {
            'http_code': http_code,
            'http_body': MockResponse(http_body),
            'conn_errno': conn_errno,
            'conn_error': conn_error,
        }

