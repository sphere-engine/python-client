"""
Example presents error handling for problems.update() API method
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
problemCode = 'NONEXISTING_CODE'
newProblemName = 'New example problem name'

try:
    response = client.problems.update(problemCode, newProblemName)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 400:
        # aggregates two possible reasons of 400 error
        # empty problem code, empty problem name
        print('Bad request (empty problem code, empty problem name), details available in the message: ' + str(e))
    elif e.code == 404:
        # aggregates two possible reasons of 404 error
        # non existing problem or masterjudge
        print('Non existing resource (problem, masterjudge), details available in the message: ' + str(e))
