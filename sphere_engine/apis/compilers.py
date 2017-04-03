# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

from sphere_engine.exceptions import SphereEngineException
from .base import AbstractApi

class CompilersApiSubmissions(AbstractApi):
    """
    Sphere Engine Problems module for submissions
    """

    def create(self, source_code, compiler_id=1, _input='', priority=None,
               experimental=None):
        """ Create submission

        :param source_code: source code
        :type source_code: string
        :param compiler_id: id of the compiler (default 1, i.e. C++)
        :type compiler_id: integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param experimental: execute in experimental mode (default false)
        :type : bool
        :returns: submission id
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 400 for non integer compilerId
        """

        if not source_code:
            raise SphereEngineException('empty source code', 400)

        try:
            c_id = int(compiler_id)
        except:
            raise SphereEngineException('compilerId should be integer', 400)

        resource_path = '/submissions'
        method = 'POST'
        post_params = {
            'sourceCode': source_code,
            'compilerId': c_id,
            'input': _input
        }
        if priority != None:
            post_params['priority'] = priority

        if experimental != None:
            post_params['experimental'] = bool(experimental)

        response = self.api_client.call_api(resource_path, method, {}, {}, {},
                                            post_params=post_params,)

        if 'id' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def get(self, _id, with_source=False, with_input=False, with_output=False,
            with_stderr=False, with_cmpinfo=False):
        """ Get submission details

        :param _id: number of problems to get (default 10)
        :type _id: integer
        :param with_source: determines whether source code of the submission
                            should be returned (default False)
        :type with_source: bool
        :param with_input: determines whether input data of the submission
                          should be returned (default False)
        :type with_input: bool
        :param with_output: determines whether output produced by the program
                           should be returned (default False)
        :type with_output: bool
        :param with_stderr: determines whether stderr
                           should be returned (default False)
        :type with_stderr: bool
        :param with_cmpinfo: determines whether compilation information
                            should be returned (default False)
        :type with_cmpinfo: bool
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
            'withSource': int(with_source),
            'withInput': int(with_input),
            'withOutput': int(with_output),
            'withStderr': int(with_stderr),
            'withCmpinfo': int(with_cmpinfo),
        }

        response = self.api_client.call_api(resource_path, method, {'id': _id},
                                            query_data,)

        if 'status' not in response:
            raise SphereEngineException('invalid or empty response', 422)

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

        if isinstance(ids, (list, int)) is False:
            raise ValueError("getSubmissions method accepts only list or integer.")

        if isinstance(ids, (list)):
            ids = ','.join([str(x) for x in set(ids) if isinstance(x, int) and x > 0])

        resource_path = '/submissions'
        method = 'GET'

        params = {
            'ids': ids
        }

        response = self.api_client.call_api(resource_path, method, {}, params)

        if 'items' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

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

        if stream not in ["input", "stdin", "output", "stdout", "stderr",
                          "error", "cmpinfo", "source"]:
            raise SphereEngineException('stream doesn\'t exist', 404)

        resource_path = '/submissions/{id}/{stream}'
        method = 'GET'

        path_params = {
            'id': _id,
            'stream': stream
        }

        response = self.api_client.call_api(resource_path, method, path_params,
                                            response_type='file')

        return response

class CompilersApi(AbstractApi):
    """
    Sphere Engine Problems module base class
    """

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
        :raises SphereEngineException: code 422 for invalid or empty response
        """

        resource_path = '/test'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, )

        if 'answerToLifeAndEverything' not in response:
            raise SphereEngineException('invalid or empty response', 422)

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

        if 'items' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response
