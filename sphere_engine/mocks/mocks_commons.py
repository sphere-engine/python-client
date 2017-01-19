import json

from sphere_engine.exceptions import SphereEngineException

class MockCommons(object):
    
    def __init__(self, api_client):
        self.api_client = api_client

    def is_access_token_correct():
        return self.access_token == 'correct_access_token'

    # /**
    #  * Returns value under key in associative array
    #  * @param array $array associative array
    #  * @param string $key key to be looked in array
    #  * @param boolean $null_if_not_exists function returns null if value doesn't exists, otherwise exception is thrown
    #  * @throws \Exception if $null_if_not_exists is false and the value doesn't exist
    #  * @return mixed
    #  */
    def get_param(array, key, none_if_not_exists):
        try:
            return array[key]
        except IndexError:
            if none_if_not_exists:
                return none
            else:
                raise Exception('Lack of ' + key + ' parameter')

    def get_data_path(self, routing_json_path):
        """
        Gets json path to data from json path from routing

            :param routing_json_path: path to routing json
            :type routing_json_path: string
            :raises IOError on nonexisting JSON file
            :raises KeyError on nonexisting data in JSON
            :returns: path to data
            :rtype: string
        """    
        
        with open('./client-commons/mockRouting.json') as mock_routing:    
            mock_routing = json.load(mock_routing)
            path_array = routing_json_path.split('/')

            for p in path_array:
                mock_routing = mock_routing[p]

            return mock_routing

    def get_mock_data(self, routing_json_path):
        """
        Gets data from JSON mock file.

            :param routing_json_path: path to routing json
            :type routing_json_path: string
            :raises IOError on nonexisting JSON file
            :raises KeyError on nonexisting data in JSON
            :returns: data from json file
            :rtype: MockResponse
        """    
        
        with open('./client-commons/mockData.json') as mock_data:    
            mock_data = json.load(mock_data)
            data_json_path = self.get_data_path(routing_json_path)
            path_array = data_json_path.split('/')

            for p in path_array:
                mock_data = mock_data[p]

            httpCode = mock_data['httpCode'] if 'httpCode' in mock_data else 0
            httpBody = mock_data['httpBody'] if 'httpBody' in mock_data else ''
            connErrno = mock_data['connErrno'] if 'connErrno' in mock_data else 0
            connError = mock_data['connError'] if 'connError' in mock_data else ''

            return MockResponse(httpBody)    

class MockResponse(object):

    text = None

    def __init__(self, text):
        self.text = text

    def json(self):
        return self.text
