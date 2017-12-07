"""
Example presents error handling for problems.deleteTestcase() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemCode = 'EXAMPLE'
testcaseNumber = 0

try:
    response = client.problems.deleteTestcase(problemCode, testcaseNumber)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        print('Non existing resource, error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
