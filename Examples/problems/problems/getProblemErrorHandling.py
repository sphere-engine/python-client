"""
Example presents error handling for problems.get() API method
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
problemCode = 'NONEXISTING_CODE'

try:
    response = client.problems.get(problemCode)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 404:
        print('Problem does not exist')