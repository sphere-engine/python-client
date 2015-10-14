#
# Sphere Engine API
#
# LICENSE
#
#
# @copyright  Copyright (c) 2015 Sphere Research Labs (http://sphere-research.com)
# @license    link do licencji
# @version    0.6

import requests

from base import AbstractApi

class ProblemsApi(AbstractApi):
    
    problems = None
    judges = None
    submissions = None
    
    def __init__(self, api_client):
        super(ProblemsApi, self).__init__(api_client)
        self.problems = ProblemsApiProblems(api_client)
        self.judges = ProblemsApiJudges(api_client)
        self.submissions = ProblemsApiSubmissions(api_client)
    
    def test(self):
        
        resource_path = '/test'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, method, )
        return response
    
    def compilers(self):
        """
        Get available languages
        :return list of languages or error
        """
        
        resource_path = '/compilers'
        method = 'GET'
        
        response = self.api_client.call_api(resource_path, 
                                            method,
        )
        return response
    
class ProblemsApiProblems(AbstractApi):

    def all(self, limit=10, offset=0):
        
        resource_path = '/problems'
        method = 'GET'
        
        query_params = {
            'limit': limit,
            'offset': offset
        }
        
        return self.api_client.call_api(resource_path, method, {}, query_params)
        
    def create(self, name, body, _type='bin', interactive=False, masterjudgeId=1001):
        
        resource_path = '/problems'
        method = 'POST'
        
        post_params = {
           'name': name,
           'body': body,
           'type': _type,
           'interactive': interactive,
           'masterjudgeId': masterjudgeId
        }
        
        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)
        
    def get(self, code):
        
        resource_path = '/problems/{code}'
        method = 'GET'
        
        path_params = {
            'code': code
        }
        
        return self.api_client.call_api(resource_path, method, path_params)
        
    def update(self, code, name=None, body=None, _type=None, interactive=None, masterjudgeId=None, activeTestcases=None):
        
        path_params = {
           'code': code  
        };
        
        resource_path = '/problems/{code}'
        method = 'PUT'
        
        post_params = {}
        if name:
            post_params['name'] = name;    
        if body:
            post_params['body'] = body
        if _type:
            if _type not in ['min', 'max', 'bin',]:
                raise ValueError('Wrong type')
            post_params['type'] = _type
        if interactive != None:
            post_params['interactive'] = 1 if interactive else 0
        if masterjudgeId:
            post_params['masterjudgeId'] = masterjudgeId
        if activeTestcases:
            post_params['activeTestcases'] = ','.join(activeTestcases)
        
        return self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)
        
    def updateActiveTestcases(self, code, activeTestcases):
        
        self.update(code, activeTestcases=activeTestcases)
    
    def allTestcases(self, problemCode):
        
        resource_path = '/problems/{problemCode}/testcases'
        method = 'GET'
        
        path_params = {
           'problemCode': problemCode
        };
        
        return self.api_client.call_api(resource_path, method, path_params)
    
    def createTestcase(self, problemCode, _input, output, timelimit, judgeId, active=True):
    
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
    
        resource_path = '/problems/{problemCode}/testcases/{number}'
        method = 'GET'
    
        path_params = {
            'problemCode': problemCode,
            'number': number
        };
        
        return self.api_client.call_api(resource_path, method, path_params)
    
    def updateTestcase(self, problemCode, number, _input=None, output=None, timelimit=None, judgeId=None):
        
        resource_path = '/problems/{problemCode}/testcases/{number}'
        method = 'PUT'
        
        path_params = {
            'problemCode': problemCode,
            'number': number
        }
        
        post_params = {}
        if input:
            post_params['input'] = _input
        if output:
            post_params['output'] = output
        if timelimit:
            post_params['timelimit'] = timelimit
        if judgeId:
            post_params['judgeId'] = judgeId
        
        return self.api_client.call_api(resource_path, method, path_params, {}, {}, post_params)
        
    def getTestcaseFile(self, problemCode, number, filename):
    
        resource_path = '/problems/{problemCode}/testcases/{number}/{filename}'
        method = 'GET'
        
        if filename not in ['input', 'output']:
            raise ValueError('Wrong filename')
        
        path_params = {
            'problemCode': problemCode,
            'number': number,
            'filename': filename
        }
        
        return self.api_client.call_api(resource_path, method, path_params)   

    
class ProblemsApiJudges(AbstractApi):
        
    def all(self, limit=10, offset=0, type='testcase'):
        
        resource_path = '/judges'
        method = 'GET'
        
        query_params = {
            'limit': limit,
            'offset': offset
        }
           
        return self.api_client.call_api(resource_path, method, {}, query_params)
    
    def create(self, sourceCode, compilerId=1, type='testcase', name=''):
        
        resource_path = '/judges'
        method = 'POST'
        
        post_params = {
            'source': sourceCode,
            'compilerId': compilerId,
            'type': type,
            'name': name,
        }
        
        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)
    
    def get(self, _id):
        
        resource_path = '/judges/{id}'
        method = 'GET'
        
        host_params = {
            'id': _id
        }
        
        return self.api_client.call_api(resource_path, method, host_params, )
    
    def update(self, id, sourceCode=None, compilerId=None, name=None):
        
        resource_path = '/judges/{id}'
        method = 'PUT'
        
        host_params = {
            'id': id
        }
        
        post_params = {}
        if sourceCode:
            post_params['source'] = sourceCode
        if compilerId:
            post_params['compilerId'] = compilerId
        if name:
            post_params['name'] = name
            
        return self.api_client.call_api(resource_path, method, host_params, {}, {}, post_params)
    
        
class ProblemsApiSubmissions(AbstractApi):
    
    #
    # Get submission by ID
    #
    # @param  integer   id                    id of the submission
    #
    # @return submission info as dictionary or error
    # 
    def get(self, id):
        
        resource_path = '/submissions/{id}'
        method = 'GET'
        
        host_params = {
          'id': id  
        }
        
        return self.api_client.call_api(resource_path, method, host_params, )


    #
    # Send submission
    #
    # @param  string       problemCode       code of the problem
    # @param  string       source            source code
    # @param  integer      language          language id
    # @param  string       contestCode       code of the contest
    # @param  integer      userId            user ID
    # @param  bool         private           flag for private submissions
    #
    # @return submission id or error
    # 
    def create(self, problemCode, source, compilerId=None, contestCode=None, userId=None, private=False):
        
        resource_path = '/submissions'
        method = 'POST'
        
        post_params = {
            'problemCode': problemCode,
            'compilerId': compilerId,
            'source': source
        }
        if contestCode:
            post_params['contestCode'] = contestCode
        if userId:
            post_params['userId'] = userId
        if private:
            post_params['private'] = int(private)
        
        return self.api_client.call_api(resource_path, method, {}, {}, {}, post_params)
    
