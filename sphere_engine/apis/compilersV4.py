# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

from sphere_engine.exceptions import SphereEngineException
from .base import AbstractApi
import six

class CompilersApiV4Submissions(AbstractApi):
    """
    Sphere Engine Problems module for submissions
    """

    def create(self, source='', compiler_id=1, _input='', priority=None, time_limit=None, memory_limit=None, compiler_version_id=None):
        """ Create submission

        :param source: source code (default '')
        :type source: string
        :param compiler_id: id of the compiler (default 1, i.e. C++)
        :type compiler_id: integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param time_limit: time limit (default 5)
        :type integer
        :param memory_limit: memory limit (default: no limit)
        :type integer
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type integer
        :returns: submission id
        :rtype: json
        :raises SphereEngineException
        """

        return self.__create(source, compiler_id, _input, priority, {}, time_limit, memory_limit, compiler_version_id)

    def createMultiFiles(self, files={}, compiler_id=1, _input='', priority=None, time_limit=None, memory_limit=None, compiler_version_id=None):
        """ Create submission with multi files

        :param files: files {fileName: fileContent} (default {})
        :type files: dictionary
        :param compiler_id: id of the compiler (default 1, i.e. C++)
        :type compiler_id: integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param time_limit: time limit (default 5)
        :type integer
        :param memory_limit: memory limit (default: no limit)
        :type integer
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type integer
        :returns: submission id
        :rtype: json
        :raises SphereEngineException
        """
        
        return self.__create('', compiler_id, _input, priority, files, time_limit, memory_limit, compiler_version_id)

    def createWithTarSource(self, tar_source='', compiler_id=1, _input='', priority=None, time_limit=None, memory_limit=None, compiler_version_id=None):
        """ Create submission from tar source

        :param tar_source: tar source (default '')
        :type tar_source: string
        :param compiler_id: id of the compiler (default 1, i.e. C++)
        :type compiler_id: integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param time_limit: time limit (default 5)
        :type integer
        :param memory_limit: memory limit (default: no limit)
        :type integer
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type integer
        :returns: submission id
        :rtype: json
        :raises SphereEngineException
        """
        
        return self.__create(tar_source, compiler_id, _input, priority, {}, time_limit, memory_limit, compiler_version_id)
        
    def __create(self, source='', compiler_id=1, _input='', priority=None, files={}, time_limit=None, memory_limit=None, compiler_version_id=None):
        """ Create submission

        :param source: source code (default '')
        :type source: string
        :param compiler_id: id of the compiler (default 1, i.e. C++)
        :type compiler_id: integer
        :param _input: input for the program (default '')
        :type : string
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param time_limit: time limit (default 5)
        :type integer
        :param memory_limit: memory limit (default: no limit)
        :type integer
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type integer
        :returns: submission id
        :rtype: json
        :raises SphereEngineException
        """
        
        try:
            c_id = int(compiler_id)
        except:
            raise SphereEngineException('compilerId should be integer', 400)
    
        resource_path = '/submissions'
        method = 'POST'
        post_params = {
            'source': source,
            'compilerId': c_id,
            'input': _input
        }
        files_params = {}

        if priority != None:
            post_params['priority'] = priority

        if len(files):
            for k, v in files.items():
                if not isinstance(v, six.string_types):
                    continue
                files_params['files['+k+']'] = (k, v);
            post_params['source'] = ''

        if time_limit != None:
            post_params['timeLimit'] = time_limit
            
        if memory_limit != None:
            post_params['memoryLimit'] = memory_limit

        if compiler_version_id != None:
            post_params['compilerVersionId'] = compiler_version_id

        response = self.api_client.call_api(resource_path, method, {}, {}, {},
            post_params=post_params, files_params=files_params)

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def get(self, _id):
        """ Get submission details

        :param _id: submission id
        :type _id: integer
        :returns: submission details
        :rtype: json
        :raises SphereEngineException
        """

        if not _id:
            raise SphereEngineException('empty _id value', 400)

        resource_path = '/submissions/{id}'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, {'id': _id})

        if 'result' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def getMulti(self, ids):
        """ Fetches status of multiple submissions (maximum 20 ids)
            Results are sorted ascending by id.

        :param ids: submission ids
        :type ids: integer|list
        :returns: submissions details
        :rtype: json
        :raises SphereEngineException
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
            raise SphereEngineException('unexpected error', 400)

        return response

    def getStream(self, _id, stream):
        """ Fetch raw stream

        :param _id: submission id
        :type _id: integer
        :param stream: name of the stream, source|input|output|error|cmpinfo
        :type stream: string
        :returns: submission details
        :rtype: json
        :raises SphereEngineException
        """

        if not _id:
            raise SphereEngineException('empty _id value', 400)

        if stream not in ["source", "input", "output", "error", "cmpinfo"]:
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

class CompilersApiV4(AbstractApi):
    """
    Sphere Engine Problems module base class
    """

    @property
    def submissions(self):
        """
        :return: CompilersApiV4Submissions """
        return self._submissions

    def __init__(self, api_client):
        super(CompilersApiV4, self).__init__(api_client)
        self._submissions = CompilersApiV4Submissions(api_client)

    def test(self):
        """ Test API connection

        :returns: Test message
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/test'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, )

        if 'message' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def compilers(self):
        """ Get available compilers

        :returns: List of compilers
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/compilers'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method)

        if 'items' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response
