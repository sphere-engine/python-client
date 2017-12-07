"""
Example presents error handling for createProblemTestcase() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
code = 'EXAMPLE'
input = 'model input'
output = 'model output'
time_limit = 5
judgeId = 1

try:
    response = client.problems.createTestcase(code, input, output, time_limit, judgeId)
    # response['number'] stores the number of created testcase
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 403:
        print('Access to the problem is forbidden')
    elif e.code == 404:
    	print('Problem does not exist')	
    elif e.code == 400:
    	print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
