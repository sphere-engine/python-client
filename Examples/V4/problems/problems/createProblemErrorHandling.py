"""
Example presents error handling for problems.create() API method
"""
from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV4(accessToken, endpoint)

# API usage
name = 'Example problem'

try:
    response = client.problems.create(name)
    # response['id'] stores the ID of the created problem
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
