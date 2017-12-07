"""
Example presents error handling for problems.create() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
code = 'EXAMPLE'
name = 'Example problem'

try:
    response = client.problems.create(code, name)
    # response['id'] stores the ID of the created problem
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 400:
        # aggregates four possible reasons of 400 error
        # empty problem code, empty problem name, not unique problem code, invalid problem code
        print('Bad request (empty problem code, empty problem name, not unique problem code, invalid problem code), details available in the message: ' + str(e))
    elif e.code == 404:
        print('Masterjudge does not exist')
