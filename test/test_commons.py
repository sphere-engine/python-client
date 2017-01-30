import json

class MockResponse(object):

    text = None

    def __init__(self, text):
        self.text = text

    def json(self):
        return self.text

def get_mock_data(data_json_path):
    """
    Gets data from JSON mock file.

        :param routing_json_path: path to routing json
        :type routing_json_path: string
        :raises IOError on nonexisting JSON file
        :raises KeyError on nonexisting data in JSON
        :returns: data from json file
        :rtype: dict
    """    
    
    with open('./client-commons/mockData.json') as mock_data:    
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
