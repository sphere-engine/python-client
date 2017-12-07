"""
Example presents error handling for submissions.create() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
problemCode = 'TEST'
source = '<source code>'
nonexistingCompiler = 99999;

try:
    response = client.submissions.create(problemCode, source, nonexistingCompiler)
    # response['id'] stores the ID of the created submission
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 402:
        print('Unable to create submission')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
