# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

from sphere_engine.exceptions import SphereEngineException
from .base import AbstractApi
import six

class ProblemsApiV4Problems(AbstractApi):
    """
    Sphere Engine Problems module for problems
    """

    def all(self, limit=10, offset=0, short_body=False):
        """ Get all problems

        :param limit: number of problems to get (default 10)
        :type limit: integer
        :param offset: starting number (default 0)
        :type offset: integer
        :param short_body: determines whether shortened body should be returned (default False)
        :type short_body: bool
        :returns: list of problems
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems'
        method = 'GET'

        query_params = {
            'limit': limit,
            'offset': offset,
            'shortBody': int(short_body)
        }

        response = self.api_client.call_api(resource_path, method, {}, query_params)

        if 'paging' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def create(self, name, masterjudge_id, body='', type_id=0, interactive=False, code=None):
        """ Create a new problem

        :param name: problem name
        :type name: string
        :param masterjudge_id: masterjudge id
        :type masterjudge_id: integer
        :param body: problem body
        :type body: string
        :param type_id: problem type id (0-binary, 1-minimize, 2-maximize) (default 0)
        :type type_id: string
        :param interactive: interactive problem flag (default False)
        :type interactive: bool
        :param code: problem code
        :type code: string
        :returns: code of created problem
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems'
        method = 'POST'

        if code == '':
            raise SphereEngineException('empty code', 400)

        if name == '':
            raise SphereEngineException('empty name', 400)

        if type_id not in [0, 1, 2]:
            raise SphereEngineException('wrong type', 400)

        post_params = {
            'name': name,
            'body': body,
            'typeId': type_id,
            'interactive': interactive,
            'masterjudgeId': masterjudge_id
        }

        if code is not None:
            post_params['code'] = code

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def get(self, _id, short_body=False):
        """ Retrieve an existing problem

        :param _id: problem id
        :type _id: integer
        :param short_body: determines whether shortened body should be returned (default False)
        :type short_body: bool
        :returns: problem details
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{id}'
        method = 'GET'

        path_params = {
            'id': _id
        }
        query_params = {
            'shortBody': int(short_body)
        }

        response = self.api_client.call_api(resource_path, method, path_params, query_params)

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def update(self, _id, name=None, masterjudge_id=None, body=None, type_id=None, interactive=None,
               active_testcases=None):
        """ Update an existing problem

        :param _id: problem id
        :type _id: integer
        :param name: problem name (default None)
        :type name: string
        :param masterjudge_id: masterjudge id (default None)
        :type masterjudge_id: integer
        :param body: problem body (default None)
        :type body: string
        :param type_id: problem type id (0-binary, 1-minimize, 2-maximize) (default None)
        :type type_id: string
        :param interactive: interactive problem flag (default None)
        :type interactive: bool
        :param active_testcases: list of active testcases IDs (default None)
        :type active_testcases: List[integer]
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        if _id == '':
            raise SphereEngineException('empty id', 400)

        if name == '':
            raise SphereEngineException('empty name', 400)

        path_params = {
            'id': _id
        }

        resource_path = '/problems/{id}'
        method = 'PUT'

        post_params = {}
        if name != None:
            post_params['name'] = name
        if body != None:
            post_params['body'] = body
        if type_id != None:
            if type_id not in [0,1,2]:
                raise SphereEngineException('wrong type id', 400)
            post_params['typeId'] = type_id
        if interactive != None:
            post_params['interactive'] = 1 if interactive else 0
        if masterjudge_id != None:
            post_params['masterjudgeId'] = masterjudge_id
        if active_testcases != None:
            post_params['activeTestcases'] = ','.join(map(str, active_testcases))

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def delete(self, id):
        """ Delete the problem

        :param id: problem id
        :type id: integer
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{id}'
        method = 'DELETE'

        path_params = {
            'id': id
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def updateActiveTestcases(self, _id, active_testcases):
        """ Update active testcases related to the problem

        :param _id: problem id
        :type _id: integer
        :param active_testcases: list of active testcases IDs
        :type active_testcases: List[integer]
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        self.update(_id, active_testcases=active_testcases)

    def allTestcases(self, problem_id):
        """ Retrieve list of problem testcases

        :param problem_id: problem code
        :type problem_id: integer
        :returns: problem testcases
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases'
        method = 'GET'

        path_params = {
            'problemId': problem_id
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if 'testcases' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def createTestcase(self, problem_id, _input='', output='', time_limit=1,
                       judge_id=1, active=True):
        """ Create a problem testcase

        :param problem_id: problem id
        :type problem_id: integer
        :param _input: model input data (default '')
        :type _input: string
        :param output: model output data (default '')
        :type output: string
        :param time_limit: time limit in seconds (default 1)
        :type time_limit: double
        :param judge_id: judge id
        :type judge_id: integer
        :param active: if test should be active (default True)
        :type active: bool
        :returns: number of created testcase
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases'
        method = 'POST'

        path_params = {
            'problemId': problem_id
        }

        post_params = {
            'input': _input,
            'output': output,
            'timeLimit': time_limit,
            'judgeId': judge_id,
            'active': active
        }

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        if 'number' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def getTestcase(self, problem_id, number):
        """ Retrieve problem testcase

        :param problem_id: problem id
        :type problem_id: integer
        :param number: testcase number
        :type number: integer
        :returns: testcase details
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases/{number}'
        method = 'GET'

        path_params = {
            'problemId': problem_id,
            'number': number
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if 'number' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def updateTestcase(self, problem_id, number, _input=None, output=None,
                       time_limit=None, judge_id=None, active=None):
        """ Update the problem testcase

        :param problemId: problem id
        :type problemId: integer
        :param number: testcase number
        :type number: integer
        :param _input: model input data (default None)
        :type _input: string
        :param output: model output data (default None)
        :type output: string
        :param time_limit: time limit in seconds (default None)
        :type time_limit: double
        :param judgeId: judge id (default None)
        :type judgeId: integer
        :param active: if test should be active (default None)
        :type active: bool
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases/{number}'
        method = 'PUT'

        path_params = {
            'problemId': problem_id,
            'number': number
        }

        post_params = {}
        if _input != None:
            post_params['input'] = _input
        if output != None:
            post_params['output'] = output
        if time_limit != None:
            post_params['timeLimit'] = time_limit
        if judge_id != None:
            post_params['judgeId'] = judge_id
        if active != None:
            post_params['active'] = active

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def deleteTestcase(self, problem_id, number):
        """ Delete the problem testcase

        :param problem_id: problem id
        :type problem_id: integer
        :param number: testcase number
        :type number: integer
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases/{number}'
        method = 'DELETE'

        path_params = {
            'problemId': problem_id,
            'number': number
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def getTestcaseFile(self, problem_id, number, filename):
        """ Retrieve a problem testcase file

        :param problem_id: problem code
        :type problem_id: integer
        :param number: testcase number
        :type number: integer
        :param filename: filename (input|output)
        :type filename: string
        :returns: file content
        :rtype: string
        :raises SphereEngineException
        """

        resource_path = '/problems/{problemId}/testcases/{number}/{filename}'
        method = 'GET'

        if filename not in ['input', 'output']:
            raise SphereEngineException('non existing file', 404)

        path_params = {
            'problemId': problem_id,
            'number': number,
            'filename': filename
        }

        response = self.api_client.call_api(resource_path, method, path_params,
                                            response_type='file')

        return response


class ProblemsApiV4Judges(AbstractApi):
    """
    Sphere Engine Problems module for judge
    """

    def all(self, limit=10, offset=0, type_id=0):
        """ List of all judges

        :param limit: number of judges to get (default 10)
        :type limit: integer
        :param offset: starting number (default 0)
        :type offset: integer
        :param type_id: type id of judge to be retrieved (0-test case, 1-master)
        :type type_id: integer
        :returns: list of judges
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/judges'
        method = 'GET'

        query_params = {
            'limit': limit,
            'offset': offset,
            'typeId': type_id
        }

        response = self.api_client.call_api(resource_path, method, {}, query_params)

        if 'items' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def create(self, source_code, compiler_id=1, type_id=0, name='', shared=False, compiler_version_id=None):
        """ Create a new judge

        :param source_code: judge source code
        :type source_code: string
        :param compiler_id: compiler id (default 1, i.e. C++)
        :type compiler_id: integer
        :param type_id: judge type id (0-test case, 1-master)
        :type type_id: integer
        :param name: judge name (default '')
        :type name: string
        :param shared: shared (default False)
        :type shared: bool
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: id of created judge
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/judges'
        method = 'POST'

        if source_code == '':
            raise SphereEngineException("empty source", 400)

        post_params = {
            'source': source_code,
            'compilerId': compiler_id,
            'typeId': type_id,
            'name': name,
            'shared': shared
        }

        if compiler_version_id != None:
            post_params['compilerVersionId'] = compiler_version_id

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def get(self, _id):
        """ Get judge details

        :param _id: judge id
        :type _id: integer
        :returns: judge details
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/judges/{id}'
        method = 'GET'

        host_params = {
            'id': _id
        }

        response = self.api_client.call_api(resource_path, method, host_params, )

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def update(self, _id, source_code=None, compiler_id=None, name=None, shared=None, compiler_version_id=None):
        """ Update judge

        :param _id: judge id
        :type _id: integer
        :param source_code: judge source code(default None)
        :type source_code: string
        :param compiler_id: compiler id (default None)
        :type compiler_id: integer
        :param name: judge name (default None)
        :type name: string
        :param shared: shared (default False)
        :type shared: bool
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/judges/{id}'
        method = 'PUT'

        if source_code != None and source_code == '':
            raise SphereEngineException('empty source', 400)

        host_params = {
            'id': _id
        }

        post_params = {}
        if source_code != None:
            post_params['source'] = source_code
        if compiler_id != None:
            post_params['compilerId'] = compiler_id
        if name != None:
            post_params['name'] = name
        if shared != None:
            post_params['shared'] = shared

        if compiler_version_id != None:
            post_params['compilerVersionId'] = compiler_version_id

        response = self.api_client.call_api(resource_path, method, host_params, {}, {}, post_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def getJudgeFile(self, _id, filename):
        """ Retrieve a judge file

        :param _id: judge id
        :type _id: integer
        :param filename: filename (source)
        :type filename: string
        :returns: file content
        :rtype: string
        :raises SphereEngineException
        """
        
        resource_path = '/judges/{id}/{filename}'
        method = 'GET'

        if filename not in ['source']:
            raise SphereEngineException('non existing file', 404)

        path_params = {
            'id': _id,
            'filename': filename
        }

        response = self.api_client.call_api(resource_path, method, path_params,
                                            response_type='file')

        return response


class ProblemsApiV4Submissions(AbstractApi):
    """
    Sphere Engine Problems module for submissions
    """

    def get(self, _id):
        """ Fetch submission details

        :param id: submission id
        :type _id: integer
        :returns: submission details
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/submissions/{id}'
        method = 'GET'

        host_params = {
            'id': _id
        }

        response = self.api_client.call_api(resource_path, method, host_params, )

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response

    def getSubmissionFile(self, _id, filename):
        """ Retrieve a submission file

        :param _id: submission id
        :type _id: integer
        :param filename: filename (source|output|error|cmpinfo|debug)
        :type filename: string
        :returns: file content
        :rtype: string
        :raises SphereEngineException
        """
        
        resource_path = '/submissions/{id}/{filename}'
        method = 'GET'

        if filename not in ['source', 'output', 'error', 'cmpinfo', 'debug']:
            raise SphereEngineException('non existing file', 404)

        path_params = {
            'id': _id,
            'filename': filename
        }

        response = self.api_client.call_api(resource_path, method, path_params,
                                            response_type='file')

        return response

    def getMulti(self, ids):
        """ Fetches status of multiple submissions (maximum 20 ids)
            Results are sorted ascending by id.

        :param ids: submission ids
        :type ids: integer|list
        :returns: submissions details
        :rtype: json
        :raises SphereEngineException
        :raises ValueError: for invalid ids param
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
    
    def create(self, problem_id, source, compiler_id=None, priority=None, tests=[], compiler_version_id=None):
        """ Create a new submission

        :param problem_id: problem id (or code)
        :type problem_id: integer
        :param source: submission source code
        :type source: string
        :param compiler_id: compiler id
        :type compiler_id: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type priority: integer
        :param tests: tests to run (default [])
        :type tests: list
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: id of created submission
        :rtype: json
        :raises SphereEngineException
        """
        
        return self.__create(problem_id, source, compiler_id, priority, {}, tests, compiler_version_id)
        
    def createMultiFiles(self, problem_id, files, compiler_id=None, priority=None, tests=[], compiler_version_id=None):
        """ Create a new submission with multi files

        :param problem_id: problem id (or code)
        :type problem_id: integer
        :param files: files (default {})
        :type tests: dict
        :param compiler_id: compiler id
        :type compiler_id: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type priority: integer
        :param tests: tests to run (default [])
        :type tests: list
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: id of created submission
        :rtype: json
        :raises SphereEngineException
        """
        
        return self.__create(problem_id, '', compiler_id, priority, files, tests, compiler_version_id)

    def createWithTarSource(self, problem_id, tar_source, compiler_id=None, priority=None, tests=[], compiler_version_id=None):
        """ Create a new submission from tar source

        :param problem_id: problem id (or code)
        :type problem_id: integer
        :param tar_source: tar(tar.gz) source
        :type tar_source: string
        :param compiler_id: compiler id
        :type compiler_id: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type priority: integer
        :param tests: tests to run (default [])
        :type tests: list
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: id of created submission
        :rtype: json
        :raises SphereEngineException
        """
        
        return self.__create(problem_id, tar_source, compiler_id, priority, {}, tests, compiler_version_id)
        
    def __create(self, problem_id, source, compiler_id=None, priority=None, files={}, tests=[], compiler_version_id=None):
        """ Create a new submission

        :param problem_id: problem id (or code)
        :type problem_id: integer
        :param source: submission source code
        :type source: string
        :param compiler_id: compiler id
        :type compiler_id: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type priority: integer
        :param files: files (default {})
        :type tests: dict
        :param tests: tests to run (default [])
        :type tests: list
        :param compiler_version_id: id of the compiler version (default: default for api v4)
        :type compiler_version_id: integer
        :returns: id of created submission
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/submissions'
        method = 'POST'

        post_params = {
            'problemId': problem_id,
            'compilerId': compiler_id,
            'source': source
        }
        files_params = {}

        if priority != None:
            post_params['priority'] = priority
            
        if len(files):
            for k, v in files.items():
                if not isinstance(v, six.string_types):
                    continue
                files_params['files['+k+']'] = v
            post_params['source'] = ''

        if len(tests):
            post_params['tests'] = ','.join(tests);

        if compiler_version_id != None:
            post_params['compilerVersionId'] = compiler_version_id

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params, files_params)

        if 'id' not in response:
            raise SphereEngineException('unexpected error', 400)

        return response
    
    def update(self, _id):
        """ Update an existing submission

        :param _id: submission id
        :type _id: integer
        :returns: void
        :rtype: json
        :raises SphereEngineException
        """

        path_params = {
            'id': _id
        }

        resource_path = '/submissions/{id}'
        method = 'PUT'

        post_params = {}

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('unexpected error', 400)

        return response

class ProblemsApiV4(AbstractApi):
    """
    Sphere Engine Problems module base class
    """

    @property
    def problems(self):
        """
        :return: ProblemsApiProblems """
        return self._problems

    @property
    def judges(self):
        """
        :return: ProblemsApiJudges """
        return self._judges

    @property
    def submissions(self):
        """
        :return: ProblemsApiSubmissions """
        return self._submissions

    def __init__(self, api_client):
        """
        @param api_client: sphere_engine.api_client.ApiClient
        """
        super(ProblemsApiV4, self).__init__(api_client)
        self._problems = ProblemsApiV4Problems(api_client)
        self._judges = ProblemsApiV4Judges(api_client)
        self._submissions = ProblemsApiV4Submissions(api_client)

    def test(self):
        """ Test API connection

        :returns: test message
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/test'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, )
        return response

    def compilers(self):
        """ Get available compilers

        :returns: list of compilers
        :rtype: json
        :raises SphereEngineException
        """

        resource_path = '/compilers'
        method = 'GET'

        response = self.api_client.call_api(resource_path,
                                            method,)
        return response
