"""
Example presents error handling for problems.deleteTestcase() API method
"""
import os
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = 'your_access_token'
endpoint = 'problems.sphere-engine.com'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'EXAMPLE'
nonexistingTestcaseNumber = 9999

try:
    response = client.problems.deleteTestcase(problemCode, nonexistingTestcaseNumber)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        # aggregates two possible reasons of 404 error
        # non existing problem or testcase
        print('Non existing resource (problem, testcase), details available in the message: ' + str(e))
