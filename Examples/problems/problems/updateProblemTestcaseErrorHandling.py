"""
Example presents error handling for problems.updateTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = os.environ['SE_ACCESS_TOKEN_PROBLEMS']
endpoint = os.environ['SE_ENDPOINT_PROBLEMS']

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
testcaseNumber = 0
newNonexistingJudge = 9999

try:
    response = client.problems.updateTestcase(problemCode, testcaseNumber, None, None, None, newNonexistingJudge)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        # aggregates three possible reasons of 404 error
        # non existing problem, testcase or judge
        print('Non existing resource (problem, testcase or judge), details available in the message: ' + str(e))
