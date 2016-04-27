"""
Example presents error handling for problems.updateActiveTestcases() API method
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
activeTestcases = [1,2,3]

try:
    response = client.problems.updateActiveTestcases(problemCode, activeTestcases)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 400:
        print('Empty problem code')
    elif e.code == 404:
        print('Non existing problem')
