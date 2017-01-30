#
# Sphere Engine API
#
# LICENSE
#
#
# @copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
# @license    link do licencji
# @version    0.6

from .base import AbstractApi
from sphere_engine.exceptions import SphereEngineException

class CompilersApiSubmissions(AbstractApi):

    def create(self, sourceCode, compilerId=1, _input='', priority=None):
        """ Create submission

        :param sourceCode: source code
        :type : string
        :param compilerId: id of the compiler (default 1, i.e. C++)
        :type : integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :returns: submission id
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 400 for non integer compilerId
        """

        if not sourceCode:
            raise SphereEngineException('empty source code', 400)

        try:
            _cId = int(compilerId)
        except:
            raise SphereEngineException('compilerId should be integer', 400)

        resource_path = '/submissions'
        method = 'POST'
        post_params = {
                       'sourceCode': sourceCode,
                       'compilerId': compilerId,
                       'input': _input
        }
        if priority != None:
            post_params['priority'] = priority

        response = self.api_client.call_api(resource_path,
                                            method,
                                            {},
                                            {},
                                            {},
                                            post_params=post_params,
        )
        return response

    def get(self, _id, withSource=False, withInput=False, withOutput=False, withStderr=False, withCmpinfo=False):
        """ Get submission details

        :param _id: number of problems to get (default 10)
        :type _id: integer
        :param withSource: determines whether source code of the submission should be returned (default False)
        :type withSource: bool
        :param withInput: determines whether input data of the submission should be returned (default False)
        :type withInput: bool
        :param withOutput: determines whether output produced by the program should be returned (default False)
        :type withOutput: bool
        :param withStderr: determines whether stderr should be returned (default False)
        :type withStderr: bool
        :param withCmpinfo: determines whether compilation information should be returned (default False)
        :type withCmpinfo: bool
        :returns: submission details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 404 for non existing submission
        """

        if not _id:
            raise SphereEngineException('empty _id value', 400)

        resource_path = '/submissions/{id}'
        method = 'GET'
        query_data = {
            'withSource': int(withSource),
            'withInput': int(withInput),
            'withOutput': int(withOutput),
            'withStderr': int(withStderr),
            'withCmpinfo': int(withCmpinfo),
        }

        response = self.api_client.call_api(resource_path,
                                            method,
                                            {'id': _id},
                                            query_data,
        )
        return response
    
    def getMulti(self, ids):
        """ Fetches status of multiple submissions (maximum 20 ids)
            Results are sorted ascending by id.

        :param ids: submission ids
        :type ids: integer|list
        :returns: submissions details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises ValueError: for invalid _ids param
        """
        
        if isinstance(ids, (list, int)) == False:
            raise ValueError("getSubmissions method accepts only list or integer.")
        
        if isinstance(ids, (list)):
            ids = ','.join(list(map(str, filter(lambda x: isinstance(x, (int)) and x > 0, set(ids)))))
        
        resource_path = '/submissions'
        method = 'GET'

        params = {
          'ids': ids
        }

        return self.api_client.call_api(resource_path, method, {}, params)
    
    def getStream(self, _id, stream):
        """ Fetch raw stream

        :param _id: number of problems to get (default 10)
        :type _id: integer
        :param stream: name of the stream, input|output|stderr|cmpinfo|source
        :type stream: string
        :returns: submission details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty id value
        :raises SphereEngineException: code 404 for non existing submission or non existing stream
        """

        if not _id:
            raise SphereEngineException('empty _id value', 400)

        if not stream in ["input", "stdin", "output", "stdout", "stderr", "error", "cmpinfo", "source"]:
            raise SphereEngineException('stream doesn\'t exist', 404)

        resource_path = '/submissions/{id}/{stream}'
        method = 'GET'

        path_params = {
            'id': _id,
            'stream': stream
        }

        response = self.api_client.call_api(resource_path,
                                            method,
                                            path_params
        )
        return response

class CompilersApi(AbstractApi):

    @property
    def submissions(self):
        """
        :return: CompilersApiSubmissions """
        return self._submissions

    def __init__(self, api_client):
        super(CompilersApi, self).__init__(api_client)
        self._submissions = CompilersApiSubmissions(api_client)

    def test(self):
        """ Test API connection

        :returns: Test message
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/test'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, )
        return response

    def compilers(self):
        """ Get available compilers

        :returns: List of compilers
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/compilers'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method)
        return response
