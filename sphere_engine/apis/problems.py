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

class ProblemsApiProblems(AbstractApi):

    def all(self, limit=10, offset=0, shortBody=False):
        """ Get all problems

        :param limit: number of problems to get (default 10)
        :type limit: integer
        :param offset: starting number (default 0)
        :type offset: integer
        :param shortBody: determines whether shortened body should be returned (default False)
        :type shortBody: bool
        :returns: list of problems
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        """

        resource_path = '/problems'
        method = 'GET'

        query_params = {
            'limit': limit,
            'offset': offset,
            'shortBody': int(shortBody)
        }

        return self.api_client.call_api(resource_path, method, {}, query_params)

    def create(self, code, name, body='', _type='bin', interactive=False, masterjudgeId=1001):
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
        :param masterjudgeId: masterjudge id (default 1001, i.e. Score is % of correctly solved testcases)
        :type masterjudgeId: integer
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
           'masterjudgeId': masterjudgeId
        }

        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

    def get(self, code, shortBody=False):
        """ Retrieve an existing problem

        :param code: problem code
        :type code: string
        :param shortBody: determines whether shortened body should be returned (default False)
        :type shortBody: bool
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
            'shortBody': int(shortBody)
        }

        return self.api_client.call_api(resource_path, method, path_params, query_params)

    def update(self, code, name=None, body=None, _type=None, interactive=None, masterjudgeId=None, activeTestcases=None):
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
        :param masterjudgeId: masterjudge id (default None)
        :type masterjudgeId: integer
        :param activeTestcases: list of active testcases IDs (default None)
        :type activeTestcases: List[integer]
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
        };

        resource_path = '/problems/{code}'
        method = 'PUT'

        post_params = {}
        if name != None:
            post_params['name'] = name;
        if body != None:
            post_params['body'] = body
        if _type != None:
            if _type not in ['min', 'max', 'bin', 'minimize', 'maximize', 'binary']:
                raise SphereEngineException('wrong type', 400)
            post_params['type'] = _type
        if interactive != None:
            post_params['interactive'] = 1 if interactive else 0
        if masterjudgeId != None:
            post_params['masterjudgeId'] = masterjudgeId
        if activeTestcases != None:
            post_params['activeTestcases'] = ','.join(map(str, activeTestcases))

        return self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

    def updateActiveTestcases(self, code, activeTestcases):
        """ Update active testcases related to the problem

        :param code: problem code
        :type code: string
        :param activeTestcases: list of active testcases IDs
        :type activeTestcases: List[integer]
        :returns: void
        :rtype: json
        :raises SphereEngineException: code 401 for invalid access token
        :raises SphereEngineException: code 403 for modifying foreign problem
        :raises SphereEngineException: code 400 for empty problem code
        :raises SphereEngineException: code 404 for non existing problem
        """

        self.update(code, activeTestcases=activeTestcases)

    def allTestcases(self, problemCode):
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
           'problemCode': problemCode
        };

        return self.api_client.call_api(resource_path, method, path_params)

    def createTestcase(self, problemCode, _input='', output='', timelimit=1, judgeId=1, active=True):
        """ Create a problem testcase

        :param problemCode: problem code
        :type problemCode: string
        :param _input: model input data (default '')
        :type _input: string
        :param output: model output data (default '')
        :type output: string
        :param timelimit: time limit in seconds (default 1)
        :type timelimit: double
        :param judgeId: judge id (default 1, i.e. Ignore extra whitespaces)
        :type judgeId: integer
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
           'problemCode': problemCode
        };

        post_params = {
            'input': _input,
            'output': output,
            'timelimit': timelimit,
            'judgeId': judgeId,
            'active': active
        };

        return self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

    def getTestcase(self, problemCode, number):
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
            'problemCode': problemCode,
            'number': number
        };

        return self.api_client.call_api(resource_path, method, path_params)

    def updateTestcase(self, problemCode, number, _input=None, output=None, timelimit=None, judgeId=None, active=None):
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
            'problemCode': problemCode,
            'number': number
        }

        post_params = {}
        if input != None:
            post_params['input'] = _input
        if output != None:
            post_params['output'] = output
        if timelimit != None:
            post_params['timelimit'] = timelimit
        if judgeId != None:
            post_params['judgeId'] = judgeId
        if active != None:
            post_params['active'] = active

        return self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)

    def deleteTestcase(self, problemCode, number):
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
            'problemCode': problemCode,
            'number': number
        };

        return self.api_client.call_api(resource_path, method, path_params)

    def getTestcaseFile(self, problemCode, number, filename):
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

        if filename not in ['input', 'output']:
            raise SphereEngineException('nonexisting file', 404)

        path_params = {
            'problemCode': problemCode,
            'number': number,
            'filename': filename
        }

        return self.api_client.call_api(resource_path, method, path_params, response_type='file')


class ProblemsApiJudges(AbstractApi):

    def all(self, limit=10, offset=0, type='testcase'):
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

        return self.api_client.call_api(resource_path, method, {}, query_params)

    def create(self, sourceCode, compilerId=1, type='testcase', name=''):
        """ Create a new judge

        :param sourceCode: judge source code
        :type sourceCode: string
        :param compilerId: compiler id (default 1, i.e. C++)
        :type compilerId: integer
        :param type: judge type
        :type type: string ('testcase' or 'master')
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

        if sourceCode == '':
            raise SphereEngineException("empty source", 400)

        post_params = {
            'source': sourceCode,
            'compilerId': compilerId,
            'type': type,
            'name': name,
        }

        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

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

        return self.api_client.call_api(resource_path, method, host_params, )

    def update(self, _id, sourceCode=None, compilerId=None, name=None):
        """ Update judge

        :param _id: judge id
        :type _id: integer
        :param sourceCode: judge source code(default None)
        :type sourceCode: string
        :param compilerId: compiler id (default None)
        :type compilerId: integer
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

        if sourceCode != None and sourceCode == '':
            raise SphereEngineException('empty source', 400)

        host_params = {
            'id': _id
        }

        post_params = {}
        if sourceCode != None:
            post_params['source'] = sourceCode
        if compilerId != None:
            post_params['compilerId'] = compilerId
        if name != None:
            post_params['name'] = name

        return self.api_client.call_api(resource_path, method, host_params, {}, {}, post_params)


class ProblemsApiSubmissions(AbstractApi):

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

        return self.api_client.call_api(resource_path, method, host_params, )
    
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
    
    def create(self, problemCode, source, compilerId=None, userId=None, priority=None):#, contestCode=None, private=False):
        """ Create a new submission

        :param problemCode: problem code
        :type problemCode: string
        :param source: submission source code
        :type source: string
        :param compilerId: compiler id
        :type compilerId: integer
        :param userId: user id
        :type userId: integer
        :param priority: priority of the submission (default normal priority, eg. 5 for range 1-9)
        :type : integer
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
            'problemCode': problemCode,
            'compilerId': compilerId,
            'source': source
        }
        if userId != None:
            post_params['userId'] = userId
        if priority != None:
            post_params['priority'] = priority
        #if contestCode != None:
        #    post_params['contestCode'] = contestCode
        #if private:
        #    post_params['private'] = int(private)

        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)

class ProblemsApi(AbstractApi):

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
                                            method,
        )
        return response