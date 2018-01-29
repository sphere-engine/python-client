# coding: utf-8

"""
Sphere Engine API

@copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
"""

from sphere_engine.exceptions import SphereEngineException
from .base import AbstractApi

class ProblemsApiProblems(AbstractApi):
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
        :raises SphereEngineException: code 401 for invalid access token
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
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def create(self, code, name, body='', _type='bin', interactive=False, masterjudge_id=1001):
        """ Create a new problem

        :param code: problem code
        :type code: string
        :param name: problem name
        :type name: string
        :param body: problem body
        :type body: string
        :param _type: problem type (default 'bin')
        :type _type: string ('binary', 'min' or 'max')
        :param interactive: interactive problem flag (default False)
        :type interactive: bool
        :param masterjudge_id: masterjudge id (default 1001, i.e. % of correctly solved testcases)
        :type masterjudge_id: integer
        :returns: code of created problem
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty problem code
        :raises SphereEngineException: code 400 for empty problem name
        :raises SphereEngineException: code 400 for not unique problem code
        :raises SphereEngineException: code 400 for invalid problem code
        :raises SphereEngineException: code 400 for invalid type
        :raises SphereEngineException: code 404 for non existing masterjudge
        """

        resource_path = '/problems'
        method = 'POST'

        if code == '':
            raise SphereEngineException('empty code', 400)

        if name == '':
            raise SphereEngineException('empty name', 400)

        if _type not in ['min', 'max', 'bin', 'minimize', 'maximize', 'binary']:
            raise SphereEngineException('wrong type', 400)

        post_params = {
            'code': code,
            'name': name,
            'body': body,
            'type': _type,
            'interactive': interactive,
            'masterjudgeId': masterjudge_id
        }

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

        if 'code' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def get(self, code, short_body=False):
        """ Retrieve an existing problem

        :param code: problem code
        :type code: string
        :param short_body: determines whether shortened body should be returned (default False)
        :type short_body: bool
        :returns: problem details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 404 for non existing problem
        """

        resource_path = '/problems/{code}'
        method = 'GET'

        path_params = {
            'code': code
        }
        query_params = {
            'shortBody': int(short_body)
        }

        response = self.api_client.call_api(resource_path, method, path_params, query_params)

        if 'code' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def update(self, code, name=None, body=None, _type=None, interactive=None,
               masterjudge_id=None, active_testcases=None):
        """ Update an existing problem

        :param code: problem code
        :type code: string
        :param name: problem name (default None)
        :type name: string
        :param body: problem body (default None)
        :type body: string
        :param _type: problem type (default None)
        :type _type: string ('binary', 'min' or 'max')
        :param interactive: interactive problem flag (default None)
        :type interactive: bool
        :param masterjudge_id: masterjudge id (default None)
        :type masterjudge_id: integer
        :param active_testcases: list of active testcases IDs (default None)
        :type active_testcases: List[integer]
        :returns: code of created problem
        :rtype: json
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for modifying foreign problem
        :raises SphereEngineException: code 400 for empty problem code
        :raises SphereEngineException: code 400 for empty problem name
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing masterjudge
        """

        if code == '':
            raise SphereEngineException('empty code', 400)

        if name == '':
            raise SphereEngineException('empty name', 400)

        path_params = {
            'code': code
        }

        resource_path = '/problems/{code}'
        method = 'PUT'

        post_params = {}
        if name != None:
            post_params['name'] = name
        if body != None:
            post_params['body'] = body
        if _type != None:
            if _type not in ['min', 'max', 'bin', 'minimize', 'maximize', 'binary']:
                raise SphereEngineException('wrong type', 400)
            post_params['type'] = _type
        if interactive != None:
            post_params['interactive'] = 1 if interactive else 0
        if masterjudge_id != None:
            post_params['masterjudgeId'] = masterjudge_id
        if active_testcases != None:
            post_params['activeTestcases'] = ','.join(map(str, active_testcases))

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        return response

    def updateActiveTestcases(self, code, active_testcases):
        """ Update active testcases related to the problem

        :param code: problem code
        :type code: string
        :param active_testcases: list of active testcases IDs
        :type active_testcases: List[integer]
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for modifying foreign problem
        :raises SphereEngineException: code 400 for empty problem code
        :raises SphereEngineException: code 404 for non existing problem
        """

        self.update(code, active_testcases=active_testcases)

    def allTestcases(self, problem_code):
        """ Retrieve list of problem testcases

        :param problemCode: problem code
        :type problemCode: string
        :returns: problem testcases
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for retrieving testcases of foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        """

        resource_path = '/problems/{problemCode}/testcases'
        method = 'GET'

        path_params = {
            'problemCode': problem_code
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if 'testcases' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def createTestcase(self, problem_code, _input='', output='', timelimit=1,
                       judge_id=1, active=True):
        """ Create a problem testcase

        :param problem_code: problem code
        :type problem_code: string
        :param _input: model input data (default '')
        :type _input: string
        :param output: model output data (default '')
        :type output: string
        :param timelimit: time limit in seconds (default 1)
        :type timelimit: double
        :param judge_id: judge id (default 1, i.e. Ignore extra whitespaces)
        :type judge_id: integer
        :param active: if test should be active (default True)
        :type active: bool
        :returns: number of created testcase
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for adding a testcase to foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing judge
        """

        resource_path = '/problems/{problemCode}/testcases'
        method = 'POST'

        path_params = {
            'problemCode': problem_code
        }

        post_params = {
            'input': _input,
            'output': output,
            'timelimit': timelimit,
            'judgeId': judge_id,
            'active': active
        }

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        if 'number' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def getTestcase(self, problem_code, number):
        """ Retrieve problem testcase

        :param problemCode: problem code
        :type problemCode: string
        :param number: testcase number
        :type number: integer
        :returns: testcase details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for retrieving a testcase of foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing testcase
        """

        resource_path = '/problems/{problemCode}/testcases/{number}'
        method = 'GET'

        path_params = {
            'problemCode': problem_code,
            'number': number
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if 'number' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def updateTestcase(self, problem_code, number, _input=None, output=None,
                       timelimit=None, judge_id=None, active=None):
        """ Update the problem testcase

        :param problemCode: problem code
        :type problemCode: string
        :param number: testcase number
        :type number: integer
        :param _input: model input data (default None)
        :type _input: string
        :param output: model output data (default None)
        :type output: string
        :param timelimit: time limit in seconds (default None)
        :type timelimit: double
        :param judgeId: judge id (default None)
        :type judgeId: integer
        :param active: if test should be active (default None)
        :type active: bool
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for adding a testcase to foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing testcase
        :raises SphereEngineException: code 404 for non existing judge
        """

        resource_path = '/problems/{problemCode}/testcases/{number}'
        method = 'PUT'

        path_params = {
            'problemCode': problem_code,
            'number': number
        }

        post_params = {}
        if _input != None:
            post_params['input'] = _input
        if output != None:
            post_params['output'] = output
        if timelimit != None:
            post_params['timelimit'] = timelimit
        if judge_id != None:
            post_params['judgeId'] = judge_id
        if active != None:
            post_params['active'] = active

        response = self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

        return response

    def deleteTestcase(self, problem_code, number):
        """ Delete the problem testcase

        :param problemCode: problem code
        :type problemCode: string
        :param number: testcase number
        :type number: integer
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for retrieving a testcase of foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing testcase
        """

        resource_path = '/problems/{problemCode}/testcases/{number}'
        method = 'DELETE'

        path_params = {
            'problemCode': problem_code,
            'number': number
        }

        response = self.api_client.call_api(resource_path, method, path_params)

        if not isinstance(response, dict) or response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def getTestcaseFile(self, problem_code, number, filename):
        """ Retrieve a problem testcase file

        :param problemCode: problem code
        :type problemCode: string
        :param number: testcase number
        :type number: integer
        :param filename: filename
        :type filename: string
        :returns: file content
        :rtype: string
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for retrieving a testcase of foreign problem
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing testcase
        :raises SphereEngineException: code 404 for non existing file
        """

        resource_path = '/problems/{problemCode}/testcases/{number}/{filename}'
        method = 'GET'

        if filename not in ['input', 'output', 'stdin', 'stdout']:
            raise SphereEngineException('nonexisting file', 404)

        path_params = {
            'problemCode': problem_code,
            'number': number,
            'filename': filename
        }

        response = self.api_client.call_api(resource_path, method, path_params,
                                            response_type='file')

        return response


class ProblemsApiJudges(AbstractApi):
    """
    Sphere Engine Problems module for judge
    """

    def all(self, limit=10, offset=0, _type='testcase'):
        """ List of all judges

        :param limit: number of judges to get (default 10)
        :type limit: integer
        :param offset: starting number (default 0)
        :type offset: integer
        :returns: list of judges
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/judges'
        method = 'GET'

        query_params = {
            'limit': limit,
            'offset': offset
        }

        response = self.api_client.call_api(resource_path, method, {}, query_params)

        if 'items' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def create(self, source_code, compiler_id=1, _type='testcase', name=''):
        """ Create a new judge

        :param source_code: judge source code
        :type source_code: string
        :param compiler_id: compiler id (default 1, i.e. C++)
        :type compiler_id: integer
        :param _type: judge type
        :type _type: string ('testcase' or 'master')
        :param name: judge name (default '')
        :type name: string
        :returns: id of created judge
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 404 for non existing compiler
        """

        resource_path = '/judges'
        method = 'POST'

        if source_code == '':
            raise SphereEngineException("empty source", 400)

        post_params = {
            'source': source_code,
            'compilerId': compiler_id,
            'type': _type,
            'name': name,
        }

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

        if 'id' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def get(self, _id):
        """ Get judge details

        :param _id: judge id
        :type _id: integer
        :returns: judge details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for retrieving foreign judge details
        :raises SphereEngineException: code 404 for non existing judge
        """

        resource_path = '/judges/{id}'
        method = 'GET'

        host_params = {
            'id': _id
        }

        response = self.api_client.call_api(resource_path, method, host_params, )

        if 'id' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def update(self, _id, source_code=None, compiler_id=None, name=None):
        """ Update judge

        :param _id: judge id
        :type _id: integer
        :param source_code: judge source code(default None)
        :type source_code: string
        :param compiler_id: compiler id (default None)
        :type compiler_id: integer
        :param name: judge name (default None)
        :type name: string
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for modifying foreign judge
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 404 for non existing judge
        :raises SphereEngineException: code 404 for non existing compiler
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

        response = self.api_client.call_api(resource_path, method, host_params, {}, {}, post_params)

        return response


class ProblemsApiSubmissions(AbstractApi):
    """
    Sphere Engine Problems module for submissions
    """

    def get(self, _id):
        """ Fetch submission details

        :param id: submission id
        :type _id: integer
        :returns: submission details
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 404 for non existing submission
        """

        resource_path = '/submissions/{id}'
        method = 'GET'

        host_params = {
            'id': _id
        }

        response = self.api_client.call_api(resource_path, method, host_params, )

        if 'id' not in response:
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
            raise SphereEngineException('invalid or empty response', 422)

        return response

    def create(self, problem_code, source, compiler_id=None, user_id=None,
               priority=None, experimental=None):
        """ Create a new submission

        :param problem_code: problem code
        :type problem_code: string
        :param source: submission source code
        :type source: string
        :param compiler_id: compiler id
        :type compiler_id: integer
        :param user_id: user id
        :type user_id: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
        :param experimental: execute in experimental mode (default false)
        :type : bool
        :returns: id of created submission
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 400 for empty source code
        :raises SphereEngineException: code 404 for non existing problem
        :raises SphereEngineException: code 404 for non existing user
        :raises SphereEngineException: code 404 for non existing compiler
        """

        resource_path = '/submissions'
        method = 'POST'

        if source == '':
            raise SphereEngineException('empty source', 400)

        post_params = {
            'problemCode': problem_code,
            'compilerId': compiler_id,
            'source': source
        }

        if user_id != None:
            post_params['userId'] = user_id

        if priority != None:
            post_params['priority'] = priority

        if experimental != None:
            post_params['experimental'] = bool(experimental)

        response = self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

        if 'id' not in response:
            raise SphereEngineException('invalid or empty response', 422)

        return response

class ProblemsApi(AbstractApi):
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
        super(ProblemsApi, self).__init__(api_client)
        self._problems = ProblemsApiProblems(api_client)
        self._judges = ProblemsApiJudges(api_client)
        self._submissions = ProblemsApiSubmissions(api_client)

    def test(self):
        """ Test API connection

        :returns: test message
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/test'
        method = 'GET'

        response = self.api_client.call_api(resource_path, method, )
        return response

    def compilers(self):
        """ Get available compilers

        :returns: list of compilers
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/compilers'
        method = 'GET'

        response = self.api_client.call_api(resource_path,
                                            method,)
        return response
