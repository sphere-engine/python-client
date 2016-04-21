"""
Example presents error handling for createProblemTestcase() API method
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
code = 'EXAMPLE'
input = 'model input'
output = 'model output'
timelimit = 5
nonexistingJudge = 9999

try:
    response = client.problems.createTestcase(code, input, output, timelimit, nonexistingJudge)
    # response['number'] stores the number of created testcase
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        # aggregates two possible reasons of 400 error
        # non existing problem and judge
        print('Non existing resource (problem or judge), details available in the message: ' + str(e))
