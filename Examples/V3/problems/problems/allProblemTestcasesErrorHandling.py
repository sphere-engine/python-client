"""
Example presents error handling for problems.allTestcases() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'NONEXISTING_CODE'

try:
    response = client.problems.allTestcases(problemCode)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        print('Problem does not exist')
