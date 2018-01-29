"""
Example presents error handling for problems.getTestcase() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemId = 42
nonexistingTestcaseNumber = 999

try:
    response = client.problems.getTestcase(problemId, nonexistingTestcaseNumber)
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
        # aggregates two possible reasons of 404 error
        # non existing problem or testcase
        print('Non existing resource (problem, testcase), details available in the message: ' + str(e))
